import os
import sqlite3
from contextlib import contextmanager, asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

DB = os.environ.get('DATABASE_URL', 'sqlite:///./reservations.db')

@contextmanager
def connection():
    if DB.startswith('sqlite:///'):
        conn = sqlite3.connect(DB[10:])
    else:
        import psycopg
        conn = psycopg.connect(DB)
    try:
        yield conn
    finally:
        conn.close()

def sql(statement):
    return statement if DB.startswith('sqlite:///') else statement.replace('?', '%s')

def init_db():
    with connection() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS reservations (id VARCHAR(36) PRIMARY KEY, resource VARCHAR(100) NOT NULL, starts_at VARCHAR(32) NOT NULL, customer VARCHAR(100) NOT NULL, UNIQUE(resource, starts_at))')
        conn.commit()

class Reservation(BaseModel):
    resource: str = Field(min_length=1, max_length=100, pattern=r'.*\S.*')
    customer: str = Field(min_length=1, max_length=100, pattern=r'.*\S.*')
    starts_at: datetime

@asynccontextmanager
async def lifespan(_app):
    init_db()
    yield

app = FastAPI(title='Yoyaku Cloud', lifespan=lifespan)

@app.get('/', include_in_schema=False)
def demo():
    return FileResponse(Path(__file__).parent / 'static' / 'index.html')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/reservations', status_code=201)
def create_reservation(item: Reservation):
    import uuid
    if item.starts_at.tzinfo is None or item.starts_at.utcoffset() is None:
        raise HTTPException(422, 'starts_at must include a timezone')
    starts_at = item.starts_at.astimezone(timezone.utc).isoformat(timespec='microseconds')
    rid = str(uuid.uuid4())
    try:
        with connection() as conn:
            conn.execute(sql('INSERT INTO reservations (id, resource, starts_at, customer) VALUES (?, ?, ?, ?)'), (rid, item.resource.strip(), starts_at, item.customer.strip()))
            conn.commit()
    except Exception as exc:
        if isinstance(exc, sqlite3.IntegrityError) or getattr(exc, 'sqlstate', None) == '23505':
            raise HTTPException(409, 'This time slot is already reserved') from exc
        raise
    return {'id': rid, 'resource': item.resource.strip(), 'starts_at': starts_at, 'customer': item.customer.strip()}

@app.get('/reservations/{reservation_id}')
def get_reservation(reservation_id: str):
    with connection() as conn:
        row = conn.execute(sql('SELECT id, resource, starts_at, customer FROM reservations WHERE id = ?'), (reservation_id,)).fetchone()
    if not row:
        raise HTTPException(404, 'Reservation not found')
    return dict(zip(('id', 'resource', 'starts_at', 'customer'), row))

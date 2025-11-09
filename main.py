from fastapi import FastAPI,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session

app = FastAPI(title="Real-time Async Stack")

@app.get("/")
def read_root(db: AsyncSession = Depends(get_db_session)):
    return {"status": "ok", "db_connection": "successful"}
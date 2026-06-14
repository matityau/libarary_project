from fastapi import FastAPI
from  database import db_connection
from routes import book_routes,member_routes,report_routes
import uvicorn
import os
import logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s|%(levelname)s|%(message)s",
    filename="logs/app.log"
)

logger = logging.getLogger(__name__)
logger.info("Application uploading now ")

app = FastAPI()

db_connection.create_tables()

app.include_router(book_routes.router,prefix="/books",tags=["books"])
app.include_router(member_routes.router,prefix="/members",tags=["Members"])
app.include_router(report_routes.router,prefix="/reports",tags=["Reports"])


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
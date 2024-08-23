import uvicorn
import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import generate_output, issue
from src.database import models
from src.database.issues_database import engine


models.IssueBase.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_output.router)
app.include_router(issue.router)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Messages Clustering")
    parser.add_argument("--host", default='0.0.0.0', type=str, help="Address")
    parser.add_argument("--port", default=8005, type=int, help="Port number")
    parser.add_argument("--reload", default=False, action='store_true', help="Auto reload")

    args = parser.parse_args()
    uvicorn.run("__main__:app", host=args.host, port=args.port, reload=args.reload)


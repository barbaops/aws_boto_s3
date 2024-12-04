from fastapi import FastAPI
from api.routes import aws

app = FastAPI()

app.include_router(aws.router, prefix="/aws", tags=["AWS"])

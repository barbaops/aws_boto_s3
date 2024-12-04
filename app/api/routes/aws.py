from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.bucket_models import AWS
from services.aws_service import AWSService

router  = APIRouter()

@router.get("/buckets")
async def list_aws_buckets(request: AWS):
    try:
        aws_service = AWSService(
            access_key = request.access_key,
            secret_key = request.secret_key
        )
        result = aws_service.list_buckets()
        return {"buckets": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create/bucket")
async def create_aws_bucket(request: AWS):
    try:
        aws_service = AWSService(
            access_key = request.access_key,
            secret_key = request.secret_key
        )
        result = aws_service.create_bucket(request)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete/bucket/{bucket_name}")
async def delete_aws_bucket(request: AWS, bucket_name: str):
    try:
        aws_service = AWSService(
            access_key = request.access_key,
            secret_key = request.secret_key
        )
        result = aws_service.delete_bucket(bucket_name)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update/bucket/{bucket_name}")
async def update_aws_bucket(bucket_name: str, request: AWS):
    try:
        aws_service = AWSService(
            access_key = request.access_key,
            secret_key = request.secret_key
        )
        result = aws_service.update_bucket_acl(bucket_name, request.acl)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

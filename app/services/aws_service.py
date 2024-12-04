from models.bucket_models import AWS
import boto3

class AWSService:
    def __init__(self, access_key: str, secret_key: str):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def create_bucket(self, request: AWS):
        # Condicional para a região 'us-east-1', que não precisa do LocationConstraint
        create_bucket_params = {
            "Bucket": request.name,
            "ACL": request.acl
        }

        if request.region != "us-east-1":
            create_bucket_params["CreateBucketConfiguration"] = {
                "LocationConstraint": request.region
            }

        try:
            # Criação do bucket
            self.client.create_bucket(**create_bucket_params)

            # Configuração de criptografia, se necessário
            if request.encryption:
                self.client.put_bucket_encryption(
                    Bucket=request.name,
                    ServerSideEncryptionConfiguration={
                        "Rules": [{
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": request.encryption
                            }
                        }]
                    }
                )

            # Configuração de logs, se necessário
            if request.logging and request.logging_bucket:
                self.client.put_bucket_logging(
                    Bucket=request.name,
                    BucketLoggingStatus={
                        "LoggingEnabled": {
                            "TargetBucket": request.logging_bucket,
                            "TargetPrefix": f"{request.name}/"
                        }
                    }
                )

            # Configuração de bloqueio de acesso público, se necessário
            if request.block_public:
                self.client.put_public_access_block(
                    Bucket=request.name,
                    PublicAccessBlockConfiguration={
                        "BlockPublicAcls": True,
                        "IgnorePublicAcls": True,
                        "BlockPublicPolicy": True,
                        "RestrictPublicBuckets": True,
                    }
                )

            # Configuração de políticas de ciclo de vida, se necessário
            if request.lifecycle:
                self.client.put_bucket_lifecycle_configuration(
                    Bucket=request.name,
                    LifecycleConfiguration={
                        "Rules": request.lifecycle
                    }
                )

            return f"Bucket {request.name} created successfully in region {request.region}"

        except ClientError as e:
            # Captura de exceções mais específicas
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise RuntimeError(f"Failed to create bucket {request.name}: {error_code} - {error_message}")
        except Exception as e:
            # Exceção genérica
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    def list_buckets(self):
        try:
            response    =  self.client.list_buckets()
            return response
        except Exception as e:
            raise RuntimeError(f"Error to get all buckets {e}")
    
    def delete_bucket(self, request: AWS):
        try:
            response    = self.client.delete_bucket(
                Bucket  = request.name
            )
            return f"Bucket {request.name} deleted"
        except Exception as e:
            raise RuntimeError(f"{e}")
    
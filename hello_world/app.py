import json
import os

import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver

# https://awslabs.github.io/aws-lambda-powertools-python/#features
tracer = Tracer()
logger = Logger()
app = ApiGatewayResolver()

# Global variables are reused across execution contexts (if available)
# session = boto3.Session()


@app.get("/accounts/<account_id>")
def account(account_id: str):
    return {"account": f"{account_id}"}


@app.get("/accounts/<account_id>/source_networks")
def account_nested(account_id: str):
    return {"account": f"{account_id}"}


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise

from aws_cdk import (
    # Duration,
    Stack,
    aws_iam,
    aws_lambda,
    aws_apigateway, Duration,
    # aws_sqs as sqs,
)
from constructs import Construct

class TextApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        summary_lambda = aws_lambda.Function(
            self,
            "PythonSummaryLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="summary_app.index.lambda_handler",
            code=aws_lambda.Code.from_asset("services"),
            timeout=Duration.seconds(30),
        )

        summary_lambda.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=["arn:aws:bedrock:us-east-1::model/*"]
            )
        )
        api = aws_apigateway.RestApi(self, "PY-TextApi")

        summary_integration = aws_apigateway.LambdaIntegration(
            summary_lambda,
            proxy=True,
            integration_responses=[
                aws_apigateway.IntegrationResponse(
                    status_code="200",
                    response_templates={
                        "application/json": "$input.path('$.body')"
                    }
                )
            ]
        )

        text_resource = api.root.add_resource("text")
        text_resource.add_method("POST", summary_integration,)

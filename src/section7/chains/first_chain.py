import boto3
from langchain_aws import BedrockLLM as Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import ChatPromptTemplate

AWS_REGION = "us-east-1"


bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)


def invoke_model(prompt: str) -> str:
    response = model.invoke(prompt)
    print(response)
    return response


def fist_chain(prompt: str) -> str:
    """
    First chain that invokes the model with the given prompt.
    """
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "Write a short description for the product provided by the user."),
            ("human", "{product_name}"),
        ]
    )
    chain = template.chain(model)

    response = chain.invoke({"product_name": prompt})
    print(response)
    return response


if __name__ == "__main__":
    # Example usage
    product_name = "Amazon Echo Dot"
    fist_chain(product_name)

    # You can also invoke the model directly
    # response = invoke_model("What is the capital of France?")
    # print(response)
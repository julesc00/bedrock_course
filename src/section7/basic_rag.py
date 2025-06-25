import boto3
from langchain_aws import BedrockLLM as Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws.vectorstores import FaissBedrockVectorStore as FAISS

AWS_REGION = "us-east-1"
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)

data = [
    "The weather is nice today.",
    "I love programming in Python.",
    "Last night's game was exciting.",
    "Jemima likes to eat fruits and vegetables.",
    "Jemima enjoys pizza.",
]

question = "What does Jemima like to eat?"

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    client=bedrock,
    region_name=AWS_REGION,
)
vectorstore = FAISS.from_texts(data, bedrock_embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # Maybe we can add a score threshold here

results = retriever.get_relevant_documents(question)

results_list = [result.page_content for result in results]

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers questions based on the provided context: {context}"),
        ("human", "{question}"),
    ]
)

chain = template.pipe(model)

response = chain.invoke({
    "context": results_list,
    "question": question,
})
print(response)

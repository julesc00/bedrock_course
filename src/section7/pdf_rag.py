import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockLLM as Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_aws.vectorstores import FaissBedrockVectorStore as FAISS


AWS_REGION = "us-east-1"
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)

question = "What theme does Gone with the Wind explore?"

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    client=bedrock,
    region_name=AWS_REGION,
)

# Load the PDF document
loader = PyPDFLoader("data/gone_with_the_wind.pdf")
splitter = RecursiveCharacterTextSplitter(separators=["\n"], chunk_size=200)
docs = loader.load()
splitted_docs = splitter.split_documents(docs)

# Create vector store
vector_store = FAISS.from_documents(splitted_docs, bedrock_embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

results = retriever.get_relevant_documents(question)
result_string = [result.page_content for result in results]

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers questions based on the provided context: {context}"),
        ("human", "{question}"),
    ]
)

chain = template.pipe(model)

response = chain.invoke({
    "context": result_string,
    "question": question,
})
print(response)

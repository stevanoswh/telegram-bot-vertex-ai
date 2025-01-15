from src.utils import load_file, text_split, download_embedding
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as LangchainPinecone

load_dotenv()
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

extracted_data = load_file("data/")
text_chunks = text_split(extracted_data)
embeddings = download_embedding('./credentials.json')

index_name = "csbot"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)

docsearch = LangchainPinecone.from_texts(
    texts = [t.page_content for t in text_chunks],
    embedding=embeddings,
    index_name=index_name
)
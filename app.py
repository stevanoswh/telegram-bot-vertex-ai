import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from langchain_community.vectorstores import Pinecone as LangchainPinecone 
from langchain.agents import Tool, AgentType, initialize_agent
from src.utils import get_google_sheets_service, get_sheets_data, download_embedding
from src.prompt import prompt_template

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

# def main():
    # load_dotenv()

    # PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    # SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

    # pc = Pinecone(api_key = PINECONE_API_KEY)
    # index_name = "csbot"
    # index_model = pc.index(
    #     index_name
    # )

    # service = get_google_sheets_service('./credentials.json')

    # data = get_sheets_data(service, SPREADSHEET_ID, "Sheet1!A1:G42")

    # embeddings = download_embedding('./credentials.json')

    # docsearch = LangchainPinecone.from_existing_index('csbot', embeddings)


def spreadsheet_tool(query: str) -> str:
    """
    Mengambil data dari Google Spreadsheet sesuai query atau
    langsung mengembalikan data yang sudah diambil.
    
    'query' bisa diabaikan atau dimanfaatkan untuk filtering
    di dalam spreadsheet.
    """
    # Contoh minimal: kembalikan data apa adanya
    # tapi Anda bisa menambahkan logika filtering di sini
    service = get_google_sheets_service('./credentials.json')
    data = get_sheets_data(service, SPREADSHEET_ID, "Sheet1!A1:G42")
    
    # Ubah data menjadi string
    return str(data)

embeddings = download_embedding('./credentials.json')
docsearch = LangchainPinecone.from_existing_index('csbot', embeddings)

def pinecone_tool(query: str) -> str:
    docs = docsearch.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    return context

tools = [
    Tool(
        name="Spreadsheet Jadwal",
        func=spreadsheet_tool,
        description="Gunakan tool ini bila pertanyaan berhubungan dengan jadwal ILED di Enigmacamp."
    ),
    Tool(
        name="Pinecone KB",
        func=pinecone_tool,
        description="Gunakan tool ini untuk mencari informasi umum selain data jadwal ILED."
    )
]


def run_agent(question: str):
    llm = VertexAI(model="gemini-2.0-flash-exp", temperature=0.3)
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"prefix" : prompt_template}
    )

    response = agent.run(question)
    return response

def main():
    load_dotenv()
    question = "prosedur pelaksanaan ILED gimana emangnya?"
    answer = run_agent(question)
    print(answer)

if __name__ == "__main__":
    main()
    




    




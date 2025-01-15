from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def load_file(data):
    pdf_loader = DirectoryLoader(
        data,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )

    txt_loader =DirectoryLoader(
        data,
        glob='*.txt',
        loader_cls=TextLoader
    )
    pdf_document = pdf_loader.load()
    txt_document = txt_loader.load()
    return pdf_document + txt_document

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=20)
    text_chunk = text_splitter.split_documents(extracted_data)

    return text_chunk

def download_embedding(json_keyfile_dict):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_keyfile_dict
    embeddings= VertexAIEmbeddings(model_name="text-embedding-004")
    return embeddings

def get_google_sheets_service(json_keyfile_dict):
    credentials = service_account.Credentials.from_service_account_file(
                    json_keyfile_dict,
                    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]                                                 
                )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_sheets_data(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range = range_name).execute()
    values = result.get('values', [])
    return values


import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.tools import tool

# Initialize embeddings and make a retriever
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest", base_url=("http://")) #good
pdf_path = "data/MPLS L3VPN Troubleshooting Guide_v3.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)

try:
    pages = pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages.")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise

# Split the documents into chunks using a text splitter or markdown splitter
#text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_splitter = MarkdownTextSplitter(chunk_size=600, chunk_overlap=200)
pages_split = text_splitter.split_documents(pages)

# Create vectorstore
persist_directory = r"vectorstore/persisted_data"
collection_name = "troubleshooting_guide"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Vectorstore created with {len(pages_split)} chunks.")
except Exception as e:
    print(f"Error creating vectorstore: {e}")
    raise

# Create a retriever from the vectorstore
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10, "fetch_k": 20}
)

@tool
def retrieve_tool(query: str) -> str:
    """This tool searches and returns information from the MPLS L3VPN Troubleshooting Guide document."""
    try:
        docs = retriever.invoke(query)
        if not docs:
            return "No relevant information found."
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error retrieving information: {e}"
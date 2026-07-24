# src/rag_manager.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Cargar las variables de entorno (como la GOOGLE_API_KEY)
load_dotenv()

# Obtener la ruta base del proyecto para no tener problemas con los directorios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diccionario con las rutas exactas de los 3 documentos obligatorios
DOCS = {
    "marca": os.path.join(BASE_DIR, "data", "01_Manual_de_Marca.txt"),
    "campanas": os.path.join(BASE_DIR, "data", "02_Guia_Campanas_KPIs.txt"),
    "cumplimiento": os.path.join(BASE_DIR, "data", "03_Cumplimiento_Publicitario.txt")
}

def crear_retriever(ruta_archivo: str, nombre_coleccion: str):
    """
    Lee un TXT, lo divide en chunks, genera embeddings con Gemini y lo guarda en ChromaDB.
    Retorna un retriever para que el agente pueda hacer consultas.
    """
    # 1. Cargar el documento
    loader = TextLoader(ruta_archivo, encoding='utf-8')
    documentos = loader.load()
    
    # 2. Estrategia de Chunking
    # Usamos 500 caracteres con un traslape de 50. Como los documentos son cortos y concisos,
    # esto asegura que no cortemos ideas por la mitad ni saturemos el contexto.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documentos)
    
    # 3. Generación de Embeddings obligatorios con Gemini
    # Aquí forzamos la lectura explícita de la API Key para evitar el error 404
    # 3. Generación de Embeddings obligatorios con Gemini
    # 3. Generación de Embeddings con Gemini
    # 3. Generación de Embeddings con Gemini
    # 3. Generación de Embeddings con el modelo actual de Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    
    # 4. Almacenamiento en Chroma (Vector Store)
    # Se crea una carpeta 'chroma_db' local para no gastar tokens re-vectorizando en cada ejecución
    persist_directory = os.path.join(BASE_DIR, "chroma_db", nombre_coleccion)
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        collection_name=nombre_coleccion,
        persist_directory=persist_directory
    )
    
    # Retornamos el recuperador configurado para traer los 3 fragmentos más relevantes (Top-K = 3)
    return vector_store.as_retriever(search_kwargs={"k": 3})

def obtener_todos_los_retrievers():
    """
    Inicializa y devuelve los tres retrievers independientes exigidos por la rúbrica.
    """
    print("Iniciando vectorización y carga de RAG (puede tomar unos segundos)...")
    
    retriever_marca = crear_retriever(DOCS["marca"], "col_marca")
    retriever_campanas = crear_retriever(DOCS["campanas"], "col_campanas")
    retriever_cumplimiento = crear_retriever(DOCS["cumplimiento"], "col_cumplimiento")
    
    print("¡Bases de conocimiento vectorizadas con éxito!")
    
    return {
        "marca": retriever_marca,
        "campanas": retriever_campanas,
        "cumplimiento": retriever_cumplimiento
    }
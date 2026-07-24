# src/orchestrator.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from src.rag_manager import obtener_todos_los_retrievers
from src.action_tools import herramientas_accion
from src.prompts import PROMPT_ORQUESTADOR

def crear_orquestador():
    print("Configurando el Orquestador (Versión a prueba de balas)...")
    
    # 1. Obtener los retrievers del Rol 1
    retrievers = obtener_todos_los_retrievers()
    
    # 2. Funciones auxiliares para conectar la base de datos con el agente
    def buscar_marca(query: str) -> str:
        docs = retrievers["marca"].invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])

    def buscar_campanas(query: str) -> str:
        docs = retrievers["campanas"].invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])

    def buscar_cumplimiento(query: str) -> str:
        docs = retrievers["cumplimiento"].invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])

    # 3. Crear las Herramientas (Tools) manualmente usando el núcleo de LangChain
    tool_marca = Tool(
        name="agente_marca",
        description="Busca y responde preguntas sobre identidad de marca, uso de logotipo, colores y plantillas oficiales de Patito S.A.",
        func=buscar_marca
    )
    
    tool_campanas = Tool(
        name="agente_campanas",
        description="Busca y responde sobre planificación de campañas, canales, KPIs y métricas de desempeño.",
        func=buscar_campanas
    )
    
    tool_cumplimiento = Tool(
        name="agente_cumplimiento",
        description="Busca y responde sobre claims permitidos, publicidad responsable, uso de datos y consentimiento.",
        func=buscar_cumplimiento
    )
    
    # 4. Juntar todas las herramientas: Los 3 de RAG + Tu agente de Acción (Registro)
    todas_las_herramientas = [tool_marca, tool_campanas, tool_cumplimiento] + herramientas_accion
    
    # 5. Configurar el LLM (Gemini 1.5 Flash) inyectando el system prompt directamente en el modelo
    # 5. Configurar el LLM con el modelo correcto
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-3.5-flash", 
        temperature=0
    )
    # 6. Crear el Agente con LangGraph limpio (sin argumentos de modificadores externos)
    orquestador = create_react_agent(
        model=llm,
        tools=todas_las_herramientas
    )
    
    return orquestador
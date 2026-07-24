# app.py
import os
import warnings
from dotenv import load_dotenv
from src.orchestrator import crear_orquestador

# Ocultar advertencias innecesarias de LangChain
warnings.filterwarnings("ignore")

def main():
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
        return

    print("="*60)
    print("MESA DE AYUDA IA - MARKETING PATITO S.A.")
    print("="*60)
    
    try:
        orquestador = crear_orquestador()
    except Exception as e:
        print(f"Error al iniciar el sistema: {e}")
        return

    print("\n¡Sistema listo! Escribe tu consulta o 'salir' para terminar.")
    
    while True:
        consulta = input("\n👤 Tu consulta: ")
        if consulta.lower() in ['salir', 'exit', 'quit']:
            print("👋 ¡Hasta luego!")
            break
            
        if not consulta.strip():
            continue
            
        print("\n🤖 Pensando (analizando herramientas y documentos)...")
        try:
            # Nuevo formato de LangGraph: Se envía como un mensaje de usuario
            inputs = {"messages": [("user", consulta)]}
            
            # Ejecutar el orquestador
            respuesta = orquestador.invoke(inputs)
            
            # LangGraph devuelve una lista de mensajes; extraemos el último (la respuesta de Gemini)
            mensaje_final = respuesta["messages"][-1].content
            
            print("\n✅ RESPUESTA:")
            print(mensaje_final)
            
        except Exception as e:
            print(f"\n❌ Error al procesar la consulta: {e}")

if __name__ == "__main__":
    main()
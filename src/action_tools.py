import os
import uuid
from datetime import datetime
from langchain.tools import tool

@tool
def registrar_campana(
    nombre: str = "",
    objetivo: str = "",
    canales: str = "",
    publico_objetivo: str = "",
    presupuesto: str = "",
    fecha_inicio: str = "",
    fecha_fin: str = "",
    consentimiento_email: str = ""
) -> str:
    """
    Herramienta para registrar una solicitud de campaña de marketing[cite: 4].
    Usa esta herramienta SOLO cuando el usuario haya dado su confirmación explícita para registrar la campaña.
    """
    
    # 1. Sistema de control: Validar que estén todos los datos obligatorios[cite: 4]
    faltantes = []
    if not nombre: faltantes.append("nombre de la campaña")
    if not objetivo: faltantes.append("objetivo (awareness, leads o conversión)")
    if not canales: faltantes.append("canal(es)")
    if not publico_objetivo: faltantes.append("público objetivo")
    if not presupuesto: faltantes.append("presupuesto")
    if not fecha_inicio: faltantes.append("fecha de inicio")
    if not fecha_fin: faltantes.append("fecha de fin")
    
    # Validación extra: si usa email, debe confirmar que el público dio consentimiento[cite: 4]
    if "email" in canales.lower() and not consentimiento_email:
        faltantes.append("confirmación de consentimiento de marketing para email")

    # 2. Si falta algo, detenemos la acción y le pedimos al usuario lo que falta[cite: 4]
    if faltantes:
        campos = ", ".join(faltantes)
        return f"Para poder registrar la campaña, necesito que me proporciones los siguientes datos faltantes: {campos}."

    # 3. Generar un identificador único y la fecha/hora actual[cite: 4]
    id_campana = f"RMB-{str(uuid.uuid4())[:6].upper()}"
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 4. Formatear la cadena de texto que se va a guardar
    registro = (
        f"[{fecha_registro}] ID: {id_campana} | "
        f"Campaña: {nombre} | Objetivo: {objetivo} | Canales: {canales} | "
        f"Público: {publico_objetivo} | Presupuesto: {presupuesto} | "
        f"Fechas: {fecha_inicio} al {fecha_fin}\n"
    )

    # 5. Escribir en el archivo de texto local[cite: 4]
    ruta_archivo = os.path.join(os.path.dirname(__dirname__), "data", "registro_campanas.txt")
    
    try:
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write(registro)
        return f"¡Éxito! La campaña ha sido registrada en el sistema con el identificador {id_campana} a las {fecha_registro}."
    except Exception as e:
        return f"Error interno al intentar registrar la campaña: {str(e)}"

# Exportamos la lista de herramientas para que el Orquestador (Rol 3) pueda importarla
herramientas_accion = [registrar_campana]
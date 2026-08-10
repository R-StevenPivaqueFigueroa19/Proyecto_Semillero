<div align="center">

#  MESA DE AYUDA IA - MARKETING PATITO S.A.

### SEMILLERO IA NETLIFE - PROYECTO FINAL 
**Universidad de Guayaquil | Ingeniería en Sistemas - Séptimo Semestre**

<br>

**Equipo Desarrollador:**
| 👨‍💻 **Ronald Steven Pivaque Figueroa** | 👩‍💻 **Rosero Lopez Marylin Nicolle** | 👩‍💻 **Zambrano Vasquez Ana Michelle** |
| :---: | :---: | :---: |

</div>

<br>

> **Objetivo del Proyecto:**
> Prototipo funcional de una mesa de ayuda basada en Inteligencia Artificial para el Departamento de Marketing de Patito S.A. Este sistema utiliza agentes especializados construidos con **LangChain** y **LangGraph**, impulsados por **Google Gemini**, para automatizar la atención interna, responder consultas sobre marca, campañas y normativas, además de ejecutar acciones de registro automatizado.

---

<br>

## 🚀 Requisitos Previos

* **Python:** Versión 3.10 o superior.
* **Credenciales:** Una API Key válida de Google Gemini.
* **Control de Versiones:** Git (opcional, para clonar el repositorio).

<br>

---

<br>

## Instalación y Ejecución

Sigue estos pasos detallados para levantar el entorno y ejecutar el sistema localmente:

<br>

### **Paso 1: Clonar el repositorio**
Abre tu terminal y descarga el código fuente a tu máquina local:

```bash
git clone [https://github.com/R-StevenPivaqueFigueroa19/Proyecto_Semillero.git](https://github.com/R-StevenPivaqueFigueroa19/Proyecto_Semillero.git)
cd Proyecto_Semillero

---

# **Paso 2: Crear y activar el entorno virtual**

Para evitar conflictos con otras instalaciones de Python y mantener el proyecto completamente aislado, se recomienda crear un entorno virtual antes de instalar las dependencias.

### ** Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

> **Nota:** Si aparece un error en color rojo al activar el entorno virtual, ejecuta el siguiente comando para otorgar permisos temporales y vuelve a intentarlo.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### **macOS /  Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# **Paso 3: Instalar las dependencias**

Con el entorno virtual ya activado, instala todas las librerías necesarias para ejecutar el proyecto.

```bash
pip install -r requirements.txt
```

---

# **Paso 4: Configurar las variables de entorno**

El sistema utiliza la API de Google Gemini para el funcionamiento de los modelos de inteligencia artificial.

1. Copia el archivo **`.env.example`**.
2. Renómbralo como **`.env`**.
3. Abre el archivo y agrega tu clave de API de Google Gemini.

```env
GOOGLE_API_KEY="TU_CLAVE_AQUI"
```

---

# **Paso 5: Ejecutar la aplicación**

Una vez configurado el entorno e instaladas las dependencias, inicia la Mesa de Ayuda IA ejecutando el siguiente comando.

```bash
python app.py
```

---

# **Arquitectura y Flujo del Sistema**

El proyecto implementa una arquitectura basada en un **Agente Orquestador (ReAct)** utilizando **LangGraph**, permitiendo enrutar automáticamente cada consulta hacia el agente especializado correspondiente.

## **Flujo de ejecución**

1. El usuario ingresa una consulta en lenguaje natural desde la interfaz de línea de comandos (**app.py**).

2. El **Orquestador (orchestrator.py)** analiza la intención de la consulta.

3. Dependiendo del tipo de solicitud, el orquestador envía la petición hacia el agente correspondiente.

- **Agentes RAG** para consultas de información.
- **Agente de Acción** para registrar campañas.

4. El agente procesa la solicitud recuperando información desde ChromaDB o validando los datos ingresados.

5. Finalmente, el Orquestador consolida toda la información y entrega una respuesta al usuario.

---

# **Agentes Implementados**

## **Agente de Marca (RAG)**

Responde consultas relacionadas con:

- Manual de marca.
- Paleta de colores.
- Tipografías institucionales.

---

## **Agente de Campañas (RAG)**

Proporciona información acerca de:

- KPIs.
- Canales de marketing.
- Objetivos de campañas.

---

## **Agente de Cumplimiento (RAG)**

Valida aspectos relacionados con:

- Claims publicitarios.
- Políticas de privacidad.
- Uso correcto de datos personales.

---

## **Agente de Acción (Registro)**

Permite registrar nuevas campañas realizando las siguientes validaciones:

- Verifica que existan los **8 campos obligatorios**.
- Solicita confirmación explícita del usuario antes del registro.
- Genera un identificador único.
- Guarda la información en:

```text
data/registro_campanas.txt
```

---

# **Decisiones Técnicas y Arquitectónicas**

## **Aislamiento del Entorno (VENV)**

Se implementó un entorno virtual (**venv**) para aislar completamente las dependencias del proyecto.

Esta decisión garantiza:

- Replicabilidad del entorno.
- Evita conflictos de versiones.
- No modifica la instalación global de Python.

---

## ** Modelo LLM**

Se utilizó el modelo:

```text
gemini-3.5-flash
```

Configurado con:

- Temperatura = **0**

Esto permite respuestas totalmente deterministas y reduce las alucinaciones durante el proceso de enrutamiento.

---

## **Embeddings**

Los vectores fueron generados utilizando:

```text
GoogleGenerativeAIEmbeddings
(models/gemini-embedding-001)
```

---

## **Estrategia de Chunking**

Se configuró el procesamiento de documentos con los siguientes parámetros:

```text
Chunk Size    : 500 caracteres
Chunk Overlap : 50 caracteres
```

Esta configuración permite mantener las ideas completas dentro de cada fragmento y mejorar la recuperación de contexto.

---

## **Base Vectorial (ChromaDB)**

Se implementaron colecciones persistentes independientes:

- col_marca
- col_campanas
- col_cumplimiento

El recuperador utiliza:

```text
Top-K = 3
```

Esto permite recuperar únicamente los tres fragmentos más relevantes para cada consulta, optimizando el consumo de tokens.

---

# **Riesgos y Mejoras Futuras**

## **Lectura del historial de campañas**

Actualmente el Agente de Acción únicamente registra información.

Como mejora futura se propone implementar una herramienta que permita consultar campañas previamente registradas.

---

## **Gestión de permisos (RBAC)**

Todos los usuarios poseen actualmente el mismo nivel de acceso.

En una versión productiva debería incorporarse un sistema de control de acceso basado en roles (**RBAC**).

---

## **Persistencia en Base de Datos**

Actualmente la información se almacena en un archivo de texto.

Como mejora futura se recomienda migrar el almacenamiento hacia una base de datos como:

- PostgreSQL
- MongoDB

Esto permitirá manejar concurrencia y mejorar la seguridad de los datos.

---

## **Trazabilidad Avanzada**

Se propone implementar un sistema de auditoría que registre:

- Qué documentos fueron consultados.
- Qué chunks fueron recuperados.
- Qué agente respondió la consulta.

Con ello será posible mejorar la trazabilidad y facilitar futuras tareas de monitoreo y depuración.

---
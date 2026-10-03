# IA Core Bank - Agentic Trade Finance Assistant

Initial FastAPI project structure for an Agentic AI banking assistant.

## Current endpoints

- `GET /health`
- `GET /api/chat/hello`
- Swagger UI: `/docs`

## Run locally

Activate your virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Then open:

- http://localhost:8000/health
- http://localhost:8000/api/chat/hello
- http://localhost:8000/docs

==============================================================
INFORMACION:
INGESTA DATOS:
FASE 1 — INGESTA DEL DOCUMENTO

PDF / DOCX / HTML
   ↓
Extraer texto
   ↓
Chunking
   ↓
chunk-0
chunk-1
chunk-2
chunk-3
   ↓
Embedding de cada chunk
   ↓
Vector DB

Ejemplo:
chunk-0 → [0.12, 0.88, 0.31, ...]
chunk-1 → [0.55, 0.11, 0.72, ...]
chunk-2 → [0.91, 0.33, 0.21, ...]

==============================================================
Eso queda guardado.
Luego viene la consulta:

FASE 2 — CONSULTA

Usuario:
"Who is the beneficiary?"
   ↓
LangGraph
   ↓
MCP Client
   ↓
MCP Server
   ↓
tool: search_documents(query)
   ↓
Retriever
==============================================================

Y aquí dentro del Retriever ocurre lo importante:

Query:
"Who is the beneficiary?"
   ↓
Embedding Model
   ↓
Query Embedding
[0.89, 0.35, 0.20, ...]

==============================================================

Ese vector de la pregunta se compara con los vectores ya guardados:

Query embedding
       ↓
Vector DB
       ↓
compara contra:

chunk-0 embedding
chunk-1 embedding
chunk-2 embedding
chunk-3 embedding

==============================================================

Ese vector de la pregunta se compara con los vectores ya guardados:

chunk-2 → distance 1.00
chunk-0 → distance 1.73
chunk-3 → distance 1.75

y devuelve:

Top-K
   ↓
chunk-2
chunk-0
chunk-3

==============================================================

Entonces, juntando todo:

Usuario
  ↓
"Who is the beneficiary?"
  ↓
LangGraph Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
search_documents(query)
  ↓
Retriever
  ↓
Embedding Model
  ↓
crear embedding de la QUERY
  ↓
Vector DB
  ↓
comparar query embedding vs chunk embeddings ya almacenados
  ↓
similarity / distance
  ↓
Top-K chunks
  ↓
Context Builder
  ↓
LLM
  ↓
Respuesta


==============================================================

La diferencia importantísima es esta:


DOCUMENTO
→ se chunkea
→ cada chunk genera embedding
→ se guarda

QUERY
→ NO se chunkea normalmente
→ genera 1 embedding
→ se compara contra los embeddings guardados
==============================================================

Así que podrías imaginarlo matemáticamente como:


query vector
      ↓
      ●

chunk-0 ●

chunk-1          ●

chunk-2  ●   ← más cercano

chunk-3       ●

Y por eso chunk-2 sale primero.
Una forma muy simple de memorizarlo:

INGESTA:
Document → chunks → embeddings → Vector DB

CONSULTA:
Question → embedding → Vector DB → matching chunks
==============================================================


RESUMEN DE RAG: 

Sí: RAG incluye al LLM.
El nombre lo dice:

RAG = Retrieval-Augmented Generation

==============================================================
Tiene dos partes:

1. Retrieval
   ↓
   buscar información relevante

2. Generation
   ↓
   el LLM genera la respuesta usando esa información
==============================================================
Entonces esto:

Pregunta
  ↓
Embedding de la query
  ↓
Vector DB
  ↓
Top-K chunks
  ↓
Context

es solo la parte de Retrieval.

==============================================================


Y luego:

Context + Question
  ↓
LLM
  ↓
Respuesta

es la parte de Generation.

==============================================================

==========>
Todo junto:

QUESTION
   ↓
RETRIEVAL
   ↓
query embedding
   ↓
vector search
   ↓
relevant chunks
   ↓
context
   ↓
GENERATION
   ↓
LLM
   ↓
final answer
==============================================================
==============================================================
==============================================================
==============================================================

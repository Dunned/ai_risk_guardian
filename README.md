# Proyecto: AI Risk Guardian
![alt text](image.png)
## Descripción General

AI Risk Guardian es un asistente conversacional especializado en Model Risk Management (MRM).  
Su propósito es apoyar a los equipos de riesgo en el monitoreo, validación y gestión de modelos de machine learning, combinando un frontend moderno con un backend inteligente basado en agentes de IA.  

El sistema permite realizar consultas relacionadas con normativa SBS, documentación metodológica, métricas de desempeño (Gini, KS, PSI, etc.) y bitácoras de modelos, brindando respuestas rápidas, interpretables y alineadas con los procesos regulatorios.
![alt text](image-1.png)
---

## Objetivo

Facilitar la consulta, documentación y control regulatorio de modelos de riesgo, centralizando información dispersa y automatizando tareas repetitivas mediante herramientas de inteligencia artificial integradas.

---

## Funcionalidades Clave

- Autenticación segura mediante OAuth2 (Google) con control de acceso.
- Interfaz de chat responsiva construida con Next.js y TailwindCSS.
- Agente de IA especializado en MRM que responde sobre:
  - Validación y monitoreo de modelos.
  - Métricas regulatorias y de desempeño.
  - Cumplimiento SBS / Basilea.
  - Documentación técnica y bitácoras.
- Integración con fuentes internas (Athena, Elasticsearch, PostgreSQL).
- Despliegue flexible en Docker, Google Cloud Run o Vercel.

---

## Arquitectura del Proyecto

El proyecto se divide en dos componentes principales:

### 1. Frontend
- Framework: Next.js 14 (React)
- Estilos: TailwindCSS
- Autenticación: NextAuth con Google OAuth2
- Despliegue: Vercel  
- URL de producción: https://ai-risk-guardian-fxbkkj4uo-eduardojaureguir-3116s-projects.vercel.app/
- Características principales:
  - Interfaz conversacional moderna.
  - Historial de interacciones.
  - Control de sesión seguro.

### 2. Backend (Agente IA)
- Framework: Flask
- IA: LangChain / LangGraph (orquestación de agentes)
- Modelo: OpenAI GPT-4.1
- Bases de datos:
  - Athena (métricas de performance)
  - Elasticsearch (RAG: normativa, bitácoras y documentos)
  - PostgreSQL (checkpoint LangGraph)
- Contenerización: Docker
- Despliegue: Google Cloud Run

---

## Instalación y Configuración

### Requisitos Previos
- Python 3.10+
- Node.js 18+
- Docker y gcloud CLI (para despliegue en Cloud Run)
- Cuenta en OpenAI, Google Cloud y Elasticsearch

---

### Clonación del Repositorio

git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

---

### 1. Backend – Flask (Agente IA)

#### Dependencias

cd backend
pip install -r requirements.txt

#### Variables de Entorno

Crea un archivo .env en la carpeta backend:

OPENAI_API_KEY=tu_api_key
LANGCHAIN_API_KEY=tu_api_langchain
LANGCHAIN_PROJECT=ai-risk-guardian
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
DB_URI=postgresql://user:password@host:port/dbname
ES_URL=https://tu-servidor-elastic:9200
ES_USER=elastic
ES_PASSWORD=tu_password
S3_STAGING=s3://ruta/staging/

#### Ejecución Local

python app.py

El servicio estará disponible en:
http://localhost:8080

#### Prueba del Endpoint

curl "http://localhost:8080/agent?idagente=001&msg=Gini del modelo infcuovehi en 202502"

---

### 2. Frontend – Next.js

#### Instalación

cd frontend
npm install

#### Variables de Entorno

Crea un archivo .env.local en frontend:

NEXTAUTH_URL=https://ai-risk-guardian-fxbkkj4uo-eduardojaureguir-3116s-projects.vercel.app/
GOOGLE_CLIENT_ID=tu_client_id
GOOGLE_CLIENT_SECRET=tu_client_secret
OPENAI_API_KEY=tu_api_key
API_BACKEND_URL=https://tu-backend.cloudrun.app

#### Ejecución Local

npm run dev

La aplicación estará disponible en:
http://localhost:3000

---

## Despliegue

### Opción A – Docker

Construcción de imagen

docker build -t ai-risk-guardian .

Ejecución

docker run -d -p 8080:8080   -e OPENAI_API_KEY="tu_api_key"   -e LANGCHAIN_API_KEY="tu_api_langchain"   -e DB_URI="postgresql://user:password@host:port/dbname"   ai-risk-guardian

Prueba

curl "http://localhost:8080/agent?idagente=123&msg=Modelos activos en 202501"

---

### Opción B – Google Cloud Run

Despliegue

gcloud run deploy ai-risk-guardian   --image gcr.io/<tu-proyecto>/ai-risk-guardian:latest   --platform managed   --region us-east1   --allow-unauthenticated

Asegúrate de configurar las variables de entorno directamente en el panel de Cloud Run.

---

### Opción C – Vercel (Frontend)

Despliegue del Frontend
1. Accede a https://vercel.com.
2. Importa el repositorio desde GitHub.
3. Configura las variables de entorno (.env.local).
4. Ejecuta el despliegue.

---

## Pruebas del Sistema

Una vez desplegado:

- Backend Flask:  
  GET /agent?idagente=001&msg=Modelos activos en 202501

- Frontend (interfaz):  
  https://ai-risk-guardian-fxbkkj4uo-eduardojaureguir-3116s-projects.vercel.app/

---

## Stack Tecnológico

Frontend:  
Next.js 14, React, TailwindCSS, NextAuth (OAuth2), Vercel  

Backend:  
Flask, LangChain, LangGraph, OpenAI GPT-4.1, SQLAlchemy, Elasticsearch, PostgreSQL, AWS Athena  

Infraestructura:  
Docker, Google Cloud Run, S3  

---

## Autor

Eduardo Jauregui  
LinkedIn: https://www.linkedin.com/in/eduardojaureguir

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.  
Su uso, modificación y redistribución están permitidos bajo los términos de dicha licencia.
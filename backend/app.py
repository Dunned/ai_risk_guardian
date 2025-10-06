from langchain_openai import ChatOpenAI
import os
from flask import Flask, jsonify, request
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import re
import json
from typing import Any, Dict


## datos de trazabilidad
os.environ["LANGSMITH_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = ""
os.environ["OPENAI_API_KEY"] =""




app = Flask(__name__)

@app.route('/agent', methods=['GET'])
def main():
    #Capturamos variables enviadas
    id_agente = request.args.get('idagente')
    msg = request.args.get('msg')
    #datos de configuracion
    DB_URI = ""
    
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }

    db_query_reg = ElasticsearchStore(
        es_url="", #coloca la IP de tu servidor de elastic
        es_user="elastic",
        es_password='',
        index_name="lm-reglamentos",
        embedding=OpenAIEmbeddings()
    )

    retriever_reg = db_query_reg.as_retriever()

    tool_rag_reg = retriever_reg.as_tool(
        name="buscar_reglamentos_sbs",
        description="""Consulta **normativa SBS**: resoluciones/reglamentos, artículos/capítulos, definiciones oficiales/versión.
        Úsala cuando el usuario pida algo “según la SBS” (definiciones, obligaciones, alcance, vigencia, excepciones o citas textuales por artículo).

        No la uses para: modelos específicos, métricas/bitácoras mensuales (AAAAMM), ni documentos metodológicos internos.


        Ejemplos:
        - "Definición de modelo segun reglamento"
        - "¿Qué indica la Resolución X en el Artículo 12?"
        - "A que modelos aplica el model risk managment"
        """
    )

    db_query_bit = ElasticsearchStore(
        es_url="", #coloca la IP de tu servidor de elastic
        es_user="elastic",
        es_password='',
        index_name="lm-bitacoras",
        embedding=OpenAIEmbeddings()
    )

    retriever_bit = db_query_bit.as_retriever()

    tool_rag_bitacora = retriever_bit.as_tool(
    name="busqueda_bitacora_modelos",
    description = """Consulta la BITÁCORA de modelos (Excel/CSV) por PERIODO (AAAAMM) y por MODELO.
    Úsala para:
    - Identificar modelos nuevos o dados de baja en un mes específico.
    - Verificar si un modelo está activo/inactivo y sus fechas de uso e implementación.
    - Conocer a qué banca pertenece, el tipo de modelo y si tiene ejecución automática.
    - Comparar periodos para ver qué se agregó, cambió o se retiró.
    - Obtener (si existe) el enlace al documento metodológico asociado.

    No la uses para normativa SBS ni documentos legales.

    Ejemplos:
    - "¿Qué modelo es nuevo en 202501?"
    - "Modelos activos al 202501."
    - "¿Qué modelos se dieron de baja entre 202401 y 202501?"
    - "¿Cuántos modelos hay y cuántos están activos en 202501?"
    - "¿Qué niveles de modelos hay en 202501?"
    - "Dame el link del documento metodológico del modelo X.", si te piden link deberas dar la url del documento metodológico del modelo.

    Contexto de Algunos Campos
    Los Modelos Activos son los que ya se usan, un Modelo puede estar como No en activo pero no quiere decir que este dado de baja para eso
    el campo Dado de Baja debe tener una fecha es decir un valor diferente a no Aplica.
    Si un modelo esta como No en Activo pero no tiene fecha de dado de baja quiere decir que es nuevo aun no se usa, pero ya
    se registro en la bitacora  y se usara mas adelante.
    """
    )

    db_query_docs = ElasticsearchStore(
        es_url="", #coloca la IP de tu servidor de elastic
        es_user="elastic",
        es_password='',
        index_name="lm-docs-metodologicos_v3",
        embedding=OpenAIEmbeddings()
    )

    retriever_docs = db_query_docs.as_retriever()

    tool_rag_docs = retriever_docs.as_tool(
        name="busqueda_documentos_metodologicos",
        description = """Consulta cuando te preguntan sobre la documentacion metodologica de un modelo, detalles de su creacion , metodologia, quien lo creo.
        Úsala para:

        - Responder preguntar muy personalizadas de un modelo
        - Debes mostrar solo el detalle del modelo a preguntar

        No la uses para normativa SBS ni documentos legales.

        Ejemplos:
        - "Dime informacion sobre el modelo de cobranza banca persona"
        - "Quien creo el modelo banca persona."
        - "Cuantas Variables tien el modelo"
        - "Cuales son las variables de un modelo y su importancia shap"
        - "Que metodologia se uso en un modelo"
        """
    )


    REGION = "us-east-2"
    S3_STAGING = ""
    WORKGROUP = "primary"
    SCHEMA = "datalake"

    ATHENA_URI = (
        f"awsathena+rest://@athena.{REGION}.amazonaws.com:443/{SCHEMA}"
    )

    engine = create_engine(
        ATHENA_URI,
        connect_args={
            "s3_staging_dir": S3_STAGING,
            "work_group": WORKGROUP,
            # boto3/ botocore leerán las env vars automáticamente,
            # pero puedes pasarlas explícitamente si quieres:
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            # "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),  # si aplica
            "region_name": REGION,
        }
    )

    # Envuelve en LangChain
    db_athena = SQLDatabase(engine=engine)


    SCHEMA_PERFORMANCE = """
    Tabla performance

    Descripción:
    Tabla que guarda las métricas de Athena para los resultados de performance producto del monitoreo del Modelo.
    Es la tabla ideal si quieres consultar métricas relacionadas al Gini, KS, tasa de malos (TM), indicadores de la matriz de confusión (ACCU, F1, ODDS, SENS), entre otros.

    Campos:

    modelo (STRING)
    - Descripción: Nombre del modelo.
    - Sinónimos: model, nombre modelo.

    periodo (STRING 'YYYYMM')
    - Descripción: Periodo de ejecución del monitoreo.
    - Sinónimos: p_codmes, ejecucion.

    segmento (STRING)
    - Descripción: Segmento o subpoblación.

    tipo (STRING)
    - Descripción: Tipo de métrica (gini, ks, auc, tm, accu, sens, ods, count, ratio).
    - Sinónimos: metrica, indicador, tipo.

    variable (STRING)
    - Descripción: Nombre de la variable a la cual se aplica la métrica, para todos los casos el valor es el mismo =  puntuacion bucket

    estadistico (STRING)
    - Descripción: Corte/bucket cuando la métrica se calcula segmentada por variable (p.ej., 'score>=700', '700 - 800'), son cortes de deciles

    valor (DOUBLE)
    - Descripción: Valor numérico de la métrica.
    """.strip()

    HINTS = {
        "reglas": [
            # Regla central:
            "Siempre debes filtrar por el modelo y el periodo que te estan pidiendo"
            "GINI/KS/AUC SIEMPRE van en 'tipo' (tipo IN ('gini','ks','auc')). No pongas gini/ks/auc en 'estadistico'.",
            "Para métricas con corte/bucket (count/ratio/tm por tramos), pon el detalle en 'estadistico' (ej: 'score>=700')",
            "Si no te expecifican un segmento o subpoblacion en segmento es = global"
            "Devuelve SOLO UNA sentencia SQL (SELECT), sin ``` ni texto extra.",
            "NO DDL/DML (NO CREATE/ALTER/DROP/INSERT/UPDATE/DELETE/MERGE). Solo SELECT.",
        ]
    }

    # ---------- (B) Limpieza + post-corrección GINI/KS/AUC ----------
    def _to_sql_only(txt: str) -> str:
        t = txt.strip()
        t = re.sub(r"^```(?:sql)?\s*", "", t, flags=re.IGNORECASE)
        t = re.sub(r"\s*```$", "", t)
        t = re.sub(r"(?i)^(sql\s*query|sql)\s*:\s*", "", t.strip())
        # tomar desde primer SELECT
        m = re.search(r"(?is)\bselect\b.+$", t)
        if not m:
            return "SELECT 1"
        t = m.group(0).strip()
        # cortar en primera sentencia
        if ";" in t:
            t = t.split(";", 1)[0].strip()
        # bloquear DDL/DML
        if re.search(r"(?i)\b(CREATE|ALTER|DROP|TRUNCATE|INSERT|UPDATE|DELETE|MERGE|GRANT|REVOKE)\b", t):
            return "SELECT 1"
        return t

    def _fix_gini_ks_auc(sql: str) -> str:
        """
        Si el modelo puso gini/ks/auc en 'estadistico' en vez de 'tipo', lo corrige.
        - Mueve 'estadistico = (gini|ks|auc)' a "tipo = ..."
        - Si 'tipo' ya está presente con otro valor, lo reemplaza por el correcto.
        - Si no hay 'estadistico' tras mover, lo deja como 'global' cuando convenga.
        """
        s = sql

        # Patrón WHERE ... estadistico = 'gini|ks|auc'
        pat_estad = re.compile(r"(?i)\bestadistico\s*=\s*'?(gini|ks|auc)'?")
        m_est = pat_estad.search(s)
        if m_est:
            metric = m_est.group(1).lower()
            # Quitar condición de estadistico = 'metric'
            s = pat_estad.sub("1=1", s)  # neutraliza
            # Asegurar/ajustar tipo = 'metric'
            pat_tipo = re.compile(r"(?i)\btipo\s*=\s*'[^']*'")
            if pat_tipo.search(s):
                s = pat_tipo.sub(f"tipo = '{metric}'", s)
            else:
                # Insertar al final del WHERE si existe, o agregar WHERE nuevo
                if re.search(r"(?i)\bwhere\b", s):
                    s = re.sub(r"(?i)\bwhere\b", "WHERE", s)  # normaliza
                    s = re.sub(r"(?i)\bwhere\b", "WHERE", s)  # seguridad
                    s = re.sub(r"(?i)\bwhere\b", "WHERE", s)
                    # Agrega con AND
                    s = re.sub(r"(?is)(where\s+)(.+)$", r"\1\2 AND tipo = '" + metric + "'", s)
                else:
                    s += f" WHERE tipo = '{metric}'"

            # Si removimos estadistico, y no hay ningún 'estadistico =' explícito, podemos opcionalmente fijar 'estadistico = 'global''
            if "estadistico" not in s.lower():
                # Si ya hay WHERE, agregar AND; si no, crear WHERE
                if re.search(r"(?i)\bwhere\b", s):
                    s = s + " AND estadistico = 'global'"
                else:
                    s = s + " WHERE estadistico = 'global'"

        # También arregla casos donde se haya escrito tipo='gini' y además estadistico='gini' (dup)
        if re.search(r"(?i)\btipo\s*=\s*'(gini|ks|auc)'\b", s) and re.search(r"(?i)\bestadistico\s*=\s*'(gini|ks|auc)'\b", s):
            s = re.sub(r"(?i)\bestadistico\s*=\s*'(gini|ks|auc)'\b", "estadistico = 'global'", s)

        return s

    # ---------- (C) Modelo ----------
    model = ChatOpenAI(model="gpt-4.1-2025-04-14")

    # ---------- (D) Subtool: SQL-only con FEW-SHOTS ----------
    FEW_SHOTS = """
    # Demostraciones (aprende el patrón):
    # 1) Gini global (usa 'tipo=gini', 'estadistico=global' opcional)
    # Pregunta: Gini del modelo 'Cobranza Banca Persona' en 202502
    # SQL (patrón):
    # SELECT *
    # FROM performance
    # WHERE lower(modelo) = lower('Cobranza Banca Persona')
    #   AND periodo = '202502'
    #   AND lower(tipo) = lower('gini')
    # 

    # 2) TM por corte (usa 'tipo=TM' y detalla 'estadistico')
    # Pregunta: TM del modelo 'X' en 202501 para score>=700
    # SQL (patrón):
    # SELECT *
    # FROM performance
    # WHERE lower(modelo) = lower('X')
    #   AND periodo = '202501'
    #   AND lower(tipo) = lower('tm')
    #   AND variable = 'puntuacion bucket'
    #   AND estadistico = 'score>=700'
    # 
    """.strip()

    prompt_sql_only = ChatPromptTemplate.from_template("""
    Eres experto en Athena (Presto/Trino).
    TAREA ÚNICA: DEVUELVE SOLO UNA SENTENCIA SQL (SELECT). NADA MÁS, si el campo es string todo los where que generes deben ser con la clausula lower en los 2 comparativos

    Esquema (tabla performance):
    {schema}

    HINTS:
    {hints}

    {few_shots}

    Pregunta del usuario: {question}
    SQL:
    """)

    sql_only_chain = (
        RunnablePassthrough.assign(
            schema=lambda _: SCHEMA_PERFORMANCE,
            hints=lambda _: json.dumps(HINTS, ensure_ascii=False),
            few_shots=lambda _: FEW_SHOTS,
        )
        | prompt_sql_only
        | model.bind(stop=["\nSQLResult:", "\nRespuesta:", "\nExplanation:"])
        | StrOutputParser()
        | RunnableLambda(_to_sql_only)   # limpia
        | RunnableLambda(_fix_gini_ks_auc)  # corrige si aún vino mal
    )

    # ---------- (E) Ejecutor SQL ----------
    def run_query(query: str) -> str:
        """Ejecuta una query SQL en Athena y devuelve resultados como string."""
        # print(query)  # útil para debug
        return db_athena.run(query)

    # ---------- (F) Prompt de interpretación ----------
    prompt_interpret = ChatPromptTemplate.from_template("""
    Eres analista de Model Risk Monitoring, especialista en responder resultados sobres las metricas de performance del Modelo
    Responde la consulta del usuario en lenguaje claro y que se entienda

    Contexto (schema):
    {schema}

    Pregunta: {question}
    SQL generada: {query}
    Resultado bruto:
    {response}

    Explicación:
    """)

    # ---------- (G) Cadena completa ----------
    def _exec_query(vars: Dict[str, Any]) -> Dict[str, Any]:
        sql = vars["query"]
        print(sql)
        try:
            resp = run_query(sql)
        except Exception as e:
            resp = f"__ERROR__ {type(e).__name__}: {e}"
        return {**vars, "response": resp}

    interpret_chain = (
        RunnablePassthrough.assign(
            schema=lambda _: SCHEMA_PERFORMANCE,
            query=sql_only_chain,
        )
        | RunnableLambda(_exec_query)
        | prompt_interpret
        | model
        | StrOutputParser()
    )

    # ---------- (H) Tool exportable ----------
    tool_preguntar_e_interpretar = interpret_chain.as_tool(
        name="preguntar_e_interpretar_performance",
        description="Genera la SQL sobre 'performance', la ejecuta en Athena y explica el resultado en lenguaje claro. Usa esta herramienta cuando te consulten sobre performance idicadores reportados , temas de indicadores de monitoreo reportados"
    )


    # Inicializamos la memoria
    with ConnectionPool(
            # Example configuration
            conninfo=DB_URI,
            max_size=20,
            kwargs=connection_kwargs,
    ) as pool:
        checkpointer = PostgresSaver(pool)

        # Inicializamos el modelo
        model = ChatOpenAI(model="gpt-4.1-2025-04-14")

        # Agrupamos las herramientas
        tolkit = [tool_rag_reg, tool_rag_bitacora,tool_rag_docs,tool_preguntar_e_interpretar]

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                """
                Eres un asistente gentil para consultar y llevar el control de la gestion de monitoreo sobre modelos de machine learning en un banco
                Utiliza únicamente las herramientas disponibles para responder y brindar infromacion.
                Si no cuentas con una herramienta específica para resolver una pregunta, infórmalo claramente e indica como pueded ayudar.

                Tu objetivo es guiar a los colaboradores de forma amigable, breve y conversacional, como si fueras un expero en el tema Sigue estos pasos:

                1. Saluda y pregunta: Da un saludo cálido, pregunta qué busca el colaborador y si tiene una idea clara de lo que necesita (ej. Ver modelos, indicadores de performance, estabilidad, documentacion metodologica).
                2. Consulta productos: Usa la información de productos segun su necesidad para responder con detalles de productos relevantes (nombre, descripción, precio, stock). Destaca los que tienen mayor disponibilidad
                3. Estilo: Sé breve, usa un tono entusiasta y natural. Evita tecnicismos a menos que el cliente los mencione. Responde solo lo necesario para avanzar la conversación.

                """),
                ("human", "{messages}"),
            ]
        )


        # inicializamos el agente
        agent_executor = create_react_agent(model, tolkit, checkpointer=checkpointer, prompt=prompt)
        # ejecutamos el agente
        config = {"configurable": {"thread_id": id_agente}}
        response = agent_executor.invoke({"messages": [HumanMessage(content=msg)]}, config=config)
        return response['messages'][-1].content


if __name__ == '__main__':
    # La aplicación escucha en el puerto 8080, requerido por Cloud Run
    app.run(host='0.0.0.0', port=8080)
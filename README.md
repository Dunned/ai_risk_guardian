# Proyecto: **AI Risk Guardian v24**

## 📌 Descripción General
**AI Risk Guardian v24** es un asistente conversacional especializado en **Model Risk Management (MRM)**, diseñado para apoyar a equipos de riesgo en el monitoreo, validación y gestión de modelos de machine learning en un banco.  
Integra autenticación segura, interfaz moderna y un agente de IA con capacidades de consulta regulatoria, generando una experiencia enfocada en eficiencia y cumplimiento normativo.

---

## 🎯 Objetivo
Facilitar la **consulta, documentación y control regulatorio de modelos de riesgo**, proporcionando respuestas rápidas y confiables a través de una plataforma interactiva y segura.

---

## ⚙️ Funcionalidades Clave
- 🔐 **Autenticación con Google** vía *NextAuth*, restringida a personal autorizado.  
- 💬 **Interfaz de chat elegante** con historial de conversaciones y roles diferenciados (usuario / asistente).  
- 🤖 **Agente de IA especializado en MRM**, con capacidad de responder sobre:
  - Validación de modelos.  
  - Métricas regulatorias (Gini, KS, PSI, etc.).  
  - Cumplimiento SBS / Basilea.  
  - Documentación técnica.  
- 📊 **Respuestas en tiempo real**, integradas con APIs internas.  
- 🎨 **UI moderna y responsiva** construida con *Next.js*, *TailwindCSS* y animaciones personalizadas.  

---

## 🧩 Metodología
1. **Diseño Frontend:** Next.js + TailwindCSS con enfoque en experiencia de usuario intuitiva.  
2. **Autenticación Segura:** NextAuth con OAuth2 (Google) y control de acceso exclusivo.  
3. **Agente Conversacional:** Integración con LLMs y pipeline de procesamiento de consultas para adaptar respuestas al dominio de riesgo de modelos.  
4. **Iteraciones Agile:** Desarrollo incremental, validando con el equipo de monitoreo regulatorio.  

---

## 🚀 Impacto Esperado
- ⏱️ **Reducción de tiempos** en validación y consultas regulatorias.  
- 📑 **Mejor trazabilidad** de documentación de modelos y sus métricas.  
- 🛡️ **Cumplimiento regulatorio** reforzado mediante un asistente especializado.  
- 👨‍💻 **Soporte a analistas** en tareas repetitivas, liberando tiempo para análisis de valor agregado.  

---

## 🛠️ Tecnologías Utilizadas
- **Frontend:** Next.js 14, React, TailwindCSS.  
- **Backend / API:** Next.js Route Handlers.  
- **Autenticación:** NextAuth (OAuth2 con Google).  
- **IA:** LLMs (OpenAI GPT), agentes especializados.  
- **Infraestructura:** Vercel para despliegue.  

---

👉 Este proyecto se posiciona como un **“consultor digital regulatorio”** dentro del banco, enfocado en MRM, y es escalable hacia nuevas funciones como monitoreo en tiempo real, integración con bases de métricas (Athena, S3) y generación automática de reportes regulatorios.

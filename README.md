# Simulador ATS - Sistema de Reclutamiento con IA

Sistema experto de matching entre vacantes y candidatos utilizando AGNO + Groq con análisis semántico avanzado.

## 🎯 Características Principales

### 🧠 Análisis Semántico Inteligente
- **No usa keyword matching exacto**: "React" = "ReactJS" = "Frontend con librerías modernas JS"
- Comprende sinónimos y tecnologías relacionadas
- Evalúa contexto y relevancia, no solo coincidencias textuales

### ✅ Compliance Checking Automático
- Verificación de requisitos legales (permisos de trabajo, ubicación, educación)
- **Regla crítica**: Si un requisito excluyente no se cumple → Score 0% y estado RECHAZADO
- Cumplimiento normativo automatizado

### 📊 Scoring Ponderado
- **50%** Hard Skills (tecnologías, herramientas, idiomas técnicos)
- **30%** Experiencia (años y relevancia del sector)
- **20%** Soft Skills / Culture Fit (inferidas del texto)

### 🔒 Anonimización de Datos PII
- Ignora nombre, género, edad, foto
- Evaluación objetiva basada solo en méritos profesionales
- Cumple normativas de no discriminación

### 📋 Reportes Estructurados
- Análisis detallado en formato JSON
- Recomendaciones personalizadas
- Resumen ejecutivo y análisis completo

---

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-dotenv groq agno openai
```

### 2. Configurar Variables de Entorno

Edita el archivo `.env`:

```env
# API Keys
GROQ_API_KEY=tu_clave_real_de_groq

# Configuración del Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Ejecutar el Servidor

```bash
python main.py
```

**Servidor disponible en**: `http://localhost:8000`

---

## 📚 Documentación de la API

**Swagger UI (Interactiva)**: http://localhost:8000/docs

---

## 🎯 Endpoint Principal

### Matching ATS ⭐
```http
POST /api/v1/ats/match
```

**Ejemplo de petición completa en Swagger UI**

Accede a http://localhost:8000/docs y prueba el endpoint interactivamente con los datos de ejemplo precargados.

---

## 📊 Algoritmo de Matching

1. **Ingesta y Anonimización** - Elimina datos PII
2. **Compliance Checking** - Verifica requisitos legales (❌ Fallo → Score 0%)
3. **Análisis Semántico** - Compara habilidades, experiencia y soft skills
4. **Scoring Ponderado** - 50% Hard + 30% Exp + 20% Soft
5. **Reporte JSON** - Genera análisis detallado con recomendaciones

---

## 🔒 Seguridad

- ✅ Anonimización de datos PII
- ✅ Evaluación objetiva sin discriminación
- 🔐 Nunca compartas tu GROQ_API_KEY

---

## 🚂 Despliegue en Railway

### Despliegue Rápido

1. **Push tu código a GitHub**:
   ```bash
   git add .
   git commit -m "Preparar para Railway"
   git push origin main
   ```

2. **Crear proyecto en Railway**:
   - Ve a [railway.app](https://railway.app/)
   - Clic en "New Project" → "Deploy from GitHub repo"
   - Selecciona este repositorio

3. **Configurar variables de entorno** en Railway:
   ```
   GROQ_API_KEY=tu_api_key_real
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   ```

4. **¡Listo!** Railway desplegará automáticamente tu aplicación.

📖 **Guía completa**: Ver [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

---

**¡Sistema listo para probar en Swagger! 🚀**

# 🔧 Troubleshooting Railway - "Application failed to respond"

## ✅ Cambios Realizados

He actualizado los siguientes archivos para solucionar el error:

1. **main.py** - Agregado health check endpoints (`/` y `/health`)
2. **railway.json** - Configurado `healthcheckPath` y `healthcheckTimeout`
3. **Procfile** - Agregado `--timeout-keep-alive 75`

## 🚨 Causas Comunes del Error

### 1. Variables de Entorno Faltantes ⚠️ CRÍTICO

Railway necesita la variable `GROQ_API_KEY`. Ve a tu dashboard de Railway:

**Pasos:**
1. Abre tu proyecto en Railway
2. Click en tu servicio
3. Ve a **"Variables"** (tab superior)
4. Agrega estas variables:

```bash
GROQ_API_KEY=gsk_tu_api_key_real_aqui
GROQ_MODEL=llama-3.3-70b-versatile
HOST=0.0.0.0
DEBUG=False
```

⚠️ **IMPORTANTE**: Reemplaza `gsk_tu_api_key_real_aqui` con tu API key real de Groq (desde https://console.groq.com/)

### 2. Puerto Incorrecto

✅ **Ya está corregido** - Todos los archivos ahora usan `$PORT` correctamente.

Railway asigna dinámicamente un puerto a través de la variable `$PORT`. Nuestros archivos de configuración ya lo usan correctamente.

### 3. Health Check Timeout

✅ **Ya está corregido** - He agregado:
- Endpoint `/` para health check
- Endpoint `/health` como alternativa
- `healthcheckTimeout: 300` en railway.json
- `--timeout-keep-alive 75` en uvicorn

## 📋 Pasos para Desplegar

### 1. Commit y Push los Cambios

```bash
git add .
git commit -m "fix: Agregar health checks y mejorar configuración de Railway"
git push origin main
```

### 2. En Railway Dashboard

#### Verificar Variables de Entorno PRIMERO
Antes de desplegar, **asegúrate de que GROQ_API_KEY esté configurada**:

1. Ve a tu proyecto en Railway
2. Click en "Variables"
3. Verifica que `GROQ_API_KEY` tenga un valor válido
4. Si no existe, agrégala ahora

#### Redeploy
1. Ve a "Deployments"
2. Click en "Deploy" o espera el redeploy automático
3. Observa los logs en tiempo real

### 3. Verificar los Logs

Busca estas líneas en los logs de deployment:

#### ✅ Señales de Éxito:
```
Installing dependencies...
✅ Dependencies installed correctly
Starting server...
🚀 Simulador ATS v2.0.0 iniciado
✅ GROQ_API_KEY configurada: True
```

#### ❌ Señales de Error:
```
❌ Error en startup: GROQ_API_KEY no está configurada
ModuleNotFoundError: No module named 'fastapi'
Error: Application failed to respond
```

## 🧪 Verificar el Deployment

Una vez desplegado, prueba estos endpoints:

1. **Health Check Root**: `https://tu-app.up.railway.app/`
   - Debería retornar: `{"status":"healthy","app":"Simulador ATS..."}`

2. **Health Check Alt**: `https://tu-app.up.railway.app/health`
   - Debería retornar: `{"status":"ok","app":"Simulador ATS..."}`

3. **Documentación**: `https://tu-app.up.railway.app/docs`
   - Debería mostrar la interfaz de Swagger UI

4. **API Info**: `https://tu-app.up.railway.app/api/v1/`
   - Debería retornar información del servicio

## 🐛 Si Aún Falla

### Paso 1: Revisar Logs Completos
1. En Railway, ve a "Deployments"
2. Click en el deployment más reciente
3. Copia TODOS los logs
4. Busca mensajes de error específicos

### Paso 2: Verificar Build
Asegúrate de que el build se complete exitosamente:
```
✓ nixpacks build finished
✓ Dependencies installed
✓ Starting server
```

### Paso 3: Verificar Variables de Entorno
Ejecuta este comando en la terminal de Railway (si está disponible):
```bash
echo $GROQ_API_KEY
```
Debería mostrar tu API key (oculta parcialmente).

### Paso 4: Configuración Manual (último recurso)

Si nada funciona, configura manualmente en Railway Settings:

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 75
```

## 📞 Información para Soporte

Si necesitas reportar el error, incluye:

1. ✅ **Request ID**: `KUrm3TRxSuqyvqKtezItjw` (el que mencionaste)
2. ✅ **Logs completos** del deployment
3. ✅ **Variables de entorno** configuradas (sin mostrar valores sensibles)
4. ✅ **Versión de Python**: Python 3.11 (según runtime.txt)
5. ✅ **Framework**: FastAPI + Uvicorn

## 🎯 Checklist Final

Antes de desplegar, verifica:

- [ ] ✅ Archivo `railway.json` actualizado
- [ ] ✅ Archivo `main.py` tiene health checks
- [ ] ✅ `GROQ_API_KEY` configurada en Railway Variables
- [ ] ✅ Variables `GROQ_MODEL`, `HOST`, `DEBUG` configuradas
- [ ] ✅ Archivos committeados y pusheados a GitHub
- [ ] ✅ Build completa exitosamente en Railway
- [ ] ✅ Logs muestran "iniciado" y "GROQ_API_KEY configurada: True"
- [ ] ✅ Health check endpoint responde correctamente

## 🚀 Resultado Esperado

Después de seguir estos pasos, tu aplicación debería:

1. ✅ Desplegar sin errores
2. ✅ Responder al health check en la raíz `/`
3. ✅ Mostrar documentación en `/docs`
4. ✅ Aceptar requests al endpoint `/api/v1/ats/match`

**URL de tu aplicación**: `https://[tu-proyecto].up.railway.app`

---

**Última actualización**: 12 de enero de 2026

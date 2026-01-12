# 🚂 Despliegue en Railway

Esta guía te ayudará a desplegar la aplicación de Simulador ATS en Railway.

## 📋 Requisitos Previos

- Cuenta en [Railway](https://railway.app/)
- API Key de Groq (obtener en [console.groq.com](https://console.groq.com))
- Repositorio Git (GitHub, GitLab, etc.)

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de que tu código esté subido a GitHub:

```bash
git add .
git commit -m "Preparar para despliegue en Railway"
git push origin main
```

### 2. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app/) e inicia sesión
2. Haz clic en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio `ia_usabilidad`

### 3. Configurar Variables de Entorno

En el dashboard de Railway, ve a la pestaña "Variables" y agrega:

```
GROQ_API_KEY=tu_api_key_real_de_groq
HOST=0.0.0.0
PORT=8000
DEBUG=False
GROQ_MODEL=llama-3.3-70b-versatile
```

⚠️ **IMPORTANTE**: Reemplaza `tu_api_key_real_de_groq` con tu API key real de Groq.

### 4. Desplegar

Railway detectará automáticamente los archivos de configuración y desplegará tu aplicación.

El despliegue puede tardar 2-3 minutos. Railway:
- Detectará que es una aplicación Python
- Instalará las dependencias desde `requirements.txt`
- Ejecutará el comando definido en `Procfile` o `railway.json`

### 5. Acceder a tu Aplicación

Una vez desplegado:
1. Railway te proporcionará una URL pública (ej: `https://tu-app.up.railway.app`)
2. Accede a la documentación en: `https://tu-app.up.railway.app/docs`
3. El endpoint principal está en: `https://tu-app.up.railway.app/api/v1/`

## 📝 Archivos de Configuración Creados

- **requirements.txt**: Dependencias de Python
- **Procfile**: Comando para iniciar el servidor
- **railway.json**: Configuración específica de Railway
- **.env.example**: Plantilla de variables de entorno

## 🔧 Configuración Personalizada

### Cambiar el Puerto

Railway asigna automáticamente el puerto a través de la variable `$PORT`. No es necesario modificarlo.

### Habilitar Debug

Para debugging temporal, cambia en las variables de entorno:
```
DEBUG=True
```

### Cambiar el Modelo de Groq

Puedes usar otros modelos disponibles en Groq:
```
GROQ_MODEL=mixtral-8x7b-32768
GROQ_MODEL=llama-3.1-70b-versatile
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fastapi'"

Este error indica que Railway no está instalando las dependencias. **Soluciones**:

1. **Verifica que estos archivos existan en tu repositorio**:
   - `requirements.txt`
   - `runtime.txt` (contiene: `3.11`)
   - `nixpacks.toml`
   - `railway.json`

2. **Forzar reinstalación**:
   - En Railway, ve a Settings → Redeploy
   - O empuja un commit dummy:
     ```bash
     git commit --allow-empty -m "Forzar redeploy"
     git push
     ```

3. **Verificar logs de build**:
   - En Railway, ve a Deployments → Click en el deployment activo
   - Busca en los logs si dice "Installing dependencies"
   - Si no aparece, Railway no está detectando requirements.txt

4. **Configurar Build Command manualmente**:
   - Ve a Settings → Build Command
   - Agrega: `pip install --upgrade pip && pip install -r requirements.txt`

5. **Verificar estructura del repositorio**:
   - Asegúrate de que `requirements.txt` esté en la raíz del proyecto
   - No debe estar en una subcarpeta

### Error: "Application failed to respond"
- Verifica que `GROQ_API_KEY` esté configurada correctamente
- Revisa los logs en Railway para más detalles

### Error: "Build failed"
- Asegúrate de que `requirements.txt` esté en la raíz del proyecto
- Verifica que todas las dependencias tengan versiones válidas

### Error de API Key
- Verifica que la API key de Groq sea válida
- Comprueba que la variable de entorno esté configurada sin espacios

## 📊 Monitoreo

Railway proporciona:
- **Logs en tiempo real**: Pestaña "Deployments" → Click en el despliegue activo
- **Métricas de uso**: CPU, memoria, ancho de banda
- **Health checks automáticos**: Railway verifica que tu app responda

## 💰 Costos

Railway ofrece:
- **Plan gratuito**: $5 de crédito mensual (suficiente para desarrollo/pruebas)
- **Plan Pro**: $20/mes con más recursos

## 🔗 Enlaces Útiles

- [Documentación de Railway](https://docs.railway.app/)
- [Groq API Docs](https://console.groq.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## ✅ Verificación Post-Despliegue

Prueba estos endpoints para verificar que todo funciona:

```bash
# Health check
curl https://tu-app.up.railway.app/api/v1/

# Info del sistema ATS
curl https://tu-app.up.railway.app/api/v1/ats/info

# Documentación interactiva
# Abre en el navegador: https://tu-app.up.railway.app/docs
```

---

¿Necesitas ayuda? Revisa los logs en Railway o consulta la documentación oficial.

# 🤖 Recruitment Agent - Prototipo Funcional

Sistema automatizado para analizar CVs y compararlos contra vacantes usando IA (Gemini API).

## 🚀 Características

- **Análisis de CVs**: Procesamiento de archivos PDF y Word
- **Matching Inteligente**: Comparación automática con vacantes usando Gemini API
- **Clasificación Automática**: Niveles de compatibilidad y recomendaciones
- **Interfaz Web**: HTML simple con Bootstrap para fácil uso

## 🛠️ Tecnologías

- **Backend**: FastAPI (Python)
- **IA**: Gemini API (Google)
- **Procesamiento**: pdfplumber, python-docx
- **Frontend**: HTML + Bootstrap + JavaScript
- **HTTP**: requests

## 📁 Estructura del Proyecto

```
recruitment-agent/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias Python
├── env.example         # Variables de entorno ejemplo
├── templates/          # Plantillas HTML
│   ├── index.html      # Página principal
│   └── admin.html      # Panel de administración
├── uploads/            # Archivos temporales (se crea automáticamente)
└── README.md
```

## 🚀 Instalación y Uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar API Key
```bash
cp env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

### 3. Ejecutar la aplicación
```bash
python main.py
```

### 4. Acceder a la aplicación
- **Página principal**: http://localhost:8000
- **Panel admin**: http://localhost:8000/admin
- **Documentación API**: http://localhost:8000/docs

## 🔧 Configuración

### Variables de Entorno (.env)
```env
GEMINI_API_KEY=tu_api_key_de_gemini
PORT=8000
HOST=0.0.0.0
```

### Obtener API Key de Gemini
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la key en tu archivo `.env`

## 📋 Uso del Sistema

### 1. Subir CV
1. Ve a http://localhost:8000
2. Selecciona una vacante del dropdown
3. Arrastra o selecciona un archivo PDF o Word
4. Haz clic en "Analizar CV"

### 2. Ver Resultados
El sistema mostrará:
- **Calificación**: Muy compatible, Compatible, No compatible
- **Recomendación**: Agendar entrevista, Revisar por reclutador, Descartar
- **Justificación**: Explicación del análisis

### 3. Administrar Vacantes
1. Ve a http://localhost:8000/admin
2. Agrega nuevas vacantes con título y descripción
3. Las vacantes estarán disponibles en el dropdown principal

## 🔌 API Endpoints

- `GET /` - Página principal
- `GET /admin` - Panel de administración
- `POST /upload-cv` - Subir y analizar CV
- `POST /add-job` - Agregar nueva vacante
- `GET /jobs` - Listar vacantes (JSON)

## 🎯 Funcionalidades

### Análisis de CVs
- ✅ Extracción de texto de PDF
- ✅ Extracción de texto de Word (.docx)
- ✅ Validación de archivos
- ✅ Limpieza automática de archivos temporales

### Análisis con IA
- ✅ Prompt optimizado para Gemini
- ✅ Clasificación automática
- ✅ Recomendaciones inteligentes
- ✅ Justificación detallada

### Gestión de Vacantes
- ✅ Vacante precargada por defecto
- ✅ Agregar nuevas vacantes
- ✅ Lista dinámica en frontend
- ✅ Persistencia en memoria

## 🧠 Prompt de Gemini

El sistema usa un prompt optimizado que:
1. Recibe el texto del CV y descripción de la vacante
2. Analiza compatibilidad basada en:
   - Experiencia relevante
   - Habilidades técnicas
   - Años de experiencia
   - Compatibilidad cultural
3. Devuelve respuesta estructurada en JSON

## 🔮 Próximas Mejoras

- [ ] Base de datos para persistencia
- [ ] Autenticación de usuarios
- [ ] Historial de análisis
- [ ] Exportación de reportes
- [ ] Múltiples formatos de CV
- [ ] Integración con ATS
- [ ] Análisis de sentimiento
- [ ] Recomendaciones personalizadas

## 🐛 Solución de Problemas

### Error: "Gemini API key not configured"
- Verifica que tu archivo `.env` tenga `GEMINI_API_KEY=tu_key_aqui`

### Error: "Could not extract text from file"
- Asegúrate de que el archivo sea PDF o DOCX válido
- Verifica que el archivo no esté corrupto

### Error: "Invalid response from Gemini API"
- Verifica tu conexión a internet
- Confirma que tu API key sea válida

## 📄 Licencia

MIT License - Libre para uso comercial y personal.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Cómo correr el proyecto en localhost

1. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

2. (Opcional) Si necesitas el proceso Context7 MCP, en otra terminal ejecuta:
   ```bash
   npx -y @upstash/context7-mcp@latest
   ```
   Si no sabes para qué sirve, puedes omitir este paso y probar solo el backend.

3. Ejecuta el backend:
   ```bash
   python3 main.py
   ```
   Esto levantará el servidor en http://127.0.0.1:8000

4. Accede a la aplicación desde tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Cómo obtener tu API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google (de preferencia personal, no institucional).
3. Haz clic en "Create API key" o "Crear clave de API".
4. Copia la clave generada (comienza con `AIza...`).
5. Guarda tu clave en un lugar seguro. No la compartas públicamente.
6. Usa esta clave en el campo correspondiente de la aplicación (no es necesario ponerla en archivos de configuración).

**Nota:**
- La API key es personal y tiene límites de uso gratuitos.
- Si ves errores de cuota, puedes crear otra clave o esperar al siguiente día.
- No compartas tu clave en foros, repositorios públicos ni con terceros. 
# 🤖 Recruitment Agent

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
Recruitment-Agent/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias Python
├── templates/           # Plantillas HTML
│   ├── index.html       # Página principal
│   └── admin.jinja2     # Panel de administración
├── uploads/             # Archivos temporales (se crea automáticamente)
├── static/              # Archivos estáticos (vacío por defecto)
├── .gitignore           # Exclusiones de git
└── README.md
```

## 🚀 Instalación y Uso Local

1. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación localmente:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Esto levantará el servidor en http://127.0.0.1:8000

3. Accede a la aplicación desde tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000)

4. Cuando subas un CV, la aplicación te pedirá tu API Key de Gemini (no necesitas editar archivos de entorno).

## 🚀 Despliegue en Render o Producción

1. Sube el proyecto a GitHub.
2. En Render, selecciona el repositorio y usa el siguiente comando de arranque:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. No necesitas configurar variables de entorno para la API key, ya que se ingresa desde el frontend.

## Cómo obtener tu API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google (de preferencia personal, no institucional).
3. Haz clic en "Create API key" o "Crear clave de API".
4. Copia la clave generada (comienza con `AIza...`).
5. Pega la clave en el campo correspondiente de la aplicación web.

**Nota:**
- La API key es personal y tiene límites de uso gratuitos.
- Si ves errores de cuota, puedes crear otra clave o esperar al siguiente día.
- No compartas tu clave en foros, repositorios públicos ni con terceros.

## 📋 Uso del Sistema

### 1. Subir CV
1. Ve a la página principal.
2. Selecciona una vacante del dropdown.
3. Ingresa tu API key de Gemini.
4. Arrastra o selecciona un archivo PDF o Word.
5. Haz clic en "Analizar CV".

### 2. Ver Resultados
El sistema mostrará:
- **Calificación**: Muy compatible, Compatible, No compatible
- **Recomendación**: Agendar entrevista, Revisar por reclutador, Descartar
- **Justificación**: Explicación del análisis
- **Mensaje para el candidato**: Texto personalizado generado por IA

### 3. Administrar Vacantes
1. Ve a /admin
2. Agrega nuevas vacantes con título y descripción (puedes cargar desde PDF o Word)
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

- **Error: la API key es inválida o está mal configurada**: Verifica que tu clave sea correcta y esté vigente.
- **Error de cuota**: Espera al siguiente día o crea una nueva API key.
- **Error al extraer texto**: Asegúrate de que el archivo sea PDF o DOCX válido.

## 📄 Licencia

MIT License - Libre para uso comercial y personal.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request 
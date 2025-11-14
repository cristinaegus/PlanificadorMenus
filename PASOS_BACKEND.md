# 🚀 Pasos para Configurar el Backend con IA

## 📦 Lo que se ha creado:

```
backend/
├── app.py              # Servidor FastAPI con endpoints
├── ai_menu.py          # Lógica de generación con OpenAI
├── requirements.txt    # Dependencias Python
├── .env.example        # Template para configuración
├── .gitignore         # Ignorar archivos sensibles
└── README.md          # Documentación completa
```

## 🎯 Próximos pasos para usar el backend:

### 1. Instalar dependencias Python

Abre una terminal en la carpeta `backend/` y ejecuta:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar tu API Key de OpenAI

1. Obtén una API key en: https://platform.openai.com/api-keys
2. Crea un archivo `.env` copiando el ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Edita el archivo `.env` y añade tu API key:
   ```env
   OPENAI_API_KEY=sk-tu_api_key_aqui
   ```

### 3. Iniciar el servidor backend

Ejecuta el servidor con:

```bash
python app.py
```

O alternativamente con uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: **http://localhost:8000**

### 4. Verificar que funciona

Abre tu navegador y visita: http://localhost:8000

Deberías ver un mensaje confirmando que la API está activa.

## 🚀 Características del backend:

- ✅ **Generar menú semanal completo** con preferencias y restricciones dietéticas
- ✅ **Sugerir platos específicos** para un día y comida concreta
- ✅ **CORS configurado** para conectar con tu frontend React (puerto 5173)
- ✅ **API REST** fácil de integrar

## 📡 Endpoints disponibles:

### Generar menú completo
```http
POST http://localhost:8000/generar-menu
Content-Type: application/json

{
  "preferencias": "Me gusta el pescado y las verduras",
  "restricciones": "Sin gluten",
  "tipo_cocina": "mediterránea"
}
```

### Sugerir un plato específico
```http
POST http://localhost:8000/sugerir-comida
Content-Type: application/json

{
  "dia": "Lunes",
  "tipo_comida": "comida",
  "estilo": "mediterráneo"
}
```

## 🔗 Próximo paso: Integración con React

Una vez que el backend esté funcionando, se puede integrar en tu aplicación React para que los usuarios generen menús automáticamente con un botón.

## ⚠️ Notas importantes:

- La API de OpenAI tiene costos por uso (GPT-3.5-turbo es económico)
- Nunca subas el archivo `.env` con tu API key a repositorios públicos
- El archivo `.gitignore` ya está configurado para proteger tu `.env`
## integracion con React 
¡Perfecto! He integrado completamente la funcionalidad de IA en tu aplicación React.

🎉 ¿Qué se ha agregado?
1. Botón "Generar con IA" ✨
Aparece junto al botón de imprimir
Abre un modal para configurar las preferencias
2. Modal de configuración con:
Selector de persona: Elige si generar el menú para Cristina o Marisa
Tipo de cocina: Mediterránea, Asiática, Italiana, etc.
Preferencias: Campo opcional (ej: "Me gusta el pescado")
Restricciones: Campo opcional (ej: "Sin gluten")
3. Conexión con el backend
Llama al endpoint http://localhost:8000/generar-menu
Muestra un spinner mientras genera
Aplica el menú generado a la tabla seleccionada
🚀 Cómo probarlo:
Inicia el backend (si no lo has hecho):


cd backendpython app.py
La aplicación React ya debería estar corriendo en http://localhost:5173

Prueba la funcionalidad:

Haz clic en el botón "Generar con IA" (morado con icono de estrella)
Selecciona para quién generar (Cristina o Marisa)
Elige el tipo de cocina
Opcionalmente añade preferencias y restricciones
Haz clic en "Generar"
¡El menú se llenará automáticamente!
⚠️ Nota importante:
Asegúrate de tener:

✅ El backend corriendo en http://localhost:8000
✅ Tu API Key de OpenAI configurada en el archivo .env
✅ Las dependencias instaladas (pip install -r requirements.txt)
¿Quieres probar la funcionalidad ahora o necesitas ayuda con algo más?


## creamos un entorno virtual para el backend
python -m venv venv
# Activar el entorno virtual    
¡Excelente! ✅ Todo está configurado:

✅ Entorno virtual creado en venv
✅ Entorno activado (ves el (venv) en el prompt)
✅ Dependencias instaladas:
FastAPI
Uvicorn
Requests (para Spoonacular)
Python-dotenv
Pydantic

Claude Sonnet 4.5 • 1x
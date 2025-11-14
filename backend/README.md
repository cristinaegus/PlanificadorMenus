# Backend - Generador de Menús con IA

Backend en Python con FastAPI y OpenAI para generar menús semanales automáticamente.

## 📋 Requisitos

- Python 3.8 o superior
- API Key de OpenAI ([obtener aquí](https://platform.openai.com/api-keys))

## 🚀 Instalación

### 1. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar API Key de OpenAI

Crea un archivo `.env` en la carpeta `backend/`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tu API Key:

```env
OPENAI_API_KEY=sk-tu_api_key_aqui
```

### 3. Iniciar el servidor

```bash
python app.py
```

O con uvicorn directamente:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

## 📡 Endpoints API

### 1. Verificar estado
```http
GET http://localhost:8000/
GET http://localhost:8000/health
```

### 2. Generar menú semanal completo
```http
POST http://localhost:8000/generar-menu
Content-Type: application/json

{
  "preferencias": "Me gusta el pescado y las verduras",
  "restricciones": "Sin gluten",
  "tipo_cocina": "mediterránea"
}
```

**Respuesta:**
```json
{
  "success": true,
  "menu": {
    "Lunes": {"lunch": "Ensalada de quinoa con aguacate", "dinner": "Salmón al horno con espárragos"},
    "Martes": {"lunch": "...", "dinner": "..."},
    ...
  }
}
```

### 3. Sugerir un plato específico
```http
POST http://localhost:8000/sugerir-comida
Content-Type: application/json

{
  "dia": "Lunes",
  "tipo_comida": "comida",
  "estilo": "mediterráneo"
}
```

**Respuesta:**
```json
{
  "success": true,
  "sugerencia": "Paella de mariscos",
  "dia": "Lunes",
  "tipo_comida": "comida"
}
```

## 🔧 Estructura de archivos

```
backend/
├── app.py              # Servidor FastAPI con endpoints
├── ai_menu.py          # Lógica de IA con OpenAI
├── requirements.txt    # Dependencias Python
├── .env.example        # Template de variables de entorno
├── .env               # Tu configuración (no incluir en git)
└── README.md          # Esta documentación
```

## 🌐 Integración con Frontend

El backend ya está configurado con CORS para aceptar peticiones desde:
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (Create React App)

Para llamar desde React:

```javascript
// Generar menú completo
const response = await fetch('http://localhost:8000/generar-menu', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    preferencias: 'Me gusta el pescado',
    restricciones: 'Sin gluten',
    tipo_cocina: 'mediterránea'
  })
});
const data = await response.json();
console.log(data.menu);
```

## 💡 Notas importantes

1. **Costos de OpenAI**: La API de OpenAI tiene costos por uso. GPT-3.5-turbo es más económico que GPT-4.
2. **Rate limits**: OpenAI tiene límites de peticiones por minuto según tu plan.
3. **Seguridad**: Nunca subas el archivo `.env` con tu API key a repositorios públicos.

## 🐛 Troubleshooting

### Error: "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### Error: "Invalid API Key"
Verifica que tu `.env` tenga la API key correcta y que el archivo esté en la carpeta `backend/`.

### Error de CORS
Agrega el origen de tu frontend en `app.py` en la lista `allow_origins`.

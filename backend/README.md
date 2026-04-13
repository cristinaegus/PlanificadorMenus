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

### 4. Generar PDF menú de casa
```http
POST http://localhost:8000/generar-menu-casa
Content-Type: application/json

{
  "id_cristina": 1,
  "id_marisa": 1
}
```

Retorna un archivo PDF para descargar.

## 🏥 Endpoints de Dietas Médicas

### 1. Generar PDF con todos los modelos de dieta
```http
GET http://localhost:8000/dieta-modelos/generar-pdf-completo
```
Genera un PDF completo con los 4 modelos de dieta de 1000 kcal para cirugía de obesidad.

### 2. Generar PDF de un modelo específico
```http
GET http://localhost:8000/dieta-modelos/generar-pdf-modelo/1
GET http://localhost:8000/dieta-modelos/generar-pdf-modelo/2
GET http://localhost:8000/dieta-modelos/generar-pdf-modelo/3
GET http://localhost:8000/dieta-modelos/generar-pdf-modelo/4
```
Genera un PDF para el modelo específico (1, 2, 3 o 4).

### 3. Generar resumen de modelos
```http
GET http://localhost:8000/dieta-modelos/generar-resumen
```
Genera un PDF con tabla resumen de todos los modelos.

### 4. Obtener información de modelos en JSON
```http
GET http://localhost:8000/dieta-modelos/info
```

**Respuesta:**
```json
{
  "success": true,
  "modelos_disponibles": [1, 2, 3, 4],
  "descripcion": "Modelos de dieta de 1000 kcal para cirugía de obesidad",
  "modelos": { ... }
}
```

## 🔧 Estructura de archivos

```
backend/
├── app.py                     # Servidor FastAPI con endpoints
├── ai_menu.py                 # Lógica de IA con OpenAI
├── menu_casa.py               # Generación de menús de casa
├── dieta_pdf_generator.py     # Generador de PDFs de dietas médicas
├── modelos_dieta.json         # Datos de los 4 modelos de dieta
├── test_dieta_pdf.py          # Script de prueba para PDFs
├── cristina_menu1.json        # Menús de Cristina
├── marisa_menus.json          # Menús de Marisa
├── requirements.txt           # Dependencias Python
├── .env.example               # Template de variables de entorno
├── .env                       # Tu configuración (no incluir en git)
└── README.md                  # Esta documentación
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

### Usar endpoints de dietas médicas desde React

```javascript
// Descargar PDF con todos los modelos
const descargarPDFCompleto = async () => {
  const response = await fetch('http://localhost:8000/dieta-modelos/generar-pdf-completo');
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'modelos_dieta_completos.pdf';
  a.click();
  window.URL.revokeObjectURL(url);
};

// Descargar PDF de un modelo específico
const descargarModelo = async (numero) => {
  const response = await fetch(`http://localhost:8000/dieta-modelos/generar-pdf-modelo/${numero}`);
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `modelo_dieta_${numero}.pdf`;
  a.click();
};

// Obtener información de modelos
const obtenerInfoModelos = async () => {
  const response = await fetch('http://localhost:8000/dieta-modelos/info');
  const data = await response.json();
  return data.modelos;
};
```

## 💡 Notas importantes

1. **Costos de OpenAI**: La API de OpenAI tiene costos por uso. GPT-3.5-turbo es más económico que GPT-4.
2. **Rate limits**: OpenAI tiene límites de peticiones por minuto según tu plan.
3. **Seguridad**: Nunca subas el archivo `.env` con tu API key a repositorios públicos.
4. **PDFs de dietas**: Los PDFs se generan usando ReportLab y se almacenan temporalmente en el servidor.
5. **Modelos médicos**: Los modelos de dieta están basados en documentos de Osakidetza - Unidad de Nutrición 2015.

## 🐛 Troubleshooting

### Error: "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```
O reinstala todas las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Invalid API Key"
Verifica que tu `.env` tenga la API key correcta y que el archivo esté en la carpeta `backend/`.

### Error de CORS
Agrega el origen de tu frontend en `app.py` en la lista `allow_origins`.

### Error: "modelos_dieta.json not found"
Asegúrate de que el archivo `modelos_dieta.json` esté en la carpeta `backend/`.

### Probar funcionalidad de PDFs
Ejecuta el script de prueba:
```bash
python test_dieta_pdf.py
```

# 📋 Estructura de la Aplicación - Planificador de Menús

## 🎯 Descripción General

Aplicación web para planificar menús semanales con dos tablas independientes (Cristina y Marisa) que incluye generación automática de menús mediante inteligencia artificial.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Tabla      │  │   Tabla      │  │   Botón      │ │
│  │  Cristina    │  │   Marisa     │  │  Generar IA  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│              HTTP Request (POST /generar-menu)           │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              app.py (API REST)                    │  │
│  │  • POST /generar-menu                             │  │
│  │  • POST /sugerir-comida                           │  │
│  │  • GET /health                                    │  │
│  └─────────────────────┬────────────────────────────┘  │
│                        │                                 │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────────┐  │
│  │           ai_menu.py (IA & Lógica)                │  │
│  │  • Banco de recetas locales (100+ recetas)        │  │
│  │  • Integración con Spoonacular API (opcional)     │  │
│  │  • Sistema anti-repetición de recetas             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Directorios

```
Planificadormenusapp/
│
├── 📄 index.html                 # Punto de entrada HTML
├── 📄 package.json               # Dependencias frontend
├── 📄 vite.config.ts             # Configuración Vite
├── 📄 tailwind.config.js         # Configuración Tailwind CSS
├── 📄 tsconfig.json              # Configuración TypeScript
├── 📄 .gitignore                 # Archivos ignorados por Git
│
├── 📂 src/                       # CÓDIGO FRONTEND
│   ├── 📄 main.tsx              # Entrada principal React
│   ├── 📄 App.tsx               # Componente principal
│   ├── 📄 index.css             # Estilos globales
│   └── 📄 vite-env.d.ts         # Tipos TypeScript
│
└── 📂 backend/                   # CÓDIGO BACKEND
    ├── 📄 app.py                # Servidor FastAPI
    ├── 📄 ai_menu.py            # Lógica IA y recetas
    ├── 📄 requirements.txt      # Dependencias Python
    ├── 📄 .env                  # Variables de entorno (API keys)
    ├── 📄 test_api.py           # Script de pruebas API
    └── 📄 README.md             # Documentación backend
```

---

## 🎨 FRONTEND - React + TypeScript

### **Tecnologías**
- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool y servidor de desarrollo
- **Tailwind CSS** - Framework de estilos
- **react-to-print** - Generación de PDFs
- **lucide-react** - Iconos

### **Componentes Principales**

#### `App.tsx`
**Responsabilidades:**
- Gestionar estado de dos menús independientes (`weeklyPlanCristina` y `weeklyPlanMarisa`)
- Renderizar dos tablas con días horizontales y comidas verticales
- Interfaz de generación con IA (modal)
- Funcionalidad de impresión/exportación a PDF

**Estados principales:**
```typescript
const [weeklyPlanCristina, setWeeklyPlanCristina] = useState<WeeklyPlan>({...})
const [weeklyPlanMarisa, setWeeklyPlanMarisa] = useState<WeeklyPlan>({...})
const [showAIModal, setShowAIModal] = useState(false)
```

**Funciones clave:**
- `generateMenuWithAI()` - Llama al backend para generar menús
- `handleMealChangeCristina()` - Actualiza comidas de Cristina
- `handleMealChangeMarisa()` - Actualiza comidas de Marisa
- `handlePrint()` - Genera PDF con ambas tablas

### **Estructura de Datos**
```typescript
interface WeeklyPlan {
  [day: string]: {
    lunch: string;
    dinner: string;
  };
}
```

### **Características UI**
- ✅ Tablas con días en horizontal (Lunes a Domingo)
- ✅ Filas para "Comida" y "Cena"
- ✅ Textareas editables en cada celda
- ✅ Diseño responsive
- ✅ Impresión optimizada (landscape, dos tablas por página)
- ✅ Modal con formulario de preferencias para IA

---

## ⚙️ BACKEND - FastAPI + Python

### **Tecnologías**
- **FastAPI 0.104.1** - Framework web moderno
- **Uvicorn** - Servidor ASGI
- **Python 3.13** - Lenguaje de programación
- **python-dotenv** - Gestión de variables de entorno
- **Requests** - Cliente HTTP para APIs externas

### **Endpoints API**

#### `POST /generar-menu`
**Descripción:** Genera un menú semanal completo (14 comidas)

**Request Body:**
```json
{
  "preferencias": "pescado, verduras",
  "restricciones": "sin gluten",
  "tipo_cocina": "mediterránea"
}
```

**Response:**
```json
{
  "menu": {
    "Lunes": {
      "lunch": "Ensalada Griega con Queso Feta",
      "dinner": "Sopa de Verduras"
    },
    "Martes": {
      "lunch": "Pasta con Tomate y Albahaca",
      "dinner": "Tortilla de Patatas"
    },
    ...
  }
}
```

#### `POST /sugerir-comida`
**Descripción:** Sugiere una comida individual

**Request Body:**
```json
{
  "dia": "Lunes",
  "tipo_comida": "comida",
  "estilo": "mediterráneo"
}
```

#### `GET /health`
**Descripción:** Verifica el estado del servidor

**Response:**
```json
{
  "status": "healthy"
}
```

### **Configuración CORS**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🤖 MÓDULO DE INTELIGENCIA ARTIFICIAL

### **Archivo: `ai_menu.py`**

### **1. Banco de Recetas Locales**

**100+ recetas predefinidas** organizadas por:
- 🇬🇷 **Mediterránea** (20 recetas: 10 comidas + 10 cenas)
- 🇮🇹 **Italiana** (20 recetas)
- 🇨🇳 **Asiática** (20 recetas)
- 🇲🇽 **Mexicana** (20 recetas)
- 🇪🇸 **Española** (20 recetas)

**Estructura:**
```python
RECETAS_LOCALES = {
    "mediterranean": {
        "lunch": [
            "Ensalada Griega con Queso Feta",
            "Pasta con Tomate y Albahaca",
            ...
        ],
        "dinner": [
            "Sopa de Verduras",
            "Tortilla de Patatas",
            ...
        ]
    },
    ...
}
```

### **2. Funciones Principales**

#### `generar_menu_semanal(preferencias, restricciones, tipo_cocina)`
**Propósito:** Genera 14 recetas únicas (7 días × 2 comidas)

**Algoritmo:**
1. Mapea el tipo de cocina del usuario a categoría interna
2. Mapea restricciones dietéticas
3. Itera sobre 7 días:
   - Busca receta para comida
   - Busca receta para cena
   - Almacena IDs usados para evitar repetición
4. Retorna diccionario con menú completo

**Sistema anti-repetición:**
```python
used_recipe_ids = []  # Rastrea recetas usadas
lunch_recipe, lunch_id = buscar_receta(..., used_recipe_ids)
used_recipe_ids.append(lunch_id)  # Evita reutilización
```

#### `buscar_receta(cuisine, diet, meal_type, query, exclude_ids)`
**Propósito:** Selecciona una receta única del banco local

**Lógica:**
1. Filtra recetas por tipo de cocina y comida
2. Mezcla aleatoriamente (`random.shuffle`)
3. Busca primera receta no usada (ID no en `exclude_ids`)
4. Genera ID único usando hash del nombre
5. Retorna tupla `(nombre_receta, id_receta)`

**Generación de ID único:**
```python
recipe_id = hash(receta) % 10000  # ID único entre 0-9999
```

### **3. Integración con Spoonacular API (Opcional)**

**Funcionalidad:**
- Si las recetas locales no son suficientes
- Fallback cuando el límite diario no se ha alcanzado
- API Key almacenada en `.env`

**Límites:**
- Plan gratuito: 50 puntos/día
- Cada búsqueda: ~1-2 puntos
- Error 402: límite alcanzado → usa recetas locales

**Configuración:**
```env
SPOONACULAR_API_KEY=c6a71ac36ea14252af855b2f4199cee3
```

---

## 🔄 Flujo de Datos Completo

### **Generación de Menú con IA**

```
1. Usuario hace clic en "Generar con IA" 
   ↓
2. Se abre modal con formulario:
   - Preferencias alimentarias
   - Restricciones dietéticas
   - Tipo de cocina
   ↓
3. Frontend envía POST a /generar-menu
   ↓
4. Backend (app.py) recibe request
   ↓
5. Llama a ai_menu.generar_menu_semanal()
   ↓
6. Para cada día (Lunes-Domingo):
   a. Llama buscar_receta() para comida
   b. Selecciona receta aleatoria no usada
   c. Llama buscar_receta() para cena
   d. Selecciona receta diferente
   ↓
7. Retorna JSON con 14 recetas únicas
   ↓
8. Frontend actualiza ambas tablas
   ↓
9. Usuario puede editar manualmente
   ↓
10. Usuario imprime PDF con ambos menús
```

---

## 🚀 Cómo Ejecutar la Aplicación

### **1. Instalar Dependencias**

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
cd backend
python -m pip install -r requirements.txt
```

### **2. Iniciar Servidores**

**Terminal 1 - Frontend:**
```bash
npm run dev
# Corre en http://localhost:5173
```

**Terminal 2 - Backend:**
```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
# Corre en http://localhost:8000
```

### **3. Acceder a la Aplicación**
Abre tu navegador en: **http://localhost:5173**

---

## 🔧 Configuración de Entorno

### **Backend - `.env`**
```env
SPOONACULAR_API_KEY=tu_api_key_aqui
```

⚠️ **Nota:** Este archivo está en `.gitignore` para proteger credenciales

---

## 📦 Dependencias

### **Frontend (`package.json`)**
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-to-print": "^2.15.1",
    "lucide-react": "^0.index"
  },
  "devDependencies": {
    "typescript": "~5.6.2",
    "vite": "^5.4.8",
    "tailwindcss": "^3.4.14"
  }
}
```

### **Backend (`requirements.txt`)**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.5.0
```

---

## 🎯 Características Implementadas

### ✅ **Funcionalidades Completadas**

#### Frontend
- [x] Dos tablas independientes (Cristina y Marisa)
- [x] Layout horizontal (días en columnas)
- [x] Edición manual de comidas
- [x] Botón "Generar con IA"
- [x] Modal con preferencias personalizables
- [x] Exportación a PDF
- [x] Impresión optimizada (landscape)
- [x] Diseño responsive
- [x] Estado independiente por tabla

#### Backend
- [x] API REST con FastAPI
- [x] Generación de menús semanales
- [x] Sistema anti-repetición de recetas
- [x] Banco de 100+ recetas locales
- [x] Integración con Spoonacular API
- [x] Manejo de errores y fallbacks
- [x] CORS configurado
- [x] Logging detallado

#### IA y Recetas
- [x] 5 tipos de cocina (mediterránea, italiana, asiática, mexicana, española)
- [x] Selección aleatoria sin repetición
- [x] Recetas auténticas y variadas
- [x] IDs únicos para cada receta
- [x] Funciona sin internet (recetas locales)

---

## 🐛 Solución de Problemas

### **"Receta Mediterranean" aparece en lugar de nombres reales**
**Causa:** Límite de API de Spoonacular alcanzado (50 puntos/día)  
**Solución:** ✅ Implementado banco de recetas locales como fallback

### **CORS Error en frontend**
**Causa:** Backend no permite origen del frontend  
**Solución:** ✅ CORS configurado para localhost:5173 y :3000

### **Recetas repetidas**
**Causa:** No se rastreaban IDs de recetas usadas  
**Solución:** ✅ Sistema `exclude_ids` implementado

---

## 📈 Futuras Mejoras Posibles

- [ ] Persistencia de menús en base de datos
- [ ] Autenticación de usuarios
- [ ] Lista de compras automática
- [ ] Información nutricional por plato
- [ ] Recetas favoritas
- [ ] Historial de menús generados
- [ ] Compartir menús por enlace
- [ ] Modo oscuro
- [ ] Exportar a formato Excel
- [ ] Integración con calendario

---

## 👥 Uso

### **Planificar Manualmente**
1. Escribe directamente en las celdas de cada día
2. Separa comida y cena en filas diferentes
3. Imprime cuando termines

### **Generar con IA**
1. Click en botón "Generar con IA" (⚡)
2. Completa preferencias (opcional)
3. Click en "Generar Menú"
4. Revisa y edita si es necesario
5. Imprime el resultado

---

## 📄 Licencia

Aplicación privada - Cristina & Marisa

---

## 📞 Soporte

Para problemas técnicos, revisar:
- Logs del backend (terminal de uvicorn)
- Consola del navegador (errores frontend)
- Archivo `test_api.py` para verificar conexión API

---

**Última actualización:** 14 de noviembre de 2025

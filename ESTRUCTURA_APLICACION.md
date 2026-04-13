# 📋 Estructura de la Aplicación - Planificador de Menús

## 🎯 Descripción General

Aplicación web para planificar menús semanales con dos tablas independientes (Cristina y Marisa) que incluye generación automática de menús mediante inteligencia artificial.

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React)                            │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Planificador │  │   Listado    │  │   Selector   │          │
│  │   (Tablas)   │  │  de Platos   │  │   de Menú    │          │
│  │  Cristina +  │  │  (RecipeList)│  │(MenuSelector)│          │
│  │   Marisa     │  │              │  │  Desplegables│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↕                 ↕                  ↕                    │
│    Navegación        Navegación        Navegación               │
│         ↓                                     ↓                   │
│    Generar IA                  HTTP Request (POST /generar-menu) │
└───────────────────────────────────────┬──────────────────────────┘
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
│   ├── 📄 App.tsx               # Componente principal con planificador
│   ├── 📄 RecipeList.tsx        # Componente de listado de platos
│   ├── 📄 MenuSelector.tsx      # Componente selector de menú con opciones
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

#### `App.tsx` - Planificador de Menús
**Responsabilidades:**
- Gestionar estado de dos menús independientes (`weeklyPlanCristina` y `weeklyPlanMarisa`)
- Renderizar dos tablas con días horizontales y comidas verticales
- Interfaz de generación con IA (modal)
- Funcionalidad de impresión/exportación a PDF
- Navegación entre vistas (Planificador ↔ Listado de Platos)

**Estados principales:**
```typescript
const [currentView, setCurrentView] = useState<'planner' | 'recipes'>('planner')
const [weeklyPlanCristina, setWeeklyPlanCristina] = useState<WeeklyPlan>({...})
const [weeklyPlanMarisa, setWeeklyPlanMarisa] = useState<WeeklyPlan>({...})
const [showAIModal, setShowAIModal] = useState(false)
```

**Funciones clave:**
- `generateMenuWithAI()` - Llama al backend para generar menús
- `handleMealChangeCristina()` - Actualiza comidas de Cristina
- `handleMealChangeMarisa()` - Actualiza comidas de Marisa
- `handlePrint()` - Genera PDF con ambas tablas

#### `RecipeList.tsx` - Gestión de Recetas
**Responsabilidades:**
- Mostrar listado completo de platos disponibles
- Sistema de búsqueda por nombre o ingredientes
- Filtros por categoría (Comida/Cena) y tipo de cocina
- Añadir nuevas recetas al catálogo
- Eliminar recetas existentes
- Navegación de regreso al planificador

**Estados principales:**
```typescript
const [recipes, setRecipes] = useState<Recipe[]>([...])
const [newRecipe, setNewRecipe] = useState<Omit<Recipe, 'id'>>({...})
const [showAddForm, setShowAddForm] = useState(false)
const [searchTerm, setSearchTerm] = useState('')
const [filterCategory, setFilterCategory] = useState('Todas')
const [filterCuisine, setFilterCuisine] = useState('Todas')
```

**Tipos de Datos:**
```typescript
type Recipe = {
  id: number;
  name: string;
  category: string;
  cuisine: string;
  ingredients?: string;
}
```

**Funciones clave:**
- `handleAddRecipe()` - Añade nueva receta al listado
- `handleDeleteRecipe(id)` - Elimina receta por ID
- `filteredRecipes` - Aplica búsqueda y filtros
- `onBack()` - Regresa a la vista del planificador

#### `MenuSelector.tsx` - Selector de Menú con Opciones
**Responsabilidades:**
- Mostrar categorías de menú con opciones desplegables
- Permitir selección de opciones para cada categoría
- Añadir nuevas categorías personalizadas
- Eliminar categorías existentes
- Generar PDF con menú seleccionado
- Resetear todas las selecciones

**Estados principales:**
```typescript
const [menuSections, setMenuSections] = useState<MenuOption[]>([...])
const [newSection, setNewSection] = useState({ name: '', options: '' })
const [showAddForm, setShowAddForm] = useState(false)
```

**Tipos de Datos:**
```typescript
type MenuOption = {
  id: number;
  name: string;            // Nombre de la categoría (Ej: "Entrante")
  options: string[];       // Array de opciones disponibles
  selectedOption: string;  // Opción actualmente seleccionada
}
```

**Categorías Predefinidas:**
- Entrante (7 opciones)
- Primer Plato (7 opciones)
- Segundo Plato (7 opciones)
- Postre (6 opciones)
- Bebida (6 opciones)

**Funciones clave:**
- `handleOptionChange(id, value)` - Actualiza opción seleccionada
- `handleAddSection()` - Añade nueva categoría de menú
- `handleDeleteSection(id)` - Elimina categoría
- `handleReset()` - Resetea todas las selecciones
- `handlePrint()` - Genera PDF con menú completo

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
- ✅ **Navegación entre 3 vistas (Planificador ↔ Listado ↔ Menú)**
- ✅ **Botón "Listado de Platos" para gestionar recetas**
- ✅ **Botón "Elige Menú" para selector de opciones**

### **Listado de Platos - Características**
- 🔍 **Búsqueda avanzada** por nombre o ingredientes
- 🏷️ **Filtros dinámicos** por categoría y tipo de cocina
- ➕ **Añadir recetas** con formulario completo
- 🗑️ **Eliminar recetas** individualmente
- 📋 **Vista en tarjetas** con información detallada
- 🎨 **Etiquetas de color** para categorías y cocinas
- ⬅️ **Botón de retorno** al planificador

### **Selector de Menú - Características**
- 🍽️ **Opciones desplegables** por categoría
- ✅ **5 categorías predefinidas** (Entrante, Primer Plato, Segundo, Postre, Bebida)
- ➕ **Añadir categorías personalizadas** con múltiples opciones
- 🗑️ **Eliminar categorías** existentes
- 🔄 **Resetear selección** completa
- 📄 **Generar PDF** con menú seleccionado
- 📅 **Fecha automática** en el documento
- 📊 **Resumen impreso** de selecciones
- ⬅️ **Navegación** de regreso al planificador

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

## 🔄 Flujos de Datos Completos

### **1. Navegación entre Vistas**

```
1. Usuario en vista Planificador
   ↓
2. Click en botón "Listado de Platos" (verde)
   ↓
3. Estado currentView cambia de 'planner' a 'recipes'
   ↓
4. Se renderiza componente RecipeList
   ↓
5. Usuario puede:
   - Buscar recetas
   - Filtrar por categoría/cocina
   - Añadir nuevas recetas
   - Eliminar recetas
   ↓
6. Click en "Volver al Planificador"
   ↓
7. Estado currentView vuelve a 'planner'
   ↓
8. Se renderiza componente App con tablas
```

### **2. Gestión de Recetas**

```
BÚSQUEDA:
1. Usuario escribe en campo de búsqueda
   ↓
2. Estado searchTerm se actualiza
   ↓
3. filteredRecipes filtra por nombre e ingredientes
   ↓
4. Lista se actualiza en tiempo real

FILTRADO:
1. Usuario selecciona categoría o cocina
   ↓
2. Estados filterCategory/filterCuisine se actualizan
   ↓
3. filteredRecipes aplica múltiples filtros
   ↓
4. Solo se muestran recetas que coinciden

AÑADIR RECETA:
1. Click en "Añadir Nuevo Plato"
   ↓
2. Formulario se despliega (showAddForm = true)
   ↓
3. Usuario completa campos
   ↓
4. Click en "Guardar Plato"
   ↓
5. handleAddRecipe() crea nuevo objeto Recipe
   ↓
6. ID generado con Date.now()
   ↓
7. Receta agregada a array recipes
   ↓
8. Formulario se cierra y resetea

ELIMINAR RECETA:
1. Click en icono de papelera
   ↓
2. handleDeleteRecipe(id) se ejecuta
   ↓
3. recipes.filter() excluye la receta con ese ID
   ↓
4. Lista se actualiza inmediatamente
```

### **3. Generación de Menú con IA**

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

#### Frontend - Planificador
- [x] Dos tablas independientes (Cristina y Marisa)
- [x] Layout horizontal (días en columnas)
- [x] Edición manual de comidas
- [x] Botón "Generar con IA"
- [x] Modal con preferencias personalizables
- [x] Exportación a PDF
- [x] Impresión optimizada (landscape)
- [x] Diseño responsive
- [x] Estado independiente por tabla

#### Frontend - Listado de Platos
- [x] **Vista completa de recetas disponibles**
- [x] **Sistema de búsqueda por nombre/ingredientes**
- [x] **Filtros dinámicos por categoría**
- [x] **Filtros dinámicos por tipo de cocina**
- [x] **Formulario para añadir recetas**
- [x] **Función de eliminar recetas**
- [x] **Navegación entre vistas (botones)**
- [x] **Diseño con tarjetas informativas**
- [x] **Etiquetas de color por categoría/cocina**
- [x] **5 recetas precargadas de ejemplo**
- [x] **Contador de recetas filtradas**

#### Frontend - Selector de Menú 🆕
- [x] **Opciones desplegables por categoría**
- [x] **5 categorías predefinidas con opciones**
- [x] **Añadir categorías personalizadas**
- [x] **Eliminar categorías existentes**
- [x] **Selección de opciones para cada categoría**
- [x] **Botón "Elige Menú" en página principal**
- [x] **Resetear todas las selecciones**
- [x] **Generar PDF con menú completo**
- [x] **Fecha automática en documento**
- [x] **Resumen impreso de selecciones**
- [x] **Navegación de regreso al planificador**
- [x] **Diseño responsive con gradiente naranja/amarillo**

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

### Planificador
- [ ] Persistencia de menús en base de datos
- [ ] Autenticación de usuarios
- [ ] Lista de compras automática
- [ ] Información nutricional por plato
- [ ] Historial de menús generados
- [ ] Compartir menús por enlace
- [ ] Modo oscuro
- [ ] Exportar a formato Excel
- [ ] Integración con calendario

### Listado de Platos
- [ ] **Guardar recetas en localStorage**
- [ ] **Conectar con backend para persistencia**
- [ ] **Importar/Exportar recetas en JSON**
- [ ] **Imágenes para cada receta**
- [ ] **Tiempo de preparación**
- [ ] **Nivel de dificultad**
- [ ] **Recetas favoritas (marcadores)**
- [ ] **Paginación para listados largos**
- [ ] **Ordenar por nombre/categoría/cocina**
- [ ] **Arrastrar recetas al planificador**

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

### **Gestionar Listado de Platos**
1. **Acceder:** Click en botón verde "Listado de Platos"
2. **Buscar:** Escribe en el campo de búsqueda
3. **Filtrar:** Usa selectores de categoría y cocina
4. **Añadir receta:**
   - Click en "Añadir Nuevo Plato"
   - Completa el formulario
   - Click en "Guardar Plato"
5. **Eliminar receta:** Click en icono de papelera 🗑️
6. **Volver:** Click en "Volver al Planificador"

### **Selector de Menú con Opciones** 🆕
1. **Acceder:** Click en botón naranja "Elige Menú"
2. **Seleccionar opciones:**
   - Usa los desplegables para cada categoría
   - Elige una opción de cada lista
3. **Añadir categoría personalizada:**
   - Click en "Añadir Categoría"
   - Escribe el nombre (Ej: "Guarnición")
   - Escribe las opciones separadas por comas
   - Click en "Guardar Categoría"
4. **Eliminar categoría:** Click en icono de papelera 🗑️
5. **Resetear:** Click en "Resetear Selección" para limpiar todo
6. **Generar PDF:** Click en "Descargar PDF" para obtener el menú
7. **Volver:** Click en "Volver al Planificador"

---

## � Detalles Técnicos Adicionales

### **RecipeList.tsx - Gestión de Estado**

**Estructura de Receta:**
```typescript
type Recipe = {
  id: number;           // ID único generado con Date.now()
  name: string;         // Nombre del plato
  category: string;     // "Comida" o "Cena"
  cuisine: string;      // Tipo de cocina
  ingredients?: string; // Ingredientes principales (opcional)
}
```

**Recetas Precargadas:**
```typescript
[
  { id: 1, name: 'Ensalada Griega con Queso Feta', category: 'Comida', cuisine: 'Mediterránea' },
  { id: 2, name: 'Pasta con Tomate y Albahaca', category: 'Comida', cuisine: 'Italiana' },
  { id: 3, name: 'Sopa de Verduras', category: 'Cena', cuisine: 'Mediterránea' },
  { id: 4, name: 'Paella Valenciana', category: 'Comida', cuisine: 'Española' },
  { id: 5, name: 'Tacos de Pollo', category: 'Comida', cuisine: 'Mexicana' }
]
```

**Algoritmo de Filtrado:**
```typescript
const filteredRecipes = recipes.filter((recipe) => {
  const matchesSearch = 
    recipe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    recipe.ingredients?.toLowerCase().includes(searchTerm.toLowerCase());
  const matchesCategory = filterCategory === 'Todas' || recipe.category === filterCategory;
  const matchesCuisine = filterCuisine === 'Todas' || recipe.cuisine === filterCuisine;
  return matchesSearch && matchesCategory && matchesCuisine;
});
```

**Tipos de Cocina Disponibles:**
- Mediterránea
- Italiana
- Asiática
- Mexicana
- Española

---

## �📄 Licencia

Aplicación privada - Cristina & Marisa

---

## 📞 Soporte

Para problemas técnicos, revisar:
- Logs del backend (terminal de uvicorn)
- Consola del navegador (errores frontend)
- Archivo `test_api.py` para verificar conexión API

---

**Última actualización:** 21 de noviembre de 2025

**Cambios recientes:**
- 🍽️ Añadido componente MenuSelector.tsx para elegir menú con opciones
- � Sistema de categorías desplegables (Entrante, Primer Plato, Segundo, Postre, Bebida)
- ➕ Funcionalidad de añadir/eliminar categorías personalizadas
- 📄 Generación de PDF con menú seleccionado
- 🔄 Botón de reseteo para limpiar selecciones
- 🎨 Interfaz con gradiente naranja/amarillo
- ✨ Añadido componente RecipeList.tsx para gestión de recetas (18/11/2025)
- 🔄 Implementado sistema de navegación entre vistas (18/11/2025)

Página Principal (Planificador)
    ├── Botón Naranja "Elige Menú" → MenuSelector
    ├── Botón Verde "Listado de Platos" → RecipeList  
    ├── Botón Morado "Generar con IA" → Modal IA
    └── Botón Azul "Imprimir PDF" → Exportar

MenuSelector
    ├── Header con título y botón "Volver"
    ├── Botones de acción:
    │   ├── "Añadir Categoría" (Verde)
    │   ├── "Resetear Selección" (Gris)
    │   └── "Descargar PDF" (Azul)
    ├── Formulario añadir categoría (desplegable)
    └── Lista de categorías con selectores
        └── Cada categoría puede eliminarse

    1. Nuevo Componente: MenuSelector.tsx
Características principales:

✅ 5 categorías predefinidas:

🥗 Entrante (7 opciones)
🍝 Primer Plato (7 opciones)
🍖 Segundo Plato (7 opciones)
🍰 Postre (6 opciones)
🥤 Bebida (6 opciones)
✅ Funcionalidades interactivas:

Selectores desplegables para cada categoría
Añadir categorías personalizadas
Eliminar categorías
Resetear todas las selecciones
Generar PDF con menú completo
✅ PDF optimizado:

Incluye fecha automática
Muestra solo opciones seleccionadas
Resumen completo al final
Formato profesional para impresión
2. Navegación Actualizada en App.tsx
✅ Botón naranja "Elige Menú" (con icono 🍽️)
✅ Estado de navegación expandido: 'planner' | 'recipes' | 'menu'
✅ Navegación fluida entre las 3 vistas
3. Documentación Actualizada
✅ ESTRUCTURA_APLICACION.md completamente actualizado
✅ Diagrama de arquitectura con las 3 vistas
✅ Instrucciones de uso detalladas
✅ Características técnicas documentadas
✅ Backend Iniciado Correctamente
Estado: ✅ Ejecutándose
URL: http://localhost:8000
Puerto: 8000
Modo: Desarrollo con recarga automática
📋 Endpoints Disponibles
La API del generador de menús está funcionando con los siguientes endpoints:

POST /generar-menu - Genera un menú semanal completo
POST /sugerir-comida - Sugiere un plato específico
POST /generar-menu-casa - Genera PDF del menú de casa
GET /health - Verifica el estado del servidor
🔧 Configuración
Entorno: Entorno virtual Python activado
Framework: FastAPI con uvicorn
CORS: Configurado para frontend en puertos 5173, 5175, 3000
Recarga: Activada para desarrollo
El servidor está listo para recibir peticiones del frontend. Puedes verificar que funciona accediendo a http://localhost:8000 en tu navegador.

Claude Sonnet 4 • 1x


Reviewed App.tsx and checked package.json
Voy a revisar tu aplicación Vite y el archivo de configuración para ver en qué puerto puedes iniciarla:

Reviewed 3 files
¡Perfecto! Veo que tienes una aplicación Vite + React + TypeScript con un planificador de menús. Te explico cómo iniciarla:

🚀 Cómo Iniciar tu Aplicación Vite Frontend:
1. Puerto por Defecto de Vite:
Puerto: 5173 (puerto por defecto de Vite)

2. Comandos para Iniciar:
Ejecutado Get-Location
Ejecutar en Terminal
Ejecutado Set-Location ..
Ejecutar en Terminal
Ejecutado npm run dev
Started Vite application successfully on port 5173
🎉 ¡APLICACIÓN VITE INICIADA EXITOSAMENTE!
✅ Ahora Tienes 2 Aplicaciones Funcionando:
🎯 Frontend Vite + React:
🌐 URL: http://localhost:5173/
⚡ Framework: Vite + React + TypeScript
🍽️ App: Planificador de Menús (tu interfaz original)
✨ Features: Tabla de menús semanales, impresión, etc.
🏥 Backend FastAPI:
🌐 URL: http://localhost:8001/
🔧 Framework: FastAPI + Python
📄 Features: Generador de PDFs de dietas médicas
🚀 Cómo Usar Ambas Aplicaciones:
📱 Para UI del Planificador de Menús:
Abre: http://localhost:5173/

Interfaz React con tabla de menús semanales
Funciones de impresión
Diseño con Tailwind CSS
🏥 Para Dietas Médicas:
Abre: http://localhost:8001/

Interfaz web para descargar PDFs médicos
4 modelos de dieta de OSAKIDETZA
API REST para integración
💡 Integración Recomendada:
Puedes integrar ambas aplicaciones agregando en tu React (puerto 5173) botones que llamen a la API del backend (puerto 8001) para generar PDFs médicos.

📋 Estado Actual:
✅ Frontend Vite: Funcionando en puerto 5173
✅ Backend FastAPI: Funcionando en puerto 8001
✅ PDFs médicos: Listos para descargar
✅ Interfaz planificador: Lista para usar


✅ ¿Qué He Agregado?
🔧 Funcionalidades Nuevas:
✅ Nuevo botón "Dietas Médicas" en la barra superior
✅ Modal completo con interfaz profesional para dietas
✅ Descargas directas de todos los PDFs médicos
✅ Estados de carga con spinners durante descargas
✅ Manejo de errores con mensajes informativos
✅ Viewer de información JSON en ventana separada

📱 Nueva Interfaz Incluye:
🏥 PDF Completo → Todos los 4 modelos en un archivo
📊 Tabla Resumen → Vista comparativa de modelos
🔢 Modelos Individuales → Botones 1, 2, 3, 4 por separado
ℹ️ Ver información detallada → JSON con todos los datos
🌐 Integración de APIs:
Frontend React (puerto 5173) → Tu aplicación principal
Backend FastAPI (puerto 8001) → Generador de PDFs médicos
Comunicación perfecta entre ambos sistemas
🚀 ¿Cómo Usar Ahora?
1. Abre tu aplicación React:
http://localhost:5173/

2. Verás el nuevo botón "Dietas Médicas" (color teal)
3. Al hacer click se abre un modal con:
Descripción de OSAKIDETZA
Botones grandes para PDF completo y resumen
Grid con botones para modelos individuales
Información detallada en JSON
4. ¡Los PDFs se descargan automáticamente!
📋 Estado Actual del Sistema:
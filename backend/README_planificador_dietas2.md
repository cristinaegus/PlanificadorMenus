# Planificador Semanal de Dietas 2

Este sistema genera menús semanales automáticamente basados en las opciones definidas en el archivo `dietas_2.json`.

## Archivos incluidos

### 📊 Datos
- **`dietas_2.json`**: Contiene todas las opciones de menús organizadas por categorías:
  - 4 opciones de desayuno
  - 4 opciones de snacks/merienda  
  - 9 opciones de comidas
  - 6 opciones de cenas
  - Requisitos diarios (60gr pan, 1.5L agua)

### 🐍 Scripts Python

#### `planificador_semanal_simple.py` (Recomendado)
- **Sin dependencias externas** (solo Python estándar)
- Genera menús aleatorios o secuenciales
- Exporta en formatos: TXT y CSV
- Interfaz de consola amigable

#### `planificador_semanal_dietas2.py` (Avanzado)
- Utiliza pandas y openpyxl para funcionalidades avanzadas
- Exporta en formato Excel con formato mejorado
- Requiere instalación de dependencias adicionales

#### `test_planificador.py`
- Script de pruebas para verificar funcionamiento
- Valida la carga de datos y generación de menús

## 🚀 Instalación y Uso

### Instalación de dependencias (solo para versión avanzada)
```bash
pip install pandas openpyxl
```

### Uso básico
```bash
# Ejecutar planificador simple (sin dependencias)
python planificador_semanal_simple.py

# Ejecutar pruebas
python test_planificador.py

# Ejecutar planificador avanzado (requiere pandas)
python planificador_semanal_dietas2.py
```

## 📋 Características

### Tipos de menú
- **Aleatorio**: Selecciona opciones al azar cada día
- **Secuencial**: Rota las opciones sistemáticamente

### Formatos de salida
- **Consola**: Visualización formatada con emojis
- **TXT**: Archivo de texto plano
- **CSV**: Compatible con Excel/Google Sheets
- **Excel**: Formato avanzado con columnas ajustadas (solo versión avanzada)

### Estructura del menú semanal
Cada día incluye:
- 🌅 **Desayuno**: Opciones variadas con lácteos, cereales y fruta
- 🥪 **Snack/Merienda**: Opciones ligeras
- 🍽️ **Comida**: Plato principal + complementos fijos (pan, fruta, aceite)
- 🌙 **Cena**: Opciones de cena + complementos fijos

### Requisitos diarios automáticos
- 60gr de pan total al día
- 1.5 litros de agua al día

## 📁 Archivos generados

Los archivos se guardan con formato de fecha y hora:
- `menu_semanal_dietas2_YYYYMMDD_HHMM.txt`
- `menu_semanal_dietas2_YYYYMMDD_HHMM.csv`
- `menu_semanal_dietas2_YYYYMMDD_HHMM.xlsx` (solo versión avanzada)

## 🔧 Personalización

Para modificar las opciones de menú, edita el archivo `dietas_2.json` siguiendo la estructura existente:

```json
{
  "dietas_2": {
    "desayunos": {
      "opciones": [...] 
    },
    "snacks_media_manana_merienda": {
      "opciones": [...]
    },
    "comidas": {
      "opciones": [...],
      "complementos_fijos": [...]
    },
    "cenas": {
      "opciones": [...],
      "complementos_fijos": [...]
    }
  }
}
```

## 💡 Ejemplo de uso en código

```python
from planificador_semanal_simple import PlanificadorSemanalSimple

# Crear planificador
planificador = PlanificadorSemanalSimple('dietas_2.json')

# Generar menú aleatorio
menu = planificador.generar_menu_semanal(modo='aleatorio')

# Mostrar en consola
planificador.imprimir_menu_semanal(menu)

# Guardar archivos
planificador.guardar_menu_txt(menu)
planificador.generar_menu_csv(menu)
```

## ✅ Validación

El sistema incluye validaciones automáticas:
- Verificación de existencia del archivo JSON
- Validación de estructura de datos
- Manejo de errores en la carga de archivos
- Pruebas unitarias incluidas

---

**Nota**: Este planificador está diseñado para ser flexible y fácil de usar, permitiendo la generación rápida de menús variados para toda la semana mientras respeta los requisitos nutricionales establecidos.
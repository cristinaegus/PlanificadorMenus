# 🔄 Cambio de API: OpenAI → Spoonacular

Se ha actualizado el backend para usar **Spoonacular API** en lugar de OpenAI para generar menús más realistas con recetas existentes.

---

## 📋 Cambios realizados en los archivos:

### 1. **`backend/ai_menu.py`**
- ✅ Reemplazado OpenAI GPT por Spoonacular API
- ✅ Usa endpoint `/recipes/complexSearch` para buscar recetas reales
- ✅ Soporta filtros por tipo de cocina (mediterránea, asiática, italiana, etc.)
- ✅ Soporta restricciones dietéticas (vegetariana, vegana, sin gluten)
- ✅ Busca recetas específicas para comida y cena

### 2. **`backend/requirements.txt`**
```diff
- openai==1.3.5
+ requests==2.31.0
```

### 3. **`backend/.env.example`**
```diff
- OPENAI_API_KEY=tu_api_key_aqui
+ SPOONACULAR_API_KEY=tu_api_key_aqui
```

---

## 🚀 Pasos para configurar Spoonacular:

### 1. Obtener API Key de Spoonacular (GRATIS)

1. Visita: https://spoonacular.com/food-api/console#Dashboard
2. Crea una cuenta o inicia sesión
3. Ve al Dashboard y copia tu **API Key**

**Plan gratuito incluye:**
- ✅ 150 requests por día
- ✅ Acceso a 365,000+ recetas
- ✅ Búsqueda por ingredientes, dietas y cocinas

### 2. Actualizar el archivo `.env`

Edita `backend/.env` y reemplaza con tu API Key:

```env
SPOONACULAR_API_KEY=tu_api_key_de_spoonacular_aqui
```

### 3. Reinstalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 4. Reiniciar el servidor

```bash
python app.py
```

O con uvicorn:

```bash
uvicorn app:app --reload
```

---

## ✨ Ventajas de usar Spoonacular:

| Característica | Spoonacular | OpenAI |
|---------------|-------------|---------|
| **Costo** | 150 req/día gratis | Pago por uso |
| **Recetas** | Reales y existentes | Generadas (pueden no existir) |
| **Base de datos** | 365,000+ recetas | N/A |
| **Filtros avanzados** | ✅ Sí | ⚠️ Limitado |
| **Información nutricional** | ✅ Disponible | ❌ No |

---

## 🧪 Probar la API

Una vez configurado, prueba el endpoint:

```bash
curl -X POST http://localhost:8000/generar-menu \
  -H "Content-Type: application/json" \
  -d '{
    "preferencias": "pescado y verduras",
    "restricciones": "sin gluten",
    "tipo_cocina": "mediterránea"
  }'
```

---

## ⚠️ Notas importantes:

- El archivo `.env` está protegido en `.gitignore` (no se subirá a Git)
- Con el plan gratuito tienes 150 requests/día (suficiente para uso personal)
- Si necesitas más requests, Spoonacular ofrece planes de pago
- Las recetas devueltas son recetas reales con nombres específicos

---

## 🔗 Recursos útiles:

- **Dashboard de Spoonacular**: https://spoonacular.com/food-api/console#Dashboard
- **Documentación API**: https://spoonacular.com/food-api/docs
- **Ejemplos de endpoints**: https://spoonacular.com/food-api/docs#Search-Recipes-Complex

---

## 🐛 Solución de problemas:

### Error: "Invalid API Key"
- Verifica que tu API Key esté correctamente copiada en `.env`
- Asegúrate de que el archivo se llame exactamente `.env` (sin extensión adicional)

### Error: "Module 'requests' not found"
```bash
pip install requests
```

### Límite de requests alcanzado
- El plan gratuito se resetea cada 24 horas
- Considera upgrade si necesitas más requests

---

¡Tu aplicación ahora genera menús con recetas reales de Spoonacular! 🎉

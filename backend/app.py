from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import ai_menu

app = FastAPI(title="Menu Generator API", version="1.0.0")

# Configurar CORS para permitir peticiones desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite y otros puertos comunes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class MenuRequest(BaseModel):
    preferencias: Optional[str] = ""
    restricciones: Optional[str] = ""
    tipo_cocina: Optional[str] = "mediterránea"

class SugerenciaRequest(BaseModel):
    dia: str
    tipo_comida: str = "comida"  # 'comida' o 'cena'
    estilo: Optional[str] = "mediterráneo"

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "message": "Menu Generator API - Backend activo",
        "version": "1.0.0",
        "endpoints": {
            "/generar-menu": "POST - Genera un menú semanal completo",
            "/sugerir-comida": "POST - Sugiere un plato específico",
            "/health": "GET - Verifica el estado del servidor"
        }
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {"status": "ok", "message": "Servidor funcionando correctamente"}

@app.post("/generar-menu")
def generar_menu(request: MenuRequest):
    """
    Genera un menú semanal completo usando IA
    
    Body:
    {
        "preferencias": "Me gusta el pescado y las verduras",
        "restricciones": "Sin gluten",
        "tipo_cocina": "mediterránea"
    }
    """
    try:
        menu = ai_menu.generar_menu_semanal(
            preferencias=request.preferencias,
            restricciones=request.restricciones,
            tipo_cocina=request.tipo_cocina
        )
        
        if menu is None:
            raise HTTPException(status_code=500, detail="Error al generar el menú con IA")
        
        return {
            "success": True,
            "menu": menu,
            "parametros": {
                "preferencias": request.preferencias,
                "restricciones": request.restricciones,
                "tipo_cocina": request.tipo_cocina
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar menú: {str(e)}")

@app.post("/sugerir-comida")
def sugerir_comida(request: SugerenciaRequest):
    """
    Genera una sugerencia para una comida específica
    
    Body:
    {
        "dia": "Lunes",
        "tipo_comida": "comida",
        "estilo": "mediterráneo"
    }
    """
    try:
        sugerencia = ai_menu.generar_sugerencia_comida(
            dia=request.dia,
            tipo_comida=request.tipo_comida,
            estilo=request.estilo
        )
        
        if sugerencia is None:
            raise HTTPException(status_code=500, detail="Error al generar sugerencia con IA")
        
        return {
            "success": True,
            "sugerencia": sugerencia,
            "dia": request.dia,
            "tipo_comida": request.tipo_comida
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar sugerencia: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

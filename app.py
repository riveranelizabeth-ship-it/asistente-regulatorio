from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(
    title="Asistente de Evaluación Regulatoria",
    description="Clasificación de riesgos regulatorios en proyectos bancarios",
    version="2.0"
)

class Proyecto(BaseModel):
    descripcion: str

@app.get("/")
def inicio():
    return {
        "mensaje": "Asistente de Evaluación Regulatoria activo"
    }

@app.post("/evaluar")
def evaluar_proyecto(proyecto: Proyecto):
    try:
        modelo = joblib.load("modelo_regulatorio.pkl")
        prediccion = modelo.predict([proyecto.descripcion])

        return {
            "proyecto": proyecto.descripcion,
            "riesgo_identificado": str(prediccion[0])
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

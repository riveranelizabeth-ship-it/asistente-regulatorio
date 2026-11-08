
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

descripciones = [
    "Contratación digital de crédito con firma electrónica y biometría",
    "Tratamiento de datos personales sensibles de clientes",
    "Modelo de inteligencia artificial para aprobar créditos",
    "Transferencias bancarias mediante aplicación móvil",
    "Actualización de información pública en el portal bancario",
    "Mejora de diseño visual de una página informativa",
    "Cambio de colores en la aplicación bancaria",
    "Actualización de contenido educativo financiero",
    "Implementación de autenticación biométrica",
    "Automatización de decisiones crediticias"
]

riesgos = [
    "Alto", "Alto", "Alto", "Medio",
    "Bajo", "Bajo", "Bajo", "Bajo",
    "Alto", "Alto"
]

modelo = Pipeline([
    ("vectorizador", TfidfVectorizer()),
    ("clasificador", LogisticRegression(max_iter=1000))
])

modelo.fit(descripciones, riesgos)

joblib.dump(modelo, "modelo_regulatorio.pkl")

print("Modelo guardado correctamente")


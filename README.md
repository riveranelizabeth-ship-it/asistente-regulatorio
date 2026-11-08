# Asistente de Evaluación Regulatoria

**Proyecto académico — Fase II: Ejecución**  
**Gestión de Proyectos de Inteligencia Artificial**

## 1. Descripción y alcance

Prototipo de apoyo para una **evaluación preliminar de la complejidad jurídico-regulatoria** de iniciativas de banca digital en México. A partir de la descripción textual de un proyecto, el modelo genera una categoría de clasificación. Su propósito es apoyar la identificación inicial de asuntos que podrían requerir un análisis jurídico más profundo; **no sustituye la valoración de un especialista ni determina el cumplimiento normativo**.

El nombre del campo de respuesta, `riesgo_identificado`, se conserva por compatibilidad con el código actual; conceptualmente, el proyecto busca aproximar la **complejidad jurídico-regulatoria**, no calcular una probabilidad de incumplimiento.

## 2. Arquitectura y tecnologías

```text
Usuario / Swagger UI
        |
        | Solicitud HTTP con JSON
        v
FastAPI (app.py, puerto 8000)
        |
        | joblib.load + predict
        v
Modelo entrenado (modelo_regulatorio.pkl)
        |
        v
Respuesta JSON: riesgo_identificado

Aplicación y modelo empaquetados en Docker
```

- **Python 3.11** como base del contenedor.
- **FastAPI** para exponer los endpoints y generar la documentación Swagger.
- **scikit-learn** y **joblib** como dependencias del modelo.
- **Docker** para construir y ejecutar el servicio de manera reproducible.
- **pandas** y **uvicorn** como dependencias declaradas en `requirements.txt`.

> El repositorio debe incluir el archivo binario `modelo_regulatorio.pkl`. El código de entrenamiento (`entrenar_modelo.py`), si se incorpora, permite documentar la procedencia del modelo, pero el contenedor necesita el archivo `.pkl` ya generado.

## 3. Estructura del repositorio

```text
asistente-regulatorio/
├── README.md
├── app.py
├── Dockerfile
├── requirements.txt
├── entrenar_modelo.py        # si se incluye el script utilizado
├── modelo_regulatorio.pkl    # necesario para ejecutar el servicio
└── evidencias/
    ├── Evidencia 1 ... 6     # capturas de pruebas; conservar extensiones reales
    ├── 07_imagen_docker.png
    ├── 08_contenedor_ejecucion.png
    └── 09_integracion_api_swagger.png
```

**Nota:** Los nombres de las primeras seis imágenes son orientativos. Antes de publicar, comprobar sus nombres y extensiones reales y actualizar los enlaces correspondientes.

## 4. Requisitos técnicos

Para ejecución local:

1. Equipo con Docker Desktop instalado y en funcionamiento.
2. Acceso a una terminal.
3. Archivos `app.py`, `Dockerfile`, `requirements.txt` y `modelo_regulatorio.pkl` en la raíz del proyecto.
4. Puerto local 8000 disponible.
5. Conexión a Internet durante la construcción para descargar la imagen base y las dependencias.

No es necesario instalar Python localmente si se utiliza la imagen Docker y el modelo ya está entrenado.

## 5. Construcción y ejecución local con Docker

Desde la terminal, entrar en la carpeta del proyecto:

```bash
cd ~/Desktop/asistente-regulatorio
```

Construir la imagen:

```bash
docker build -t asistente-regulatorio .
```

Ejecutar el contenedor:

```bash
docker run --rm -p 8000:8000 asistente-regulatorio
```

Abrir la documentación interactiva:

```text
http://localhost:8000/docs
```

Comprobar el servicio desde otra ventana de terminal:

```bash
curl http://localhost:8000/
```

Resultado esperado:

```json
{"mensaje":"Asistente de Evaluación Regulatoria activo"}
```

La URL `localhost` solo es accesible desde el equipo donde se ejecuta Docker; no es un enlace público para el profesor.

## 6. Integración de la API

### `GET /`

Verifica que la aplicación esté activa. No ejecuta el modelo.

### `POST /evaluar`

Recibe una descripción de proyecto en formato JSON, carga `modelo_regulatorio.pkl`, realiza una predicción y devuelve la categoría.

**Ejemplo de solicitud:**

```json
{
  "descripcion": "Una institución bancaria implementará contratación digital con reconocimiento facial y análisis automatizado de información financiera."
}
```

**Estructura de la respuesta:**

```json
{
  "proyecto": "[descripción enviada]",
  "riesgo_identificado": "[categoría predicha por el modelo]"
}
```

La categoría concreta depende del modelo y del texto enviado. La API también puede responder con error HTTP 500 si falla la carga del modelo o la predicción.

**Ejemplo de prueba desde terminal:**

```bash
curl -X POST http://localhost:8000/evaluar \
  -H 'Content-Type: application/json' \
  -d '{"descripcion":"Una institución bancaria implementará contratación digital con reconocimiento facial y análisis automatizado de información financiera."}'
```

Swagger permite ejecutar esta misma solicitud desde el navegador mediante **Try it out → Execute**.

## 7. Pruebas y validación

### Metodología

Se realizaron pruebas manuales sobre el endpoint `POST /evaluar` mediante Swagger, con descripciones de iniciativas bancarias de diferente complejidad. Se observaron las respuestas y se contrastaron con una **expectativa jurídico-funcional preliminar**. Las expectativas no constituyen etiquetas validadas por un panel de especialistas ni métricas estadísticas de desempeño.

### Matriz de pruebas funcionales

| ID | Escenario evaluado | Clasificación obtenida | Análisis |
|---|---|---|---|
| F1 | Contratación de crédito personal en banca móvil con firma electrónica, biometría, IA y datos financieros | Alto | Coherente con la complejidad esperada para el caso. |
| F2 | Rediseño exclusivamente visual de saldos y movimientos, sin cambios contractuales, de autenticación ni tratamiento de datos | Alto | Posible sobreclasificación; la descripción sugería menor complejidad. |
| F3 | Bloqueo y desbloqueo temporal de tarjeta desde la app, con controles existentes y sin modificar condiciones contractuales | Bajo | Coherente con la expectativa preliminar para el caso descrito. |
| F4 | Notificaciones automáticas de movimientos por móvil o correo en productos existentes | Bajo | Resultado plausible, sujeto a revisión de privacidad, comunicaciones y seguridad. |

### Matriz de pruebas extremas

| ID | Escenario evaluado | Expectativa de referencia | Resultado obtenido | Hallazgo |
|---|---|---|---|---|
| E1 | Descripción genérica de una nueva funcionalidad digital, sin datos suficientes | No concluyente | Bajo | El modelo asigna una categoría sin detectar insuficiencia de información. |
| E2 | Plataforma de crédito con IA, biometría, datos financieros y contratación electrónica sin intervención humana | Alto | Alto | Coincide con la expectativa para un escenario de múltiples factores sensibles. |
| E3 | Mejora visual de la app combinada con intercambio de información de cuentas con terceros autorizados mediante APIs | Alto, como hipótesis de prueba | Bajo | Posible subclasificación de una iniciativa mixta; requiere análisis específico del esquema de datos y terceros. |

### Resultados y limitaciones

- **Integración funcional:** las pruebas permitieron enviar descripciones a la API y recibir categorías del modelo.
- **Aciertos observados:** el prototipo identificó como Alto los escenarios F1 y E2; clasificó como Bajo los escenarios F3 y F4, de forma plausible según sus descripciones.
- **Discrepancias:** F2 y E3 muestran posibles errores de clasificación frente a las expectativas preliminares.
- **Información insuficiente:** E1 muestra que la API no ofrece una respuesta específica para descripciones que no permiten evaluar el caso.
- **Alcance de la evidencia:** estas siete pruebas son exploratorias; no permiten afirmar un porcentaje de precisión, sensibilidad, exactitud ni validación estadística del modelo.
- **Causas no confirmadas:** sin un análisis de características y del conjunto de entrenamiento, no puede atribuirse una clasificación concreta a palabras o factores específicos.

### Recomendaciones para la Fase III

1. Ampliar y revisar el conjunto de entrenamiento con ejemplos representativos de banca digital mexicana.
2. Definir criterios y etiquetas de complejidad con especialistas jurídicos.
3. Incorporar casos mixtos, descripciones insuficientes y escenarios límite.
4. Establecer reglas de abstención o solicitud de información adicional cuando falten datos.
5. Evaluar con un conjunto de prueba separado y métricas adecuadas; mantener revisión humana en decisiones relevantes.

## 8. Evidencias

Las capturas se encuentran en la [carpeta `evidencias/`](evidencias/). Allí se documentan las pruebas manuales y los componentes técnicos de la ejecución local.

| Evidencia | Qué acredita | Archivo |
|---|---|---|
| 1 a 6 | Capturas de pruebas realizadas mediante la API | [Consultar carpeta](evidencias/) |
| 7 | Imagen Docker creada y disponible localmente | [Imagen Docker](evidencias/07_imagen_docker.png) |
| 8 | Contenedor activo con puerto 8000 publicado | [Contenedor en ejecución](evidencias/08_contenedor_ejecucion.png) |
| 9 | Swagger mostrando `GET /` y `POST /evaluar` | [Integración API](evidencias/09_integracion_api_swagger.png) |

> Antes de la entrega, verificar que los nueve archivos estén efectivamente en el repositorio, que los enlaces abran y que las capturas de pruebas se correspondan con las descripciones de la matriz. Las seis capturas no necesariamente representan una prueba distinta cada una; la matriz refleja los siete escenarios reportados durante la ejecución.

## 9. Manual de despliegue en la nube: Google Cloud Run

### 9.1 Estrategia

Se propone desplegar el servicio en **Google Cloud Run**, una plataforma administrada que ejecuta aplicaciones en contenedores. Esta opción permite reutilizar la arquitectura Docker desarrollada y evita administrar directamente una máquina virtual.

**Estado:** procedimiento documentado y **no ejecutado ni validado en la nube** durante esta fase. La ejecución demostrada corresponde al entorno local.

### 9.2 Requisitos y consideraciones previas

- Cuenta de Google Cloud y proyecto con **facturación habilitada**; el uso de servicios puede generar costos.
- Permisos para habilitar APIs y desplegar servicios en Cloud Run y Cloud Build.
- **Google Cloud CLI (`gcloud`)** instalada y autenticada, o acceso a Cloud Shell.
- Código fuente, Dockerfile, dependencias y `modelo_regulatorio.pkl` incluidos en la carpeta del proyecto.
- Selección de región; por ejemplo, `us-central1` como referencia técnica, sujeto a políticas de residencia de datos y requisitos institucionales.
- No utilizar datos reales de clientes ni información bancaria confidencial para esta demostración académica.

### 9.3 Preparar Google Cloud

Iniciar sesión y seleccionar el proyecto (reemplazar el identificador de ejemplo):

```bash
gcloud auth login
gcloud config set project ID_DE_TU_PROYECTO
```

Habilitar los servicios requeridos:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

En un entorno organizacional, el administrador puede necesitar asignar roles adicionales a la identidad de despliegue y a la cuenta de servicio de construcción. Revisar los requisitos vigentes de permisos en la documentación oficial.

### 9.4 Desplegar desde el código fuente

Desde la raíz del repositorio:

```bash
cd ~/Desktop/asistente-regulatorio
```

Ejecutar:

```bash
gcloud run deploy asistente-regulatorio \
  --source . \
  --region us-central1 \
  --port 8000 \
  --memory 1Gi \
  --allow-unauthenticated
```

**Explicación:**

- `--source .` envía el proyecto para su construcción; al existir un Dockerfile, el proceso de construcción puede utilizarlo.
- `--region` establece la región del servicio.
- `--port 8000` es **indispensable para este Dockerfile**, porque Uvicorn escucha en el puerto 8000, no en el puerto 8080 que Cloud Run utiliza de manera predeterminada.
- `--memory 1Gi` establece una asignación inicial de memoria que debe ajustarse según el consumo observado.
- `--allow-unauthenticated` publica el endpoint para una **demostración académica sin datos sensibles**. En un entorno bancario o con información real, **no debe habilitarse acceso público sin controles**; se debe preferir autenticación, autorización, políticas de red y gobierno de datos.

La plataforma puede solicitar confirmaciones para crear recursos de construcción y repositorios de imágenes. El proceso requiere conectividad y permisos adecuados.

### 9.5 Verificar el servicio desplegado

Al terminar correctamente, Cloud Run muestra una URL pública de servicio (variable según el proyecto). Consultar la URL desde consola o mediante:

```bash
gcloud run services describe asistente-regulatorio \
  --region us-central1 \
  --format='value(status.url)'
```

Con la URL **real** obtenida, verificar:

```text
https://URL-REAL-DEL-SERVICIO/
https://URL-REAL-DEL-SERVICIO/docs
```

También es posible enviar un POST a `https://URL-REAL-DEL-SERVICIO/evaluar` con el mismo JSON utilizado localmente. No sustituir esta URL por `localhost` para una demostración remota.

### 9.6 Validación posterior y solución de problemas

- **Error de arranque:** verificar que el servicio escucha en `0.0.0.0:8000` y que Cloud Run tiene configurado `--port 8000`.
- **Error 500 al evaluar:** confirmar que `modelo_regulatorio.pkl` existe y se incluyó en la imagen; consultar registros del servicio.
- **Error de construcción:** comprobar dependencias, permisos de Cloud Build y facturación.
- **Consumo de memoria:** revisar registros y métricas y ajustar la memoria o las dependencias.
- **Acceso no autorizado:** revisar la configuración de autenticación e IAM; no exponer datos sensibles para resolver un problema de acceso.

Comando orientativo para consultar registros:

```bash
gcloud run services logs read asistente-regulatorio --region us-central1 --limit 50
```

### 9.7 Seguridad y costos

Para un despliegue productivo se requerirían, entre otros controles, autenticación, autorización, gestión de identidades, registro de accesos, monitoreo, protección de datos, revisión de dependencias y gobierno del modelo. El procedimiento anterior describe un **entorno académico de demostración**, no una arquitectura lista para producción bancaria. Conviene revisar cuotas, facturación y eliminar recursos de prueba cuando ya no se necesiten.

### 9.8 Documentación oficial de referencia

- [Google Cloud Run: desplegar desde código fuente](https://cloud.google.com/run/docs/deploying-source-code)
- [Google Cloud Run: configurar el puerto del contenedor](https://cloud.google.com/run/docs/configuring/services/containers)
- [Google Cloud Run: autenticación de usuarios y servicios](https://cloud.google.com/run/docs/authenticating/overview)
- [Google Cloud SDK: instalación](https://cloud.google.com/sdk/docs/install)

## 10. Conclusiones

La Fase II permitió construir y ejecutar localmente un contenedor Docker, exponer una API con FastAPI y efectuar pruebas manuales con diferentes escenarios bancarios. La integración técnica funcionó en las pruebas realizadas. Al mismo tiempo, las discrepancias identificadas muestran que **un servicio técnicamente operativo no implica un modelo suficientemente validado para decisiones jurídicas**. La siguiente fase deberá priorizar la calidad de datos, la definición de criterios de clasificación, la evaluación cuantitativa y la supervisión humana.

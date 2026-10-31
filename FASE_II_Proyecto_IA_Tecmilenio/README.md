# FASE II - Asistente de IA para atención financiera

Prototipo **académico** derivado del business case de FASE I. Implementa frontend y backend conectados por API. **No incorpora todavía un LLM ni RAG real**: usa respuestas FAQ deterministas, con fuentes de demostración y escalamiento humano.

## Requisitos
Python 3.11+, Docker Engine/Desktop (para contenedor), Git. No se usan datos reales.

## Ejecutar con Python
```bash
python -m venv .venv
# Activar entorno virtual según sistema operativo
pip install -r requirements-dev.txt
uvicorn app.main:app --host 127.0.0.1 --port 8080
```
Abrir http://localhost:8080, documentación de API en http://localhost:8080/docs.

## Docker
```bash
docker build -t asistente-financiero-fase2:1.0 .
docker run --rm -p 8080:8080 asistente-financiero-fase2:1.0
# Alternativa: docker compose up --build
```
Verificar `curl http://localhost:8080/health`.

## API
- `GET /`: interfaz web.
- `GET /health`: estado de servicio.
- `POST /api/chat`: JSON `{ "question": "¿Cómo consulto mi estado de cuenta?" }`.

## Pruebas
`python -m pytest -q` desde la raíz.

## Publicación GitHub
```bash
git init
git add .
git commit -m "FASE II: prototipo API y Docker"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```
Crear previamente repositorio vacío en GitHub; reemplazar los valores de ejemplo. No subir secretos ni información personal.

## Alcance y límites
El business case de FASE I proyecta 240,000 tickets/año, 32% de automatización y ROI de 176.3%; son **supuestos**, no resultados de este prototipo. No usar para decisiones crediticias ni operaciones sensibles.

FROM python:3.12-slim AS build

RUN pip install --no-cache-dir sphinx==9.1.1 sphinx_rtd_theme==3.1.0

COPY docs /docs

RUN sphinx-build docs/source /build/

FROM nginx:latest AS prod
COPY --from=build /build/ /usr/share/nginx/html/

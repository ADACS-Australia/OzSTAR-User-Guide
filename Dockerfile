FROM python:3.12-slim AS build

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY docs /docs

RUN sphinx-build -b html -W --keep-going /docs/source /build/

FROM nginx:latest AS prod

COPY --from=build /build/ /usr/share/nginx/html/
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

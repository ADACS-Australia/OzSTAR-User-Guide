FROM debian:bookworm-slim as build

RUN apt update && apt install -y python3-venv
RUN bash -c "python3 -m venv venv && source venv/bin/activate && pip install sphinx sphinx_rtd_theme"

COPY docs /docs

RUN bash -c "source venv/bin/activate && sphinx-build docs/source /build/"

FROM nginx:latest as prod
COPY --from=build /build/ /usr/share/nginx/html/

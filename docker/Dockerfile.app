FROM docker.artifactory.dhl.com/python:3.11-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Patch security updates
RUN sed -i 's#http://deb.debian.org/debian-security#https://artifactory.dhl.com/artifactory/debian-security#g' /etc/apt/sources.list.d/debian.sources || true \
    && sed -i 's#http://security.debian.org/debian-security#https://artifactory.dhl.com/artifactory/debian-security#g' /etc/apt/sources.list.d/debian.sources || true \
    && sed -i 's#http://deb.debian.org/debian#https://artifactory.dhl.com/artifactory/debian-remote#g' /etc/apt/sources.list.d/debian.sources || true \
    && apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends git libgomp1 \
    && apt-get clean \
    && useradd -u 8877 jarvis --user-group --create-home

WORKDIR /csai

# # Install dependencies
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --locked --no-install-project --verbose

ADD . /csai

# Sync the project
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync --locked --verbose

# RUN --mount=type=cache,target=/root/.cache uv sync --frozen --no-dev --no-editable -v 
# RUN uv venv
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "src/app.py"]
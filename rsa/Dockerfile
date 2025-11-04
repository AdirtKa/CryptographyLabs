FROM python:3.12-slim-trixie

RUN apt update && apt upgrade

WORKDIR /app

RUN pip install fastapi requests pycryptodome uvicorn --no-cache-dir

COPY rsa.py server.py generate_keys.py ./

EXPOSE 8093
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8093"]
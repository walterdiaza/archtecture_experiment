FROM python:3.13

RUN pip install poetry==1.8.4

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev 


EXPOSE 8002

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
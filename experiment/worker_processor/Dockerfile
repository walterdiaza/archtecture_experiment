FROM python:3.13

RUN pip install poetry==1.8.4

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev 


EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "worker.py"]
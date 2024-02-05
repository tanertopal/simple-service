FROM python:3.10

COPY . .

RUN pip install poetry && poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:main"]


FROM public.ecr.aws/lambda/python:3.10

# Atau pakai python:3.10-slim jika tidak pakai AWS Lambda base image
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
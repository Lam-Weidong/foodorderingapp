
FROM python:slim

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app

EXPOSE 15000

# Run app.py when the container launches
CMD ["python", "app.py"]

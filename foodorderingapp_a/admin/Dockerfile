
# Use an official Python runtime as a parent image
FROM python:slim


ADD . /admin 

WORKDIR /admin


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 16000

# Run app.py when the container launches
CMD ["python3", "admin.py"]


# Use an official Python runtime as a parent image
FROM python:slim


ADD . /shop 

WORKDIR /shop


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 15002

# Run app.py when the container launches
CMD ["python3", "shop.py"]

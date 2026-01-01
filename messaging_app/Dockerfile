# 1 . Use an official python base image
FROM python:3.10

# 2. set the directory inside the conatiner where the commands will run
WORKDIR /app

# 3. Copy the requirements file into the container
COPY Requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# 5. copy the resst of your application code
COPY . . 

# 6. Tell docker which port the app uses
EXPOSE 8000

# 7. The command to run your app
CMD ["python","manage.py","runserver","0.0.0.0:8000"]


 
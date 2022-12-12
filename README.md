# jwt-authentication-in-flask
Implementation of jwt authentication using flask

#Steps to run using docker
1. docker build -t jwt_app .
2. docker run -dp 5000:5000 --name jwt jwt_app

#Steps to run without docker
1. py -m venv .venv
2. activate your virtual environment 
    .\.venv\Scripts\activate
3. pip install -r requirements.txt
4. flask run 
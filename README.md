
# Building API using FastAPI framework
Current project allows consumers to manage vessels:create, update,retrieve a list of vessels from the server.
An additinal feature is to make above operations by date and destination of the vessel. 
SQLite used for the DataBase 

-----

## RUN the app: </br>
###  Option 1 use Docker:
```docker build -t NAME .``` </br>
```docker run -p 80:80 NAME ```</br>


### Option 2:
install requirements;
``` uvicorn main:app --reload ```

----

You can use Interactive API docs (/docs) or alternative automatic documentation for UI(/redoc)
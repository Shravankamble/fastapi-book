# Usage 

<h2> Clone the Repository Using Git Command Given Below </h2> 

`git clone https://github.com/Shravankamble/fastapi-book.git` and then after cloning change the directory to `cd fastapi-book`

Activate Virtual Environment

> install the dependencies after activating the virtual/dev environment!

Commands to create and activate the python virtual/dev environment

`python3 -m venv venv`

`source ./venv/bin/activate`

after activating the virtual environment install the Dependencies.

<h2> Dependencies Installation </h2> 

`pip3 install -r requirements.txt`

<h4> The Three Main Dependencies are: </h4>

```
FastAPI
Uvicorn
SQlAlchemy
```
<hr>

**After all the installations above are completed. Start Postgresql server and create the database and also create an `.env` and put this given variables below and set your own database values.**

```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your password
DATABASE_NAME=your database name
DATABASE_USERNAME=postgres
# this is a dummy key use this command (openssl rand -hex 32) to generate a 32 bit secret key
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256 you can use different algorithm such as RS256    
ACCESS_TOKEN_EXPIRE_TIME=the jwt access token expiration time 
```

After all this is setup.

use this command to run the fastapi server

`uvicorn app.main:app --reload`

open the browser and visit `http://127.0.0.1:8000/docs` you will be directed to the swagger ui by FastAPI.

You can see all the usable API endpoints there. 



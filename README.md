# SpendyByte

[![Django CI](https://github.com/ajinzrathod/spendybyte/actions/workflows/django.yml/badge.svg)](https://github.com/ajinzrathod/spendybyte/actions/workflows/django.yml)

0. Clone the repo and go inside the directory: 
```bash
git clone git@github.com:ajinzrathod/spendybyte.git`
cd spendybyte
```

1. Create a Postgres database
```bash
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
```

2. Create a database in the same postgres container

3. Create a file named `.env` in **spendybyte** folder. The file should look like this.
```.env
SECRET_KEY=yoursecretkey
DATABASE_NAME=spendybyte
DATABASE_USER=user
DATABASE_PASSWORD=awesomepassword
```
Replace the details as per your database config

5. Install Python. We are using python 3.11, so it would be recommended to use the same version

6. Create a virtual environment
```bash
python3.11 -m venv ./env
```

7. Activate the virtual environment
```bash
source ./env/bin/activate
```
8. Install dependecies
```bash
pip install -r requirements.txt
```

9. Run the application
```
python manage.py runserver
```

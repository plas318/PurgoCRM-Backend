# Purgo CRM Backend

- Django

- DjangoRestFramework

- Drf-Spectacular

### Install and Run Purgo Backend

Install Dependencies

```
$ cd pip install -r requirements.txt
```
Migrate database

```
$ python manage.py migrate
```

And Run server
```
$ python manage.py runserver --no-reload
```

### Change Server Settings

change SERVER to local, aws based on db 
```
SERVER = 'local'
if SERVER == 'local':
    # Local Sqlite db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
elif SERVER == 'aws':
    # Amazon aws ec2 server db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("NAME"),
            'USER': os.getenv("USER"),
            'PASSWORD': os.getenv("PASSWORD"),
            'HOST': os.getenv("HOST"),
            'PORT': os.getenv("PORT"),
        }    
    }
```

### Backend API Swagger 
Run server and go [here](http://ec2-18-116-40-72.us-east-2.compute.amazonaws.com:8000/api/schema/swagger-ui/)

or use the url endpoint below
```
/api/schema/swagger-ui/
```
Redoc
```
/api/schema/redoc/
```
Swagger ui should provide a page like this:

![purgo_back_test](https://github.com/purgo-capstone/back/assets/64758800/17846878-9ad3-4b48-929c-039cc0e4c98b)


## AWS Server Settings

clone backend api
```
git clone -b hospital-app-14 --single-branch http://github.com/purgo-capstone/back
```

setup venv
```
python3.8 -m venv venv
```

install requirements
```
pip install -r requirements.txt
```

migrate database schemas
```
python manage.py migrate
```

run django test server (not for production) use wsgi or gunicorn instead for production
```
python manage.py runserver 0:8000 --noreload 
```

### Docker Related
run mysql docker
```
sudo docker ps -a

sudo docker start (container_id)
```

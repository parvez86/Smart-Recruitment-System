# Clone the project
```
git clone https://github.com/parvez86/Smart-Recruitment-System.git
```
# Install required packages
```
pip install -r requirements.txt
```
# Config database
For MySQL

Adds to settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': Your database name, 
        'HOST': Your host,
        'PORT': Your host port,
        'USER': Your mysql username,
        'PASSWORD': Your mysql user password,
    }
}
```
# Test DB connection
```
python manage.py makemigrations
python manage.py migrate
```
# Run project
```
python manage.py runserver
```

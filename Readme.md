Virtual environment
Before we install Django we will get you to install an extremely useful tool to help keep your coding environment tidy on your computer.

At the root dir create a virtualenv using,
```
python3 -m venv venv
```
And activate it using
```
source venv/bin/activate
```

And then clone the project

After cloning the project, make sure you install all dependencies of geodjango using:

https://docs.djangoproject.com/en/3.0/ref/contrib/gis/

Once all settings are installed,
Migrate to the project folder and run below for data migration
```
python manage.py migrate
```
```
python manage.py library_dataset
```
```
python manage.py emergency_support
```

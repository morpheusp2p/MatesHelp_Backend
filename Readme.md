Repository for MatesHelp Backend
=========

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

After cloning the project, make sure you install all dependencies of geodjango which are mentioned in the link below

https://docs.djangoproject.com/en/3.0/ref/contrib/gis/

Once all settings are installed,
Migrate to the project folder and run below for data migration
```
pip install -r requirements.txt
python manage.py migrate
python manage.py library_dataset
python manage.py emergency_support
python manage.py free_resources
python manage.py centrelink
python manage.py hospitals
python manage.py needle_exchange
```

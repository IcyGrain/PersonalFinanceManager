# PersonalFinanceManager
for hackathon

To run:
cd manage.py directory

then command:
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
  

  python manage.py runserver
  
  
 you can explore and update database by open url localhost:8000/admin/, the username and password is you set in "createsuperuser"
 
 
 "models.py" store the data model
 "views.py" store the service function
 "urls.py" manage the url of application that you can access

#Fitrangi source

##README

###To install dependencies
1. sudo apt-get install python-dev
2. sudo pip install -r requirements.txt

if pip is not install then run: 
	sudo easy_install pip 
and then try the step 2 again.


###To Setup the database (Make sure the mongodb is installed on local)
python manage.py db_fixture -l


###To Run the server
-----------------
python manage.py runserver

Go to [http://localhost:5000]


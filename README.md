#Fitrangi source

##README

###To install dependencies
1. sudo apt-get install python-dev
2. sudo pip install -r requirements.txt

if pip is not install then run: 
	sudo easy_install pip 
and then try the step 2 again.

###Get data from dropbox to your fitrangi repository.
1. Go inside the repository where you have downloaded the code.
2. From inside the repository, run the following command
	```
	ln -s <path to dropbox>/fitrangi/alldata.json alldata.json
	```

###To Setup the database (Make sure the mongodb is installed on local)
Run the following command to create the database content on your local mongo db.
```
python manage.py db_fixture --local
```


###To Run the server
-----------------
``` 
python manage.py runserver
```

Go to http://localhost:5000


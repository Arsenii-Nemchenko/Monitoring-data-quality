# Monitoring-data-quality
### ...
## The purpose of this project is to allow a user to follow the changes in data by concrete metrics in the file that is going to be changing.

# How to run program from shell
* Make sure that you have installed the newest version of python on your pc

* Clone this repository
* Go to the root folder of repository
* .../Rocnikovy_project
* Set up a .env file on in the .../Rocnikovy_project/Code/src folder:
*    It has to contain the following lines to access your postgres database:
    DB_HOST=yourhost
    DB_NAME=databasename
    DB_USER=username
    DB_PASSWORD=password
* To run the code enter python -m Code.Gui.main_window

# Reiquirements for files

* File syntax name_timestamp(14 digits)
* Example: my_file_20251124111111.json

# Automated generation of the file stream

* File_sender directory contains file_sender.py
* User can run it and create an automated file stream to the chosen directory
* The file names of those files will be converted into the needed format
* The copies of a chosen file of csv, json or parquet format will be copied to the directory

# How to run file_sender.py

* Open command prompt
* Go to the root folder of repository .../Rocnikovy_project/File_sender
* To run it enter python file_sender.py
* Set up the file stream on a window


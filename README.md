# Monitoring-data-quality
### ...
## The purpose of this project is to allow a user to follow the changes in data by concrete metrics in the file that is going to be changing.

# How to run program from shell

* Clone this repository
* Go to the root folder of repository
* Rocnikovy_project\Code
* Set up a .env file on in the src folder:
*    It has to contain the following lines to access your postgres database:
    DB_HOST=yourhost
    DB_NAME=databasename
    DB_USER=username
    DB_PASSWORD=password
* To run the code enter python -m Code.Gui.main_window

# Reiquirements for files

* File syntax name_timestamp(14 digits)
* Example: my_file_20251124111111.json

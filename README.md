# Auth
This project uses face recognition as a security for workplace. This app stores the identity of all the people who are allowed to enter the workplace, and when they want to enter workplace they have to first be verify their identity, upon validation they will be allowed to enter, thus avoiding the entry of unauthorized people and maintaining the security of the workplace.
![alt text](https://github.com/rhyths08/Auth/blob/main/icon.png)
# Demo
[Video Demo]()
# System Requirments
Following things are necessary for this project to work on your system:
- Python 3.10
- MySql Server(It should be a running server, to store the data of the app)
# Installation Process
1: Install the requirments.
```
pip install -r requirment.txt
```
2: Create Database
```
python database.py
```
After running this command, cmd will ask you to enter username and password of your MySql server. This will allow the app to create a database in your MySql server.
3: Run The App
```
python main.py
```
After running this command, cmd will ask you to enter your username and password of your sql server. This will allow the app to access the database it created in your server.

![alt text](https://github.com/rhyths08/Auth/blob/main/pictures/1.png)


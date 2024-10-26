This repo is aimed at automating the work of a django developer. 

Steps to take advantage of it. 

Commands to run step by step.

Step 1:
Open your terminal / Cmd/ Console on local machine or server.

Step 2:
mkdir "Your_directory_Name"
cd "Your_directory_Name"

Step 3:
git init (Initialise a git directory)

Step 4:
git pull "repo URL"

Now you have the files locally.

Step 5:
Now run ./setup.sh 
This will ask you about all the important details of your django project. 
Once given, press enter and the entire project will be setup with instalations in minutes. 

It will install venv and dependencies and make a requirements.txt also.
Note: This installs some dependencies of open AI also, but if you do not need them, remove them.

See all dependencies using pip show list

Now once this is done, you can now, just make minor adjustments as needed but alsmost everything is setup from settings.py to views.py

Step 6:

Copy reload.sh in the root directory

Using ./reload.sh

You can any time view test your apache2 configration for any file or logs of your app / server with just 1 command.

Overall this should automate and save a lot of time for you. 









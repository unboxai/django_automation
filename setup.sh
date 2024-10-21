#!/bin/bash

# Function to prompt for input if not provided as arguments
get_input() {
    if [ -z "$1" ]; then
        read -p "$2: " input
        echo "$input"
    else
        echo "$1"
    fi
}

# Assign arguments or prompt
project_name=$(get_input "$1" "Enter the Django project name")
app_name=$(get_input "$2" "Enter the Django app name")
venv_name=$(get_input "$3" "Enter the virtual environment name")
allowed_hosts=$(get_input "$4" "Enter allowed hosts (comma-separated, no spaces)")
project_path=$(get_input "$5" "Enter the full path where the project should be created")

# Ensure the specified directory exists, create it if it doesn't
mkdir -p "$project_path"
cd "$project_path" || { echo "Error: Could not change to project path $project_path"; exit 1; }

# Create and activate the virtual environment at the correct level
python3 -m venv "$venv_name"
source "$venv_name/bin/activate"

# Create a directory for the project and navigate into it
mkdir "$project_name"
cd "$project_name" || { echo "Error: Could not change to project directory $project_name"; exit 1; }

# Upgrade pip and install Django
pip install --upgrade pip

# Install necessary Python packages
echo "Installing necessary packages..."

pip install gradio openai django requests

# Create requirements.txt at the project level
pip freeze > requirements.txt

# Start the Django project
django-admin startproject "$project_name" .

# Start the Django app
python manage.py startapp "$app_name"

# Create static, staticfiles, and media directories
mkdir -p static staticfiles media

# Modify settings.py
settings_file="$project_name/settings.py"

# Add app to INSTALLED_APPS
if grep -q "INSTALLED_APPS = \[" "$settings_file"; then
    sed -i "s/INSTALLED_APPS = \[/INSTALLED_APPS = [\n    '$app_name',/" "$settings_file"
fi

# Add ALLOWED_HOSTS
allowed_hosts_formatted=$(echo "$allowed_hosts" | tr ',' "' '" | tr '\n' ' ' | sed "s/ /', '/g")
sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ['$allowed_hosts_formatted']/" "$settings_file"

# Ensure import os is present
if ! grep -q "import os" "$settings_file"; then
    sed -i '1iimport os' "$settings_file"
fi

# Add static and media settings
echo "
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
" >> "$settings_file"

# Create templates directory in the app
mkdir -p "$app_name/templates"

# Create urls.py in the app with basic content
cat <<EOL > "$app_name/urls.py"
from django.urls import path
from . import views

urlpatterns = [
    # Define your app's URLs here
]
EOL

# Setup complete
echo "Django project '$project_name' with app '$app_name' has been set up in $project_path/$project_name."
echo "Virtual environment '$venv_name' is created at $project_path/$venv_name."
echo "requirements.txt is at the project level: $project_path/$project_name/requirements.txt"
echo "Static, staticfiles, and media directories have been created."
echo "settings.py has been updated with ALLOWED_HOSTS, STATIC and MEDIA configurations."
echo "The app has been added to INSTALLED_APPS."
echo "templates directory and urls.py have been created in the app directory."

import sys
import subprocess
import pkg_resources
import os

# Required packages
REQUIRED_PACKAGES = [
    'gradio',
    'openai',
    'django',
    'requests'
]

def install_packages(packages):
    """
    Install missing packages using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)

def check_and_install_dependencies(required_packages):
    """
    Check for missing packages and install them.
    """
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in required_packages if pkg.lower() not in installed_packages]

    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        install_packages(missing_packages)
        print("Dependencies installed successfully. Restarting the script...")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    else:
        print("All dependencies are already installed.")

# Check and install dependencies
check_and_install_dependencies(REQUIRED_PACKAGES)

# Now import the packages
import gradio as gr
import openai
import django
import requests

# Rest of your Gradio interface and functions
# [Insert your existing creator.py code here]


import gradio as gr
import subprocess
import os
import openai

# Define available models with descriptions
AVAILABLE_MODELS = {
    "GPT-4o": "Our high-intelligence flagship model for complex, multi-step tasks",
    "GPT-4o mini": "Our affordable and intelligent small model for fast, lightweight tasks",
    "o1-preview": "Language model trained with reinforcement learning to perform complex reasoning.",
    "o1-mini": "Language model trained with reinforcement learning to perform complex reasoning.",
    "GPT-4 Turbo": "Previous high-intelligence model.",
    "GPT-4": "Previous high-intelligence model.",
    "GPT-3.5 Turbo": "A fast, inexpensive model for simple tasks",
    # Add other models as needed
}

# Function to execute the shell script
def run_setup(project_name, app_name, venv_name, allowed_hosts, project_path):
    script_path = os.path.join(os.getcwd(), 'setup.sh')
    
    if not os.path.exists(script_path):
        return f"Error: Shell script not found at {script_path}"
    
    # Ensure the shell script is executable
    if not os.access(script_path, os.X_OK):
        try:
            os.chmod(script_path, 0o755)
        except Exception as e:
            return f"Error setting execute permissions on shell script: {str(e)}"
    
    # Prepare the command with arguments
    command = [
        'bash',
        script_path,
        project_name,
        app_name,
        venv_name,
        allowed_hosts,
        project_path
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return f"**Setup Successful:**\n```\n{result.stdout}\n```"
    except subprocess.CalledProcessError as e:
        return f"**An error occurred during setup:**\n```\n{e.stderr}\n```"
    except Exception as e:
        return f"**Unexpected error:**\n```\n{str(e)}\n```"

# Function to generate content using OpenAI
def generate_content(instructions, file_type, project_path, app_name, model):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai.api_key:
        return "Error: OpenAI API key not set. Please set the `OPENAI_API_KEY` environment variable."
    
    prompt = f"""
Create a Django `{file_type}.py` file for the app '{app_name}' based on the following instructions:

{instructions}

Ensure the code follows best practices and includes necessary imports.
"""

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=1500,
            temperature=0.3,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        content = response.choices[0].text.strip()
        
        # Determine file path
        file_path = os.path.join(project_path, app_name, f"{file_type}.py")
        
        # Save content to the file
        with open(file_path, 'w') as f:
            f.write(content)
        
        return f"`{file_type}.py` has been successfully created at `{file_path}`."
    
    except openai.error.OpenAIError as e:
        return f"**OpenAI API error:** {str(e)}"
    except Exception as e:
        return f"**An error occurred while generating `{file_type}.py`:** {str(e)}"

# Gradio Interface Functions
def step1(project_name, app_name, venv_name, allowed_hosts, project_path):
    return run_setup(project_name, app_name, venv_name, allowed_hosts, project_path)

def step2(instructions, project_path, app_name, model):
    return generate_content(instructions, "views", project_path, app_name, model)

def step3_urls(instructions, project_path, app_name, model):
    return generate_content(instructions, "urls", project_path, app_name, model)

def step3_models(instructions, project_path, app_name, model):
    return generate_content(instructions, "models", project_path, app_name, model)

# Define the Gradio Blocks Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ Django Project Automator")
    gr.Markdown("Automate your Django project setup and file generation using this tool.")
    
    with gr.Tab("Step 1: Initialize Project"):
        with gr.Column():
            project_name = gr.Textbox(label="Django Project Name", placeholder="myproject")
            app_name = gr.Textbox(label="Django App Name", placeholder="myapp")
            venv_name = gr.Textbox(label="Virtual Environment Name", placeholder="venv")
            allowed_hosts = gr.Textbox(label="Allowed Hosts (comma-separated, no spaces)", placeholder="localhost,127.0.0.1")
            project_path = gr.Textbox(label="Project Path", placeholder="/path/to/projects")
            setup_btn = gr.Button("🛠️ Setup Project")
            setup_output = gr.Markdown(label="Output")
            
            setup_btn.click(
                step1,
                inputs=[project_name, app_name, venv_name, allowed_hosts, project_path],
                outputs=setup_output
            )
    
    with gr.Tab("Step 2: Generate `views.py`"):
        with gr.Column():
            instructions_views = gr.Textbox(label="Instructions for `views.py`", placeholder="Describe the views you want...", lines=5)
            model_views = gr.Dropdown(
                choices=list(AVAILABLE_MODELS.keys()),
                label="Select OpenAI Model",
                value="GPT-4o",
                info="Choose the OpenAI model to generate `views.py`. Different models offer varying capabilities and cost points."
            )
            generate_views_btn = gr.Button("✨ Generate `views.py`")
            views_output = gr.Markdown(label="Output")
            
            generate_views_btn.click(
                step2,
                inputs=[instructions_views, project_path, app_name, model_views],
                outputs=views_output
            )
    
    with gr.Tab("Step 3: Generate `urls.py` and `models.py`"):
        with gr.Row():
            with gr.Column():
                instructions_urls = gr.Textbox(label="Instructions for `urls.py`", placeholder="Describe the URLs you want...", lines=3)
                model_urls = gr.Dropdown(
                    choices=list(AVAILABLE_MODELS.keys()),
                    label="Select OpenAI Model",
                    value="GPT-4o",
                    info="Choose the OpenAI model to generate `urls.py`. Different models offer varying capabilities and cost points."
                )
                generate_urls_btn = gr.Button("✨ Generate `urls.py`")
                urls_output = gr.Markdown(label="Output")
                
                generate_urls_btn.click(
                    step3_urls,
                    inputs=[instructions_urls, project_path, app_name, model_urls],
                    outputs=urls_output
                )
            with gr.Column():
                instructions_models = gr.Textbox(label="Instructions for `models.py`", placeholder="Describe the models you want...", lines=3)
                model_models = gr.Dropdown(
                    choices=list(AVAILABLE_MODELS.keys()),
                    label="Select OpenAI Model",
                    value="GPT-4o",
                    info="Choose the OpenAI model to generate `models.py`. Different models offer varying capabilities and cost points."
                )
                generate_models_btn = gr.Button("✨ Generate `models.py`")
                models_output = gr.Markdown(label="Output")
                
                generate_models_btn.click(
                    step3_models,
                    inputs=[instructions_models, project_path, app_name, model_models],
                    outputs=models_output
                )
    
    gr.Markdown("""
    ---
    **⚠️ Important:** Ensure that the `setup.sh` script is in the same directory as this application and is executable. Also, make sure that your OpenAI API key is set as an environment variable `OPENAI_API_KEY`.
    """)
    
# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()

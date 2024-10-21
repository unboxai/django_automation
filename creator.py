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
def generate_views(instructions, project_path, app_name, model):
    return generate_content(instructions, "views", project_path, app_name, model)

def generate_urls(instructions, project_path, app_name, model):
    return generate_content(instructions, "urls", project_path, app_name, model)

def generate_models(instructions, project_path, app_name, model):
    return generate_content(instructions, "models", project_path, app_name, model)

# Define the Gradio Blocks Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ Django Project Automator")
    gr.Markdown("Automate your Django project file generation using this tool.")
    
    with gr.Tab("Configure Project"):
        with gr.Column():
            project_path = gr.Textbox(label="Project Path", placeholder="/path/to/your/project", lines=1)
            app_name = gr.Textbox(label="Django App Name", placeholder="myapp", lines=1)
            submit_config = gr.Button("Set Configuration")
            config_status = gr.Markdown()
            
            def set_configuration(p_path, a_name):
                if not os.path.exists(p_path):
                    return f"Error: The project path `{p_path}` does not exist."
                if not os.path.isdir(p_path):
                    return f"Error: `{p_path}` is not a directory."
                # Optionally, verify that the app directory exists
                app_path = os.path.join(p_path, a_name)
                if not os.path.exists(app_path):
                    return f"Warning: The app directory `{app_path}` does not exist yet."
                return f"Configuration set successfully! Project Path: `{p_path}`, App Name: `{a_name}`."
            
            submit_config.click(
                set_configuration,
                inputs=[project_path, app_name],
                outputs=config_status
            )
    
    with gr.Tab("Generate `views.py`"):
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
                generate_views,
                inputs=[instructions_views, project_path, app_name, model_views],
                outputs=views_output
            )
    
    with gr.Tab("Generate `urls.py`"):
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
                generate_urls,
                inputs=[instructions_urls, project_path, app_name, model_urls],
                outputs=urls_output
            )
    
    with gr.Tab("Generate `models.py`"):
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
                generate_models,
                inputs=[instructions_models, project_path, app_name, model_models],
                outputs=models_output
            )
    
    gr.Markdown("""
    ---
    **⚠️ Important:**
    - Ensure that your OpenAI API key is set as an environment variable `OPENAI_API_KEY`.
    - Make sure that the `project_path` and `app_name` are correctly configured in the **Configure Project** tab.
    - Generated files will overwrite existing files with the same name in the specified Django app.
    """)

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()

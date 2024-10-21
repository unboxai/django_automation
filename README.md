# django_automation
This tool should automate creation of any web application. The goal is to use Django for backend. Postgre for db, Rect and Next.js for front end and do it all in minutes. It should build a good starting point to further refine and act on. 


# 🛠️ Django Project Automator

Automate your Django project setup and file generation using this Gradio-based web application. This tool streamlines the process of initializing Django projects, setting up virtual environments, and generating essential files (`views.py`, `urls.py`, `models.py`) using OpenAI's Language Models.

## Features

- **Project Initialization:** Create a Django project with a virtual environment effortlessly.
- **File Generation:** Generate `views.py`, `urls.py`, and `models.py` based on your custom instructions.
- **Model Selection:** Choose from a variety of OpenAI models to control the complexity and cost of the generated content.
- **User-Friendly Interface:** Interactive web interface built with Gradio.
- **OpenAI Integration:** Leverage AI to generate Django files adhering to best practices.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Step 1: Initialize Project](#step-1-initialize-project)
  - [Step 2: Generate `views.py`](#step-2-generate-viewspy)
  - [Step 3: Generate `urls.py` and `models.py`](#step-3-generate-urlspy-and-modelspy)
- [Model Selection](#model-selection)
- [Repository Structure](#repository-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **Git**
- **OpenAI API Key**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/django-automator.git
   cd django-automator

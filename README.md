# Streamlit MentorIA+ Platform

This repository contains a web application built with Streamlit designed to enhance learning through AI-powered coaching, assessments, and progress tracking.

## 🧠 Project Overview

This platform provides an interactive learning experience through:

- ✅ AI-driven training chat for personalized coaching
- 📚 Learning path navigation for structured content access
- 📝 Knowledge assessments to track progress
- 📊 Progress dashboard for insights and analytics
- 🎓 Course creation tools for coaches to develop new training materials
- 🎤 Voice interaction with speech recognition and text-to-speech features

## 🛠️ Technologies Used

- 🔍 **Azure OpenAI** - AI-powered chatbot and content generation
- 🎤 **Azure Speech** - Speech-to-text and text-to-speech for voice interaction
- 📂 **Azure Storage** - Storing and retrieving training materials
- 🖥 **Streamlit** - Interactive and user-friendly web interface
- 🚀 **Power BI** - Data visualization for learning progress tracking
- 🛠 **FastAPI** - Backend API integration

## 📁 Project Structure

- 🏠 **Home** - Personalized landing page with mood-based interaction
- 🚀 **Learning Path** - Structured training program for guided learning
- 💬 **AI Training Chat** - Interactive chatbot for training assistance
- 📝 **Assessments** - Evaluate knowledge with quizzes
- 📊 **Dashboard** - Track progress and performance insights via Power BI
- 🛠 **Course Creation** - Tools for building and managing training content
- 📂 **Topic Content** - Detailed topic exploration and study materials

## 🚀 Installation

### 1️⃣ Prerequisites

Ensure you have the following installed:

- Python >= 3.11
- pip
- Virtualenv (optional but recommended)

### 2️⃣ Clone the repository

```sh
git clone https://github.com/Dany21x/streamlit_ai_job_coach
cd streamlit_ai_job_coach
```

### 3️⃣ Create and activate a virtual environment

```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 4️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

## 🌐 Environment Variables

Before running the application, set up the required environment variables in a `.env` file. Use `example.env` as a reference and provide the necessary values:

```sh
SPEECH_KEY=
SPEECH_REGION=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_STORAGE_CONTAINER_NAME=
API_QUESTIONS_URL=
API_RESPONSES_FEEDBACK_URL=
API_RESPONSES_DATABASE_URL=
API_LOGIN_URL=
POWER_BI_URL=
API_TOPICS_TO_DB=
```

Copy the example file and fill in your credentials:

```sh
cp example.env .env
```

## ▶️ Running the Application

Start the Streamlit application with:

```sh
streamlit run app.py
```

If your main application file has a different name, replace `app.py` accordingly.

## 🛠 Deployment

To deploy the application to a cloud provider (such as Azure), follow these steps:

1. **Login to Azure CLI:**
   ```sh
   az login
   ```
2. **Ensure Azure CLI is up to date:**
   ```sh
   az upgrade
   ```
3. **Create a resource group:**
   ```sh
   az group create --name learning-platform-rg --location eastus
   ```
4. **Create Azure Container Registry:**
   ```sh
   az acr create --resource-group learning-platform-rg \  
   --name <container-registry-name> --sku Basic
   ```
5. **Build and Push Docker Image:**
   ```sh
   az acr build \  
     --resource-group learning-platform-rg \  
     --registry <container-registry-name> \  
     --image learning-platform:latest .
   ```

## 🚀 Deploying on Streamlit Cloud

1. Push your project to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click on **New app** and connect your GitHub repository.
4. Set up the **main file** (e.g., `app.py`) and configure **environment variables** in the settings.
5. Click **Deploy** and Streamlit will handle the rest!


<br>

🐝 **Powered by Bee Code**
<p align="center">
  <img src="assets/bee_code.png" alt="Bee Code Logo" width="100">
</p>
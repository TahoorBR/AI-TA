Here's a **README.md** file for your project **AI-TA: Artificial Intelligence Teaching Assistant**, written in a clear and professional style suitable for GitHub or similar platforms:

---

````markdown
# AI-TA: Artificial Intelligence Teaching Assistant

AI-TA is an AI-powered teaching assistant chatbot that helps educators automate routine academic tasks such as course outline creation, quiz and assignment generation, grading, and personalized feedback. The system is designed to save teachers time, reduce workload, and improve the learning experience for students.

## 🔍 Overview

AI-TA uses a locally deployed LLaMA 3.2 3B model via Ollama to generate high-quality educational content. The application is built with Python (Flask), React, and SQLite3. It supports both web and desktop environments and is accessible through a custom domain using ngrok tunneling.

## ✨ Features

- 📚 **Course Outline Generator** – Automatically generate structured course plans.
- ❓ **Quiz Generator** – Create multiple-choice quizzes from prompt-based inputs.
- 📝 **Assignment Generator** – Generate assignment tasks based on topics.
- 🧠 **Personalized Feedback** – Provide feedback to students based on performance.
- ✅ **Automated Grading** – Grade quizzes and assignments instantly.
- 🌐 **Web/Desktop Deployment** – Runs locally or on a custom domain via ngrok.
- 🤖 **Powered by LLaMA 3.2** – Efficient and context-aware content generation.

## 🛠️ Tech Stack

- **Frontend:** React, HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Database:** SQLite3
- **AI Model:** LLaMA 3.2 3B via [Ollama](https://ollama.com/)
- **Deployment:** ngrok + Custom Domain (e.g., `www.ai-ta.online`)

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Flask
- SQLite3
- Node.js (for React frontend)
- Ollama CLI (for running LLaMA model)
- ngrok (for custom domain tunneling)

### Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/ai-ta.git
   cd ai-ta
````

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Flask Backend**

   ```bash
   python app.py
   ```

4. **Start Frontend (React)**

   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Start Ollama model**

   ```bash
   ollama run llama3
   ```

6. **Run ngrok tunnel**

   ```bash
   ngrok http 80
   ```

## 📊 Evaluation

The system achieved:

* ✅ 92% accuracy in quiz generation
* ✅ 89% usefulness score for personalized feedback (based on teacher reviews)

## 📦 Deployment

AI-TA can be packaged into a standalone desktop app using PyInstaller. For public access, it uses ngrok tunneling with a custom domain (e.g., GoDaddy DNS settings).

## 🧩 Future Enhancements

* Add user authentication (OAuth2/JWT)
* Expand multilingual support
* Migrate to cloud hosting (AWS EC2, Railway)
* Add voice interface for accessibility

## 👨‍💻 Authors

* Muhammad Tahoor Bin Rauf
* Mahrukh Zafar
* Eman Sarwar

**Supervisor:** Dr. Muhammad Tahir Akram
**Institution:** Air University, Islamabad

## 📄 License

This project is for academic and non-commercial use. Licensing terms can be added based on project requirements.


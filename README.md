# Flexcube Copilot

Flexcube Copilot is an AI-powered assistant designed to automate and streamline Oracle Flexcube customizations. It leverages advanced LLMs to analyze requirements, perform impact assessments, and generate code, ensuring a structured and efficient workflow for developers and business analysts.

## 🚀 Features

- **Requirement Analysis**: Automatically distills business requirements into technical specifications.
- **Impact Assessment**: Identifies potential risks and affected modules during customization.
- **Code Generation**: Generates standard Oracle Flexcube customization code (SQL, PL/SQL, etc.) based on refined requirements.
- **Web-Based Interface**: A clean, intuitive dashboard to manage the entire customization lifecycle.

## 🛠️ Tech Stack

- **Backend**: Python 3.12+ / Flask
- **AI Core**: Google Generative AI (Gemini 2.0 Flash)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **Version Control**: Git / GitHub

## 📂 Project Structure

```text
flexcube_copilot/
├── src/
│   ├── agents/            # Specialized AI agents (Requirement, Impact, Code Gen)
│   ├── core/              # LLM integration and core data models
│   ├── web/               # Flask application and UI static files
│   └── ...
├── .gitignore             # Git ignore configuration
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## 🏁 Getting Started

### Prerequisites

- Python 3.12 or higher installed.
- A Google API Key for Gemini.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JoelPMathew/Flexcube-Copilot.git
   cd Flexcube-Copilot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Ensure your `GOOGLE_API_KEY` is configured in your environment.

### Running the App

Start the Flask development server:
```bash
python src/web/app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

## 📈 Current Status

The project is currently in active development. Core agents for requirement analysis, impact assessment, and code generation are functional and integrated with a preliminary web interface.

---


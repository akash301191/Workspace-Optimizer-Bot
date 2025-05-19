# Workspace Optimizer Bot

Workspace Optimizer Bot is a practical Streamlit application that analyzes your desk setup from a photo and generates a personalized ergonomic report. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot detects posture risks, prioritizes improvements, and suggests ergonomic products to help you create a healthier, more productive workspace.

## Folder Structure

```
Workspace-Optimizer-Bot/
├── workspace-optimizer-bot.py
├── README.md
└── requirements.txt
```

* **workspace-optimizer-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Workspace Photo Upload**
  Upload a photo of your current desk setup for visual analysis.

* **Ergonomic Focus Selection**
  Choose your primary focus area—posture correction, organization, or full ergonomic assessment—and set your improvement goal.

* **AI-Powered Workspace Analysis**
  The Posture Analyzer agent identifies risks, while other agents evaluate their severity, suggest actionable fixes, and recommend ergonomic tools.

* **Personalized Optimization Report**
  Receive a clean, structured Markdown report with risk areas, improvement priorities, fix strategies, and shopping recommendations.

* **Download Option**
  Download your ergonomic workspace report as a `.md` file for future reference.

* **Clean Streamlit UI**
  Built with Streamlit for a responsive and user-friendly experience.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Workspace-Optimizer-Bot.git
   cd Workspace-Optimizer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run workspace-optimizer-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI and SerpAPI API keys in the sidebar.
   * Upload a photo of your workspace.
   * Select your ergonomic focus and goal.
   * Click **🪑 Generate Workspace Optimization Report**.
   * View and download your personalized AI-generated ergonomic report.

3. **Download Option**
   Use the **📥 Download Workspace Report** button to save your findings as a `.md` file.

## Code Overview

* **`render_workspace_setup_preferences()`**: Captures user input including workspace photo, focus area, and ergonomic goals.

* **`render_sidebar()`**: Manages API key input and stores them in Streamlit’s session state.

* **`generate_workspace_report()`**:

  * Uses the `Posture & Setup Analyzer` to detect ergonomic issues from the uploaded image.
  * The `Ergonomic Risk Evaluator` prioritizes those issues.
  * The `Fix Advisor` suggests personalized improvements.
  * The `Product Finder` recommends relevant ergonomic products using SerpAPI.

* **`main()`**: Orchestrates the app layout, user interaction, and report generation pipeline.

## Contributions

Contributions are welcome! If you'd like to improve the bot, fix bugs, or add new features, feel free to fork the repo, create a new branch, and open a pull request. Please keep changes clean, modular, and focused.
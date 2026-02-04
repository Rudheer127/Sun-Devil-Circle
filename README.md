# Sun Devil Circles ☀️😈

A peer support platform for ASU students, featuring AI-powered personalized suggestions and empathetic support.

## Features
- **Semantic Matching**: Connects students with peers and groups based on shared challenges, interests, and profile compatibility.
- **AI Support**: Uses Cerebras AI (Llama 3.3 70B) to provide empathetic responses and personalized resource suggestions.
- **Topic-Based Chat**: Real-time group chats with AI moderation and message editing/deleting.
- **Resource Hub**: Curated ASU resources and support options.
- **25+ Support Groups**: Pre-configured peer support groups covering emotional wellness, academic challenges, identity communities, and daily functioning. Includes groups for anxiety, depression, LGBTQ+ students, international students, and more.
- **Smart Search**: Search groups by name, description, or topic labels for easier discovery.
- **Best Match Sorting**: Groups and peers are ranked by compatibility based on profile overlap, shared challenges, and semantic similarity.

## 🚀 Running on macOS / Linux

Follow these steps to run the project on a new Mac or Linux system:

### 1. Clone the Repository
Open your Terminal and run:
```bash
git clone https://github.com/Rudheer127/Sun-Devil-Circle.git
cd Sun-Devil-Circle
```

### 2. Set Up a Virtual Environment
It's best practice to use a virtual environment to manage dependencies:
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (you'll see (venv) in your prompt)
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask server:
```bash
python app.py
```

### 5. Access the App
Open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 💻 Running on Windows

1. **Clone**: `git clone https://github.com/Rudheer127/Sun-Devil-Circle.git`
2. **Virtual Env** (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install**: `pip install -r requirements.txt`
4. **Run**: `python app.py`

## 🔑 AI Configuration

The application is pre-configured with a default API key for the Cerebras AI features, so **it works out of the box**.

If you wish to use your own API key, you can set an environment variable:
```bash
export CEREBRAS_API_KEY="your-api-key-here"
```

## 🛠 Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **AI**: Cerebras Cloud SDK (Llama 3.3 70B)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

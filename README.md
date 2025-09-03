# Codex : A Personal Codex Agent 

### A context-aware agent that can answer questions about Umutesa (yep, that's me) 
## Key Features

- **Voice Input**: Record questions using built-in microphone
- **Speech-to-Text**: Automatic transcription using Google Speech Recognition
- **Guessing Games**: Multiple choice questions about documents
- **Knowledge Challenges**: Open-ended Q&A with similarity-based scoring for best and most accuare response
- **Visual Story Telling**: Image-based answers
- **Multi input**: Accepts pdf docs , datasets , url websites as input

##  Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Microphone (for voice features)
- Internet connection (for model downloads)
- No API needed
- Run on CPU

### Step 1: Clone or Download
```bash
    git clone 
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run on Virtual Environmnet within Linux ()

```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

### Step 4: Run the Application
```bash
streamlit run src/main.py
```

The application will open in your web browser at `http://localhost:8501`




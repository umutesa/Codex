# Codex : A Personal Codex Agent 

##### Codex is an intelligent, interactive agent that understands context and responds to questions using multiple input formats. Whether you're exploring documents, datasets, or websites, Codex brings your personal knowledge to life through voice, visuals, and Q&A to answe questions about Umutesa .




## Key Features

**Personalised chatbot about Umutesa**: Answer questions about Umutesa


 
 **Text-to-Speech(audio)**: Automatic transcription using Google Speech Recognition
 
  
 **Guessing Games**: Multiple choice questions about documents
 

 **Knowledge Challenges**: Open-ended Q&A with similarity-based scoring for best and most accuare response


 **Visual Story Telling**: Image-based answers

 **Multi input**: Accepts pdf docs , datasets , url websites as input

##  Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Microphone (for voice features)
- Internet connection (for model downloads)
- No API needed
- Runs on CPU (no GPU needed)

### Step 1: Clone or Download
```bash
    git clone https://github.com/umutesa/Codex.git
```

### Step 2: Run on Virtual Environmnet within a Linux Environment (Recommended)

```bash
python3 -m venv codex_env
source codex_env/bin/activate
cd src/
pip install -r requirements.tx

```

### Step 3: Run the Application (in src folder)
```bash
streamlit run main.py
```

### Step 4: Upload Docs
```bash
1. upload the data.json with the src/ folder
2. upload Umutesa's resume
3. upload Umutesa website's as a url link : https://umutesa.github.io/umutesa_munyurangabo.github.io/
```

The application will open in your web browser at `http://localhost:8501`

### Reference

Please see atached report within report folder




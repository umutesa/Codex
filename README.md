# Codex : A Personal Codex Agent 

### Codex is an intelligent, interactive agent that understands context and responds to questions using multiple input formats. Whether you're exploring documents, datasets, or websites, Codex brings your personal knowledge to life through voice, visuals, and Q&A to answe questions about Umutesa

<img width="1322" height="607" alt="Screenshot from 2025-09-04 10-28-52" src="https://github.com/user-attachments/assets/faf4690e-5889-4d99-87e4-7b68221ed768" />


## Key Features

**Personalised chatbot about Umutesa**: Answer questions about Umutesa
<img width="1293" height="547" alt="Screenshot from 2025-09-04 10-31-35" src="https://github.com/user-attachments/assets/fbf45599-55d8-4f3d-9cd4-e6f784dd2e4d" />

 
 **Text-to-Speech(audio)**: Automatic transcription using Google Speech Recognition
 <img width="1259" height="430" alt="Screenshot from 2025-09-04 10-32-09" src="https://github.com/user-attachments/assets/f14ea0f9-429a-4292-8cb7-9ec426df9794" />

  
 **Guessing Games**: Multiple choice questions about documents
  <img width="1849" height="579" alt="Screenshot from 2025-09-04 10-35-28" src="https://github.com/user-attachments/assets/4b94cb4e-f24a-4574-952c-48f065bdd862" />

 **Knowledge Challenges**: Open-ended Q&A with similarity-based scoring for best and most accuare response
  <img width="1251" height="260" alt="Screenshot from 2025-09-04 10-34-40" src="https://github.com/user-attachments/assets/99e5167d-b71c-460e-85e7-ed5b1d674cc1" />

 **Visual Story Telling**: Image-based answers
 **Multi input**: Accepts pdf docs , datasets , url websites as input
  <img width="1861" height="803" alt="Screenshot from 2025-09-04 10-33-54" src="https://github.com/user-attachments/assets/2a49f927-88ba-4fec-9e05-c6ab1b8cbb84" />


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

The application will open in your web browser at `http://localhost:8501`




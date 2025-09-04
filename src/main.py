import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, JSONLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
import json
import requests
import tempfile
import torch
import random
import pyttsx3
from io import BytesIO

st.set_page_config(page_title="Codex: Umutesa Chatbot", layout="wide")
st.image("https://images.unsplash.com/photo-1606788075763-1f9e1fa4c5b5", width='stretch')
st.title("Get to know Umutesa...")
st.write("Upload PDFs, TXT, CSV, JSON, or enter URLs (website, CV, Wikipedia). Get Q&A, stories, fun facts, and guessing games!")

# -- Set background image --
def set_background_image(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image("https://images.unsplash.com/photo-1503264116251-35a269479413")

# -- Some sample data with images generated --
SAMPLE_DATA = [
  {
    "question": "What kind of engineer is Umutesa?",
    "answer": "Umutesa is a multidisciplinary engineer who blends her technical skilld with creative problem-solving. With a BSc in Electrical and Computer Engineering, she approaches challenges with a systems-level mindset—balancing hardware constraints with software capabilities to build solutions that are not only functional but easy to use. Her creativity shines in the way she reimagines conventional approaches, often introducing innovative twists that make her work stand out. Whether it's designing embedded systems or designing intelligent solutions, she thrives at the intersection of feasibility and imagination.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/professional-photo.png",
    "category": "Professional Identity",
    "difficulty": "Medium"
  },
  {
    "question": "What are Umutesa's strongest technical skills?",
    "answer": "Umutesa’s technical toolkit is both broad and deep. She is fluent in Java, C++, and python. Her specialization in computer vision includes advanced techniques like object detection using YOLO, multi-object tracking, and people tracking in dynamic environments. She’s particularly skilled at integrating vision algorithms with real-time systems, enabling autonomous agents to perceive and respond to their surroundings.",
    "image_url": "https://img.freepik.com/free-photo/artificial-intelligence-concept-with-robot-face_23-2147857223.jpg?w=740&q=80",
    "category": "Technical Skills",
    "difficulty": "Medium"
  },
  {
    "question": "What project is Umutesa most proud of?",
    "answer": "Umutesa’s proudest achievement is her master’s thesis: 'Vision-Only Socially Compliant Navigation for Autonomous Robots.' This project tackled one of the most complex challenges in robotics—predicting human trajectories in crowded, occluded environments using only visual input. She developed algorithms that allowed mobile robots to navigate safely and respectfully around people, even when visibility was limited and both the robot and pedestrians were in motion. The work required deep understanding of human behavior modeling, real-time vision processing, and ethical design principles. It was a culmination of late nights, relentless debugging, and a passion for creating technology that harmonizes with human spaces.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/1745785550879.jpeg",
    "category": "Projects",
    "difficulty": "Hard"
  },
  {
    "question": "What does Umutesa value in a team or company culture?",
    "answer": "Umutesa thrives in environments that foster collaboration, mentorship, and continuous growth. She believes that the best ideas emerge when people feel safe to share freely. She values diversity and finds joy in learning from others’ unique perspectives. Her ideal company culture celebrates shared success, encourages upskilling, and supports personal milestones. Whether it’s a team sport, a birthday celebration, or a group hackathon, she sees these moments as the glue that binds a team together. Ultimately, she seeks a workplace that feels less like a job and more like a mission-driven community.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/1745785550879.jpeg",
    "category": "Work Culture",
    "difficulty": "Medium"
  },
  {
    "question": "What is Umutesa's approach to learning or debugging?",
    "answer": "Umutesa approaches debugging as a learning opportunity. She starts by identifying the root cause using first principles such as whether the tool/concept/algorithm is being used correctly, and consulting documentation to understand expected behavior. She believes that every bug is a clue to a deeper gap in understanding. Additionally, she uses platforms like CLion for C++ and VS Code for Python, leveraging their debugging modes to inspect variables, trace execution paths, and isolate anomalies. Her methodical approach combines intuition with discipline, and she often documents her findings to build a personal knowledge base for future reference. For her, debugging isn’t just about fixing,it’s closing the gap in understanding.",
    "image_url": "https://media.istockphoto.com/id/1393379238/photo/work-performance-is-influenced-by-skills-abilities-and-competence-the-concept-of-the.jpg?s=612x612&w=0&k=20&c=JmF3ow_Nn1jLVsjVWSmrCgBpJhJ3FnxX2rVIxWlO68Q=",
    "category": "Problem Solving",
    "difficulty": "Medium"
  }, 
  
  {
    "question": "What are Umutesa's core technical skills?",
    "answer": "Umutesa’s technical expertise spans both breadth and depth. She is proficient in Python, C++, Java, and MATLAB, with strong foundations in front-end technologies like HTML, CSS, and JavaScript. Her backend experience includes SQL, APIs, Flask, and cloud platforms like AWS and Azure Databricks. She’s skilled in data visualization using Power BI and Tableau, and has hands-on experience with tools like Git, ROS2, Linux, and Jupyter. Her software engineering knowledge includes OOP, multithreading, unit testing, and Agile/Scrum methodologies. In AI, she works with PyTorch and TensorFlow, building models using CNNs, GANs, LSTMs, Transformers, and LLMs. Her computer vision work includes object detection, tracking, and image processing using OpenCV and scikit-image.",
    "image_url": "https://media.istockphoto.com/id/1393379238/photo/work-performance-is-influenced-by-skills-abilities-and-competence-the-concept-of-the.jpg?s=612x612&w=0&k=20&c=JmF3ow_Nn1jLVsjVWSmrCgBpJhJ3FnxX2rVIxWlO68Q=",
    "category": "Technical Skills",
    "difficulty": "Hard"
  },
  {
    "question": "Where did Umutesa study?",
    "answer": "Umutesa studied at the University of Cape Town, earning a Bachelor of Science in Electrical and Computer Engineering (2019–2022). She is currently pursuing a Master of Science in Engineering (Mechatronics), focusing on vision-only socially compliant navigation robotics (2023–2025).",
    "image_url": "https://www.studentroom.co.za/wp-content/uploads/2024/10/uct-1.webp",
    "category": "Education",
    "difficulty": "Easy"
  },
  {
    "question": "What awards has Umutesa received?",
    "answer": "Umutesa has been recognized for her academic excellence and leadership. She earned a place on the Dean’s Merit List, received the UCT Plus Bronze Leadership Award, and was honored with the Engineering Mentorship Award for her commitment to guiding and supporting fellow students.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG-20230519-WA0009.jpg",
    "category": "Achievements",
    "difficulty": "Easy"
  },
  {
    "question": "What motivates Umutesa at work?",
    "answer": "Umutesa is driven by a deep desire to serve others. She finds fulfillment in understanding the goals and challenges of those she works with and using her skills to help them succeed. She’s also energized by complex problems—breaking them down, overcoming obstacles, and celebrating milestones. Her motivation stems from purpose, challenge, and the joy of contributing to meaningful outcomes.",
    "image_url": "https://static.wixstatic.com/media/f02629_3fd15850806c498e8864f365f94bfb24~mv2.jpg/v1/fill/w_1000,h_662,al_c,q_85,usm_0.66_1.00_0.01/f02629_3fd15850806c498e8864f365f94bfb24~mv2.jpg",
    "category": "Work Ethic",
    "difficulty": "Medium"
  },
  {
    "question": "What is Umutesa currently reading?",
    "answer": "As of September 2025, Umutesa is currently reading 'Man’s Search for Meaning' by Viktor Frankl. She finds the book deeply moving and believes it offers a profound perspective on life, that even in the most extreme circumstances, a person can find meaning and purpose.",
    "image_url": "https://www.highereducationdigest.com/wp-content/uploads/2019/02/IMG_20190209_105045_800x480-550x330.jpg",
    "category": "Personal Interests",
    "difficulty": "Easy"
  },
  {
    "question": "What is Umutesa's mission and vision?",
    "answer": "Umutesa’s mission is to engineer with empathy. As a woman in STEM, she advocates for inclusive approaches that reflect diverse social contexts. Her vision is to challenge biases and design solutions that honor the human stories behind technical challenges. She believes engineering should be rooted in ethics, empathy, and a deep understanding of people’s lived experiences.",
    "image_url": "https://www.cavsconnect.com/wp-content/uploads/2021/05/9QiIw1TISWcsLjEir3fjRgghYtsQjPYODMt8WPei-900x479.jpeg",
    "category": "Values",
    "difficulty": "Hard"
  },
  {
    "question": "What makes Umutesa stand apart from other engineers?",
    "answer": "Umutesa is a proud representative of women in STEM, blending technical excellence with creativity and empathy. She finds inspiration in both art and nature, and brings a human-centered approach to every project. Her ability to connect deeply with people and understand their needs makes her a rare kind of engineer, one who builds with both heart and mind.",
    "image_url": "https://bs-uploads.toptal.io/blackfish-uploads/components/open_graph_image/8960450/og_image/optimized/image__9_-41b0561dffe7466e8169919ce75f6ef0.png",
    "category": "Identity",
    "difficulty": "Medium"
  }, 
  
    {
    "question": "Who is Umutesa?",
    "answer": "Umutesa is a proud representative of women in STEM, blending technical excellence with creativity and empathy. She finds inspiration in both art and nature, and brings a human-centered approach to every project. Her ability to connect deeply with people and understand their needs makes her a rare kind of engineer—one who builds with both heart and mind.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/professional-photo.png",
    "category": "Identity",
    "difficulty": "Medium"
  }, 
    
  {
    "question": "What kind of tasks energize or drain Umutesa?",
    "answer": "Umutesa thrives on tasks that challenge her intellectually and creatively. She’s most energized when exploring something new—whether it’s a novel concept, a complex problem, or an unfamiliar tool. The excitement of discovery and growth fuels her motivation. On the flip side, she finds disorganization and poor communication draining. A lack of clarity or structure can disrupt her flow and diminish her enthusiasm.",
    "image_url": "https://specials-images.forbesimg.com/imageserve/61e73ae465e456a45d43ea88/Shot-of-office-staff-jumping/960x0.jpg?fit=scale",
    "category": "Work Style",
    "difficulty": "Medium"
  },
  {
    "question": "How does Umutesa collaborate best with others?",
    "answer": "Umutesa collaborates best in environments that value open communication, mutual respect, and shared goals. She enjoys working with people who bring diverse perspectives and believes that collaboration is strongest when everyone feels heard. She’s proactive in offering support, and thrives when there’s a balance between independence and teamwork. Clear roles, constructive feedback, and a spirit of curiosity make her an engaged and thoughtful teammate.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/1745785550879.jpeg",
    "category": "Collaboration",
    "difficulty": "Medium"
  },
  {
    "question": "Where does Umutesa want to grow?",
    "answer": "Umutesa sees growth as a lifelong journey. She believes there’s always room to learn—whether it’s mastering a new technical skill, deepening academic expertise, or building professional confidence. Right now, she’s focused on strengthening her voice in professional spaces, refining her communication, and expanding her impact through mentorship and leadership. For her, growth is about evolving with purpose and staying curious.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/1745785550879.jpeg",
    "category": "Personal Development",
    "difficulty": "Medium"
  },
  {
    "question": "What does Umutesa enjoy in nature?",
    "answer": "Nature is a source of peace and inspiration for Umutesa. She finds joy in quiet walks, the sound of birds, and the calming rhythm of natural landscapes. Whether it’s a forest trail or a mountain view, nature helps her recharge and reconnect with herself.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG-20230728-WA0016.jpg",
    "category": "Personal Interests",
    "difficulty": "Easy"
  },
  {
    "question": "Why does Umutesa love the beach?",
    "answer": "The beach is one of Umutesa’s happy places. She loves the sound of waves, the warmth of the sun, and the feeling of sand beneath her feet. It’s a space where she can relax, reflect, and feel free. Whether she’s swimming, walking, or simply watching the horizon, the beach brings her a sense of calm and joy.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG_20221116_201906_757.jpg",
    "category": "Personal Interests",
    "difficulty": "Easy"
  },
  {
    "question": "What does Umutesa enjoy socially?",
    "answer": "Umutesa is deeply social and values time spent with friends, family, and new acquaintances. She enjoys meaningful conversations, shared laughter, and the energy of being around others. Whether it’s a casual hangout or a community event, she finds connection and joy in social spaces.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG-20230702-WA0040.jpg",
    "category": "Social Life",
    "difficulty": "Easy"
  },
  {
    "question": "Why does Umutesa enjoy sunsets?",
    "answer": "Sunsets are a moment of reflection for Umutesa. She loves the colors, the quiet, and the symbolism of endings that lead to new beginnings. Watching the sun dip below the horizon reminds her to pause, appreciate beauty, and embrace transitions with grace.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG-20230705-WA0011.jpg",
    "category": "Personal Interests",
    "difficulty": "Easy"
  },
  {
    "question": "What sports does Umutesa enjoy?",
    "answer": "Umutesa enjoys staying active through sports, especially running. It helps her clear her mind and stay energized. She also occasionally plays golf, appreciating the focus and calm it requires. Sports are not just physical for her—they’re a way to stay balanced and motivated.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/20240209_150932.jpg",
    "category": "Lifestyle",
    "difficulty": "Easy"
  },
  {
    "question": "Why does Umutesa enjoy volunteering?",
    "answer": "Volunteering is a meaningful part of Umutesa’s life. She finds purpose in giving back and is always seeking new opportunities to serve her community. Whether it’s mentoring, organizing events, or supporting causes she cares about, volunteering allows her to connect with others and contribute to something bigger than herself.",
    "image_url": "https://raw.githubusercontent.com/umutesa/Codex/refs/heads/main/images/IMG-20230519-WA0009.jpg",
    "category": "Values",
    "difficulty": "Medium"
  }
  
]

# -- use a female if found --
def get_female_voice(engine):
    voices = engine.getProperty("voices")
    female_keywords = [
        "female", "zira", "susan", "samantha", "anna", "lucy", "lisa",
        "karen", "julie", "mary", "linda", "emily", "sarah", "clara",
        "amy", "allison", "heather", "kathy", "maria", "olivia",
        "julia", "eva", "natalie", "emma", "grace"
    ]
    for v in voices:
        name = v.name.lower()
        if any(k in name for k in female_keywords):
            return v.id
    return voices[0].id if voices else None

# -- read out the text ---
def play_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    try:
        voice_id = get_female_voice(engine)
        if voice_id:
            engine.setProperty("voice", voice_id)
        else:
            st.warning("No female voice found, using default voice.")

        # Save to temporary wav file instead of engine.say()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            filename = fp.name

        engine.save_to_file(text, filename)
        engine.runAndWait()
        engine.stop()

        # Play in Streamlit
        st.audio(filename, format="audio/wav")

    except Exception as e:
        st.warning(f"TTS error: {e}")


def validate_and_display_image(url, caption=""):
    if not url or str(url).strip().lower() in ['nan', '', 'none']:
        return False
    try:
        r = requests.get(url, timeout=7, stream=True)
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
            st.image(r.content, caption=caption)
            return True
        else:
            return False
    except Exception:
        return False

def get_fact_image(fact):
    img_url = fact.get('image_url', '')
    if img_url and str(img_url).strip():
        return img_url
    return fact.get('image_url',None)

def load_facts(files):
    facts = []
    for file in files:
        ext = file.name.split('.')[-1]
        file.seek(0)
        try:
            if ext == 'json':
                data_raw = file.read()
                if not data_raw.strip(): continue  # skip empty files
                try:
                    data = json.loads(data_raw)
                except Exception as e:
                    st.error(f"Error reading JSON: {file.name}: {e}")
                    continue
                if isinstance(data, list): facts.extend(data)
            elif ext == 'csv':
                try:
                    df = pd.read_csv(file)
                    for _, row in df.iterrows():
                        facts.append({
                            'question': str(row.get('question', '')),
                            'answer': str(row.get('answer', '')),
                            'image_url': str(row.get('image_url', '')),
                            'category': str(row.get('category', 'General')),
                            'difficulty': str(row.get('difficulty', 'Medium')),
                            'type': str(row.get('type', 'general'))
                        })
                except Exception as e:
                    st.error(f"Error reading CSV: {file.name}: {e}")
        except Exception as e:
            st.error(f"Error reading file: {file.name}: {e}")
    return facts

def get_best_facts(query, fact_database, top_n=2):
    from difflib import SequenceMatcher
    scored = []
    for fact in fact_database:
        score = SequenceMatcher(None, query.lower(), fact['question'].lower()).ratio()
        scored.append((score, fact))
    scored.sort(reverse=True)
    return [fact for score, fact in scored[:top_n] if score > 0.15]

def get_random_fun_fact(facts):
    if not facts: facts = SAMPLE_DATA
    return random.choice(facts)

def get_guess_item(facts):
    if not facts: facts = SAMPLE_DATA
    fact = random.choice(facts)
    correct = fact['answer']
    all_answers = [f['answer'] for f in facts if f['answer'] != correct]
    if not all_answers: all_answers = [SAMPLE_DATA[0]['answer']]
    options = random.sample(all_answers, min(3, len(all_answers))) + [correct]
    random.shuffle(options)
    return fact, options, correct

def process_rag_files(files, urls):
    docs = []
    for file in files:
        file_path = tempfile.mktemp()
        with open(file_path, "wb") as f:
            f.write(file.read())
        ext = file.name.split('.')[-1]
        try:
            if ext == "pdf":
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
            elif ext == "txt":
                loader = TextLoader(file_path)
                docs.extend(loader.load())
            elif ext == "csv":
                loader = CSVLoader(file_path)
                docs.extend(loader.load())
            elif ext == "json":
                loader = JSONLoader(file_path, jq_schema=".",text_content=False)
                docs.extend(loader.load())
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")

    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs.extend(loader.load())
        except Exception as e:
            st.error(f"Error loading from URL {url}: {e}")

    return docs

@st.cache_resource
def get_rag_chain(docs):
    if not docs: return None
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50, separators=["\n\n", "\n", ". ", " ", ""])
    split_docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
    db = FAISS.from_documents(split_docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 5})
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, dtype=torch.float32)
    hf_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=2048, temperature=0.7, do_sample=True, top_p=0.9, device=-1)
    def rag_chain(query):
        docs = retriever.get_relevant_documents(query)
        context = "\n".join([d.page_content for d in docs])
        result = hf_pipeline(f"{query}\n\nContext:\n{context}")
        return result[0]['generated_text']
    return rag_chain

# --- UI State ---
st.session_state.setdefault("last_answer", "")
st.session_state.setdefault("guess_fact", None)
st.session_state.setdefault("guess_options", [])
st.session_state.setdefault("guess_correct", "")
st.session_state.setdefault("guess_answered", False)
st.session_state.setdefault("last_story", "")
st.session_state.setdefault("fun_fact", "")

uploaded_files = st.file_uploader("Upload PDF, TXT, CSV, JSON", type=["pdf", "txt", "csv", "json"], accept_multiple_files=True)
url_input = st.text_area("OR enter URLs (one per line)", placeholder="https://en.wikipedia.org/wiki/AI\nhttps://example.com/cv.pdf")
url_list = [u.strip() for u in url_input.split('\n') if u.strip()]
rag_docs = process_rag_files(uploaded_files, url_list)
fact_files = [f for f in uploaded_files if f.name.endswith('.json') or f.name.endswith('.csv')]
if fact_files:
    fact_database = load_facts(fact_files)
else:
    fact_database = SAMPLE_DATA.copy()

# --- RAG Chain ---
rag_chain = get_rag_chain(rag_docs)

# --- Q&A ---
st.header("💬 Q&A (Dataset and RAG)")
question = st.text_input("Ask anything about Umutesa or your uploaded documents:")

if st.button("Get Answer"):
    # First, try RAG if available
    answer = None
    if rag_chain and question:
        try:
            answer = rag_chain(question)
        except Exception as e:
            st.warning(f"RAG Q&A failed: {e}. Trying dataset facts.")
    # Fallback to facts within datasets
    if not answer:
        best_facts = get_best_facts(question, fact_database, top_n=1)
        if best_facts:
            answer = best_facts[0]['answer']
            img_url = get_fact_image(best_facts[0])
            if img_url: st.image(img_url, caption=best_facts[0]['question'])
        else:
            answer = SAMPLE_DATA[0]['answer']
            st.image(SAMPLE_DATA[0]['image_url'], caption=SAMPLE_DATA[0]['question'])
    st.markdown(f"**Answer:** {answer}")
    st.session_state['last_answer'] = answer

if st.session_state['last_answer']:
    if st.button("🔊 Listen "):
        play_text(st.session_state['last_answer'])

# --- Story by category ---
st.header("📚 Story by Category")
cats = sorted(set(f.get('category', 'General') for f in fact_database))
cat = st.selectbox("Pick a category", cats)
if st.button("Generate Story"):
    facts = [f for f in fact_database if f.get('category') == cat]
    if facts:
        story = " ".join([f['answer'] for f in facts])
        st.markdown(f"**Story:** {story}")
        for f in facts:
            img_url = get_fact_image(f)
            if img_url: st.image(img_url, caption=f['question'])
        st.session_state['last_story'] = story
    else:
        st.info("No facts for that category, here's a fallback image:")
        st.image(get_fact_image({'category': cat}), caption=cat)
        st.session_state['last_story'] = ""
if st.session_state.get('last_story'):
    if st.button("🔊 Listen to Story "):
        play_text(st.session_state['last_story'])

# --- Fun Fact ---
st.header("🎉 Fun Fact")
if st.button("Show Fun Fact"):
    fun_fact = get_random_fun_fact(fact_database)
    st.session_state['fun_fact'] = f"{fun_fact['question']} {fun_fact['answer']}"
    st.markdown(f"**Fun Fact:** {st.session_state['fun_fact']}")
if st.session_state.get('fun_fact'):
    if st.button("🔊 Listen to Fun Fact "):
        play_text(st.session_state['fun_fact'])

# --- Guess Game ---
st.header("🎲 Guess Game")
if st.button("New Guess"):
    fact, options, correct = get_guess_item(fact_database)
    st.session_state['guess_fact'] = fact
    st.session_state['guess_options'] = options
    st.session_state['guess_correct'] = correct
    st.session_state['guess_answered'] = False

if st.session_state.get('guess_fact'):
    st.markdown(f"**Question:** {st.session_state['guess_fact']['question']}")
    for option in st.session_state['guess_options']:
        if st.button(f"Guess: {option}"):
            st.session_state['guess_answered'] = True
            if option == st.session_state['guess_correct']:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! The correct answer: {st.session_state['guess_correct']}")
            st.info(f"Explanation: {st.session_state['guess_fact']['answer']}")
            img_url = get_fact_image(st.session_state['guess_fact'])
            if img_url:
                st.image(img_url, caption=st.session_state['guess_fact']['question'])
   

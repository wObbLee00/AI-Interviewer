#IN DEVELOPEMENT

# 🤖 AI Interviewer Bot – Your Personal Job Interview Simulator

### 🎯 Project Overview
The **AI Interviewer Bot** is an intelligent, voice-enabled interview simulation system that helps users **practice job interviews** for any role, with **real-time feedback, scoring, and adaptive questioning**.  

Users can upload their **CV/resume**, select a **desired job role**, and the system will:
- 📑 Read and understand their CV.
- 🌐 Search and learn about the target job role and responsibilities.
- 🤔 Prepare a personalized set of **technical and behavioral interview questions**.
- 🎙️ Conduct the interview (via text or voice) — with adaptive follow-up questions.
- 🧠 Evaluate their responses based on **clarity, accuracy, confidence, and delivery**.
- 📊 Generate a detailed **feedback report** with scores, strengths, and improvement tips.

> This project brings together modern AI technologies — LLMs, RAG, Whisper ASR, and multimodal analysis — to simulate realistic interviews and improve communication and confidence for job seekers.

---

## 🚀 Key Features

### 🧠 Intelligent Interview Planning
- Upload your CV and choose a desired role (e.g., *Data Analyst*, *Software Engineer*, *Product Manager*).  
- The system automatically scans your resume and job role info to prepare a custom interview plan with relevant topics.

### 🗣️ Adaptive Interview Dialogue
- AI interviewer conducts **interactive, context-aware interviews**.
- Asks **counter-questions** when answers are vague or off-topic.
- Option to switch between **voice and text** modes.

### 🎧 Speech and Confidence Analysis
- Voice captured via **microphone** (Web Audio API) and analyzed for:
  - Speech rate  
  - Pauses and hesitations  
  - Tone consistency  
- Optional **facial engagement tracking** (MediaPipe) for attentiveness feedback.

### 📊 Performance Scoring & Analytics
- Multi-dimensional rubric grading:
  - ✅ Content Accuracy  
  - 🎯 CV Alignment  
  - 💬 Communication  
  - 🔍 Reasoning  
  - 💡 Confidence & Delivery  
- Generates a **beautiful radar chart** and a **PDF report** with scores, quotes, and feedback.

### 🌐 Real-World Use Cases
- Job seekers preparing for interviews  
- HR teams evaluating candidates’ soft skills  
- Universities or bootcamps helping students prepare for technical interviews  
- AI-driven communication training tools  

---

## 🧩 System Architecture
User (Web UI)
↓
Frontend (React + Tailwind)
↓
FastAPI Backend (Python)
↓
┌────────────────────────────┐
│ AI Engine (LLM + LangChain)│
│ - CV Parser (spaCy, PyMuPDF) │
│ - Role Knowledge (RAG + ChromaDB) │
│ - Question Planner + Adaptive Dialogue │
└────────────────────────────┘
↓
Evaluation Layer

Whisper (Speech-to-Text)

TTS (ElevenLabs / Edge-TTS)

librosa (Audio analysis)

MediaPipe (Facial signals)
↓
Results & Reports (Postgres + Chart.js)

---

## ⚙️ Tech Stack

### 🧠 **Core AI Components**
| Component | Technology |
|------------|-------------|
| LLM & RAG | OpenAI GPT / LangChain + ChromaDB |
| CV Parsing | PyMuPDF, pdfminer.six, spaCy |
| Embeddings | OpenAI / SentenceTransformers |
| Prompt Orchestration | LangChain Structured Chains |
| Evaluation | Rule-based + LLM JSON grading |

### 🧩 **Backend**
- **FastAPI** – async REST API + WebSocket streaming  
- **Pydantic** – schema validation  
- **PostgreSQL (Supabase / Railway)** – structured data  
- **Redis** – session memory + rate limiting  

### 💻 **Frontend**
- **React (Vite)** – SPA interface  
- **TailwindCSS + shadcn/ui** – clean, modern UI  
- **Chart.js** – radar & trend visualization  
- **Web Audio API / MediaPipe** – mic & webcam capture  

### ☁️ **Infrastructure**
- **Docker + Docker Compose** – containerized dev environment  
- **Vercel** – frontend hosting  
- **Railway / Render** – backend hosting  
- **GitHub Actions** – CI/CD pipeline  
- **Sentry** – error tracking & logging  

---

## 🧩 Core Modules

| Module | Description |
|--------|-------------|
| **1. CV Analyzer** | Extracts structured data (skills, projects, achievements) from uploaded resumes. |
| **2. Role Knowledge RAG** | Searches for the latest job descriptions and role expectations; stores them as embeddings. |
| **3. Interview Orchestrator** | Generates dynamic questions, handles counter-questions, and maintains interview flow. |
| **4. Scoring Engine** | Uses hybrid rule-based + LLM grading to assess answers across multiple dimensions. |
| **5. Feedback Generator** | Produces a visual report with charts, strengths, weaknesses, and suggested improvements. |

---

## 🧮 Evaluation Rubric

| Criteria | Description | Weight |
|-----------|--------------|--------|
| **Content Accuracy** | Technical correctness and relevance | 30% |
| **CV Alignment** | Uses real experiences from CV | 20% |
| **Reasoning & Structure** | Logical explanation and problem-solving clarity | 20% |
| **Communication** | Clear, fluent, and professional tone | 15% |
| **Confidence & Delivery** | Speech clarity, pace, tone consistency | 15% |

---

## 🎥 Demo Flow

1. **Upload your CV** (PDF/DOCX)  
2. **Select your target job role** (e.g., “Junior Data Analyst”)  
3. **Preparation Phase (1–2 mins)** — AI reads your CV + gathers job info  
4. **Interview Starts 🎤**  
   - “Tell me about yourself.”  
   - “What challenges did you face in your last project?”  
   - Adaptive follow-ups based on your answers  
5. **Live Evaluation**  
   - Voice analysis, keyword coverage, reasoning checks  
6. **Final Feedback Report**  
   - Score breakdown + improvement tips + PDF export  

---

## 📊 Output Example

- 🎯 **Overall Score:** 78%  
- 💬 **Strengths:** Clear communication, good reasoning examples  
- ⚠️ **Improvements:** More technical depth in answers, less hesitation  
- 📄 **Report:** Downloadable PDF with radar chart visualization

---

## 🛠️ Installation & Setup

```bash
# 1️⃣ Clone the repo
git clone https://github.com/your-username/ai-interviewer-bot.git
cd ai-interviewer-bot

# 2️⃣ Backend setup
cd backend
pip install -r requirements.txt

# 3️⃣ Frontend setup
cd ../frontend
npm install
npm run dev

# 4️⃣ Run backend (FastAPI)
uvicorn main:app --reload

# 5️⃣ Visit
http://localhost:5173

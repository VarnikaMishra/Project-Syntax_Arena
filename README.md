# Project-Syntax_Arena
Its a DSA Questions Arena where you can practice and compete in coding with your friends and track your code efficiency and timing just like a video game.
# 🏟️ Syntax Arena: AI-Powered Coding Platform

**Syntax Arena** is a full-stack, automated coding challenge platform. It leverages **Gemini 3 Flash** to dynamically generate algorithmic challenges, providing an infinite stream of fresh content. The system features a custom-built judging engine that executes and validates Python code in real-time.

---

## 🚀 Why This Project is "High-End" & Scalable

### 1. Dynamic Content Pipeline (LLM-as-a-Service)
Instead of relying on a static, manual database of questions, Syntax Arena uses GenAI to generate unique challenges daily.
* **Zero Content Stagnation:** The platform never runs out of fresh problems.
* **Structured AI Output:** It utilizes strict JSON schema prompting to pipe LLM data directly into a relational database without manual intervention.

### 2. Custom Judge Engine
The project implements a **Code Execution Engine** using Python’s `subprocess` module.
* **Security & Isolation:** It manages temporary file lifecycles to ensure user code is executed and cleaned up immediately after judging.
* **Standard I/O Testing:** It simulates a real competitive programming environment by piping `stdin` and capturing `stdout` to validate logic.

### 3. Scalable Architecture
* **FastAPI Backend:** Built for high performance, low latency, and asynchronous request handling.
* **SQLite Persistence:** A lightweight but robust layer for challenge history, user progress, and XP leaderboards.

---

## 🛠️ Prerequisites
* **Python 3.9+**
* A **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/))

---

## 📥 Environment Configuration & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-link>
cd Syntax_Arena

### 2. Virtual Environment Setup
```bash
It is highly recommended to use a virtual environment to keep your system clean:

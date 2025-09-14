🇮🇳 Indian History Quiz (1900–1947)






A lightweight, interactive Streamlit quiz app designed to test your knowledge of Indian History (1900–1947).
Supports multiple question types, scoring logic, explanations, and a persistent leaderboard.

📸 Screenshot
<img src="screenshot.png" alt="App Screenshot" width="600"/>

Replace screenshot.png with your actual screenshot.

🚀 Features (MVP)

📝 Question Types: Multiple-choice, True/False, Fill-in-the-blank, Matching

⏱️ Scoring: Base points + time bonus + streak bonus (as per PRD)

📊 Leaderboard: Stores top scores in leaderboard.json (persistent)

📚 Feedback: Correct/Incorrect message with explanation per question

🏆 Gamification: Progress bar, streak tracking, achievements (planned)

🔄 Quiz Modes: Fixed (10 questions), Timed (5 minutes)

📂 Project Structure
streamlit-india-quiz/
├── app.py                 # Main Streamlit app
├── data/
│   ├── questions.json     # Static quiz question bank (~50 Q&A)
│   └── leaderboard.json   # Auto-created at runtime (persistent scores)
├── README.md              # Documentation
└── requirements.txt       # Python dependencies

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/streamlit-india-quiz.git
cd streamlit-india-quiz

2. Create and activate a virtual environment
macOS/Linux
python3 -m venv venv
source venv/bin/activate

Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py


You’ll see something like:

Local URL: http://localhost:8501
Network URL: http://192.168.0.102:8501


Open your browser at the Local URL.

📊 Data
questions.json

Contains curated quiz content (~50 questions) in schema:

{
  "id": "q0001",
  "year": 1919,
  "topic": "Jallianwala Bagh",
  "type": "mcq",
  "difficulty": "medium",
  "question": "On which date did the Jallianwala Bagh massacre take place?",
  "options": ["13 April 1919", "15 August 1919", "30 January 1919", "26 January 1920"],
  "answer": "13 April 1919",
  "explanation": "The Jallianwala Bagh massacre occurred on 13 April 1919, when British troops fired on a peaceful gathering in Amritsar."
}

leaderboard.json

Auto-generated file that persists leaderboard entries:

[
  {
    "username": "Player1",
    "mode": "fixed",
    "score": 120,
    "correct_count": 8,
    "questions_count": 10,
    "duration_seconds": 90,
    "created_at": "2025-09-14T10:25:00Z"
  }
]

🧑‍🤝‍🧑 User Personas

🎓 High-school students — revision tool for history exams

📖 History enthusiasts — casual play and competition

👩‍🏫 Teachers/quizmasters — classroom quiz resource

🛣️ Roadmap

 MVP: Fixed quiz, scoring, leaderboard

 Add badges and achievements (streak master, high scorer)

 Multiplayer challenge codes (friends leaderboard)

 Avatar selection and gamification polish

 Deployment on Streamlit Cloud / Hugging Face Spaces

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss improvements.

📜 License

This project is licensed under the MIT License — see the LICENSE
 file for details.

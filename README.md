# Anime Trivia Showdown

Anime Trivia Showdown is a web-based quiz game built with Flask, allowing users to test their knowledge of various anime series through a series of engaging questions. The application provides real-time feedback and scoring to enhance the user experience.

## 🚀 Features
- **Multiple Categories**: Choose from different anime series or genres.
- **Real-Time Feedback**: Instant validation of answers with scoring.
- **User Authentication**: Secure login and registration system to track user progress.
- **Responsive Design**: Optimized for various devices, ensuring a seamless experience on desktops, tablets, and mobiles.
- **Leaderboard**: Track high scores and compare performance with other players.

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite (default) or any preferred relational database

## 📂 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sakethpragallapati/Anime-Trivia-Showdown.git
   cd Anime-Trivia-Showdown
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install Flask and other required dependencies:
   ```bash
   pip install flask flask_sqlalchemy flask_migrate flask_login
   ```
   If additional dependencies are required, create a `requirements.txt` file:
   ```bash
   pip freeze > requirements.txt
   ```

4. **Set Up the Flask Application**:
   Ensure Flask can locate the application by setting the environment variable:
   ```bash
   export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
   ```

5. **Set Up the Database**:
   - Initialize the SQLite database:
     ```bash
     flask db init
     flask db migrate -m "Initial migration."
     flask db upgrade
     ```
   - Alternatively, configure your preferred database in `config.py`.

6. **Run the Application**:
   ```bash
   flask run
   ```
   Access the app at `http://127.0.0.1:5000/`.

## 🎮 Usage
- **Registration**: Create a new account to start playing.
- **Login**: Access your account to track your quiz history and scores.
- **Select Quiz**: Choose from available anime categories.
- **Answer Questions**: Participate in the quiz and receive immediate feedback.
- **View Scores**: Check your scores and compare with previous attempts.
- **Leaderboard**: See how your scores rank against other players.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## 💡 Acknowledgements
- Inspired by the love for anime and the desire to create an engaging learning platform.
- Thanks to all contributors and users for their support.

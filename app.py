from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a strong random secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('menu'))  # Redirect to menu page after login
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please choose another.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/menupage', methods=["GET", "POST"])
def menu():
    if 'user_id' not in session:  # Ensure the user is logged in
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        submit_value = request.form.get('submit')  # Get the value of the submitted button

        if submit_value == "ExploreAction-1":
            return redirect(url_for('anime', action='action'))  # Redirect to action page
        elif submit_value == "ExploreAction-2":
            return redirect(url_for('anime', action='shonen'))  # Redirect to shonen page
        elif submit_value == "ExploreAction-3":
            return redirect(url_for('anime', action='isakai'))  # Redirect to isekai page

    return render_template("menupage.html")  # Render the menu page on GET


@app.route('/anime', methods=["GET"])
def anime():
    action = request.args.get('action')
    
    if action == 'action':
        return render_template('action.html')  # Render action.html
    elif action == 'shonen':
        return render_template('shonen.html')  # Render shonen.html
    elif action == 'isakai':
        return render_template('isakai.html')  # Render isakai.html
    else:
        return "Anime type not found", 404  # Handle unknown actions

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    anime = request.args.get('anime')

    # Define questions for each anime
    questions = {
        "attack_on_titan": [
            {"question": "Who is the main protagonist of Attack on Titan?", "options": ["Eren Yeager", "Armin Arlert", "Mikasa Ackerman", "Levi Ackerman"], "answer": "Eren Yeager"},
            {"question": "What are the giant humanoid creatures called?", "options": ["Titans", "Ogres", "Giants", "Colossi"], "answer": "Titans"},
            {"question": "Which faction does Eren join?", "options": ["Survey Corps", "Military Police", "Garrison", "Titans"], "answer": "Survey Corps"},
            {"question": "What is the main objective of the Survey Corps?", "options": ["Defend humanity", "Study Titans", "Kill Titans", "Find Eren"], "answer": "Find Eren"},
            {"question": "What is the name of the wall protecting humanity?", "options": ["Wall Rose", "Wall Maria", "Wall Sina", "Wall Eren"], "answer": "Wall Maria"},
        ],
        "demon_slayer": [
            {"question": "What is the name of the main character?", "options": ["Tanjiro Kamado", "Zenitsu Agatsuma", "Inosuke Hashibira", "Giyu Tomioka"], "answer": "Tanjiro Kamado"},
            {"question": "What demon does Tanjiro seek to cure his sister Nezuko?", "options": ["Muzan Kibutsuji", "Akaza", "Rui", "Kibutsuji"], "answer": "Muzan Kibutsuji"},
            {"question": "What is the main weapon used by demon slayers?", "options": ["Ninjato", "Katana", "Bokken", "Dao"], "answer": "Katana"},
            {"question": "What is the name of Tanjiro's sister?", "options": ["Nezuko Kamado", "Mitsuri Kanroji", "Shinobu Kocho", "Kanao Tsuyuri"], "answer": "Nezuko Kamado"},
            {"question": "What technique does Tanjiro use to enhance his abilities?", "options": ["Breathing Techniques", "Demon Arts", "Sword Techniques", "Haki"], "answer": "Breathing Techniques"},
        ],
        "my_hero_academia": [
            {"question": "What is the name of the main protagonist?", "options": ["Izuku Midoriya", "Katsuki Bakugo", "All Might", "Shoto Todoroki"], "answer": "Izuku Midoriya"},
            {"question": "What is All Might's real name?", "options": ["Toshinori Yagi", "Shota Aizawa", "Hizashi Yamada", "Hizashi Hōgetsu"], "answer": "Toshinori Yagi"},
            {"question": "Which school do the main characters attend?", "options": ["U.A. High School", "Ketsubutsu Academy", "Shiketsu High School", "Shiketsu Academy"], "answer": "U.A. High School"},
            {"question": "What is Midoriya's Quirk?", "options": ["One For All", "Explosive", "Fire", "Ice"], "answer": "One For All"},
            {"question": "Who is the principal of U.A. High School?", "options": ["Nezu", "Aizawa", "Hizashi", "All Might"], "answer": "Nezu"},
        ],
        "one_piece": [
            {"question": "Who is the main character of One Piece?", "options": ["Monkey D. Luffy", "Roronoa Zoro", "Nami", "Sanji"], "answer": "Monkey D. Luffy"},
            {"question": "What is Luffy searching for?", "options": ["One Piece", "Treasure", "Pirate King", "Adventure"], "answer": "One Piece"},
            {"question": "What is Luffy's crew called?", "options": ["Straw Hat Pirates", "Red-Haired Pirates", "Whitebeard Pirates", "Blackbeard Pirates"], "answer": "Straw Hat Pirates"},
            {"question": "What is Luffy's ability?", "options": ["Gomu Gomu no Mi", "Mera Mera no Mi", "Suna Suna no Mi", "Yami Yami no Mi"], "answer": "Gomu Gomu no Mi"},
            {"question": "Who is Luffy's first mate?", "options": ["Zoro", "Sanji", "Nami", "Usopp"], "answer": "Zoro"},
        ],
        "naruto": [
            {"question": "What is Naruto's dream?", "options": ["To become Hokage", "To find Sasuke", "To become a ninja", "To protect his village"], "answer": "To become Hokage"},
            {"question": "What is the name of Naruto's village?", "options": ["Konoha", "Suna", "Kiri", "Kumo"], "answer": "Konoha"},
            {"question": "Who is Naruto's main rival?", "options": ["Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake", "Orochimaru"], "answer": "Sasuke Uchiha"},
            {"question": "What demon fox is sealed inside Naruto?", "options": ["Kurama", "Shukaku", "Matatabi", "Isobu"], "answer": "Kurama"},
            {"question": "What is the name of Naruto's teacher?", "options": ["Kakashi Hatake", "Jiraiya", "Minato Namikaze", "Tobirama Senju"], "answer": "Kakashi Hatake"},
        ],
        "bleach": [
            {"question": "What is the main character's name?", "options": ["Ichigo Kurosaki", "Renji Abarai", "Rukia Kuchiki", "Uryu Ishida"], "answer": "Ichigo Kurosaki"},
            {"question": "What is Ichigo's role?", "options": ["Soul Reaper", "Hollow", "Quincy", "Human"], "answer": "Soul Reaper"},
            {"question": "What is the name of Ichigo's sword?", "options": ["Zangetsu", "Tensa Zangetsu", "Muramasa", "Shikai"], "answer": "Zangetsu"},
            {"question": "Who is the main antagonist of the Soul Society Arc?", "options": ["Aizen", "Gin", "Urahara", "Yamamoto"], "answer": "Aizen"},
            {"question": "What is Rukia's last name?", "options": ["Kuchiki", "Abarai", "Urahara", "Ishida"], "answer": "Kuchiki"},
        ],
        "solo_leveling": [
            {"question": "What is the name of the main character?", "options": ["Sung Jin-Woo", "Cha Hae-In", "Go Gun-Hee", "Kim Sung-Il"], "answer": "Sung Jin-Woo"},
            {"question": "What is the term used for hunters?", "options": ["E-Rank", "D-Rank", "C-Rank", "S-Rank"], "answer": "E-Rank"},
            {"question": "What is Jin-Woo's special ability?", "options": ["Shadow Monarch", "S-Rank Hunter", "Dual Ability", "Rebirth"], "answer": "Shadow Monarch"},
            {"question": "Who is Jin-Woo's mentor?", "options": ["Go Gun-Hee", "Cha Hae-In", "Thomas Andre", "Giant"], "answer": "Go Gun-Hee"},
            {"question": "What is the name of the system Jin-Woo receives?", "options": ["System", "Game", "Leveling", "Quest"], "answer": "System"},
        ],
        "overlord": [
            {"question": "What is the main character's name?", "options": ["Ainz Ooal Gown", "Shalltear Bloodfallen", "Albedo", "Demiurge"], "answer": "Ainz Ooal Gown"},
            {"question": "What game does Ainz come from?", "options": ["Yggdrasil", "World of Warcraft", "Final Fantasy", "Sword Art Online"], "answer": "Yggdrasil"},
            {"question": "What is the name of Ainz's guild?", "options": ["Ainz Ooal Gown", "Dark Warrior", "Giant Of the East", "Great Tomb of Nazarick"], "answer": "Ainz Ooal Gown"},
            {"question": "Who is Ainz's first guardian?", "options": ["Shalltear", "Albedo", "Demiurge", "Cocytus"], "answer": "Shalltear"},
            {"question": "What is Ainz's goal in the new world?", "options": ["To become the strongest", "To find his guild members", "To conquer the world", "To revive Yggdrasil"], "answer": "To find his guild members"},
        ],
        "sword_art_online": [
            {"question": "What is the main character's name?", "options": ["Kirito", "Asuna", "Klein", "Shino"], "answer": "Kirito"},
            {"question": "What game do they get trapped in?", "options": ["SAO", "ALO", "GGO", "VRMMO"], "answer": "SAO"},
            {"question": "What is Kirito's special ability?", "options": ["Dual Wielding", "Sword Skills", "Speed", "Strength"], "answer": "Dual Wielding"},
            {"question": "What is the name of Asuna's character?", "options": ["Sinon", "Leafa", "Lizbeth", "Asuna"], "answer": "Asuna"},
            {"question": "What is the goal of the players in SAO?", "options": ["Clear the game", "Level up", "Kill the boss", "Survive"], "answer": "Clear the game"},
        ],
    }
    if 'score' not in session:
        session['score'] = 0

    selected_questions = questions.get(anime, [])
    total_questions = len(selected_questions)

    if total_questions == 0:
        return render_template('quiz.html', questions=[], score=0, anime=anime)

    if request.method == "POST":
        current_question_index = int(request.form.get('current_question', 0))
        answer = request.form.get('answer')

        # Increment score if the answer is correct
        if answer == selected_questions[current_question_index]["answer"]:
            session['score'] += 1

        current_question_index += 1

        if current_question_index >= total_questions:
            final_score = session['score']
            session.pop('score', None)  # Clear the score from session
            return redirect(url_for('quiz_completed', score=final_score, total_questions=total_questions, anime=anime))  # Pass anime

        
        return render_template('quiz.html', 
                               questions=selected_questions, 
                               current_question_index=current_question_index,
                               total_questions=total_questions,
                               anime=anime)

    return render_template('quiz.html', 
                           questions=selected_questions, 
                           current_question_index=0,
                           total_questions=total_questions,
                           anime=anime)

@app.route('/quiz_completed')
def quiz_completed():
    score = request.args.get('score', default=0, type=int)
    total_questions = request.args.get('total_questions', default=0, type=int)
    anime = request.args.get('anime', default='')  # Get the anime from the request args
    return render_template('quiz_completed.html', score=score, total_questions=total_questions, anime=anime)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
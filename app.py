import json  # Import the JSON module to handle JSON data
from flask import Flask, request, jsonify , render_template , redirect , url_for , session
from extensions import db  # Import the SQLAlchemy instance
from datetime import datetime  # Import datetime for handling date and time

app = Flask(__name__) # Initialize the Flask application

app.config['SECRET_KEY'] = '100' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@LAPTOP-59PVKG7G/Purescalp?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes' # Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

db.init_app(app)  # Initialize the SQLAlchemy instance with the Flask app

with open('questions.json', 'r') as f:
    questions = json.load(f)  # Load the quiz questions from a JSON file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_image():
    return render_template('uploadimage.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')



from models import Patient  # Import the Patient model

@app.route('/patientregistration', methods=['GET', 'POST'])
def patient_registration():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']

        new_patient = Patient(Name=name, Email=email, Age=age, Gender=gender)
        try:
            db.session.add(new_patient)
            db.session.commit()
            session['patient_id'] = new_patient.PatientID  # Store patient ID in session
            return redirect(url_for('questionnaire'))  # Redirect to questionnaire page after successful registration
        except Exception as e:
            db.session.rollback() # Rollback the session in case of error
            return jsonify({"error": str(e)}), 400

    return render_template('patientregistration.html')




from models import Doctor   # Import the Doctor model

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        specialization = request.form['specialization']

        new_doctor = Doctor(Name=name, Email=email, Password=password, Specialization=specialization)
        
        try:
            db.session.add(new_doctor)
            db.session.commit()
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        
        except Exception as e:
            db.session.rollback() # Rollback the session in case of error
            return jsonify({"error": str(e)}), 400

    return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        doctor = Doctor.query.filter_by(Email=email, Password=password).first() # Check if the doctor exists with the provided credentials

        if doctor:
            return redirect(url_for('index'))
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return render_template('login.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')



from models import Patient, Questionnaire

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    # Get the patient's ID from the session
    patient_id = session.get('patient_id')
    if not patient_id:
        return redirect(url_for('patient_registration'))  # Redirect to registration if no patient_id

    # Retrieve the current question ID from the session
    current_question_id = session.get('current_question_id', 1)

    # Ensure the current question ID is valid
    current_question = next((q for q in questions['questions'] if q['question_id'] == current_question_id), None)
    
    if not current_question:
        # If there's no valid question, start from the first question
        session['current_question_id'] = 1
        return redirect(url_for('questionnaire'))  # Redirect to the first question

    if request.method == 'POST':
        # Store the patient's answer
        answer = request.form.get(f'question{current_question_id}')  # Get the answer to the current question
        question_text = current_question['question']  # Store the question text
        completion_date = datetime.now()  # Store the current date/time
        patientID = session['patient_id']  # Ensure patient_id is in session
        
        if answer:
            # Create a new Questionnaire object based on the user's answer
            new_answer = Questionnaire(
                PatientID=patientID,  # Use the patient ID from the session
                questions=question_text,  # Store the question text
                answers=answer,  # Store the user's answer
                completionDate=completion_date  # Store the current date/time
            )

            db.session.add(new_answer)  # Add the new answer to the session
            db.session.commit()  # Commit to the database

        # Determine the next question based on the answer
        next_question_id = current_question['next_question'].get(answer)

        # If there's a next question, store it in session and redirect to it
        if next_question_id:
            session['current_question_id'] = next_question_id
            return redirect(url_for('questionnaire'))

        # If no next question, find the next root question
        else:
            # Find the next root question
            next_root_question = next((q for q in questions['questions'] if q['question_id'] > current_question_id and 'next_question' not in q), None)
            
            if next_root_question:
                session['current_question_id'] = next_root_question['question_id']
                return redirect(url_for('questionnaire'))
            
        return redirect(url_for('index'))  # Redirect to index if no next question is found

    # If it's a GET request, render the current question
    return render_template('questionnaire.html', question=current_question)

if __name__ == '__main__':
    app.run(debug=True)
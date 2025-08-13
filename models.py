from extensions import db  # Import the SQLAlchemy instance
from datetime import datetime  # Import datetime for handling date and time

class Doctor(db.Model):
    __tablename__ = 'Doctor'
     
    DoctorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(10), nullable=False)
    Specialization = db.Column(db.String(100), nullable=True)

    def __repr__(self): # String representation of the Doctor object
        return f"<Doctor {self.Name}>"
    
class Patient(db.Model):
    __tablename__ = 'Patient'
    
    PatientID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Age = db.Column(db.Integer, nullable=True)
    Gender = db.Column(db.String(10), nullable=True)

    def __repr__(self):  # String representation of the Patient object
        return f"<Patient {self.Name}>"
    

class Questionnaire(db.Model):
    __tablename__ = 'Questionnaire'
    
    QuestionnaireID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'), nullable=False)  # Foreign key to Patient model
    questions = db.Column(db.String(255), nullable=False)  # Change to 'questions' to match your database column
    answers = db.Column(db.String(255), nullable=True)  # Change to 'answers' to match your database column
    completionDate = db.Column(db.DateTime, default=datetime.now())  # Change to 'completionDate' to match your database column

    patient = db.relationship('Patient', backref=db.backref('questionnaires', lazy=True))  # Relationship to Patient model

    def __repr__(self):
        return f"<Questionnaire {self.questions}>"


class Marks(db.Model):
    __tablename__ = 'Marks'
    
    marksId = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'), nullable=False)  # Foreign key to Patient model
    marks = db.Column(db.Integer, nullable=False)

    patient = db.relationship('Patient', backref=db.backref('marks', lazy=True))  # Relationship to Patient model

    def __repr__(self):
        return f"<Marks PatientID: {self.patientId}, Marks: {self.marks}>"
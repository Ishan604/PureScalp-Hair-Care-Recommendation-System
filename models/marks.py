from extensions import db

class Marks(db.Model):
    __tablename__ = 'Marks'
    
    marksId = db.Column(db.Integer, primary_key=True)
    patientId = db.Column(db.Integer, db.ForeignKey('Patient.PatientID'), nullable=False)  # Foreign key to Patient model
    marks = db.Column(db.Integer, nullable=False)

    patient = db.relationship('Patient', backref=db.backref('marks', lazy=True))  # Relationship to Patient model

    def __repr__(self):
        return f"<Marks PatientID: {self.patientId}, Marks: {self.marks}>"

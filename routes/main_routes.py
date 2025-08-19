from flask import Blueprint, render_template

# Create blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload')
def upload_image():
    return render_template('uploadimage.html')

@main_bp.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@main_bp.route('/quiz')
def quiz():
    return render_template('quiz.html')

@main_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@main_bp.route('/haircare')
def haircare():
    return render_template('haircare.html')

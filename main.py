from flask import Flask, render_template, request, redirect, url_for, flash, session
from bing_image_downloader import downloader
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ai_ml_engine import ai_ml_engine
from encryption_utils import encrypt_field, decrypt_field, encrypt_user_sensitive_data, decrypt_user_sensitive_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobportal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Job Seeker Model
class JobSeeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(500), nullable=False)  # Encrypted phone
    gender = db.Column(db.String(500), nullable=False)  # Encrypted gender
    age = db.Column(db.String(500), nullable=False)  # Encrypted age
    password = db.Column(db.String(200), nullable=False)
    # Add more fields as needed

# Recruiter Model
class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    business_pancard = db.Column(db.String(500))  # Encrypted business pancard
    company_name = db.Column(db.String(120))
    company_address = db.Column(db.String(500))  # Encrypted company address
    password = db.Column(db.String(200), nullable=False)
    # Add more fields as needed

# Job Posting Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100))
    salary_min = db.Column(db.Integer)  # Salary in rupees
    salary_max = db.Column(db.Integer)  # Salary in rupees
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    skills = db.Column(db.Text)  # Comma-separated skills
    posted_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

users = {
    "jobseeker@gmail.com": {"password": "password123", "type": "jobSeeker"},
    "recruiter@gmail.com": {"password": "recruiter123", "type": "recruiter"}
}

trusted_domains = ["companydomain.com", "officialdomain.com"]

@app.route('/')
def index():
    return redirect(url_for('select_signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_type = request.form.get('userType')
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        business_pancard = request.form['businessPancard']
        live_picture = request.files['livePicture']
        company_name = request.form.get('companyName', None)
        company_address = request.form.get('companyAddress', None)
        employee_types = request.form.get('employeeTypes', None)
        field_of_interest = request.form.get('fieldOfInterest', None)
        max_salary = request.form.get('maxSalary', None)
        field_of_employees_need = request.form.get('fieldOfEmployeesNeed', None)

        if user_type == 'recruiter':
            email_domain = email.split('@')[1]
            if email_domain not in trusted_domains:
                flash("Please use an official company email address.", "error")
                return redirect(url_for('signup'))

            live_picture.save(f'static/uploads/{live_picture.filename}')

        users[email] = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "gender": gender,
            "age": age,
            "business_pancard": business_pancard,
            "company_name": company_name,
            "company_address": company_address,
            "employee_types": employee_types,
            "field_of_interest": field_of_interest,
            "max_salary": max_salary,
            "field_of_employees_need": field_of_employees_need,
            "password": request.form['password'],
            "type": user_type
        }

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['user_type'] = user['type']
            return redirect(url_for('home'))
        flash("Invalid email or password.", "error")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    user_email = session['user']
    user_type = session['user_type']
    user_info = None
    if user_type == 'jobSeeker':
        user_info = JobSeeker.query.filter_by(email=user_email).first()
        # Decrypt sensitive data for display
        if user_info:
            user_info.phone = decrypt_field(user_info.phone)
            user_info.gender = decrypt_field(user_info.gender)
            user_info.age = decrypt_field(user_info.age)
    elif user_type == 'recruiter':
        user_info = Recruiter.query.filter_by(email=user_email).first()
        # Decrypt sensitive data for display
        if user_info:
            user_info.business_pancard = decrypt_field(user_info.business_pancard)
            user_info.company_address = decrypt_field(user_info.company_address)
    
    # Fetch recent job postings
    jobs = Job.query.filter_by(is_active=True).order_by(Job.posted_date.desc()).limit(10).all()
    
    return render_template('home.html', user=user_info, user_type=user_type, jobs=jobs)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/select-signup')
def select_signup():
    return render_template('select_signup.html')

@app.route('/jobseeker-signup', methods=['GET', 'POST'])
def job_seeker_signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        print(f"[DEBUG] JobSeeker signup attempt: email={email}, first_name={first_name}")
        print(f"[DEBUG] Password length: {len(password)}, Confirm password length: {len(confirm_password)}")

        if password != confirm_password:
            print("[DEBUG] Passwords do not match!")
            flash("Passwords do not match.", "error")
            return redirect(url_for('job_seeker_signup'))

        print("[DEBUG] Password check passed")

        # Check if email already exists
        existing_user = JobSeeker.query.filter_by(email=email).first()
        print(f"[DEBUG] Existing user check: {existing_user}")
        if existing_user:
            print("[DEBUG] Email already exists!")
            flash("Email already registered as a job seeker.", "error")
            return redirect(url_for('job_seeker_signup'))

        print("[DEBUG] Email check passed")

        hashed_password = generate_password_hash(password)
        print(f"[DEBUG] Password hashed successfully")
        
        # Encrypt sensitive data
        encrypted_phone = encrypt_field(phone)
        encrypted_gender = encrypt_field(gender)
        encrypted_age = encrypt_field(age)
        
        new_jobseeker = JobSeeker(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=encrypted_phone,
            gender=encrypted_gender,
            age=encrypted_age,
            password=hashed_password
        )
        print(f"[DEBUG] JobSeeker object created")
        
        db.session.add(new_jobseeker)
        print(f"[DEBUG] JobSeeker added to session")
        
        db.session.commit()
        print(f"[DEBUG] JobSeeker saved to database: {new_jobseeker.id}")
        flash("Job Seeker Registration Successful!", "success")
        return redirect(url_for('job_seeker_login'))

    return render_template('jobseeker-signup.html')

@app.route('/recruiter-signup', methods=['GET', 'POST'])
def recruiter_signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        business_pancard = request.form['businessPancard']
        company_name = request.form['companyName']
        company_address = request.form['companyAddress']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        print(f"[DEBUG] Recruiter signup attempt: email={email}, first_name={first_name}")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('recruiter_signup'))

        # Check if email already exists
        if Recruiter.query.filter_by(email=email).first():
            flash("Email already registered as a recruiter.", "error")
            return redirect(url_for('recruiter_signup'))

        hashed_password = generate_password_hash(password)
        
        # Encrypt sensitive data
        encrypted_business_pancard = encrypt_field(business_pancard)
        encrypted_company_address = encrypt_field(company_address)
        
        new_recruiter = Recruiter(
            first_name=first_name,
            last_name=last_name,
            email=email,
            business_pancard=encrypted_business_pancard,
            company_name=company_name,
            company_address=encrypted_company_address,
            password=hashed_password
        )
        db.session.add(new_recruiter)
        db.session.commit()
        print(f"[DEBUG] Recruiter saved to database: {new_recruiter.id}")
        flash("Recruiter Registration Successful!", "success")
        return redirect(url_for('recruiter_login'))

    return render_template('recruiter-signup.html')

@app.route('/jobseeker-login', methods=['GET', 'POST'])
def job_seeker_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"[DEBUG] JobSeeker login attempt: email={email}, password={password}")
        user = JobSeeker.query.filter_by(email=email).first()
        print(f"[DEBUG] JobSeeker found: {user}")
        if user and check_password_hash(user.password, password):
            print("[DEBUG] JobSeeker password check passed")
            session['user'] = email
            session['user_type'] = 'jobSeeker'
            flash("Logged in successfully!", "success")
            return redirect(url_for('profile'))
        print(f"[DEBUG] JobSeeker password check failed. User password hash: {user.password[:20]}...")
        flash("Invalid email or password.", "error")
    return render_template('jobseeker-login.html')

@app.route('/recruiter-login', methods=['GET', 'POST'])
def recruiter_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"[DEBUG] Recruiter login attempt: email={email}, password={password}")
        user = Recruiter.query.filter_by(email=email).first()
        print(f"[DEBUG] Recruiter found: {user}")
        if user and check_password_hash(user.password, password):
            print("[DEBUG] Recruiter password check passed")
            session['user'] = email
            session['user_type'] = 'recruiter'
            flash("Logged in successfully!", "success")
            return redirect(url_for('profile'))
        print(f"[DEBUG] Recruiter password check failed. User password hash: {user.password[:20]}...")
        flash("Invalid email or password.", "error")
    return render_template('recruiter-login.html')

@app.route('/profile')
def profile():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user']
    user_type = session['user_type']
    
    if user_type == 'jobSeeker':
        user_info = JobSeeker.query.filter_by(email=user_email).first()
        # Decrypt sensitive data for display
        if user_info:
            user_info.phone = decrypt_field(user_info.phone)
            user_info.gender = decrypt_field(user_info.gender)
            user_info.age = decrypt_field(user_info.age)
    elif user_type == 'recruiter':
        user_info = Recruiter.query.filter_by(email=user_email).first()
        # Decrypt sensitive data for display
        if user_info:
            user_info.business_pancard = decrypt_field(user_info.business_pancard)
            user_info.company_address = decrypt_field(user_info.company_address)
    
    if not user_info:
        flash("User not found.", "error")
        return redirect(url_for('home'))
    
    return render_template('profile.html', user=user_info, user_type=user_type)

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    if session['user_type'] != 'recruiter':
        flash("Only recruiters can post jobs.", "error")
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form['title']
        company_name = request.form['company_name']
        location = request.form['location']
        salary_min = request.form['salary_min']
        salary_max = request.form['salary_max']
        job_type = request.form['job_type']
        description = request.form['description']
        requirements = request.form['requirements']
        skills = request.form['skills']
        
        # Get recruiter info
        recruiter = Recruiter.query.filter_by(email=session['user']).first()
        
        new_job = Job(
            title=title,
            company_name=company_name,
            location=location,
            salary_min=int(salary_min) if salary_min else None,
            salary_max=int(salary_max) if salary_max else None,
            job_type=job_type,
            description=description,
            requirements=requirements,
            skills=skills,
            recruiter_id=recruiter.id
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        flash("Job posted successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('post_job.html')

@app.route('/ai-recommendations')
def ai_recommendations():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    if session['user_type'] != 'jobSeeker':
        flash("AI recommendations are only available for job seekers.", "error")
        return redirect(url_for('home'))
    
    # Get user skills and preferences (you can add these fields to your forms)
    user_skills = request.args.get('skills', '')
    user_preferences = request.args.get('preferences', '')
    
    # Get all active jobs
    all_jobs = Job.query.filter_by(is_active=True).all()
    jobs_data = []
    
    for job in all_jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'company_name': job.company_name,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'job_type': job.job_type,
            'description': job.description,
            'requirements': job.requirements,
            'skills': job.skills,
            'posted_date': job.posted_date
        })
    
    # Get AI recommendations
    recommendations = ai_ml_engine.get_job_recommendations(user_skills, user_preferences, jobs_data, top_n=10)
    
    return render_template('ai_recommendations.html', recommendations=recommendations, user_skills=user_skills, user_preferences=user_preferences)

@app.route('/salary-predictor', methods=['GET', 'POST'])
def salary_predictor():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    if session['user_type'] != 'recruiter':
        flash("Salary predictor is only available for recruiters.", "error")
        return redirect(url_for('home'))
    
    predicted_salary = None
    if request.method == 'POST':
        job_type = request.form.get('job_type', 'Full-time')
        location = request.form.get('location', 'Remote')
        description_length = len(request.form.get('description', ''))
        requirements_length = len(request.form.get('requirements', ''))
        skills_count = len(request.form.get('skills', '').split(',')) if request.form.get('skills') else 0
        
        # Predict salary using simplified AI
        job_features = {
            'job_type': job_type,
            'location': location,
            'description_length': description_length,
            'requirements_length': requirements_length,
            'skills_count': skills_count
        }
        
        predicted_salary = ai_ml_engine.predict_salary(job_features)
    
    return render_template('salary_predictor.html', predicted_salary=predicted_salary)

@app.route('/market-insights')
def market_insights():
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    # Get all jobs for analysis
    all_jobs = Job.query.filter_by(is_active=True).all()
    jobs_data = []
    
    for job in all_jobs:
        jobs_data.append({
            'title': job.title,
            'company_name': job.company_name,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'job_type': job.job_type,
            'description': job.description,
            'requirements': job.requirements,
            'skills': job.skills,
            'posted_date': job.posted_date
        })
    
    # Get market trends
    trends = ai_ml_engine.analyze_job_market_trends(jobs_data)
    
    return render_template('market_insights.html', trends=trends)

@app.route('/job-insights/<int:job_id>')
def job_insights(job_id):
    if 'user' not in session or 'user_type' not in session:
        return redirect(url_for('login'))
    
    job = Job.query.get_or_404(job_id)
    
    # Generate AI insights for this job
    job_data = {
        'title': job.title,
        'company_name': job.company_name,
        'location': job.location,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'job_type': job.job_type,
        'description': job.description,
        'requirements': job.requirements,
        'skills': job.skills
    }
    
    insights = ai_ml_engine.generate_job_insights(job_data)
    
    return render_template('job_insights.html', job=job, insights=insights)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        # Add sample job seekers
        if not JobSeeker.query.filter_by(email='alice@example.com').first():
            db.session.add(JobSeeker(
                first_name='Alice', last_name='Smith', email='alice@example.com',
                phone='1234567890', gender='female', age=25,
                password=generate_password_hash('alicepass')
            ))
        if not JobSeeker.query.filter_by(email='bob@example.com').first():
            db.session.add(JobSeeker(
                first_name='Bob', last_name='Brown', email='bob@example.com',
                phone='9876543210', gender='male', age=30,
                password=generate_password_hash('bobpass')
            ))
        # Add sample recruiters
        if not Recruiter.query.filter_by(email='recruiter1@company.com').first():
            db.session.add(Recruiter(
                first_name='Carol', last_name='Johnson', email='recruiter1@company.com',
                business_pancard='PAN123456', company_name='TechCorp', company_address='123 Tech Street',
                password=generate_password_hash('recruiter1pass')
            ))
        if not Recruiter.query.filter_by(email='recruiter2@company.com').first():
            db.session.add(Recruiter(
                first_name='Dave', last_name='Williams', email='recruiter2@company.com',
                business_pancard='PAN654321', company_name='BizInc', company_address='456 Biz Avenue',
                password=generate_password_hash('recruiter2pass')
            ))
        db.session.commit()
    app.run(debug=True)

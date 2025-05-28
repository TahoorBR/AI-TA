from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, flash
from flask_bcrypt import check_password_hash
from quiz_generation import generate_quiz
from ass_generation import generate_assignment
from co_generation import generate_course_outline
from gf_generation import generate_feedback, download_feedback  # <--- new import
import os
from flask_bcrypt import generate_password_hash
from user import get_user_by_email, initialize_database, add_user # Assuming user.py has these
from functools import wraps

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Enable sessions and flash messages

# Initialize DB at app start
initialize_database()

# Simple login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Root redirects to login if not logged in, else to home
@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# Protected home page
@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route('/quiz')
@login_required
def quiz_page():
    return render_template('quiz.html')

@app.route('/ass')
@login_required
def ass_page():
    return render_template('ass.html')

@app.route('/co')
@login_required
def co_page():
    return render_template('co.html')

@app.route('/settings')
@login_required
def settings_page():
    return render_template('settings.html')

@app.route('/grading_feedback')
@login_required
def grading_feedback_page():
    return render_template('gf.html')


@app.route('/help')
@login_required
def help_page():
    return render_template('help.html')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash("Please fill all fields.")
            return render_template('signup.html')

        # Hash the password before saving
        password_hash = generate_password_hash(password).decode('utf-8')

        # Save to DB
        success = add_user(username, email, password_hash)
        if success:
            flash("Signup successful! Please login.")
            return redirect(url_for('login'))
        else:
            flash("Username or email already exists.")
            return render_template('signup.html')

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please fill in both email and password.')
            return render_template('login.html')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!')
            return redirect(url_for('home'))

        flash('Invalid email or password.')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))


# Your existing API routes remain unchanged but add login_required to protect
@app.route('/generate_quiz', methods=['POST'])
@login_required
def generate_quiz_route():
    try:
        quiz_data = request.get_json()
        if not quiz_data:
            return jsonify({'error': 'Invalid input data'}), 400

        response_text = generate_quiz(quiz_data)

        if not response_text.strip():
            return jsonify({'error': 'Failed to generate quiz content'}), 500

        return jsonify({'quiz_content': response_text})
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return jsonify({'error': 'Failed to generate quiz, please try again later.'}), 500

@app.route('/generate_assignment', methods=['POST'])
@login_required
def generate_assignment_route():
    try:
        assignment_data = request.get_json()
        if not assignment_data:
            return jsonify({'error': 'Invalid input data'}), 400

        response_text = generate_assignment(assignment_data)

        if not response_text.strip():
            return jsonify({'error': 'Failed to generate assignment content'}), 500

        return jsonify({'assignment_content': response_text})

    except Exception as e:
        print(f"Error generating assignment: {e}")
        return jsonify({'error': 'Failed to generate assignment, please try again later.'}), 500

@app.route('/generate_course_outline', methods=['POST'])
@login_required
def generate_course_outline_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input data'}), 400

        generated_text = generate_course_outline(data)

        return jsonify({'course_outline': generated_text})
    except Exception as e:
        print(f"Error generating course outline: {e}")
        return jsonify({'error': 'Failed to generate course outline. Please try again.'}), 500

@app.route('/generate_feedback', methods=['POST'])
@login_required
def generate_feedback_route():
    try:
        if request.content_type.startswith('application/json'):
            quiz_data = request.get_json()
            image_path = None
        else:
            # Handle multipart form: file + form data
            quiz_data = {
                'subject': request.form.get('subject'),
                'education_level': request.form.get('education_level'),
                'assignment_type': request.form.get('assignment_type'),
                'total_marks': int(request.form.get('total_marks', 100))
            }

            image = request.files.get('image')
            image_path = None

            if image and image.filename:
                image_dir = os.path.join('uploads')
                os.makedirs(image_dir, exist_ok=True)
                image_path = os.path.join(image_dir, image.filename)
                image.save(image_path)

        response_text = generate_feedback(quiz_data, image_path=image_path)

        if not response_text.strip():
            return jsonify({'error': 'Failed to generate feedback'}), 500

        return jsonify({'feedback_content': response_text})

    except Exception as e:
        print(f"Error generating feedback: {e}")
        return jsonify({'error': f'Failed to generate feedback: {str(e)}'}), 500

@app.route('/download_quiz')
@login_required
def download_quiz():
    filename = "quiz.docx"
    directory = os.path.join(app.root_path, 'static', 'quizzes')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download_ass')
@login_required
def download_ass():
    filename = "assignment.docx"
    directory = os.path.join(app.root_path, 'static', 'assignments')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download_co')
@login_required
def download_co():
    filename = "course_outline.docx"
    directory = os.path.join(app.root_path, 'static', 'course_outlines')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download_feedback')
@login_required
def download_feedback_route():
    filename = "feedback.docx"
    directory = os.path.join(app.root_path, 'static', 'feedback')
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_session import Session
import json
import logging

# Initialize Flask application
app = Flask(__name__)

# Configurations for template reloading and session management
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) # Initialize session management with filesystem-based storage

# Prevent responses from being cached to ensure data is always fresh
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Load exam data from JSON file
with open('exams.json', 'r') as file:
    exam_data = json.load(file)

# Route to display the home page with a list of available exams
@app.route('/')
def home():
    exam_keys = list(exam_data.keys())  # Extract keys which are the exam names
    return render_template('index.html', exam_keys=exam_keys)    

# Start an exam based on selected exam name
@app.route('/start', methods=['GET', 'POST'])
def start_exam():
    # Get the selected exam name from the form
    selected_exam = request.form.get('exam_name')
    session['selected_exam'] = selected_exam
    session['current'] = 0
    session['score'] = None
    session['total'] = len(exam_data[selected_exam])    
    session['history'] = []
    session['answered_questions'] = None
    return redirect(url_for('question'))

# Handle display and processing of individual questions
@app.route('/question', methods=['GET', 'POST'])
def question():
    selected_exam = session.get('selected_exam', None)
    question_number = session.get('current', 0)
    questions = exam_data.get(selected_exam, [])
    
    if questions and 0 <= question_number < len(questions):
            correct_answer = questions[question_number].get('correct_answer', '')

    if session.get('answered_questions', None) is None:
        session['answered_questions'] = [False] * len(questions)

    if session.get('score', None) is None:
        session['score'] =  [False] * len(questions)

    if request.method == 'POST':
        action = request.form.get('action', '')
        user_answers = request.form.getlist('answer')   # Fetch all checked answers     
        
        # Check if the answers are correct
        if user_answers == correct_answer:
            result = "Correct"                
        else:
            result = "Incorrect"

        if user_answers:
            session['answered_questions'][question_number] = True

        explanation = questions[question_number].get('explanation', '')

        # Render the same question template with results if checked
        if action == 'check':
            session['answered_questions'][question_number] = True                        
            return render_template('question.html', question=questions[question_number],
                                   current=question_number + 1, total=len(questions),
                                   result=result, explanation=explanation, user_answers=user_answers, 
                                   answered_questions=session['answered_questions'])

         # Navigation between questions
        elif action == 'next':
            session['current'] += 1 if question_number < len(questions) - 1 else 0
        elif action == 'prev':
            session['current'] -= 1 if question_number > 0 else 0
        elif action.isdigit():
            session['current'] = int(action) 

        # Append to history and update score if necessary
        if user_answers:
            if result == "Incorrect":
                session['history'].append({
                    'question': questions[question_number]['question'],
                    'correct_answer': correct_answer,
                    'user_answers': user_answers,
                    'explanation': explanation,
                    'result': result
                })
                session['score'][question_number] = False
            else:
                session['score'][question_number] = True

        return redirect(url_for('question'))

    return render_template('question.html', question=questions[question_number],
                           current=question_number + 1, total=len(questions),
                           answered_questions=session['answered_questions'])

# Route to finalize the exam and display results
@app.route('/finish', methods=['POST', 'GET'])
def finish():
    # Calculate final score and determine pass/fail based on a threshold of 83.33% coming from Comptia Sec+ exam 750/900
    final_score = session.get('score', []).count(True)    
    total = session['total']
    percentage = (final_score / total) * 100
    if percentage >= 83.33:
        result = "Pass"
    else:
        result = "Fail"
    return render_template('result.html', result=result, score=final_score, percentage=percentage, total=total, history=session['history'])


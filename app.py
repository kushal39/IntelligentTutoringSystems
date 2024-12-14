from flask import Flask, render_template, request, session
from financial_engine import FinancialEngine
import secrets
from definitions import fetch_definitions ,generate_quiz_data, calculate_score,get_definition

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    income = round (float(request.form['income']) ,2)
    expenses = round (float(request.form['expenses']) ,2)
    debt = round (float(request.form['debt']) ,2)
    investment = round (float(request.form['investment']) ,2)
    goal_amount = round (float(request.form['goal_amount']) ,2)
    credit_score = int(request.form['credit_score'])
    debt_repayment_strategy = request.form['debt_repayment_strategy']
    investment_strategy = request.form['investment_strategy']

    # initialize the FinancialEngine
    engine = FinancialEngine(
        income,
        expenses,
        debt,
        investment,
        goal_amount,
        credit_score,
        debt_repayment_strategy,
        investment_strategy
    )
    engine.create_user_data()

    # Calculate savings plan and personalized messages
    monthly_savings, time_to_goal, savings_message, debt_message, investment_message = engine.calculate_savings_plan()

    # Generate financial tips
    tips = engine.generate_financial_tips()

    # Track user's progress towards the goal
    progress_message = engine.track_progress()

    # Render the results page with personalized information
    return render_template(
        'results.html',
        monthly_savings=monthly_savings,
        time_to_goal=time_to_goal,
        savings_message=savings_message,
        debt_message=debt_message,
        investment_message=investment_message,
        tips=tips,
        progress_message=progress_message
    )

@app.route('/definition/<term>')
def definition(term):
    # Get Defination of term
    content = get_definition(term)
    return render_template('definition.html', content=content , term = term)

@app.route('/definitions')
def definitions():
    return render_template('definitions.html', all_definitions = fetch_definitions())

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = calculate_score(session['answers'], request.form)
        return render_template('quiz_results.html', score=score, total=len(session['answers']))

    # Generate a new quiz
    quiz_data, answers = generate_quiz_data()

    #Store Answers
    session['answers'] = answers
    return render_template('quiz.html', quiz_data=quiz_data)

if __name__ == '__main__':
    app.run(debug=True)

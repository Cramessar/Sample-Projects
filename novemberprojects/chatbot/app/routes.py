# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from . import db
from .models import User, Account, Transaction, SavingsPlan
from .forms import RegistrationForm, LoginForm, ChatbotForm, UploadForm
from .ai_utils import get_financial_advice, get_financial_advice_chat
from sqlalchemy import func
import csv
import io
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        account = Account(user=user)
        db.session.add(account)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('register.html', title='Register', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='Login', form=form)

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    account = current_user.account
    transactions = Transaction.query.filter_by(account_id=account.id)\
                        .order_by(Transaction.date.desc())\
                        .limit(5).all()
    return render_template('dashboard.html', title='Dashboard', account=account, transactions=transactions)

@main_bp.route('/analysis')
@login_required
def analysis():
    account = current_user.account
    transactions = Transaction.query.filter_by(account_id=account.id).all()
    advice = get_financial_advice(transactions)
    return render_template('analysis.html', title='Financial Analysis', advice=advice)

@main_bp.route('/spending_summary')
@login_required
def spending_summary():
    account = current_user.account
    spending = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter_by(account_id=account.id).group_by(Transaction.category).all()
    return render_template('spending_summary.html', title='Spending Summary', spending=spending)

@main_bp.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    form = ChatbotForm()
    if 'messages' not in session:
        session['messages'] = []

    if form.validate_on_submit():
        user_input = form.user_input.data
        # Add user's message to the conversation history
        session['messages'].append({'role': 'user', 'content': user_input})

        # Get the chatbot's response
        response = get_financial_advice_chat(session['messages'])

        # Add chatbot's response to the conversation history
        session['messages'].append({'role': 'assistant', 'content': response})

        # Save the session
        session.modified = True

        return render_template('chatbot.html', title='Financial Planner Chatbot', form=form, messages=session['messages'])

    return render_template('chatbot.html', title='Financial Planner Chatbot', form=form, messages=session.get('messages'))

@main_bp.route('/reset_chat')
@login_required
def reset_chat():
    session.pop('messages', None)
    return redirect(url_for('main.chatbot'))

@main_bp.route('/upload_transactions', methods=['GET', 'POST'])
@login_required
def upload_transactions():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.reader(stream)
                # Skip header row if it exists
                header = next(csv_input, None)
                account = current_user.account
                for row in csv_input:
                    date_str, amount_str, category, description = row
                    # Parse date string to datetime object
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Adjust format if necessary
                    transaction = Transaction(
                        date=date_obj,
                        amount=float(amount_str),
                        category=category,
                        description=description,
                        account_id=account.id
                    )
                    db.session.add(transaction)
                db.session.commit()
                flash('Transactions uploaded successfully.')
                return redirect(url_for('main.dashboard'))
            except Exception as e:
                flash(f'An error occurred while processing the file: {e}')
                return redirect(url_for('main.upload_transactions'))
    return render_template('upload_transactions.html', title='Upload Transactions', form=form)

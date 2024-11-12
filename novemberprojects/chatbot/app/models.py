# app/models.py

from . import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    account = db.relationship('Account', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(12, 2), default=0.00)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction', backref='account', lazy='dynamic')
    savings_plans = db.relationship('SavingsPlan', backref='account', lazy='dynamic')

    def __repr__(self):
        return f'<Account {self.id}>'

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    amount = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(50))
    description = db.Column(db.String(255))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'<Transaction {self.id}>'

class SavingsPlan(db.Model):
    __tablename__ = 'savings_plan'
    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(100))
    goal_amount = db.Column(db.Numeric(10, 2))
    current_amount = db.Column(db.Numeric(10, 2), default=0.00)
    target_date = db.Column(db.Date)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'<SavingsPlan {self.goal_name}>'

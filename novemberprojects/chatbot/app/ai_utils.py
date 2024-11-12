# app/ai_utils.py

import warnings
warnings.filterwarnings('ignore')
import openai
import os
from flask import current_app
import logging
from flask_login import current_user
from .models import Transaction

def get_financial_advice(transactions):
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if openai_api_key:
        openai.api_key = openai_api_key
    else:
        raise EnvironmentError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

    transaction_list = [
        f"{t.date.date()} - {t.category} - ${t.amount} - {t.description}"
        for t in transactions
    ]
    transaction_text = "\n".join(transaction_list)

    prompt = f"""
    You are a financial advisor AI assistant. Based on the following transaction history, provide personalized advice on savings plans, debt repayment strategies, and highlight areas where the user can reduce spending.

    Transactions:
    {transaction_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        advice = response['choices'][0]['message']['content'].strip()
        return advice
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "An error occurred while fetching financial advice. Please try again later."

def get_financial_advice_chat(conversation_history):
    """Generates a response from the financial planner chatbot."""
    try:
        # Retrieve OpenAI API key
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            raise EnvironmentError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

        # Fetch user's transactions
        account = current_user.account
        transactions = Transaction.query.filter_by(account_id=account.id).all()
        transaction_list = [
            f"{t.date.date()} - {t.category} - ${t.amount} - {t.description}"
            for t in transactions
        ]
        transaction_text = "\n".join(transaction_list)

        # Build the messages list, starting with a system message
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly knowledgeable Certified Financial Planner (CFP) with expertise in personal finance, "
                    "investment strategies, and financial planning. Provide clear, accurate, and personalized advice to help users "
                    "achieve their financial goals. Consider the user's transaction history when providing advice.\n\n"
                    f"Transaction History:\n{transaction_text}"
                )
            }
        ] + conversation_history

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model='gpt-4',  # Use 'gpt-4' if available
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        advice = response['choices'][0]['message']['content'].strip()
        return advice

    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "Sorry, I'm unable to process your request at the moment. Please try again later."

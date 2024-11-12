
# Banking App with Financial Planner Chatbot

An interactive banking application that allows users to:

- Register and manage an account.
- Upload transaction data via CSV files.
- View a dashboard with recent transactions.
- Analyze spending and receive financial advice.
- Interact with a financial planner chatbot for personalized advice.

The application leverages OpenAI's GPT models to provide financial analysis and advice and uses Flask for the web framework.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Registering a New User](#registering-a-new-user)
  - [Uploading Transactions via CSV](#uploading-transactions-via-csv)
  - [Using the Chatbot](#using-the-chatbot)
- [Files and Directories](#files-and-directories)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **User Authentication**: Register and log in securely.
- **Dashboard**: View account balance and recent transactions.
- **Upload Transactions**: Upload transaction data via CSV files.
- **Spending Summary**: Visual summary of spending by category.
- **Financial Analysis**: Receive personalized financial advice based on transaction history.
- **Financial Planner Chatbot**: Interact with a chatbot that provides financial advice, considering the user's transaction history.

---

## Project Structure

```
chatbot/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── ai_utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── analysis.html
│   │   ├── spending_summary.html
│   │   ├── chatbot.html
│   │   └── upload_transactions.html
│   └── static/
│       └── css/
│           └── style.css
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── venv/
```


---

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **Virtual Environment Tool**: `venv` or `virtualenv`
- **SQLite** (comes bundled with Python)

### Setting Up a Virtual Environment

1. **Navigate to the Project Directory**

   ```bash
   cd chatbot
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

### Installing Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

**Note:** The application requires `openai==0.28.0`. Ensure that the `requirements.txt` specifies this version.

If `openai` is not at version `0.28.0`, install it explicitly:

```bash
pip install openai==0.28.0
```

---

## Configuration

### Environment Variables

The application requires certain environment variables to function correctly.

1. **Set the `OPENAI_API_KEY`**

   Obtain your OpenAI API key from [OpenAI's website](https://platform.openai.com/account/api-keys) and set it as an environment variable.

   - **On Windows Command Prompt:**

     ```bash
     set OPENAI_API_KEY=your_openai_api_key_here
     ```

   - **On Windows PowerShell:**

     ```powershell
     $env:OPENAI_API_KEY="your_openai_api_key_here"
     ```

   - **On macOS/Linux:**

     ```bash
     export OPENAI_API_KEY=your_openai_api_key_here
     ```

2. **Set the `SECRET_KEY` (Optional)**

   For enhanced security, you can set a custom `SECRET_KEY`:

   - **On Windows Command Prompt:**

     ```bash
     set SECRET_KEY=your_secret_key_here
     ```

   - **On Windows PowerShell:**

     ```powershell
     $env:SECRET_KEY="your_secret_key_here"
     ```

   - **On macOS/Linux:**

     ```bash
     export SECRET_KEY=your_secret_key_here
     ```

Alternatively, you can edit `config.py` and replace `'your_secret_key_here'` with a secure key.



---

## Database Setup

Initialize the SQLite database and create the necessary tables.

1. **Activate the Virtual Environment**

   If not already activated:

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

2. **Initialize the Database**

   Run the following commands in the Python shell:

   ```bash
   python
   ```

   Inside the Python shell:

   ```python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
   exit()
   ```

---

## Running the Application

Start the Flask application:

```bash
python run.py
```

The application will run on `http://127.0.0.1:5000/` by default.

---

## Usage

### Registering a New User

1. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:5000/`.

2. **Register**

   - Click on the `Register` link.
   - Fill in a username and password.
   - Submit the form to create your account.

### Uploading Transactions via CSV

1. **Log In**

   - If not already logged in, log in with your credentials.

2. **Navigate to Upload Transactions**

   - Click on the `Upload Transactions` link in the navigation menu.

3. **Prepare Your CSV File**

   - Ensure your CSV file has the following columns:

     ```
     Date,Amount,Category,Description
     ```

   - **Example CSV Content:**

     ```csv
     Date,Amount,Category,Description
     2023-10-01,50.00,Food,Grocery shopping
     2023-10-02,1000.00,Salary,Monthly salary
     2023-10-03,-200.00,Utilities,Electricity bill
     ```

4. **Upload the CSV File**

   - On the `Upload Transactions` page, click `Choose File` and select your CSV file.
   - Click `Upload` to submit the file.
   - If successful, you will see a confirmation message, and the transactions will be added to your account.



### Using the Chatbot

1. **Access the Chatbot**

   - Click on the `Chatbot` link in the navigation menu.

2. **Interact with the Chatbot**

   - Type your financial questions into the text area.
   - Click `Ask` to submit your question.
   - The chatbot will respond, considering your transaction history.

3. **Conversation History**

   - The chatbot maintains a conversation history during your session.
   - You can reset the conversation by clicking `Reset Conversation`.

4. **Examples of Questions**

   - "How can I save more money each month?"
   - "What is the best way to pay off my credit card debt?"
   - "Based on my spending, where can I cut expenses?"

---

## Files and Directories

- **`app/`**: Contains the main Flask application code.

  - **`__init__.py`**: Initializes the Flask app.
  - **`models.py`**: Defines the database models.
  - **`routes.py`**: Contains the route handlers.
  - **`forms.py`**: Defines the web forms.
  - **`ai_utils.py`**: Contains utility functions for AI interactions.
  - **`templates/`**: HTML templates for rendering pages.
  - **`static/`**: Static files such as CSS.

- **`config.py`**: Configuration settings for the Flask app.

- **`run.py`**: Entry point to run the Flask application.

- **`requirements.txt`**: Lists the Python dependencies.

- **`README.md`**: This file.

- **`venv/`**: The virtual environment directory.

---

## Dependencies

The project relies on the following Python packages:

- **Flask**: Web framework.
- **Flask-Login**: User session management.
- **Flask-WTF**: Form handling and CSRF protection.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **openai==0.28.0**: OpenAI API client.
- **WTForms**: Form validation.
- **Werkzeug**: WSGI utilities.
- **SQLAlchemy**: Database toolkit.
- **Jinja2**: Templating engine.

**Note:** The application requires `openai==0.28.0`. Ensure that this specific version is installed.

---

## Troubleshooting

- **OpenAI API Errors**

  - If you encounter errors related to the OpenAI API, ensure that:

    - The `OPENAI_API_KEY` environment variable is set correctly.
    - You have network connectivity.
    - You have sufficient API usage quota.
    - **Version Compatibility**: The application requires `openai==0.28.0`. Ensure that this version is installed, as newer versions may have breaking changes.

- **Database Errors**

  - If you experience database issues:

    - Ensure the database is initialized.
    - Check that the `app.db` file exists in the project root.

- **CSRF Token Missing**

  - If you receive a CSRF token missing error:

    - Ensure that `SECRET_KEY` is set.
    - Verify that forms include `{{ form.hidden_tag() }}`.

- **Version Conflicts**

  - Ensure that all dependencies are installed with the correct versions as specified in `requirements.txt`.

- **Debug Mode**

  - For development, the Flask app runs in debug mode. Do not use debug mode in production.

---

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. **Fork the Repository**

   - Create a personal fork of the project.

2. **Clone the Fork**

   ```bash
   git clone https://github.com/your_username/chatbot.git
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your_feature_name
   ```

4. **Commit Your Changes**

   ```bash
   git commit -am "Add new feature"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature/your_feature_name
   ```

6. **Create a Pull Request**

   - Open a pull request on the original repository.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- **OpenAI**: For providing the GPT models used in the chatbot and financial analysis features.
- **Flask**: For the web framework used to build the application.
- **Contributors**: Thank you to everyone who has contributed to this project.

---

# Requirements.txt

Ensure your `requirements.txt` file includes the specific version of `openai`:

```
Flask
Flask-Login
Flask-WTF
Flask-Bootstrap
Flask-SQLAlchemy
openai==0.28.0
Werkzeug
WTForms
```

---

# Additional Notes

- **OpenAI Library Version**

  - The application is built to work with `openai==0.28.0`. Later versions of the OpenAI Python library have significant changes that may not be compatible with the current codebase.

- **API Changes**

  - If you wish to use a newer version of the OpenAI library, you will need to update the API calls in `ai_utils.py` to match the new API.

---

If you have any questions or need further assistance with setting up or running the application, feel free to reach out!

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from flask import Flask, request, render_template

# Load the dataset (make sure 'spam.csv' is in the same directory)
df = pd.read_csv('spam.csv', encoding='latin-1')

# Drop unnecessary columns
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

# Download stopwords from NLTK if not already done
nltk.download('stopwords')

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['cleaned_message'] = df['message'].apply(preprocess_text)

# Initialize the TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['cleaned_message']).toarray()

# Define the target variable
y = df['label'].apply(lambda x: 1 if x == 'spam' else 0)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Naive Bayes model
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Train Logistic Regression model
log_reg_model = LogisticRegression(max_iter=1000)
log_reg_model.fit(X_train, y_train)

# Train Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# ---------------------------
# 1. Feature Importance
# ---------------------------

# Feature importance for Logistic Regression
log_reg_coefficients = log_reg_model.coef_.flatten()
top_positive_coefficients = np.argsort(log_reg_coefficients)[-10:]
top_negative_coefficients = np.argsort(log_reg_coefficients)[:10]
feature_names = np.array(tfidf.get_feature_names_out())

print("Top words indicating spam (Logistic Regression):")
print(feature_names[top_positive_coefficients])

print("\nTop words indicating ham (Logistic Regression):")
print(feature_names[top_negative_coefficients])

# Feature importance for Random Forest
importances = rf_model.feature_importances_
indices = np.argsort(importances)[-10:]
print("\nTop 10 important words for Random Forest:")
for i in indices:
    print(f"{feature_names[i]}: {importances[i]:.4f}")

# ---------------------------
# 2. Hyperparameter Tuning with RandomizedSearchCV
# ---------------------------
#Adjust n_estimators if the code is taking too long. Also try using smaller data sets if it becomes an issue.
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None]
}

# Use RandomizedSearchCV for faster search
random_search_rf = RandomizedSearchCV(rf_model, param_distributions=param_grid, n_iter=5, cv=3, scoring='accuracy', random_state=42)
random_search_rf.fit(X_train, y_train)

print(f"\nBest parameters for Random Forest: {random_search_rf.best_params_}")
print(f"Best accuracy: {random_search_rf.best_score_:.4f}")

# ---------------------------
# 3. Saving and Loading Models
# ---------------------------

# Save the models and TF-IDF vectorizer
joblib.dump(log_reg_model, 'logistic_regression_model.pkl')
joblib.dump(rf_model, 'random_forest_model.pkl')
joblib.dump(nb_model, 'naive_bayes_model.pkl')
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')

# Load the models
loaded_log_reg_model = joblib.load('logistic_regression_model.pkl')
loaded_rf_model = joblib.load('random_forest_model.pkl')
loaded_nb_model = joblib.load('naive_bayes_model.pkl')
loaded_tfidf = joblib.load('tfidf_vectorizer.pkl')

# Test the loaded models
test_text = "Congratulations, you've won a free prize! Call now."
test_text_cleaned = preprocess_text(test_text)
test_text_vectorized = loaded_tfidf.transform([test_text_cleaned])

print("\nLoaded Logistic Regression prediction:", loaded_log_reg_model.predict(test_text_vectorized))
print("Loaded Random Forest prediction:", loaded_rf_model.predict(test_text_vectorized))
print("Loaded Naive Bayes prediction:", loaded_nb_model.predict(test_text_vectorized))

# ---------------------------
# 4. Deploying the Model as a Web App (Flask)
# ---------------------------

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        cleaned_message = preprocess_text(message)
        vectorized_message = loaded_tfidf.transform([cleaned_message])
        
        prediction = loaded_log_reg_model.predict(vectorized_message)[0]
        result = "Spam" if prediction == 1 else "Ham"
        
        return render_template('index.html', prediction_text=f'This email is: {result}')

if __name__ == "__main__":
    app.run(debug=True)

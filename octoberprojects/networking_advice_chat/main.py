# main.py

import openai
import gradio as gr
from transformers import pipeline
from api_keys import OPENAI_API_KEY

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Load sentiment analysis model from Hugging Face
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load a text classification model (example using pre-trained classifier)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Predefined classes or spaces
spaces = ["Tech Support", "Account Management", "Implementation", "Product Feedback"]

# Load translation pipelines
translation_pipelines = {
    "Russian": pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru"),
    "French": pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr"),
    "Spanish": pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),
    "German": pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")
}

# Function for OpenAI response
def openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers networking questions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error with OpenAI: {str(e)}"

# Function for Hugging Face sentiment analysis
def analyze_sentiment(user_input):
    result = sentiment_analyzer(user_input)
    label = result[0]['label']
    score = result[0]['score']
    return f"Sentiment: {label} (Confidence: {score:.2f})"

# Function for text classification to identify the relevant space
def classify_text(user_input):
    result = classifier(user_input, candidate_labels=spaces)
    best_class = result['labels'][0]  # Get the top predicted class
    confidence = result['scores'][0]
    return f"Classified as: {best_class} (Confidence: {confidence:.2f})"

# Function for translation
def translate_response(response, target_language):
    if target_language in translation_pipelines:
        translator = translation_pipelines[target_language]
        translation = translator(response)[0]['translation_text']
        return translation
    else:
        return "Translation not available for the selected language."

# Main function to handle user input and provide responses
def handle_question(user_input, target_language):
    # Analyze the sentiment of the question
    sentiment = analyze_sentiment(user_input)

    # Classify the input to identify the space or category
    classification = classify_text(user_input)

    # Generate a response from OpenAI
    openai_result = openai_response(user_input)

    # If a translation is requested, translate the response
    if target_language and target_language != "None":
        translated_response = translate_response(openai_result, target_language)
        return f"{classification}\n{sentiment}\n\nResponse:\n{openai_result}\n\nTranslated to {target_language}:\n{translated_response}"
    else:
        return f"{classification}\n{sentiment}\n\nResponse:\n{openai_result}"

# Gradio interface setup
chat_interface = gr.Interface(
    fn=handle_question,
    inputs=[
        gr.Textbox(lines=7, placeholder="Ask a networking question...", label="Chat with the assistant"),
        gr.Dropdown(choices=["None", "Russian", "French", "Spanish", "German"], label="Translate response to:")
    ],
    outputs=gr.Textbox(label="Response"),
    title="Networking Guru",
    description="Get expert answers and advice on networking-related topics! Optionally, translate the response into another language.",
    css=".gradio-interface { background-color: #2e3440; color: #eceff4; font-family: 'Arial'; }"
)

# Launch the interface
if __name__ == "__main__":
    chat_interface.launch(share=True)

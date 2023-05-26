
import nltk
import string
import random
import streamlit as st
import speech_recognition as sr
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLP resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# Define a list of greeting words
GREETINGS = ["hi", "hello", "hey", "hola", "howdy", "greetings"]

# Define a list of responses to greetings
GREETINGS_RESPONSES = ["Hello!", "Hi there!", "Hey!", "Hi!", "Hola!", "Howdy!", "Hiya"]

# Define a list of questions about the chatbot's well-being
WELL_BEING_QUESTIONS = ["what's good?","how far","how are you", "how are you doing", "how's it going", "how do you feel", "what's up"]

# Define a list of responses to well-being questions
WELL_BEING_RESPONSES = ["i dey o","I'm doing well, thank you for asking!", "I'm feeling great today!", "I'm a chatbot, so I don't have feelings, but thank you for asking!"]

# Load the text file and preprocess the data
with open(r"C:\Users\DELL\Desktop\untitled\healthdata.txt", 'r') as f:
    data = f.read().replace('\n', ' ')

# Tokenize the text into sentences
sentences = sent_tokenize(data)

# Define a function to preprocess each sentence
def preprocess(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Remove stopwords and punctuation
    words = [word.lower() for word in words]
    # stopwords.words('english') and if word.lower() not in  word not in string.punctuation
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]
# Define a function to find the most relevant sentence given a query
def get_most_relevant_sentence(query):
    # Preprocess the query
    query = preprocess(query)
    # Compute the similarity between the query and each sentence in the text
    max_similarity = 0
    most_relevant_sentence = ""
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / len(set(query).union(sentence))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence

# Define the chatbot function to return the response instead of printing it
def chatbot(question):
    # Check if the question is a greeting
    if any(greeting in question.lower() for greeting in GREETINGS):
        return random.choice(GREETINGS_RESPONSES)
    # Check if the question is about the chatbot's well-being
    elif any(question.lower() == well_being_question for well_being_question in WELL_BEING_QUESTIONS):
        return random.choice(WELL_BEING_RESPONSES)
    # Find the most relevant sentence
    else:
        most_relevant_sentence = get_most_relevant_sentence(question)
        # Return the answer
        return most_relevant_sentence
def main():
    st.title("Chatbot")
    st.write("Hello! I'm a chatbot. Ask me anything about the topic in the text file.")

    # Create a selectbox for the user to choose their input method
    input_method = st.selectbox("Choose your input method:", options=["Text", "Speech"])

    # Handle text input
    if input_method == "Text":
        # Create a text input for the user's question
        question = st.text_input("Ask a question:")

        # Check if the user has asked a question
        if question:
            # Get the chatbot's response to the question
            response = chatbot(question)
            st.write("Answer:", response)

    # Handle speech input
    elif input_method == "Speech":
        # Use speech recognition if available
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Say something!")
            audio = r.listen(source)
            st.write("Processing audio...")
            try:
                # Recognize speech using Google Speech Recognition
                question = r.recognize_google(audio)
                st.write("Question (from speech): ", question)
                # Get the chatbot's response to the question
                response = chatbot(question)
                st.write("Answer:", response)
                # Create a button to ask for another question in speech recognition
                if st.button("Ask another question"):
                    st.write("Say something!")
                    audio = r.listen(source)
                    st.write("Processing audio...")
                    question = r.recognize_google(audio)
                    st.write("Question (from speech): ", question)
                    response = chatbot(question)
                    st.write("Answer:", response)
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand what you said. Please try again.")


if __name__ == '__main__':
    main()


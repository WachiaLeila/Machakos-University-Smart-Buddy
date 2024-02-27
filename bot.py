import string
import nltk
import logging
import random
import re
from flask import Flask, request, jsonify, render_template
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk, pos_tag
from nltk.tree import Tree
from textblob import TextBlob

app = Flask(__name__)

# Define responses for different intents
response_templates = {
    'greeting': ['Hello!', 'Hi there!'],
    'farewell': ['Goodbye!', 'See you later.'],
    'default': ["I didn't quite understand that. Could you please rephrase or ask something else?"],
}

# Additional patterns & responses
# Add the new patterns and responses to the existing pattern list
patterns = [
    (r'hi (.*)|hello (.*)|hey (.*)|hello|hi|hey', ['Hello kimani.', 'Hi there buddy.']),
    (r'how are you', ['I am good, thank you. How can I help you today?', 'I am doing well. How can I help you today?']),
    (r'fine|good', ['That is amazing buddy', 'I am glad that you are fairing well.']),
    (r'I am not fine|I am (.*)', ['That is sad buddy, hey cheer up.']),
    (r'what is your name', ['I am smart Buddy.', 'You can call me Bud.']),
    (r'bye (.*)|goodbye (.*)|bye|goodbye', ['Goodbye!', 'See you later.']),
    (r'your favorite (.*)', ["I don't have preferences."]),
    (r'I like (.*)', ["That's great!"]),
    (r'I love (.*)', ["That's a good thing, make you cherish every moment & enjoy the better days buddy, am proud of you."]),
    (r'I need (.*)', ['Why do you need {0}?']),
    (r'(.*) (weather|temperature) (.*)', ['I am not equipped to provide real-time weather information.']),
    (r'what can you do', ['I can chat with you, provide information, and answer questions in regard to Machakos University.']),
    (r'who are you', ['I am your smart buddy, a chatbot born & raised by Python.']),
    (r'how can you help', ['I can assist you with information, answer questions, and have casual conversations based on Machakos University context.']),
    (r'what is the meaning of life', ['The meaning of life is a philosophical question with no definitive answer.']),
    (r'(.*) (hobby|hobbies)', ['I enjoy chatting and helping users.']),
    (r'(.*) (movie|movies)', ["I enjoy all kinds of movies."]),
    (r'(.*) (book|books)', ['I love reading!']),
    (r'(.*) (music|song|songs)', ["I like various types of music."]),
    (r'Units I’m supposed to register this semester|registering units|(.*) units', ['For Bsc Mathematics & Computer science year 3 sem 2 the units are: Advanced Calculus, Linear Algebra, Probability Theory, Numerical Methods']),
    (r'I have a flu can I get medication in the school dispensary', ['Yes, you can get meds, just carry your ID & go to the school dispensary.']),
    (r'when is the next elections|elections', [' Elections will be held on February 23rd, 2024.']),
    (r'Who is the school president|university president', ['The current president is Mr. Ian Rop.']),
    (r"Didn’t verify my fingerprint|Didn’t verify my fingerprint (.*)|how am I supposed to verify my fingerprint|fingerptint (.*)|fingerprint", ['Visit the security office for your biometrics to be taken.']),
    (r'When is the next interschool competitions|interschool competition|competitions (.*)', ['The Interschool competitions will be held in the last week of this semester.']),
    (r'What is the duration of the program|program period', ['Since you are taking Bsc Maths & Computer science, the program is a 4-year course.']),
    (r'What is the pass mark|pass', ['The pass mark is 40.']),
    (r'Symptoms of covid-19|covid (.*)|covid', ['COVID symptoms: fever, cough, fatigue, loss of taste/smell.']),
    #(r'Qualification of being a samu chair', ['At least have 3 provisional transcripts.']),
    (r'What should a strong portal password contain|portal password', ['For a strong password make use of uppercase, lowercase, numbers, special characters. But prioritze you level of remembering.']),
    (r'When is the reporting date|(.*) reporting date|reporting date', ['Semester 1 reporting will be on September 9th, 2024.']),
    (r'how can we contact the registrar', ["To contact the Registrar you'll have to send an email to registrar@mksu.ac.ke."]),
    (r'luban workshop', ['The Luban workshop is on the 3rd floor of the ADB building.']),
    #(r'When are the exams', ['Semester 2 exam timetable not released yet.']),
    (r'am bored', ["Makosa ni yangu, sijakushow mkuru amedrop Minisode: Mob Injustice?."]),
    (r'aah, say no more', ["Na kama k, if you see mkurugenzi in the building..."]),
    (r'you just know', ["He's got the juice (sips juice)."]),
    (r'thats whats up', ["Na ukuwe umesubscribe wadau, unajua we admire him, you know."]),
    (r'thanks', ["Shwari kimani."]),
    (r'(.*)', ["Sorry, I'm only entitled to Machakos University's jurisdiction buddy."]),
]


# Update response_templates with additional patterns
for pattern, responses in patterns:
    response_templates[f'pattern_{pattern}'] = responses

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    logging.debug('Received POST request to /process')

    # LOG REQUEST DATA
    logging.debug(f"Request method: {request.method}")
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request data: {request.get_data()}")

    # user input
    user_input = request.form.get('userInput')
    logging.debug(f"User input: {user_input}")

    # Check if user input is empty
    if not user_input:
        logging.debug('No user input received')
        return jsonify({'response': 'Error: No user input received.'})

    # Process user input
    processed_input = preprocess_input(user_input)
    logging.debug(f"processed input: {processed_input}")

    # Generate response
    response = generate_response(processed_input)
    logging.debug(f"Response: {response}")

    # return response
    return jsonify({'response': response})

def preprocess_input(input_text):
    # No preprocessing needed for this simple example
    return input_text

def generate_response(processed_input):
    # Loop through patterns and responses, return first matched response
    for pattern, responses in patterns:
        match = re.match(pattern, processed_input.lower())
        if match:
            if '{0}' in random.choice(responses):
                return responses[0].format(match.group(1))
            return random.choice(responses)
    
    # Return default response if no pattern is matched
    return random.choice(response_templates['default'])

if __name__ == '__main__':
    app.run(debug=True)

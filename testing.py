from flask import Flask, render_template, request
import google.generativeai as gen_ai

# Input your GenAI API Key here
GOOGLE_API_KEY = "AIzaSyBMvXTCa9LnfClHw36PKjrzqcE4lNxOCMI"

# Initialize the Flask app
app = Flask(__name__)

# Configure GenAI with your API key
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Initialize the GenAI model for code testing
model = gen_ai.GenerativeModel('gemini-1.0-pro')

# Static content for code testing
static_content = "You are a helpful assistant.\nCode Testing assistant.\nAssists in writing, running, and debugging tests for code coverage and quality assurance.\n"

def code_testing(user_input):
    # Combine static content with user input
    input_combined = f"{static_content}Overview and Introduction for {user_input}.\nJust give me test cases for {user_input}.\nFinally explain the result."

    # Initialize chat session
    chat_session = model.start_chat()

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/')
def index():
    return render_template('testing.html', response=None)

@app.route('/test_code', methods=['POST'])
def test_code():
    if 'file_input' in request.files:
        uploaded_file = request.files['file_input']
        user_input = uploaded_file.read().decode('utf-8')
    else:
        user_input = request.form['user_input']
        
    response = code_testing(user_input)
    return render_template('testing.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)

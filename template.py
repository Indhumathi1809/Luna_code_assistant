from flask import Flask, render_template, request
import google.generativeai as gen_ai

# Input your GenAI API Key here
GOOGLE_API_KEY = "AIzaSyBMvXTCa9LnfClHw36PKjrzqcE4lNxOCMI"

# Initialize the Flask app
app = Flask(__name__)

# Configure GenAI with your API key
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Initialize the GenAI model for code performance analysis
model = gen_ai.GenerativeModel('gemini-1.0-pro')

# Static content for code performance analysis
static_content = "Provides templates or boilerplate code for common tasks or design patterns, accelerating development and finally explain it:\n"

def code_templates(user_input):
    # Combine static content with user input
    input_combined = f"{static_content}{user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/template_code', methods=['POST'])
def template_code():
    if 'file' in request.files:
        uploaded_file = request.files['file']
        user_input = uploaded_file.read().decode('utf-8')
    else:
        user_input = request.form['user_input']
        
    response = code_templates(user_input)
    return render_template('template.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)

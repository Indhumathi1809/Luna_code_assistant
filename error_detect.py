from flask import Flask, render_template, request
import google.generativeai as gen_ai

# Input your Google API Key here
GOOGLE_API_KEY = "AIzaSyBMvXTCa9LnfClHw36PKjrzqcE4lNxOCMI"

# Check if API key is provided
if not GOOGLE_API_KEY:
    print("Please enter your Google API Key.")
    exit()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.0-pro')

app = Flask(__name__)

# Static content to concatenate with user input
static_content = "Identify and explain syntax errors and provide suggestions for correction in the following code:"

def error_detection(user_input):
    # Combine static content with user input
    input_combined = f"{static_content} {user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/')
def index():
    return render_template('error_detect.html')

@app.route('/detect_error', methods=['POST'])
def detect_error():
    user_input = ""
    if 'file' in request.files and request.files['file'].filename != '':
        uploaded_file = request.files['file']
        user_input = uploaded_file.read().decode('utf-8')
    else:
        user_input = request.form['user_input']
    
    response = error_detection(user_input)
    return render_template('error_detect.html', user_input=user_input, response=response)

if __name__ == '__main__':
    app.run(debug=True)

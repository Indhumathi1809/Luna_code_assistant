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

@app.route('/')
def index():
    return render_template('generate.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    user_input = request.form['user_input']
    assistant_response = code_generation(user_input)
    return render_template('generate.html', assistant_response=assistant_response, user_input=user_input)

def code_generation(user_input):
    # Initialize chat session
    chat_session = model.start_chat(history=[])
    
    # Send user's message to Gemini-Pro and get the response
    gemini_response = chat_session.send_message(user_input)
    
    # Return the assistant's response
    return gemini_response.text

if __name__ == '__main__':
    app.run(debug=True)

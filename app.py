from flask import Flask, render_template, request
import google.generativeai as gen_ai
from flask import jsonify
from io import StringIO
import sys
import subprocess
from gtts import gTTS
import uuid
import os

# Input your Google API Key here
GOOGLE_API_KEY = "YOUR_API_KEY"

# Check if API key is provided
if not GOOGLE_API_KEY:
    print("Please enter your Google API Key.")
    exit()
    
    
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.0-pro')

app = Flask(__name__)

OUTPUT_FOLDER = "output"

def generate_uuid():
    return str(uuid.uuid4())

def save_response_to_mp3(response, filename):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    filepath = os.path.join(OUTPUT_FOLDER, filename)
    tts = gTTS(text=response, lang='en')
    tts.save(filepath)

#assistant
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/generated_code', methods=['GET', 'POST'])
def generated_code():
    if request.method == 'POST':
        user_input = request.form['user_input']
        assistant_response = code_generation(user_input)
        # Generate a unique filename using UUID
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        return render_template('generate.html', assistant_response=assistant_response, user_input=user_input)
    else:
        return render_template('generate.html')

def code_generation(user_input):
    # Initialize chat session
    chat_session = model.start_chat(history=[])
    
    # Send user's message to Gemini-Pro and get the response
    gemini_response = chat_session.send_message(user_input)
    
    # Return the assistant's response
    return gemini_response.text


def generate_documentation(user_input):
    # Combine static content with user input
    static_content = "Give me project documentation for"
    input_combined = f"{static_content} {user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/docs_code', methods=['GET', 'POST'])
def docs_code():
    try:
        if request.method == 'POST':
            user_input = ""
            if 'file' in request.files and request.files['file'].filename != '':
                # If a file is uploaded, read its content
                uploaded_file = request.files['file']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                # If no file uploaded, get user input from the form
                user_input = request.form.get('user_input', '')

            # Generate documentation using user input
            response = generate_documentation(user_input)
            
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        
            
            # Render the template with user input and response
            return render_template('docs.html', user_input=user_input, response=response)

        # Handle GET requests to render the initial form
        return render_template('docs.html', user_input="", response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"


def error_detection(user_input):
    # Combine static content with user input
    static_content = "Identify and explain syntax errors and provide suggestions for correction in the following code:"
    input_combined = f"{static_content} {user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/detect_error', methods=['GET', 'POST'])
def detect_error():
    try:
        if request.method == 'POST':
            user_input = ""
            if 'file' in request.files and request.files['file'].filename != '':
                # If a file is uploaded, read its content
                uploaded_file = request.files['file']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                # If no file uploaded, get user input from the form
                user_input = request.form.get('user_input', '')

            # Perform error detection using user input
            response = error_detection(user_input)
                
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        
            
            # Render the template with user input and response
            return render_template('error_detect.html', user_input=user_input, response=response)

        # Handle GET requests to render the initial form
        return render_template('error_detect.html', user_input="", response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"

def code_explanation(user_input):
    # Combine static content with user input
    static_content = "Explain the code line by line and finally give me a summary overview"
    input_combined = f"{static_content} {user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/explain_code', methods=['GET', 'POST'])
def explain_code():
    try:
        if request.method == 'POST':
            user_input = ""
            if 'file' in request.files and request.files['file'].filename != '':
                # If a file is uploaded, read its content
                uploaded_file = request.files['file']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                # If no file uploaded, get user input from the form
                user_input = request.form.get('user_input', '')

            # Perform code explanation using user input
            response = code_explanation(user_input)
            
                
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        
            # Render the template with user input and response
            return render_template('explain.html', user_input=user_input, response=response)

        # Handle GET requests to render the initial form
        return render_template('explain.html', user_input="", response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"
    

def code_formatting(user_input):
    # Combine static content with user input
    static_content = "Format the following code according to style guidelines and improve readability and consistency:\n"
    input_combined = f"{static_content}{user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/format_code', methods=['GET', 'POST'])
def format_code():
    try:
        if request.method == 'POST':
            user_input = ""
            file_input = request.files.get('file_input')

            if file_input and file_input.filename != '':
                # If a file is uploaded, read its content
                user_input = file_input.read().decode('utf-8')
            else:
                # If no file uploaded, get user input from the form
                user_input = request.form.get('user_input', '')

            # Perform code formatting using user input
            assistant_response = code_formatting(user_input)
            
            # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(assistant_response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
            

            # Render the template with user input and assistant's response
            return render_template('format.html', user_input=user_input, assistant_response=assistant_response)

        # Handle GET requests to render the initial form
        return render_template('format.html', user_input="", assistant_response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"
    


def code_templates(user_input):
    # Combine static content with user input
    static_content = "Provides templates or boilerplate code for common tasks or design patterns, accelerating development and finally explain it:\n"
    input_combined = f"{static_content}{user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/template_code', methods=['GET', 'POST'])
def template_code():
    try:
        if request.method == 'POST':
            user_input = ""
            if 'file' in request.files and request.files['file'].filename != '':
                # If a file is uploaded, read its content
                uploaded_file = request.files['file']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                # If no file uploaded, get user input from the form
                user_input = request.form.get('user_input', '')

            # Perform template code generation and explanation using user input
            response = code_templates(user_input)
            
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        

            # Render the template with user input and response
            return render_template('template.html', user_input=user_input, response=response)

        # Handle GET requests to render the initial form
        return render_template('template.html', user_input="", response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"


def code_testing(user_input):
    # Combine static content with user input
    static_content = "You are a helpful assistant.\nCode Testing assistant.\nAssists in writing, running, and debugging tests for code coverage and quality assurance.\n"
    input_combined = f"{static_content}Overview and Introduction for {user_input}.\nJust give me test cases for {user_input}.\nFinally explain the result."

    # Initialize chat session
    chat_session = model.start_chat()

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/test_code', methods=['GET', 'POST'])
def test_code():
    try:
        if request.method == 'POST':
            if 'file_input' in request.files:
                uploaded_file = request.files['file_input']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                user_input = request.form.get('user_input', '')

            response = code_testing(user_input)
            
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        
            return render_template('testing.html', user_input=user_input, response=response)

        # Handle GET requests to render the initial form
        return render_template('testing.html', user_input="", response="")

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/report_generate', methods=['GET', 'POST'])
def report_generate():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
            
        
        response = generate_report(user_input)
        
        # Generate a unique filename using UUID
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        
        return render_template('report.html', user_input=user_input, response=response)
    
    # Handle GET request here
    return render_template('report.html')


def generate_report(user_input):
    input_combined = (
        f"You are a helpful assistant. Code related assistant. "
        f"Give me Report generation for {user_input} with overview, introduction, methodology, results, performance analysis and conclusion etc.."
    )

    chat_session = model.start_chat(history=[])
    gemini_response = chat_session.send_message(input_combined)

    assistant_response = gemini_response.text.strip()
    return assistant_response

def convert_code(user_input, conversion_type):
    static_content = "Static content for code conversion."
    # Combine static content with user input and conversion type
    input_combined = f"{static_content} Convert code from {user_input} to {conversion_type}."

    # Initialize chat session
    chat_session = model.start_chat(history=[])

    # Send combined message to the model and get the response
    gemini_response = chat_session.send_message(input_combined)

    # Return the assistant's response
    return gemini_response.text

@app.route('/code_convert', methods=['GET', 'POST'])
def code_convert_page():
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        conversion_type = request.form['conversion_type']  # Retrieve conversion_type from form
        
        
        # Generate a unique filename using UUID
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        
        assistant_response = convert_code(user_input, conversion_type)  # Pass both user_input and conversion_type to convert_code function
        
        return render_template('convert.html', user_input=user_input, assistant_response=assistant_response)
    
    # Handle GET request here
    return render_template('convert.html')


def code_performance(user_input):
    static_content = "Analyze the following code and suggest optimizations for performance, such as memory usage or algorithm improvements:\n"
    input_combined = f"{static_content}{user_input}"

    # Initialize chat session
    chat_session = model.start_chat(history=[])
    gemini_response = chat_session.send_message(input_combined)

    return gemini_response.text

@app.route('/analyze_code', methods=['GET', 'POST'])
def analyze_code():
    try:
        if request.method == 'POST':
            if 'file' in request.files:
                uploaded_file = request.files['file']
                user_input = uploaded_file.read().decode('utf-8')
            else:
                user_input = request.form['user_input']
            
            # Call the function to perform code performance analysis
            response = code_performance(user_input)
            
            
                # Generate a unique filename using UUID
            filename = generate_uuid() + ".mp3"
            
            # Save response to an MP3 file
            save_response_to_mp3(response, filename)
            audio_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.name == 'nt':  # Windows
                os.system(f'start {audio_path}')
        
            # Render the template with user_input and response
            return render_template('performance.html', user_input=user_input, response=response)
        
        # Handle GET requests to render the initial form
        return render_template('performance.html', user_input="", response=None)

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    
#editor

@app.route('/editor')
def editor():
    return render_template('editor.html')   


@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        user_input = request.json.get('user_input', '')

        # Check if the word "python" is present in the user input
        is_python_code = 'python' in user_input.lower()

        # Create a chat completion using the GenAI model
        input_combined = f"You are a helpful assistant. give me code related responses {user_input}"
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Get the assistant's reply
        assistant_response = gemini_response.text.split('```')[1].strip()

        # Comment out the code if the word "python" is present
        if is_python_code:
            assistant_response = f'# {assistant_response}'

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@app.route('/snippet', methods=['POST'])
def snippet_code():
    try:
        user_input = request.json.get('user_input', '')

        # Create a chat completion using the GenAI model
        input_combined = f"You are a helpful assistant. Give me code related responses. Give me a Python code snippet with function for {user_input}"
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Extract the assistant's reply
        response_parts = gemini_response.text.split('```')
        if len(response_parts) > 1:
            # If there's a code block, extract it
            code_snippet = response_parts[1].strip()
        else:
            # If no code block, comment the entire response
            code_snippet = '\n'.join([f'# {line}' for line in gemini_response.text.split('\n')])

        # Check for additional text before and after the code block and comment it out
        if len(response_parts) > 2:
            pre_text = '\n'.join([f'# {line}' for line in response_parts[0].strip().split('\n')])
            post_text = '\n'.join([f'# {line}' for line in response_parts[2].strip().split('\n')])
            assistant_response = f"{pre_text}\n{code_snippet}\n{post_text}".strip()
        else:
            assistant_response = code_snippet

        # Insert # before every occurrence of the word "python"
        assistant_response = assistant_response.replace('python', '#python')

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/debug', methods=['POST'])
def error_corrections_suggestions():
    try:
        input_code = request.json.get('input_code', '')

        # Create a chat completion using the GenAI model
        input_combined = f"You are a helpful assistant for error prediction and correction. Predict errors and warnings in the following python code, and explain them: {input_code}"
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Extract the assistant's reply
        response_parts = gemini_response.text.split('```')
        if len(response_parts) > 1:
            # If there's a code block, extract it
            assistant_response = response_parts[1].strip()
        else:
            # If no code block, comment the entire response
            assistant_response = '\n'.join([f'# {line}' for line in gemini_response.text.split('\n')])

        # Ensure "python" is commented
        assistant_response = assistant_response.replace('python', '# python')

        return jsonify({'assistant_response': assistant_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/refactor', methods=['POST'])
def code_refactor():
    try:
        refactor_input = request.json.get('refactor_input', '')

        # Create a chat completion using the GenAI model
        input_combined = f"You are a helpful assistant for Python code review and quality improvement. Analyzing Python code for potential improvements. Providing suggestions for enhancing code quality. {refactor_input}"
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Extract the assistant's reply
        response_parts = gemini_response.text.split('```')
        if len(response_parts) > 1:
            # If there's a code block, extract it
            assistant_response = response_parts[1].strip()
        else:
            # If no code block, comment the entire response
            assistant_response = '\n'.join([f'# {line}' for line in gemini_response.text.split('\n')])

        # Ensure "python" is commented
        assistant_response = assistant_response.replace('python', '# python')

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/documentation', methods=['POST'])
def code_document():
    try:
        document_input = request.json.get('document_input', '')

        # Combine the input with the necessary instructions
        input_combined = (
            "You are a knowledgeable assistant specializing in project-based code documentation. "
            "Analyze the input code to generate comprehensive project documentation. "
            "Provide detailed documentation based on the project's code structure and functionality. "
            "Incorporate best practices and project-specific information into the documentation. "
            f"{document_input}"
        )

        # Create a chat completion using the GenAI model
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Get the assistant's reply
        assistant_response = gemini_response.text.strip()

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/convert', methods=['POST'])
def code_conversion():
    try:
        # Get the input code for conversion
        conversion_input = request.json.get('conversion_input', '')

        # Check if the input code contains a comment specifying the target language
        target_language = None
        input_lines = conversion_input.split('\n')
        for line in input_lines:
            if line.strip().startswith('#convert to '):
                target_language = line.strip().replace('#convert to ', '')
                break

        if target_language:
            # Create a chat completion using the GenAI model with specified target language
            input_combined = f"You are a helpful assistant. Convert the following code to {target_language}: {conversion_input}"
            chat_session = model.start_chat(history=[])
            gemini_response = chat_session.send_message(input_combined)

            # Extract the assistant's reply
            assistant_response = gemini_response.text.split('```')[1].strip()

            # Comment out the code if it contains certain keywords
            keywords = ('java', 'c', 'cpp', 'javascript', 'python','javascript')
            if any(keyword in assistant_response.lower() for keyword in keywords):
                assistant_response = f"# {assistant_response}"

            return jsonify({
                'input_code': conversion_input,
                'output_code': assistant_response
            })
        else:
            return jsonify({'error': 'Target language not specified in input code.'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/explain', methods=['POST'])
def code_explain():
    try:
        input_code = request.json.get('input_code', '')

        # Create a chat completion using the GenAI model
        input_combined = f"You are a helpful assistant for code explanation. Just explain line by line. Brief explanation for user input code. {input_code}"
        chat_session = model.start_chat(history=[])
        gemini_response = chat_session.send_message(input_combined)

        # Get the assistant's reply
        assistant_response = gemini_response.text.strip()

        # Wrap assistant_response in comments
        commented_response = '\n'.join(['# ' + line for line in assistant_response.split('\n')])
        full_response = f"# Here is the line by line explanation for the above code:\n{commented_response}"

        return jsonify({'assistant_response': full_response})

    except Exception as e:
        return jsonify({'error': str(e)})



#compile and run

@app.route('/executeCode', methods=['POST'])
def execute_code():
    try:
        code = request.form['code']
        input_value = request.form['input']  # Get input value
        exec_result = {}
        sys.stdout = mystdout = StringIO()

        # If input is provided, execute the code with input values
        if input_value:
            input_values = input_value.split()  # Split input on spaces
            exec(code, {'input': lambda prompt="": input_values.pop(0)}, exec_result)
        else:
            # If no input provided, execute the code directly
            exec(code, {}, exec_result)

        sys.stdout = sys.__stdout__
        output = mystdout.getvalue()
        return output
    except Exception as e:
        return 'Error: ' + str(e)
    
@app.route('/executePython', methods=['POST'])
def execute_python():
    python_code = request.json['code']

    try:
        # Execute the Python code using subprocess
        result = subprocess.run(['python', '-c', python_code], capture_output=True, text=True)
        output = result.stdout.strip()
        error = result.stderr.strip() if result.stderr else None
    except Exception as e:
        output = None
        error = str(e)

    return jsonify({'output': output, 'error': error})

     

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import openai
from gtts import gTTS
import uuid
import os 

app = Flask(__name__)

# Set your OpenAI GPT-3 API key here
api_key = "YOUR_API_KEY"


OUTPUT_FOLDER = "output"

# Initialize the OpenAI client with your API key
openai.api_key = api_key

def generate_uuid():
    return str(uuid.uuid4())

def save_response_to_mp3(response, filename):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    filepath = os.path.join(OUTPUT_FOLDER, filename)
    tts = gTTS(text=response, lang='en')
    tts.save(filepath)
    
def code_generation(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code Generation assistant."},
            {"role": "system", "content": "Give me code."},
            {"role": "user", "content": user_input}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

def code_performance(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code Performance assistant."},
            {"role": "system", "content": "Analyzes code performance and suggests optimizations for efficiency, such as memory usage or algorithm improvements"},
            {"role": "system", "content": f"Enhance the code performance for {user_input}."},
            {"role": "user", "content": "Finally explain the changes ."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

def error_detection(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"check code {user_input}"},
                {"role": "user", "content": f"If error exist correct the error or issues {user_input}"},
             {"role": "system", "content": "Correct the error and issuse and explain the error."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    print(assistant_response)
    return assistant_response


def code_testing(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code Testing assistant."},
            {"role": "system", "content": "Assists in writing, running, and debugging tests for code coverage and quality assurance."},
            {"role": "system", "content": f"Overview and Introduction for {user_input}."},
             {"role": "system", "content": f"Just give me test cases for {user_input}."},
            {"role": "user", "content": "Finally explain the result ."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

def code_templates(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code related assistant."},
            {"role": "user", "content": "Provides templates or boilerplate code for common tasks or design patterns, accelerating development ."},
            {"role": "system", "content": f"Overview and Explain line by line for {user_input}."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

def code_formatting(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
           
               {"role": "system", "content": "You are a helpful assistant for Python code review and quality improvement."},
               {"role": "system", "content": "Analyzing Python code for potential improvements."},
               {"role": "system", "content": "Providing suggestions for enhancing code quality."},
               {"role": "user", "content": user_input},
               {"role": "system", "content": "Please suggest code formatting improvements."}  # Request for suggestions
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

def code_explanation(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code Explaination assistant."},
            {"role": "system", "content": f"Overview and Explain line by line for {user_input}."},
            {"role": "user", "content": "Finally explain the summary ."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response


def code_documentation(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code documentation assistant."},
             {"role": "system", "content": "Generates or suggests documentation for functions, classes, and methods based on code analysis"},
            {"role": "system", "content": "Deep Explanation for documentation."},
            {"role": "user", "content": f"Give me Project documentation for {user_input}."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response


@app.route('/docs_code', methods=['GET', 'POST'])
def docs_code():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        response = code_documentation(user_input)
        return render_template('docs.html', user_input=user_input, response=response)
    
    # Handle GET request
    return render_template('docs.html')

@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
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
    return render_template('generate.html')

@app.route('/performance', methods=['GET', 'POST'])
def performance():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']

        response = code_performance(user_input)
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('performance.html', user_input=user_input, response=response)
    return render_template('performance.html')


@app.route('/detect_error', methods=['GET', 'POST'])
def detect_error():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')  # Handle form input
        
        if 'file' in request.files:
            # Handle file upload
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        
        response = error_detection(user_input)  # Call your error detection function
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('error_detect.html', user_input=user_input, response=response)
    
    return render_template('error_detect.html')

@app.route('/format_code', methods=['GET', 'POST'])
def format_code():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        file_input = request.files.get('file_input')
        
        if file_input:
            user_input = file_input.read().decode('utf-8')

        assistant_response = code_formatting(user_input)  # Assuming code_formatting function is defined elsewhere
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('format.html', user_input=user_input, assistant_response=assistant_response)
    
    return render_template('format.html')


@app.route('/explain_code', methods=['GET','POST'])
def explain_code():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
            
        response = code_explanation(user_input)
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('explain.html', user_input=user_input, response=response)
    return render_template('explain.html')


@app.route('/test_code', methods=['GET', 'POST'])
def test_code():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        response = code_testing(user_input)
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        return render_template('testing.html', user_input=user_input, response=response)
    
    # Handle GET request
    return render_template('testing.html')



@app.route('/template_code', methods=['GET', 'POST'])
def template_code():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        response = code_templates(user_input)
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('template.html', user_input=user_input, response=response)
    
    # Handle GET request here
    return render_template('template.html')  








def generate_report(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code related assistant."},
            {"role": "user", "content": "Report generation for project with overview,introduction,methodology,results,performance analysis and conclusion etc.."},
            {"role": "system", "content": f"generate project report for {user_input}."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response





@app.route('/report_generate', methods=['GET', 'POST'])
def report_generate():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        response = generate_report(user_input)
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('report.html', user_input=user_input, response=response)
    
    # Handle GET request here
    return render_template('report.html')  




def convert_code(user_input, conversion_type):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code related assistant."},
            {"role": "user", "content": f"Convert code from {user_input} to {conversion_type}."},
            {"role": "system", "content": f"Provide the converted code for {user_input}."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response





@app.route('/code_convert', methods=['GET', 'POST'])
def code_convert():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        conversion_type = request.form['conversion_type']  # Retrieve conversion_type from form
        
        response = convert_code(user_input, conversion_type)  # Pass both user_input and conversion_type to code_templates function
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        return render_template('convert.html', user_input=user_input, response=response)
    
    # Handle GET request here
    return render_template('convert.html')



if __name__ == '__main__':
    app.run(debug=True)

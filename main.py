from flask import Flask, render_template, request
from gtts import gTTS
import uuid
import os 
from flask import jsonify
from io import StringIO
import sys
import openai
import subprocess


app = Flask(__name__)



openai.api_key = 'YOUR_API_KEY'

OUTPUT_FOLDER = "output"

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
    messages = [
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




def generate_report(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Code related assistant."},
            {"role": "user", "content": f"Give me Report generation for{user_input} with overview,introduction,methodology,results,performance analysis and conclusion etc.."},
            {"role": "system", "content": f"generate project report for {user_input}."}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response



@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')

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
    return render_template('generate.html')

@app.route('/performance', methods=['GET', 'POST'])
def performance():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']

        assistant_response = code_performance(user_input)
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('performance.html', user_input=user_input, assistant_response=assistant_response)
    return render_template('performance.html')


@app.route('/detect_error', methods=['GET', 'POST'])
def detect_error():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')  # Handle form input
        
        if 'file' in request.files:
            # Handle file upload
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        
        assistant_response = error_detection(user_input)  # Call your error detection function
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
            
        return render_template('error_detect.html', user_input=user_input, assistant_response=assistant_response)
    
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
            
        return render_template('explain.html', user_input=user_input, assistant_response=response)
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
        return render_template('testing.html', user_input=user_input, assistant_response=response)
    
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
            
        return render_template('template.html', user_input=user_input, assistant_response=response)
    
    # Handle GET request here
    return render_template('template.html')  







#editor
@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        user_input = request.json.get('user_input', '')

        # Check if the word "python" is present in the user input or assistant response
        is_python_code = 'python' in user_input.lower()

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "give me code related responses"},
                {"role": "user", "content": user_input}
            ]
        )

        # Get the assistant's reply
        assistant_response = response['choices'][0]['message']['content'].split('```')[1].strip()

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

     

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "give me code related responses"},
                 {"role": "user", "content": "give me python code with function"},
                 {"role": "user", "content": f"Give me a Python code snippet with function for {user_input}"}

            ]
        )
        


        # Get the assistant's reply
        assistant_response = response['choices'][0]['message']['content'].split('```')[1].strip()
        
        if "python" in assistant_response.lower():
            assistant_response = f"# {assistant_response}"


 

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)})
    

    
    
@app.route('/debug', methods=['POST'])
def error_corrections_suggestions():
    try:
        input_code = request.json.get('input_code', '')

     

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for error prediction and correction."},
                {"role": "system", "content": "Prediciting errors and warnings"},
                {"role": "system", "content": "python related errors and warnings"},
                {"role": "system", "content": "explain error and warnings"},
                {"role": "user", "content": input_code}

            ]
        )
        


        assistant_response = response['choices'][0]['message']['content']

        # Get the assistant's reply
        assistant_response = response['choices'][0]['message']['content'].split('```')[1].strip()
        
        if "python" in assistant_response.lower():
            assistant_response = f"# {assistant_response}"


 

        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)})
    

    
    
   
@app.route('/refactor', methods=['POST'])
def code_refactor():
    try:
        refactor_input = request.json.get('refactor_input', '')

     

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
               {"role": "system", "content": "You are a helpful assistant for Python code review and quality improvement."},
               {"role": "system", "content": "Analyzing Python code for potential improvements."},
               {"role": "system", "content": "Providing suggestions for enhancing code quality."},
                {"role": "user", "content": refactor_input}
            ]
        )
        


        assistant_response = response['choices'][0]['message']['content']

        # Get the assistant's reply
        assistant_response = response['choices'][0]['message']['content'].split('```')[1].strip()
        
        if "python" in assistant_response.lower():
            assistant_response = f"# {assistant_response}"


        return jsonify({'assistant_response': assistant_response})

    except Exception as e:
        return jsonify({'error': str(e)})
    


@app.route('/documentation', methods=['POST'])
def code_document():
    try:
        document_input = request.json.get('document_input', '')

     

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant specializing in project-based code documentation."},
                {"role": "system", "content": "Analyzing the input code to generate comprehensive project documentation."},
                {"role": "system", "content": "Providing detailed documentation based on the project's code structure and functionality."},
                {"role": "system", "content": "Incorporating best practices and project-specific information into the documentation."},
                {"role": "user", "content": document_input}
            ]


        )
        
        assistant_response = response['choices'][0]['message']['content']

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

        print('Target Language:', target_language)  # Debugging

        if target_language:
            # Create a code conversion using the GPT-3.5-turbo model with specified target language
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Converting code to {target_language}."},
                      {"role": "system", "content": "convert the input code"},
                        {"role": "system", "content": f"change the code from python to {target_language}. "},
                    {"role": "user", "content": conversion_input}
                ]
            )

            # Extract the assistant's reply
            assistant_response = response['choices'][0]['message']['content']
             # Get the assistant's reply
            assistant_response = response['choices'][0]['message']['content'].split('```')[1].strip()
        
            keywords = ('java', 'c', 'cpp' , 'javascript' , 'python' )

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

        # Create a chat completion using the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for code explanation."},
                {"role": "system", "content": "Just explain line by line."},
                {"role": "system", "content": "Brief explanation for user input code."},
                {"role": "user", "content": input_code}
            ]
        )

        assistant_response = response['choices'][0]['message']['content']

        # Wrap assistant_response in comments
        commented_response = '\n'.join(['# ' + line for line in assistant_response.split('\n')])
        full_response = f"# Here is the line by line explanation for the above code:\n{commented_response}"

        # Generate a unique filename using uuid for the audio file
        audio_filename = str(uuid.uuid4()) + ".mp3"
        
        # Specify the folder path for saving the audio file
        output_folder = 'explain_output'

        # Create the folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Initialize the gTTS object with the full_response text
        tts = gTTS(text=full_response, lang='en')  # Assuming English language ('en')

        # Save the synthesized speech to the specified folder with the unique filename
        audio_path = os.path.join(output_folder, audio_filename)
        tts.save(audio_path)

        
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        else:
            return jsonify({'error': 'Unsupported operating system'})

        return jsonify({'assistant_response': full_response, 'audio_filename': audio_path})

    except Exception as e:
        return jsonify({'error': str(e)})
    
    
    
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
def code_convert_page():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            user_input = uploaded_file.read().decode('utf-8')
        else:
            user_input = request.form['user_input']
        
        conversion_type = request.form['conversion_type']  # Retrieve conversion_type from form
        
        assistant_response = convert_code(user_input, conversion_type)  # Pass both user_input and conversion_type to code_templates function
        
        filename = generate_uuid() + ".mp3"
        
        # Save response to an MP3 file
        save_response_to_mp3(assistant_response, filename)
        audio_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.name == 'nt':  # Windows
            os.system(f'start {audio_path}')
        
        return render_template('convert.html', user_input=user_input, assistant_response=assistant_response)
    
    # Handle GET request here
    return render_template('convert.html')



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

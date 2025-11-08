from flask import Flask, render_template, request, jsonify
import openai
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

api_key = "YOUR_API_KEY"
openai.api_key = api_key



@app.route('/index')
def index():
    return render_template('index.html')

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
    
if __name__ == '__main__':
    app.run(debug=True)
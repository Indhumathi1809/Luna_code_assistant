# AI-Powered Code Editor

An AI-powered code editor named as **Luna** built with Flask and HTML templates that helps developers generate code, validate existing code, detect errors, and fix bugs using OpenAI and Google Gemini models.

## Features

- **AI Code Generation:** Generate code from natural language prompts.
- **Code Validation:** Validate code structure and identify potential issues.
- **Error Detection:** Analyze code and identify syntax errors and common bugs.
- **Automatic Error Fixing:** Suggest or generate corrected code.
- **Code Explanation:** Understand code functionality through AI-generated explanations.
- **Multiple AI Providers:** Integrate OpenAI and Google Gemini.
- **Web-Based Interface:** Interact with the editor through Flask-rendered HTML templates.
- **Error Handling:** Display meaningful messages for API failures and invalid inputs.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Jinja2 Templates
- **AI Providers:** OpenAI API, Google Gemini API
- **Configuration:** Environment variables
- **Version Control:** Git

## Project Structure

```text
ai-code-editor/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── services/
│   ├── __init__.py
│   ├── openai_service.py
│   └── gemini_service.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── editor.js
│   └── images/
└── README.md
```

*The structure above is a suggested layout; adjust it to match your actual project.*

## Prerequisites

- Python 3.10 or later
- pip
- An OpenAI API key and/or Google Gemini API key
- Internet connection for AI API requests

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-code-editor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
```

Replace the placeholder values with your own credentials. Keep the `.env` file private and never commit it to version control.

### 5. Run the Application

```bash
python app.py
```

Open the local URL displayed by Flask, typically:

`http://127.0.0.1:5000`

## Application Workflow

1. Enter a coding requirement or paste existing code.
2. Select an AI provider, OpenAI or Gemini.
3. Choose an operation: generate, validate, explain, or fix code.
4. Send the request to the Flask backend.
5. The backend processes the request through the selected AI service.
6. Display the generated code, validation results, explanations, or suggested fixes.
7. Review the output and copy or reuse the code as needed.

## AI Integration

### OpenAI

Use the OpenAI API to generate code, review existing code, explain functionality, and suggest fixes.

### Google Gemini

Use the Gemini API for code generation, code analysis, validation assistance, and error correction.

Both providers should be integrated through separate service modules so that API calls, model configuration, and error handling remain easy to maintain.

## Code Validation and Error Fixing

The application can support the following validation workflow:

- Check syntax and formatting.
- Identify common coding errors.
- Analyze potential bugs and logic issues.
- Generate corrected code and explain the changes.
- Allow users to review the proposed fixes before applying them.

**Important:** AI-generated validation is not a guarantee of correctness. Use language-specific linters, parsers, tests, and security checks where appropriate.

## Security Best Practices

- Store API keys in environment variables.
- Never expose API keys in frontend JavaScript or HTML.
- Disable Flask debug mode in production.
- Validate user input and limit request sizes.
- Add authentication and rate limiting where needed.
- Do not execute generated code on the server without strong isolation and sandboxing.
- Review AI-generated code before using it in production.

## Troubleshooting

| Issue | Suggested Solution |
|---|---|
| Missing API key | Check the `.env` file and environment configuration. |
| API request failure | Verify the API key, network connection, provider status, and usage limits. |
| Module not found | Activate the virtual environment and install requirements. |
| Flask template not found | Confirm templates are inside the `templates/` directory. |
| Generated code contains errors | Validate the output and request a correction or run automated tests. |

## Future Enhancements

- Syntax highlighting and a richer code editor.
- Support for multiple programming languages.
- Code execution in a secure sandbox.
- Git integration and version history.
- Streaming AI responses.
- Automated test generation.
- Side-by-side code comparison.
- Download generated code and project files.

## License

Add the applicable license before distributing the project.

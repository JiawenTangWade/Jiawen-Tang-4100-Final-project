from flask import Flask, request, jsonify, render_template, session
import openai
import os
import json
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

# Set OpenAI API key
openai.api_key = "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"

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load JSON data
with open('formatted_data.json', 'r') as f:
    data = json.load(f)

def read_file_content(file_path):
    """Read the content of the uploaded file"""
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        reader = PdfReader(file_path)
        content = ''.join(page.extract_text() for page in reader.pages)
    elif file_extension.lower() == '.docx':
        doc = Document(file_path)
        content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    else:
        with open(file_path, 'r') as file:
            content = file.read()
    return content

@app.route('/')
def index():
    # Initialize chat history
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('user_input')
    uploaded_file = request.files.get('file')

    # Initialize chat history
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Handle uploaded file
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)
        file_content = read_file_content(file_path)
        user_input += f"\n\nUploaded file content:\n{file_content}"

    # Construct chat history
    chat_history = session['chat_history']
    chat_history.append({"role": "user", "content": user_input})

    # Check if the request is related to JSON data
    if "list all projects" in user_input.lower() or "all project names" in user_input.lower():
        project_names = [project['Project Name'] for project in data]
        answer = "Here are the project names:\n- " + "\n- ".join(project_names)
        chat_history.append({"role": "assistant", "content": answer})
        session['chat_history'] = chat_history  # Update chat history
        return jsonify({'answer': answer})

    if "details of project" in user_input.lower():
        # Extract project name
        project_name = user_input.lower().replace("details of project", "").strip()
        project_details = next((project for project in data if project['Project Name'].lower() == project_name), None)
        if project_details:
            answer = f"Details of {project_name}:\n{json.dumps(project_details, indent=4)}"
        else:
            answer = f"No project found with the name '{project_name}'."
        chat_history.append({"role": "assistant", "content": answer})
        session['chat_history'] = chat_history  # Update chat history
        return jsonify({'answer': answer})

    # Call OpenAI API
    try:
        # Append chat history to the prompt
        prompt = "The following is a conversation with an assistant. The assistant is helpful, creative, clever, and very friendly.\n\n"
        for exchange in chat_history:
            role = "User" if exchange["role"] == "user" else "Assistant"
            prompt += f"{role}: {exchange['content']}\n"

        # Current user input
        prompt += f"User: {user_input}\nAssistant:"

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Replace with a supported model
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()

        # Update chat history
        chat_history.append({"role": "assistant", "content": answer})
        session['chat_history'] = chat_history

        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f"API call failed: {str(e)}"})

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    session.pop('chat_history', None)
    return jsonify({'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True)

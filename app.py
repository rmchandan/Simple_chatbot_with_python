from flask import Flask, render_template, request, jsonify
import json
import random
import os  # Import the os module to work with file paths

app = Flask(__name__)

# Get the full path to the "templates" folder
templates_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

def load_responses():
    try:
        with open("responses.json", "r") as file:
            responses = json.load(file)
    except FileNotFoundError:
        responses = {}
    return responses

def save_responses(responses):
    try:
        with open("responses.json", "w") as file:
            json.dump(responses, file, indent=4)
    except Exception as e:
        print(f"Error saving responses: {e}")

def add_response(category, pattern, response):
    responses = load_responses()
    if category in responses:
        responses[category]["patterns"].append(pattern)
        responses[category]["responses"].append(response)
    else:
        responses[category] = {"patterns": [pattern], "responses": [response]}
    
    if response != "I'm not sure how to respond to that.":
        save_responses(responses)

# Update the app configuration to use the full path to the "templates" folder
app.config['TEMPLATE_FOLDER'] = templates_folder

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("user_input").lower()

    responses = load_responses()
    response = None
    for category, data in responses.items():
        patterns = data["patterns"]
        for i, pattern in enumerate(patterns):
            if pattern in user_input:
                response = data["responses"][i]
                break

    if response is None:
        default_responses = responses.get("default", {"patterns": [], "responses": []})
        response = random.choice(default_responses["responses"])

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run( debug=True)


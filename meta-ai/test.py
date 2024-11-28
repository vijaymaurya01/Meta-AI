from flask import Flask, request, jsonify
from meta_ai_api import MetaAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, strict_origin_when_cross_origin=True)

# Initialize Meta AI API
ai = MetaAI()

@app.route("/generate", methods=["POST"])
def generate_response():
    # Get the input message from the request body
    api_description = request.json.get("prompt")

    # Check if the input is provided
    if not api_description:
        return jsonify({"error": "API description is required"}), 400

    # Define the custom prompt for test case generation
    prompt = f"""
    Generate structured test cases for the following API:
    {api_description}
    
    Format:
    [
        {{
            "title": "Test case title",
            "description": "Brief explanation of the test",
            "input": "Details of the input to the API",
            "expected_output": "Expected result from the API",
            "notes": "Any additional notes"
        }},
        ...
    ]
    """

    # Generate a response using Meta AI API
    response = ai.prompt(message=prompt)

    # Return the response
    return jsonify({"test_cases": response})

if __name__ == "__main__":
    app.run(port=5001, debug=True)

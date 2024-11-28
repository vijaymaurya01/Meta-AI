from flask import Flask, request, jsonify
from meta_ai_api import MetaAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Initialize Meta AI API
ai = MetaAI()

@app.route("/generate", methods=["POST"])
def generate_response():
    try:
        # Get the input message from the request body
        prompt = request.json.get("prompt")
        
        # Validate the input
        if not prompt:
            return jsonify({
                "status": "error",
                "message": "Prompt is required."
            }), 400
        
        # Custom prompt to instruct AI to respond in Markdown format
        custom_prompt = """
       Generate a response to the following user query in Markdown format. Ensure the response is clear, concise, and well-structured. Use appropriate Markdown syntax for headings, lists, code blocks, and any other formatting elements as needed.
        """
        
        # Combine the custom prompt with the user's prompt
        full_prompt = custom_prompt + "\n\n" + prompt
        
        # Generate the response using MetaAI with the full prompt
        response = ai.prompt(message=full_prompt)
        response_message = response.get("message", "")
        print("Simple message --- ", response_message)
        
        # Format the message as Markdown
        formatted_message = f"### Response\n\n{response_message}"
        # print("Formated message --- ", formatted_message)
        
        # If the response contains code, wrap it in Markdown code blocks
        if "```" not in response_message and "code" in prompt.lower():
            formatted_message = f"{response_message}"
        
        # Build the final response
        final_response = {
            "status": "success",
            "data": {
                "prompt": prompt,
                "response": {
                    "message": formatted_message,
                    "media": response.get("media", []),
                    "sources": response.get("sources", [])
                }
            }
        }
        
        # Return the response in a structured format
        return jsonify(final_response), 200
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)

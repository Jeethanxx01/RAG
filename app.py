from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import logging
from movieapp.retrieval_generation import generation
from movieapp.ingest import ingestdata

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

load_dotenv()

# Initialize the vector store and chain
try:
    vstore = ingestdata("done")
    chain = generation(vstore)
    logger.info("Successfully initialized vector store and chain")
except Exception as e:
    logger.error(f"Error initializing vector store or chain: {str(e)}")
    raise

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def get_bot_response():
    try:
        user_message = request.form["msg"]
        logger.info(f"Received query: {user_message}")
        
        # Get response from the chain
        response = chain.invoke(user_message)
        
        # Return the response as JSON
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify([{"title": "Error", "overview": "Sorry, I encountered an error. Please try again."}]), 500

if __name__ == "__main__":
    app.run(debug=True)
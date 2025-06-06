from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from moviebot.retrieval_generation import generation, is_movie_related, check_query_domain
from moviebot.ingest import ingestdata
import json

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize the vector store and generation chain
print("Initializing movie recommendation system...")
vstore = ingestdata("done")
chain = generation(vstore)
print("System initialized successfully!")

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input = msg
        
        print(f"Processing query: {input}")
        
        # First round: Check if the question is movie-related using AI
        is_related, confidence, explanation = check_query_domain(input)
        print(f"Domain check result - is_related: {is_related}, confidence: {confidence}, explanation: {explanation}")
        
        if not is_related:
            return json.dumps([{
                "title": "Domain Restriction",
                "genre": "System Message",
                "rating": 0,
                "overview": f"I'm a movie recommendation application. {explanation} Please ask me about movies, TV shows, or related entertainment topics!",
                "poster_url": "",
                "confidence": confidence
            }])
        
        # Second round: If movie-related, proceed with RAG model
        print("Query is movie-related, proceeding with RAG model...")
        result = chain.invoke(input)
        print(f"RAG model response: {result}")
        
        # Extract movie information from the response
        results = vstore.similarity_search(input, k=1)  # Only get the most relevant movie
        print(f"Found {len(results)} similar movies")
        
        if not results:
            return json.dumps([{
                "title": "No Movies Found",
                "genre": "System Message",
                "rating": 0,
                "overview": "I don't have any information about that right now. Could you try asking about something else?",
                "poster_url": "",
                "confidence": confidence,
                "explanation": "No matching movies found in the database."
            }])
        
        # Format the results as a list of movie dictionaries
        movies = []
        for doc in results:
            # Extract the movie title from the metadata
            movie_title = doc.metadata.get("title", "Unknown Title")
            
            # Create a more focused explanation for this specific movie
            focused_explanation = f"I recommend {movie_title}. It's a {doc.metadata.get('genre', 'Unknown Genre')} movie with a rating of {doc.metadata.get('rating', 0.0)}. {doc.page_content}"
            
            movie = {
                "title": movie_title,
                "genre": doc.metadata.get("genre", "Unknown Genre"),
                "rating": doc.metadata.get("rating", 0.0),
                "overview": doc.page_content,
                "poster_url": doc.metadata.get("poster_url", ""),
                "confidence": confidence,  # Include the confidence score from domain check
                "explanation": focused_explanation  # Use the focused explanation instead of the RAG model response
            }
            movies.append(movie)
        
        print("User Query:", input)
        print("Bot Response:", result)
        return json.dumps(movies)
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return json.dumps([{
            "title": "Error",
            "genre": "System Message",
            "rating": 0,
            "overview": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
            "poster_url": "",
            "confidence": 0.0
        }])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
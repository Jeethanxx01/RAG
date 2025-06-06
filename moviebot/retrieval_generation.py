from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from moviebot.ingest import ingestdata
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()

def check_query_domain(question):
    # Initialize the Gemini model for domain check
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.1,  # Lower temperature for more consistent results
        max_output_tokens=1024
    )

    # Define the prompt for domain checking
    DOMAIN_CHECK_TEMPLATE = """
    You are a domain classifier for a movie recommendation system.
    Your task is to determine if the given query is related to movies, TV shows, or entertainment content.
    
    Consider the following domains as valid:
    - Movies and films
    - TV shows and series
    - Streaming services
    - Actors and directors
    - Movie genres and categories
    - Movie ratings and reviews
    - Movie recommendations
    - Entertainment industry
    
    For the query: "{question}"
    
    Respond with ONLY a JSON object in this exact format:
    {{
        "is_movie_related": true/false,
        "confidence": 0.0-1.0,
        "explanation": "brief explanation"
    }}
    
    Do not include any other text or explanation outside the JSON object.
    """

    prompt = ChatPromptTemplate.from_template(DOMAIN_CHECK_TEMPLATE)
    
    # Create the chain for domain checking
    domain_chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        # Get the response and parse it as JSON
        response = domain_chain.invoke(question)
        
        # Clean the response to ensure it's valid JSON
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        result = json.loads(response)
        
        # Validate the response structure
        if not isinstance(result, dict):
            raise ValueError("Response is not a dictionary")
        if "is_movie_related" not in result:
            raise ValueError("Missing is_movie_related field")
        if "confidence" not in result:
            raise ValueError("Missing confidence field")
        if "explanation" not in result:
            raise ValueError("Missing explanation field")
            
        # Ensure confidence is a float between 0 and 1
        result["confidence"] = float(result["confidence"])
        if not 0 <= result["confidence"] <= 1:
            result["confidence"] = 0.5
            
        return result["is_movie_related"], result["confidence"], result["explanation"]
    except Exception as e:
        print(f"Error in domain check: {str(e)}")
        # For movie-related queries, default to True with low confidence
        if any(keyword in question.lower() for keyword in ['movie', 'film', 'watch', 'show', 'series', 'actor', 'director']):
            return True, 0.5, "Query appears to be movie-related based on keywords"
        return False, 0.0, "Unable to process query properly"

def is_movie_related(question):
    # Use the AI-based domain check instead of keyword matching
    is_related, confidence, explanation = check_query_domain(question)
    return is_related

def generation(vstore):
    # Create a retriever that gets the 5 most relevant documents
    retriever = vstore.as_retriever(search_kwargs={"k": 5})

    # Define the prompt template for the movie bot
    MOVIE_BOT_TEMPLATE = """
    You are an expert movie recommendation bot with deep knowledge of films across all genres and eras.
    You analyze movie titles, overviews, genres, and ratings to provide accurate and helpful responses.
    
    When recommending movies:
    1. Focus on recommending ONE movie that best matches the user's request
    2. Provide a clear, concise explanation of why you're recommending this specific movie
    3. Include the movie's rating and genre in your response
    4. Keep your explanation focused and engaging, highlighting what makes this movie special
    5. If the user asks about specific genres or types of movies, focus on those aspects
    
    Format your response like this:
    "I recommend [Movie Title]. It's a [genre] movie with a rating of [rating]. [Brief, engaging explanation of why this movie is worth watching, focusing on its unique aspects and appeal]"
    
    Important: Make sure your explanation matches the movie being recommended in the context.
    Do not recommend a different movie than what is shown in the context.
    
    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(MOVIE_BOT_TEMPLATE)

    # Get the Google API key from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.7,
        max_output_tokens=2048
    )

    # Create the chain that combines retrieval and generation
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == '__main__':
    print("Initializing movie recommendation system...")
    
    # Initialize the vector store
    vstore = ingestdata("done")
    
    # Create the generation chain
    chain = generation(vstore)
    
    # Test the system with a single query
    test_query = "What are some highly rated action movies?"
    print(f"\nTesting with query: {test_query}")
    print("\nResponse:", chain.invoke(test_query)) 
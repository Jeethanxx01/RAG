from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from movieapp.ingest import ingestdata
import os
from dotenv import load_dotenv

load_dotenv()

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 10})  # Increased k for better coverage

    MOVIE_BOT_TEMPLATE = """
    You are an expert movie recommendation assistant with deep knowledge of films across all genres and eras.
    Your task is to provide personalized movie recommendations and information based on the context provided.
    
    Guidelines:
    1. Use the provided movie context to give accurate and relevant recommendations
    2. Include key details like release year, director, and main actors when relevant
    3. Explain why you're recommending specific movies
    4. If the query is about a specific movie, provide detailed information about it
    5. For genre-based queries, suggest diverse movies within that genre
    6. Keep responses concise but informative
    7. If you can't find relevant information in the context, say so politely
    8. Format your response as a list of movies, with each movie having:
       Title: [Movie Title]
       Genre: [Movie Genre]
       Rating: [Rating out of 10]
       Overview: [Movie overview]
       Explanation: [Why you're recommending this movie]

    CONTEXT:
    {context}

    USER QUERY: {question}

    YOUR RESPONSE:
    """

    prompt = ChatPromptTemplate.from_template(MOVIE_BOT_TEMPLATE)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.7,
        max_output_tokens=2048,
        top_p=0.8,
        top_k=40,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    )

    def find_matching_movie(movie_title, docs):
        """Find the best matching movie from the documents."""
        best_match = None
        best_score = 0
        
        # Normalize the input title
        normalized_title = movie_title.lower().strip()
        
        for doc in docs:
            # Get the document's title and overview
            doc_title = doc.metadata.get("title", "").lower()
            doc_overview = doc.page_content.lower()
            
            # Calculate title similarity
            title_similarity = 0
            if normalized_title in doc_title or doc_title in normalized_title:
                title_similarity = 1
            elif any(word in doc_title for word in normalized_title.split()):
                title_similarity = 0.8
            
            # Calculate overview similarity
            overview_similarity = 0
            if normalized_title in doc_overview:
                overview_similarity = 0.6
            
            # Calculate total similarity score
            total_score = title_similarity + overview_similarity
            
            if total_score > best_score:
                best_score = total_score
                best_match = doc
        
        return best_match if best_score > 0 else None

    def parse_response(response_text):
        try:
            # Parse the response text into movie objects
            movies = []
            current_movie = {}
            
            # Split the response into lines and process each line
            lines = response_text.split('\n')
            for line in lines:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                    
                # Check for movie title (marked with **)
                if '**Title:**' in line:
                    # If we have a previous movie, add it to the list
                    if current_movie:
                        movies.append(current_movie)
                    current_movie = {}
                    # Extract title from between ** markers
                    title = line.split('**Title:**')[1].strip()
                    current_movie['title'] = title.strip('* ')
                
                # Check for other movie details
                elif '**Genre:**' in line:
                    genre = line.split('**Genre:**')[1].strip()
                    current_movie['genre'] = genre.strip('* ')
                elif '**Rating:**' in line:
                    rating = line.split('**Rating:**')[1].strip()
                    current_movie['rating'] = rating.strip('* ')
                elif '**Overview:**' in line:
                    overview = line.split('**Overview:**')[1].strip()
                    current_movie['overview'] = overview.strip('* ')
                elif '**Explanation:**' in line:
                    explanation = line.split('**Explanation:**')[1].strip()
                    current_movie['explanation'] = explanation.strip('* ')
            
            # Add the last movie if exists
            if current_movie:
                movies.append(current_movie)
            
            # If no movies were found, return the text as a system message
            if not movies:
                return [{"title": "System Message", "overview": response_text}]
            
            # Add poster URLs and other metadata from the context
            for movie in movies:
                if 'title' in movie:
                    # Get relevant documents for better matching
                    docs = retriever.get_relevant_documents(movie['title'])
                    
                    # Find the best matching movie
                    best_match = find_matching_movie(movie['title'], docs)
                    
                    if best_match:
                        movie['poster_url'] = best_match.metadata.get("poster_url", "")
                        movie['release_date'] = best_match.metadata.get("release_date", "")
                        # Update movie details with actual data if available
                        if not movie.get('genre'):
                            movie['genre'] = best_match.metadata.get("genre", "")
                        if not movie.get('rating'):
                            movie['rating'] = best_match.metadata.get("rating", "")
                        if not movie.get('overview'):
                            movie['overview'] = best_match.page_content
            
            return movies
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return [{"title": "System Message", "overview": response_text}]

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        | parse_response
    )

    return chain

def test_model(chain):
    test_queries = [
        "What are some good sci-fi movies from the last decade?",
        "Tell me about The Matrix",
        "Recommend me some action movies from the 90s",
        "What are the best movies directed by Christopher Nolan?",
        "Suggest some romantic comedies",
        "What are some must-watch classic movies?",
        "Tell me about the Lord of the Rings trilogy",
        "What are some good movies for a family movie night?"
    ]
    
    print("\n=== Testing Movie Recommendation Model ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest Case {i}: {query}")
        print("-" * 50)
        try:
            response = chain.invoke(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)

if __name__=='__main__':
    print("Initializing vector store...")
    vstore = ingestdata("done")
    print("Creating chain...")
    chain = generation(vstore)
    print("Running test cases...")
    test_model(chain)
    
    
    
    
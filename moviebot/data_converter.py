import pandas as pd
from langchain_core.documents import Document
import os

def dataconverter():
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "data", "mymoviedb.csv")
    
    # Read the movie dataset
    movie_data = pd.read_csv(csv_path)
    
    # Select relevant columns for the document
    data = movie_data[["Title", "Overview", "Genre", "Vote_Average", "Release_Date", "Poster_Url"]]
    
    movie_list = []
    
    # Iterate over the rows of the DataFrame
    for index, row in data.iterrows():
        # Skip rows where Overview is NaN
        if pd.isna(row['Overview']):
            continue
            
        # Construct an object with movie attributes
        obj = {
            'title': row['Title'] if not pd.isna(row['Title']) else "Unknown Title",
            'overview': row['Overview'],
            'genre': row['Genre'] if not pd.isna(row['Genre']) else "Unknown Genre",
            'rating': row['Vote_Average'] if not pd.isna(row['Vote_Average']) else 0.0,
            'release_date': row['Release_Date'] if not pd.isna(row['Release_Date']) else "Unknown Date",
            'poster_url': row['Poster_Url'] if not pd.isna(row['Poster_Url']) else ""
        }
        # Append the object to the list
        movie_list.append(obj)
    
    docs = []
    for entry in movie_list:
        # Create metadata with movie information
        metadata = {
            "title": entry['title'],
            "genre": entry['genre'],
            "rating": entry['rating'],
            "release_date": entry['release_date'],
            "poster_url": entry['poster_url']
        }
        # Create document with overview as content and other details as metadata
        doc = Document(page_content=entry['overview'], metadata=metadata)
        docs.append(doc)
    
    return docs 
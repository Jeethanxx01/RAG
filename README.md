# 🎬 Movie Recommendation Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

## 📂 Project Structure
```
movie-recommendation-chatbot/
├── app.py                 # Main Flask application
├── moviebot/             # Core RAG implementation
│   ├── __init__.py
│   ├── retrieval_generation.py  # RAG chain implementation
│   ├── data_converter.py       # Data processing utilities
│   └── ingest.py              # Vector store ingestion
├── templates/            # Frontend templates
│   └── chat.html        # Chat interface
├── static/              # Static assets
│   ├── style.css       # Main stylesheet
│   └── css/           # Additional styles
├── data/               # Data storage
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## 🚀 Overview

AI-powered Movie Recommendation Chatbot application leveraging Retrieval-Augmented Generation (RAG) architecture that combines  
LLM capabilities to enable context-aware movie recommendations and semantic search from a vector database.
Built with Python, Flask, and Google's Gemini API, this project provides intelligent movie recommendations based on user queries.

## ✨ Key Features

### 🤖 Intelligent Conversational Interface
- Real-time chat interactions
- Natural language understanding and processing
- Domain-specific movie-related query detection
- Modern, responsive UI with real-time updates

### 🎯 Advanced Movie Intelligence
- AI-powered movie recommendation engine
- Genre-based filtering
- Rating and overview information
- Movie poster integration
- Semantic search capabilities

### 🔄 Seamless Database Integration
- Vector-based movie catalog storage
- Efficient semantic search capabilities
- Scalable data management
- Real-time data ingestion and updates

### 🏢 Enterprise-Grade Architecture
- High-performance request handling
- Error handling and graceful fallbacks
- Confidence scoring for recommendations
- Modular and maintainable codebase

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/movie-recommendation-chatbot.git
   cd movie-recommendation-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file with the following structure:
   ```ini
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 🔧 Technical Stack

### Backend
- **Framework**: Flask
- **Language**: Python 3.8+
- **AI/ML**: 
  - Google Gemini API
  - LangChain
  - Vector Database Integration

### Frontend
- **Templates**: HTML5
- **Styling**: CSS3
- **Interactivity**: JavaScript

### Dependencies
- langchain-astradb
- langchain
- google-generativeai
- langchain-google-genai
- datasets
- pypdf
- python-dotenv
- flask

## 🧪 Testing

### RAG System Test Cases

#### 1. Domain Detection Tests
- **Movie-Related Queries**
  - "Can you recommend a good action movie?"
  - "What are some popular sci-fi films?"
  - "Tell me about romantic comedies"
  - Expected: High confidence scores (>0.8) with movie-related responses

- **Non-Movie Queries**
  - "What's the weather like today?"
  - "Tell me about cooking recipes"
  - "How to fix a car?"
  - Expected: Low confidence scores (<0.3) with appropriate domain restriction messages

#### 2. Recommendation Accuracy Tests
- **Genre-Specific Queries**
  - "Recommend me a horror movie"
  - "Show me some comedy films"
  - "What are the best drama movies?"
  - Expected: Recommendations match requested genre with high relevance

- **Complex Queries**
  - "Movies similar to Inception"
  - "Films with Tom Hanks"
  - "Award-winning movies from 2023"
  - Expected: Contextually relevant recommendations with proper metadata

#### 3. Response Quality Tests
- **Response Structure**
  - Title presence and accuracy
  - Genre classification
  - Rating information
  - Overview completeness
  - Poster URL validation
  - Expected: All fields populated with valid data

- **Response Time**
  - Average response time < 2 seconds
  - No timeout errors
  - Consistent performance under load

#### 4. Error Handling Tests
- **Invalid Inputs**
  - Empty queries
  - Very long queries
  - Special characters
  - Expected: Graceful error handling with user-friendly messages

- **Edge Cases**
  - No results found scenarios
  - Partial matches
  - Expected: Appropriate fallback responses

#### 5. Integration Tests
- **API Integration**
  - Google Gemini API connectivity
  - Vector store operations
  - Expected: Successful API calls and data retrieval

- **End-to-End Flow**
  - Complete user interaction flow
  - Data persistence
  - Expected: Seamless user experience

## 🔑 API Configuration

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API Key
3. Add to `.env`:
   ```ini
   GOOGLE_API_KEY=your_api_key_here
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Jeethan Joel Crasta**-  [GitHub](https://github.com/Jeethanxx01)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Contributions are welcome! Please feel free to submit a Pull Request.

## 📂 Quick Navigation
- [View Project Images](Images/)
- [OpenAI Version of the Project](OpenAI_version/)




# 🎬 AI-Powered Movie Recommendation Chatbot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

## About

An intelligent movie recommendation system that leverages the power of Google's Gemini API and Retrieval-Augmented Generation (RAG) architecture. This project combines advanced natural language processing with vector-based semantic search to provide context-aware movie recommendations. Built with Flask and Python, it features a modern chat interface that understands user preferences and delivers personalized movie suggestions with detailed information, ratings, and poster images. The system's robust architecture ensures high performance, scalability, and maintainability, making it a perfect showcase of modern AI integration in web applications.

## 🎯 Project Highlights

- **Advanced AI Integration**: Leverages Google's Gemini API and RAG (Retrieval-Augmented Generation) architecture for intelligent movie recommendations
- **Real-time Semantic Search**: Implements vector-based database for efficient movie catalog storage and retrieval
- **Enterprise Architecture**: Built with scalability and maintainability in mind using Flask and modern Python practices
- **Interactive UI**: Features a responsive chat interface with real-time updates and movie poster integration


## 📂 Quick Navigation
- [View Project Images](Images/)

## 🚀 Key Technical Achievements

### 🤖 AI & Machine Learning
- Implemented RAG architecture for context-aware movie recommendations
- Integrated Google's Gemini API for natural language understanding
- Developed semantic search capabilities using vector embeddings
- Built confidence scoring system for recommendation accuracy

### 💻 Full-Stack Development
- **Backend**: Flask-based RESTful API with modular architecture
- **Frontend**: Responsive UI with real-time chat functionality
- **Database**: Vector store integration for efficient semantic search
- **DevOps**: Environment-based configuration and dependency management

### 🔧 Technical Stack
- **Languages**: Python 3.8+, JavaScript
- **Frameworks**: Flask, LangChain
- **AI/ML**: Google Gemini API, Vector Database
- **Frontend**: HTML5, CSS3, JavaScript
- **Tools**: Git, pip, python-dotenv

## 📊 Project Impact

- **Performance**: Average response time < 2 seconds
- **Accuracy**: High confidence scores (>0.8) for movie-related queries
- **Scalability**: Modular architecture supporting easy feature additions
- **Maintainability**: Comprehensive test coverage and documentation

## 🛠️ Technical Implementation

### Core Components
```
movie-recommendation-chatbot/
├── app.py                 # Main Flask application
├── moviebot/             # Core RAG implementation
│   ├── retrieval_generation.py  # RAG chain implementation
│   ├── data_converter.py       # Data processing utilities
│   └── ingest.py              # Vector store ingestion
├── templates/            # Frontend templates
├── static/              # Static assets
└── data/               # Data storage
```

### Key Features
1. **Intelligent Recommendation Engine**
   - Genre-based filtering
   - Rating and overview information
   - Movie poster integration
   - Semantic search capabilities

2. **Robust Error Handling**
   - Graceful fallbacks
   - Input validation
   - API error management
   - User-friendly error messages

3. **Performance Optimization**
   - Efficient vector search
   - Caching mechanisms

## 🚀 Getting Started

### 🛠️ Installation

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
   ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
   ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
   ASTRA_DB_KEYSPACE=your_astra_db_keyspace
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

### ☁️ AWS Deployment

#### Prerequisites
- AWS Account
- EC2 Instance
- Security Group Configuration

#### Deployment Steps

1. **EC2 Instance Setup**
   ```bash
   sudo apt-get update
   sudo apt install git curl unzip tar make sudo vim wget -y
   git clone <your-repository-url>
   ```

2. **Environment Configuration**
   ```bash
   touch .env
   # Add your environment variables
   ```

3. **Install Dependencies**
   ```bash
   sudo apt install python3-pip
   pip3 install -r requirements.txt --break-system-packages
   ```

4. **Security Configuration**
   - Configure Security Group for port 5000
   - Allow inbound traffic from 0.0.0.0/0

5. **Launch Application**
   ```bash
   python3 app.py
   ```

### 🔑 API Configuration

#### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API Key
3. Add to `.env`:
   ```ini
   GOOGLE_API_KEY=your_api_key_here
   ```

#### Astra DB Setup
1. Create account at [DataStax Astra](https://astra.datastax.com/)
2. Create new database
3. Generate token
4. Configure `.env`:
   ```ini
   ASTRA_DB_API_ENDPOINT=your_endpoint
   ASTRA_DB_APPLICATION_TOKEN=your_token
   ASTRA_DB_KEYSPACE=your_keyspace
   ```

## 🧪 Quality Assurance

- Comprehensive test suite covering:
  - Domain detection
  - Recommendation accuracy
  - Response quality
  - Error handling
  - API integration
  - End-to-end flows

## 👨‍💻 Author

**Jeethan Joel Crasta**
- [GitHub](https://github.com/Jeethanxx01)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---





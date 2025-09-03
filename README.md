# 🎓 Linkeder - AI-Powered Student Recruitment Platform

A conversational AI platform that enables intelligent querying of university student profiles using Retrieval-Augmented Generation (RAG) architecture. Built with OpenAI GPT-4, Chroma vector database, and Streamlit for seamless user interactions.

## 🚀 Features

- **Conversational AI Interface**: Natural language queries about student profiles
- **Multi-turn Conversations**: Intelligent context handling for follow-up questions
- **Dual Interface**: Web-based Streamlit UI and command-line interface
- **Advanced Search**: Vector similarity search with semantic embeddings
- **Query Classification**: Automatic detection of new searches vs. follow-up questions
- **Session Management**: Persistent conversation history across sessions
- **Real-time Processing**: Live chat interface with loading indicators

## 🛠️ Tech Stack

- **Backend**: Python, LangChain, OpenAI GPT-4
- **Vector Database**: Chroma with OpenAI embeddings
- **Frontend**: Streamlit (Web UI), Rich (CLI)
- **Data Processing**: Pandas, CSV handling
- **Environment**: Python-dotenv for configuration

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkeder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

### Web Interface (Recommended)

Launch the Streamlit web application:
```bash
streamlit run frontend_streamlit.py
```

The web interface will open in your browser with:
- Chat-based interaction
- Session state management
- Real-time responses
- Loading indicators

### Command Line Interface

For CLI usage:
```bash
python frontend.py
```

## 💬 Example Queries

### Basic Profile Searches
- "Show me students with Python and machine learning skills"
- "Find students from MIT studying computer science"
- "List students with internship experience at Google"

### Follow-up Questions
- "What about their leadership experience?"
- "Do they have any startup experience?"
- "Show me their research background"

### Complex Queries
- "Find students with cybersecurity skills who have won hackathons"
- "Show me data science students from top universities with AWS experience"
- "List students with both academic achievements and industry experience"

## 🏗️ Architecture

### Core Components

1. **RAGInstance Class** (`backend.py`)
   - Handles data ingestion and vector database setup
   - Manages query processing and response generation
   - Maintains conversation history

2. **Query Classification System**
   - Distinguishes between new searches and follow-up questions
   - Optimizes search performance and user experience
   - Handles context-dependent queries

3. **Vector Database Integration**
   - Uses Chroma with OpenAI embeddings
   - Implements similarity search with configurable thresholds
   - Provides semantic matching capabilities

### Data Structure

Student profiles include:
- **Name**: Student's full name
- **University**: Institution name
- **Major**: Field of study
- **Graduation Year**: Expected graduation date
- **Skills**: Technical and soft skills
- **Achievements**: Academic and professional accomplishments
- **Experience**: Internships and work experience
- **Email ID**: Contact information

## 🔍 How It Works

1. **Data Ingestion**: CSV files are processed and converted to vector embeddings
2. **Query Processing**: User queries are classified and optimized for search
3. **Vector Search**: Similarity search finds relevant student profiles
4. **Response Generation**: GPT-4 generates contextual responses based on retrieved data
5. **Context Management**: Conversation history is maintained for follow-up questions

## 📊 Data Generation

The project includes automated data generation scripts:
- `profile_generation1.py`: Creates realistic student profiles
- Generates 1000+ profiles with diverse skills and experiences
- Ensures data uniqueness and variety

## 🎯 Use Cases

- **Recruitment**: Find candidates with specific skill sets
- **Networking**: Connect students with similar interests
- **Research**: Analyze student demographics and skills
- **Career Services**: Match students with opportunities

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for GPT-4 access
- Model parameters can be adjusted in the code

### Search Parameters
- Similarity threshold: 0.45-0.50 (configurable)
- Number of results: 10 profiles per query
- Temperature: 0.0 for consistent responses

## 🚨 Important Notes

- **Demo Data**: All student profiles are generated for demonstration purposes
- **API Costs**: OpenAI API usage incurs costs based on token consumption
- **Rate Limits**: Respect OpenAI API rate limits for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- LangChain for RAG framework
- Streamlit for web interface
- Chroma for vector database

---

**Note**: This is a demonstration project. All student data is fictional and generated for testing purposes.
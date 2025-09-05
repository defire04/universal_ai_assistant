#  AI Assistant

An intelligent AI assistant with RAG (Retrieval-Augmented Generation) capabilities, built with Python and deployed via Telegram Bot. The system combines document knowledge base with AI conversation capabilities to provide contextual and accurate responses.

## 🏗️ Architecture Overview

The AI Assistant consists of several integrated components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   Gemini AI     │    │  Vector Store   │
│   (aiogram)     │◄──►│  (LLM Engine)   │    │  (PostgreSQL +  │
│                 │    │                 │    │   pgvector)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Ollama      │
                    │  (Embeddings)   │
                    │ nomic-embed-    │
                    │   text:v1.5     │
                    └─────────────────┘
```

### Core Components:

1. **Telegram Bot Interface** - User interaction layer using aiogram framework
2. **Gemini AI Engine** - Google's Gemini model for natural language generation
3. **Vector Database** - PostgreSQL with pgvector extension for semantic search
4. **Ollama Embeddings** - Local embedding generation using nomic-embed-text model
5. **RAG Service** - Retrieval-Augmented Generation for context-aware responses
6. **Document Processing** - PDF and text file ingestion and chunking

## 🚀 Features

- **Intelligent Chat Interface**: Natural conversation through Telegram
- **Document-Based Responses**: Answers based on uploaded company documents
- **Semantic Search**: Vector-based similarity search for relevant context
- **Multi-Format Support**: PDF and TXT document processing
- **Access Control**: User-based permission system
- **Real-time Processing**: Asynchronous document processing and response generation
- **Scalable Architecture**: Containerized deployment with Docker Compose

## 🛠️ Technology Stack

- **Backend Framework**: Python 3.11+ with AsyncIO
- **AI/ML Stack**:
  - Google Gemini API (LLM)
  - Ollama (Local embeddings)
  - nomic-embed-text:v1.5 (Embedding model)
- **Database**: PostgreSQL 16 with pgvector extension
- **Bot Framework**: aiogram 3.15.0
- **Document Processing**: PyPDF2, custom text chunking
- **Configuration**: Pydantic Settings with environment variables
- **Logging**: Loguru for structured logging
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Telegram Bot Token (from @BotFather)
- Google Gemini API Key

## ⚡ Quick Start

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd ai-assistant
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# elegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ALLOWED_USER_IDS=123456789,987654321

# Application Configuration
APP_NAME="AI Assistant"

# Optional Gemini Configuration
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.7

# Vector Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5433/universal_ai
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text:v1.5

# Document Processing
CHUNK_SIZE=1200
MIN_CHUNK_SIZE=250
MAX_CHUNKS=10000

DEBUG_RAG=true
LOG_LEVEL=DEBUG
SIMILARITY_THRESHOLD=0.05
RAG_TOP_K=15

# Context Memory Configuration
CONTEXT_MEMORY_ENABLED=true
CONTEXT_MESSAGES_LIMIT=5
CONTEXT_TOKEN_LIMIT=4000

SYSTEM_PROMT=
DOCUMENTS_FOLDER="./documents"
```

### 3. Prepare Documents

Create a `documents` folder and add your PDF or TXT files:

```bash
mkdir documents
# Copy your company documents here
cp /path/to/your/documents/*.pdf documents/
cp /path/to/your/documents/*.txt documents/
```

### 4. Start Infrastructure Services

```bash
# Start database and ollama services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Download Ollama Embedding Model

After Ollama service is running, pull the embedding model:

```bash
# Connect to ollama container
docker exec -it ollama-service ollama pull nomic-embed-text:v1.5

# Verify model is downloaded
docker exec -it ollama-service ollama list
```

### 6. Install Python Dependencies and Run Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 7. Verify Installation

1. **Check Ollama model**: `docker exec -it ollama-service ollama list`
2. **Access pgAdmin**: http://localhost:5050 (admin@universal.ai / admin123)
3. **Test Telegram bot**: Send `/start` to your bot

## 📁 Project Structure

```
ai-assistant/
├── app/
│   ├── ai/                     # AI integration modules
│   │   ├── __init__.py
│   │   ├── gemini.py          # Gemini AI client
│   │   └── models.py          # Request/response models
│   ├── core/                   # Core application components
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging setup
│   ├── telegram/               # Telegram bot components
│   │   ├── __init__.py
│   │   ├── bot.py             # Bot initialization
│   │   ├── handlers/          # Message handlers
│   │   │   ├── __init__.py
│   │   │   └── messages.py
│   │   └── middlewares/       # Bot middlewares
│   │       └── access.py      # Access control
│   └── vector_db/             # Vector database components
│       ├── __init__.py
│       ├── reader.py          # Document reader
│       ├── repositories/
│       │   └── vector_repository.py
│       └── services/
│           ├── embedding_service.py
│           └── rag_service.py
├── documents/                  # Document storage folder
├── docker-compose.yaml        # Container orchestration
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
└── README.md                  # This file
```

## 🔧 Configuration Guide

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | ✅ |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | - | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | - | ✅ |
| `OLLAMA_BASE_URL` | Ollama API endpoint | http://localhost:11434 | ❌ |
| `EMBEDDING_MODEL` | Ollama embedding model | nomic-embed-text:v1.5 | ❌ |
| `GEMINI_MODEL` | Gemini model version | gemini-2.0-flash | ❌ |
| `ALLOWED_USER_IDS` | Comma-separated Telegram user IDs | - | ❌ |
| `DOCUMENTS_FOLDER` | Path to documents directory | ./documents | ❌ |
| `CHUNK_SIZE` | Document chunk size for processing | 1200 | ❌ |
| `RAG_TOP_K` | Number of context chunks to retrieve | 5 | ❌ |
| `SIMILARITY_THRESHOLD` | Minimum similarity score for context | 0.5 | ❌ |
| `DEBUG_RAG` | Enable RAG debugging logs | false | ❌ |

### Docker Services

| Service | Port | Purpose | Volume |
|---------|------|---------|--------|
| `postgres-universal-python-ai` | 5433 | Vector database with pgvector | universal_ai_postgres_data |
| `pgadmin` | 5050 | Database administration UI | - |
| `ollama` | 11434 | Embedding generation service | ollama_data |

## 💬 Usage Guide

### Bot Commands

- `/start` - Initialize conversation and get welcome message

### Interaction Flow

1. **Start conversation**: Send `/start` to the bot
2. **Ask questions**: Send any text message with your question
3. **Get AI response**: Bot searches documents and provides contextual answers
4. **Continue conversation**: Ask follow-up questions naturally

### Example Interactions

```
User: /start
Bot: 👋 Hello, User!
     🤖 I am the AI assistant of the company.
     📚 I have access to the corporate knowledge base.
     💬 Just write your question and I will answer based on company documents.

User: What are our company's vacation policies?
Bot: 🤖 Based on company documents, employees are entitled to 25 days of annual leave...

User: How do I submit a vacation request?
Bot: 🤖 To submit a vacation request, you need to...
```

## 🔍 How RAG Works

The Retrieval-Augmented Generation (RAG) process works as follows:

1. **Document Ingestion**: 
   - PDF and TXT files from the `documents` folder are processed
   - Documents are split into chunks (default: 1200 characters)
   - Minimum chunk size is 250 characters to ensure meaningful content

2. **Vector Generation**: 
   - Each chunk is converted to embeddings using Ollama's nomic-embed-text:v1.5 model
   - Embeddings are 768-dimensional vectors representing semantic meaning

3. **Storage**: 
   - Embeddings stored in PostgreSQL with pgvector extension
   - Includes original content, metadata, and vector representations
   - HNSW index for fast similarity search

4. **Query Processing**: 
   - User questions are embedded using the same model
   - Vector similarity search finds relevant chunks

5. **Context Retrieval**: 
   - Top K most relevant chunks retrieved (default: 5)
   - Similarity threshold filters low-relevance results (default: 0.5)

6. **AI Generation**: 
   - Gemini AI generates responses using retrieved context
   - System prompt guides response style and format

## 🐛 Troubleshooting

### Common Issues

1. **Ollama service not accessible**:
   ```bash
   # Check if Ollama is running
   docker-compose ps
   
   # Check Ollama logs
   docker-compose logs ollama
   
   # Test Ollama API
   curl http://localhost:11434/api/version
   ```

2. **Embedding model not downloaded**:
   ```bash
   # Pull the model manually
   docker exec -it ollama-service ollama pull nomic-embed-text:v1.5
   
   # Verify model exists
   docker exec -it ollama-service ollama list
   ```

3. **Database connection issues**:
   ```bash
   # Check PostgreSQL logs
   docker-compose logs postgres-universal-python-ai
   
   # Verify database is accessible
   docker exec -it universal_ai_postgres psql -U ai_user -d universal_ai -c "SELECT version();"
   ```

4. **Bot not responding**:
   ```bash
   # Check application logs when running
   python main.py
   
   # Verify bot token and user permissions in .env
   # Check if user ID is in ALLOWED_USER_IDS
   ```

5. **No context found in responses**:
   ```bash
   # Check if documents are in the documents folder
   ls -la documents/
   
   # Verify documents were processed (check logs)
   # Lower similarity threshold if needed
   # Enable debug logging: DEBUG_RAG=true
   ```

6. **Gemini API errors**:
   ```bash
   # Verify API key is correct
   # Check quota and billing in Google Cloud Console
   # Ensure Gemini API is enabled
   ```

### Log Analysis

Enable detailed logging for debugging:

```env
# In .env file
LOG_LEVEL=DEBUG
DEBUG_RAG=true
```

Common log patterns to look for:
- `RAG: X chunks from {...}, scores: [...]` - Successful context retrieval
- `RAG: no relevant context found` - No matching documents
- `Added X chunks from {source}` - Document processing completion
- `Gemini error:` - AI API issues

## 🔒 Security Considerations

- **API Keys**: 
  - Store sensitive keys in `.env` file
  - Never commit `.env` to version control
  - Use environment-specific keys for production

- **User Access**: 
  - Configure `ALLOWED_USER_IDS` to restrict bot access
  - Monitor unauthorized access attempts
  - Regularly review user permissions

- **Database Security**: 
  - Use strong passwords for PostgreSQL
  - Consider SSL connections for production
  - Limit database network access

- **Document Security**:
  - Ensure sensitive documents are properly classified
  - Monitor document access and processing
  - Consider encryption for sensitive content

- **Network Security**: 
  - Ensure proper firewall rules for exposed ports
  - Use reverse proxy for production deployments
  - Enable HTTPS for web interfaces

## 🚀 Production Deployment

### Environment Configuration

1. **Production Environment Variables**:
   ```env
   # Use production API keys
   GEMINI_API_KEY=prod_key_here
   
   # Production database with SSL
   DATABASE_URL=postgresql://user:pass@prod-db:5432/ai_db?sslmode=require
   
   # Reduced logging in production
   LOG_LEVEL=INFO
   DEBUG_RAG=false
   ```

2. **Docker Production Override**:
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   services:
     postgres-universal-python-ai:
       environment:
         POSTGRES_PASSWORD: ${POSTGRES_PROD_PASSWORD}
       volumes:
         - /var/lib/postgresql/data:/var/lib/postgresql/data
   ```

### Scaling Considerations

- **Database Scaling**: Use external managed PostgreSQL for better performance
- **Caching**: Implement Redis for embedding cache
- **Load Balancing**: Use multiple application instances behind load balancer
- **Monitoring**: Set up proper monitoring and alerting

### Performance Optimization

1. **Vector Database Tuning**:
   ```sql
   -- Optimize HNSW index parameters
   CREATE INDEX CONCURRENTLY idx_embedding_hnsw 
   ON vector_store USING hnsw (embedding vector_cosine_ops) 
   WITH (m = 16, ef_construction = 64);
   ```

2. **Embedding Cache**: Consider caching frequent embeddings
3. **Batch Processing**: Process multiple documents in batches
4. **Connection Pooling**: Optimize database connection pools

## 📊 Monitoring and Metrics

### Key Metrics to Monitor

- **Response Time**: Bot response latency
- **Context Retrieval**: RAG similarity scores and chunk count
- **API Usage**: Gemini API calls and costs
- **Database Performance**: Query execution times
- **Error Rates**: Failed requests and exceptions

### Logging Strategy

```python
# Example production logging configuration
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the project structure
4. Add tests if applicable
5. Update documentation as needed
6. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-assistant.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Start development services
docker-compose up -d postgres-universal-python-ai pgadmin ollama

# Run tests
python -m pytest tests/
```

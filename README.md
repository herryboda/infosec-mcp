# Company Policy MCP Server

An intelligent server that answers company-specific questions based on company policies and standards using LLM technology.

## Features

- Question answering from company policies and standards
- Local file-based storage for policies
- Secure API endpoints
- Easy policy document ingestion
- Real-time responses

## Architecture

The system uses:
- FastAPI for the backend server
- OpenAI's GPT models for question answering
- LangChain for document processing and retrieval
- Local file system for policy storage

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_api_key
STORAGE_DIR=storage  # Optional, defaults to 'storage'
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   ├── llm_service.py
│   │   └── document_service.py
│   └── main.py
├── storage/
│   └── policies/  # Where policy documents are stored
├── tests/
├── requirements.txt
└── README.md
```

## Usage

1. Start the server locally:
```bash
uvicorn app.main:app --reload
```

2. Send questions to the API:
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"question": "What is our company's remote work policy?"}'
```

3. Ingest a new policy document:
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"content": "Your policy document text here", "name": "remote_work_policy.txt"}'
```

## Security

- All API endpoints are secured with API keys
- Policy documents are stored locally in the specified storage directory
- Access logging for audit trails

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
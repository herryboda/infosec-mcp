# Company Policy MCP Server

An intelligent server that answers company-specific questions based on company policies and standards using LLM technology.

## Features

- Question answering from company policies and standards
- AWS serverless architecture
- Secure API endpoints
- Easy policy document ingestion
- Real-time responses

## Architecture

The system uses:
- AWS Lambda for serverless compute
- API Gateway for REST API endpoints
- OpenAI's GPT models for question answering
- LangChain for document processing and retrieval

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

3. Deploy to AWS:
```bash
# Instructions for AWS deployment will be added
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
     -d '{"question": "What is our company's remote work policy?"}'
```

## Security

- All API endpoints are secured with API keys
- Company documents are encrypted at rest
- Access logging for audit trails

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
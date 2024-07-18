# Django Chatbot REST API

This project implements a chatbot using Django REST framework. The chatbot uses advanced natural language processing techniques to provide intelligent responses to user queries.

## Features

- REST API endpoint for chatbot interactions
- Utilizes OpenAI's GPT model for generating responses
- Implements session management for conversation continuity
- Uses Milvus for efficient vector search
- Combines BM25 and IVF_FLAT retrieval methods for improved accuracy

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- pip (Python package manager)
- Milvus server running (default: localhost:19530)
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/django-chatbot-api.git
   cd django-chatbot-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the Django development server:
   ```
   python manage.py runserver
   ```

## Usage

To interact with the chatbot, send a POST request to the `/api/chat/` endpoint with a JSON payload containing the user's input:

```
POST /api/chat/
Content-Type: application/json

{
    "user_input": "Your question or message here"
}
```

The API will respond with a JSON object containing the chatbot's response:

```json
{
    "ai_response": "The chatbot's response to your input"
}
```

## Project Structure

- `chatbot/` - Main application directory
  - `models.py` - Defines the ChatSession model
  - `serializers.py` - Defines input and output serializers
  - `views.py` - Contains the ChatbotView for handling requests
  - `chatbot_logic.py` - Implements the core chatbot functionality
  - `urls.py` - Defines URL routing for the chatbot API
- `chatbot_project/` - Project configuration directory
- `data/` - Directory for storing text files used by the chatbot

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT model
- Milvus for vector similarity search
- Django and Django REST framework teams
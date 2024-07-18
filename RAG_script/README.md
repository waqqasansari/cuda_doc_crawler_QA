# Advanced RAG Chatbot

This project implements an advanced Retrieval-Augmented Generation (RAG) chatbot using state-of-the-art natural language processing techniques. The chatbot is designed to process multiple text files, use semantic chunking for better context understanding, and employ ensemble retrieval methods for improved response accuracy.

## System Requirements

- Ubuntu >= 20.04 (x86_64)
- Python 3.8 or later

## Project Structure

```
.
└── RAG_script/
    └── RAG_qa.py
```

The main `ChatbotLogic` class is located in the `RAG_script/RAG_qa.py` file.

## Features

- Semantic chunking for improved text segmentation
- Milvus Lite for efficient vector storage
- Ensemble retrieval combining BM25, FLAT, and IVF_FLAT methods
- Context-aware reranking for more relevant responses
- Handling of multiple text files
- Conversation history management

## Installation

1. Clone the repository:

   ```
   git clone git clone https://github.com/your-username/cuda_doc_crawler_QA.git
   cd cuda_doc_crawler_QA/RAG_script
   ```

2. Create a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. **Run the script:**

   ```
   python RAG_qa.py
   ```

2. **Interaction:**

   - Begin the conversation with a greeting message from the bot.

     ```python
     print("Bot: Hello! How can I assist you today?")
     ```

   - Enter your queries or messages when prompted (prefixed with "You: ").

     ```python
     while True:
         user_input = input("You: ")
     ```

   - To end the conversation, type any of the termination commands: "exit", "quit", or "bye".

     ```python
         if user_input.lower() in ['exit', 'quit', 'bye']:
             print("Bot: Goodbye!")
             break
     ```

   - The bot processes your input and provides a response based on its logic.
     ```python
         response = assistant.process_message(session_id, user_input)
         print("Bot:", response["answer"])
     ```

## Configuration

You can adjust various parameters in the `ChatbotLogic` class to fine-tune the chatbot's performance:

- Modify the `min_subsection_length`, `max_subsection_length`, and `num_clusters` in `SemanticChunker` for different chunking behavior.
- Adjust the `search_kwargs={"k": 5}` in the retrievers to change the number of retrieved documents.
- Modify the weights in `EnsembleRetriever` to prioritize different retrieval methods.

## Acknowledgments

This project uses several open-source libraries and models, including LangChain, OpenAI's GPT models, and Milvus Lite. We thank the developers and maintainers of these projects for their valuable work.

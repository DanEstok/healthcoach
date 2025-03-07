# Health Coach Chatbot

_Created by Daniel Estok - Spark Tech Repair_

A rule-based and ML-enhanced chatbot that provides personalized wellness tips and basic nutrition advice. Available as both a command-line application and a web interface.

## Features

- Natural language processing to understand user queries
- Rule-based responses for common wellness questions
- ML-enhanced personalized recommendations using Hugging Face transformers
- Basic nutrition advice and wellness tips
- Intent classification and semantic search capabilities
- User profiles for personalized interactions
- Available in both command-line and web interface versions

## Project Structure

_Designed by Daniel Estok - Spark Tech Repair_

- `app.py`: Main application entry point for command-line interface
- `web_app.py`: Flask web application interface
- `chatbot/`: Core chatbot functionality
  - `nlp_processor.py`: NLP processing utilities
  - `rule_engine.py`: Rule-based response system
  - `ml_enhancer.py`: Machine learning enhancement
  - `hf_models.py`: Hugging Face transformer models integration
  - `knowledge_base.py`: Wellness and nutrition knowledge base
  - `user_profile.py`: User profile management for personalization
- `data/`: Training data and knowledge resources
- `models/`: Cached transformer models
- `static/`: Web assets (CSS, JavaScript) for the web interface
- `templates/`: HTML templates for the web interface
- `utils/`: Utility functions
- `requirements.txt`: Project dependencies

## Setup and Installation

```bash
# Clone the repository
git clone https://github.com/DanEstok/healthcoach.git
cd healthcoach

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Important Note:** On first run, the application will download several Hugging Face transformer models which may take some time depending on your internet connection (potentially 5-15 minutes). These models include:

- Question-answering model (deepset/roberta-base-squad2)
- Intent classification model (facebook/bart-large-mnli)
- Sentence embedding model (sentence-transformers/all-MiniLM-L6-v2)

The models will be cached in the `models/` directory for future use, so subsequent runs will start much faster.

## Usage

_Implemented by Daniel Estok - Spark Tech Repair_

### Command-line Interface

To run the chatbot in command-line mode:

```bash
python app.py
```

Interact with the chatbot by typing your health and wellness questions. Examples:

- "What should I eat for more energy?"
- "How can I improve my sleep?"
- "Give me a quick workout for my lunch break"
- "What are good sources of protein?"

Type 'quit', 'exit', or 'bye' to end the session.

### Web Interface

To run the chatbot with the web interface:

```bash
python web_app.py
```

This will start a Flask web server, typically at http://localhost:8080/. Open this URL in your browser to interact with the Health Coach through a user-friendly web interface.

The web interface features:

- Chat-like interaction with the Health Coach
- Saved conversation history
- About page with usage information
- Mobile-responsive design

## How It Works

_Engineered by Daniel Estok - Spark Tech Repair_

The Health Coach chatbot processes user queries through several steps:

1. **NLP Processing**: Analyzes the user's input to identify intent and entities
2. **Rule Engine**: Attempts to match the query with predefined rules
3. **ML Enhancement**: If rule confidence is low, enhances responses using ML models
4. **User Profiling**: Tracks user interactions to personalize future responses

The system uses a combination of rule-based logic and machine learning to provide relevant, personalized wellness advice.

## Technologies Used

- Python
- NLTK for natural language processing
- Hugging Face Transformers for advanced NLP capabilities
- Sentence Transformers for semantic search
- Scikit-learn for ML components
- Flask for the web interface

## Dependencies

The project uses the following key dependencies:

- numpy, pandas, scikit-learn for data processing
- nltk for natural language processing
- torch, transformers, and sentence-transformers for ML capabilities
- flask for the web interface

Note that spaCy has been removed from the requirements as it was causing loading issues.

## Disclaimer

Health Coach provides general wellness information and is not a substitute for professional medical advice. Always consult with healthcare professionals for medical concerns or before making significant changes to your diet or exercise routine.

---

© 2025 Daniel Estok - Spark Tech Repair. All rights reserved.

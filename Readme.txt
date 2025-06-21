Darwix AI Technical Assessment

This project showcases two powerful AI features I built for the Darwix technical assessment. Both features demonstrate practical applications of modern AI technology in real-world scenarios.

What's Inside

I've implemented two distinct AI-powered solutions:
1. An audio transcription service that can identify different speakers
2. A smart blog title generator that creates engaging titles from content

Getting Started

Before you begin, make sure you have:
- Python 3.8 or newer installed
- The pip package manager
- A Deepgram API key for the transcription feature

Setting Up the Project

First, clone this repository to your local machine:
git clone <your-repo-url>
cd darwix-ai-assessment

Next, install the required Python packages:
pip install django djangorestframework requests keybert sentence-transformers

Don't forget to add your Deepgram API key to the api.py file where it says DEEPGRAM_API_KEY.

Audio Transcription with Speaker Detection

This feature uses Deepgram's advanced speech recognition technology to convert audio files into text while identifying who said what. It's particularly useful for meeting recordings, interviews, or any multi-speaker audio content.

What makes this special:
- Works with 36 different languages automatically
- Identifies individual speakers in conversations
- Handles various audio formats like MP3, WAV, M4A, and more
- Provides clean, structured results

To start the transcription service:
python api.py

The service will be available at http://localhost:8000

How to use it:
Send your audio file to the /transcribe/ endpoint using a POST request. You can name the file field whatever you want - the system is flexible.

Example with curl:
curl -X POST -F "audio=@your-audio-file.mp3" http://localhost:8000/transcribe/

You'll get back a JSON response showing the detected language, full transcript, and speaker-separated text like this:

{
  "language": "en",
  "transcript": "Hello how are you today I am fine thank you",
  "speakers": [
    {
      "speaker": "Speaker 0",
      "text": "Hello how are you today"
    },
    {
      "speaker": "Speaker 1", 
      "text": "I am fine thank you"
    }
  ]
}

Smart Blog Title Generator

This tool analyzes your blog content and suggests three compelling titles using advanced natural language processing. It's built with KeyBERT and a multilingual model that understands context and extracts meaningful keywords.

Key features:
- Uses sophisticated NLP algorithms
- Works with multiple languages
- Filters out common stop words for better results
- Generates exactly three title options
- Integrates seamlessly with Django applications

To run the title generator:
python main.py

Access it at http://localhost:8000

Send your blog content to /generate-titles/ as JSON:

curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Your blog post content goes here..."}' \
     http://localhost:8000/generate-titles/

The response will include three suggested titles:
{
  "titles": [
    "Artificial Intelligence Transforming",
    "Machine Learning Algorithms", 
    "Ai Revolutionizing Industries"
  ]
}

Testing Everything Out

For the transcription service:
1. Find an audio file on your computer
2. Upload it using curl or a tool like Postman
3. Check that the speakers are properly identified

For the title generator:
1. Write some blog content or use existing text
2. Send it as JSON to the API
3. See what creative titles it suggests

How I Built This

The transcription feature leverages Deepgram's robust API, which handles the heavy lifting of speech recognition and speaker identification across 36 languages. I focused on creating a clean interface that accepts various file formats and returns well-structured data.

For the title generator, I chose KeyBERT with the paraphrase-multilingual-MiniLM-L12-v2 model because it excels at understanding context and extracting meaningful phrases from text. The system intelligently filters results to provide the most relevant title suggestions.

Both services include comprehensive error handling to manage file validation, API errors, network issues, and malformed requests gracefully.

This implementation demonstrates practical AI integration that could easily be expanded for production use cases.
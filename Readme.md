# Audio Processing and Fact Checking with OpenAI

This project takes audio input either from a microphone or an audio file, transcribes the audio to text using OpenAI's Whisper API, and then fact checks the transcribed text using OpenAI's GPT-3 model. 

The application utilizes multi-threading to perform the audio transcription and fact checking tasks concurrently.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.6 or higher
- OpenAI Python client `openai` - You can install this via pip:
    ```
    pip install openai
    ```
- `speech_recognition` module for audio recognition, install via pip:
    ```
    pip install SpeechRecognition
    ```
- An API key from OpenAI.

### Setting up the Environment Variable

This project requires you to set up an environment variable for your OpenAI API key.

- Set the OpenAI API key as an environment variable:
    ```bash
    export OPENAI_KEY="your-openai-api-key"
    ```

### Running the Application

- Navigate to the project's root directory, and run the application:
    ```bash
    python main.py --source 'microphone'
    ```
- You can replace 'microphone' with a file path to an audio file to process audio from a file instead of a microphone.

## Understanding the Code

### main.py

This is the main script that runs the application. It creates a queue and two threads. One thread records audio and pushes it into the queue, and the other thread pulls from the queue, transcribes the audio to text, and fact checks it.

### AudioTranscription Class

This class handles audio input. It can accept audio input either from a microphone or an audio file. It then pushes the audio data into a queue.

### FactChecker Class

This class pulls audio data from a queue, saves it as a .wav file, transcribes the audio to text using OpenAI's Whisper model, and then fact checks the transcribed text using OpenAI's GPT-3 model.

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

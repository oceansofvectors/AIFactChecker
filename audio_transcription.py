import openai
import speech_recognition as sr

from logs import logger


class AudioTranscription:

    def __init__(self, source='microphone', sample_rate=16000, duration=10):
        self.sample_rate = sample_rate
        self.duration = duration
        self.source = source
        if self.source == 'microphone':
            self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()

    def listen(self):
        if self.source == 'microphone':
            return self.listen_from_microphone()
        else:
            return self.listen_from_file(self.source)

    def listen_from_microphone(self):
        with self.microphone as source:
            try:
                logger.info("Adjusting for ambient noise.")
                self.recognizer.adjust_for_ambient_noise(source)
                logger.info("Listening for audio.")
                audio = self.recognizer.listen(source)
                logger.info("Audio received.")
                return audio
            except sr.UnknownValueError:
                logger.error("Could not understand audio.")
                return None
            except sr.RequestError as e:
                logger.error(f"Error requesting results from Google Speech Recognition service; {e}")
                return None

    def listen_from_file(self, audio_file_path):
        with sr.AudioFile(audio_file_path) as source:
            try:
                logger.info("Reading audio from file.")
                audio = self.recognizer.record(source)
                logger.info("Audio read from file.")
                return audio
            except sr.UnknownValueError:
                logger.error("Could not understand audio.")
            except sr.RequestError as e:
                logger.error(f"Error requesting results from Google Speech Recognition service; {e}")

    def record_thread(self, queue):
        while True:
            audio = self.listen()
            if audio:
                queue.put(audio)

    def save_audio(self, audio_data, file_name="audio.wav"):
        with open(file_name, "wb") as f:
            f.write(audio_data.get_wav_data())

    def transcribe_audio(self, audio_data):
        """
        Function to transcribe audio using OpenAI's Whisper model.
        """
        # Save the AudioData to a file
        file_path = "audio.wav"
        self.save_audio(audio_data, file_path)
        logger.info(f"Saved audio data to file: {file_path}")

        # Open the audio file
        audio_file = open(file_path, "rb")

        # Send the audio file to the Whisper ASR API
        logger.info(f"Sending audio file to Whisper API for transcription")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Extract the transcription text
        transcription = transcript.get('text')

        logger.info(f"Transcription completed: {transcription}")
        return transcription

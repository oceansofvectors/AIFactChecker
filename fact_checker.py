import openai

from logs import logger


class FactChecker:

    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

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

    def fact_check_with_gpt3(self, text):
        logger.info(f"Sending the transcription to GPT-3 for fact checking")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"Fact check this statement: {text}"},
            ]
        )
        answer = {'Statement': text, "Fact Check": completion.choices[0].message.content}
        logger.info(f"Fact checked result: {answer}")
        return answer

    def fact_check_thread(self, q):
        while True:
            # Get the file path from the queue
            file_path = q.get()
            logger.info(f"Received file path from queue: {file_path}")

            # Transcribe the audio
            transcription = self.transcribe_audio(file_path)

            # Fact check the transcription with GPT-3
            fact_check_result = self.fact_check_with_gpt3(transcription)

            # Print the result
            logger.info(f'Fact check result: {fact_check_result}')

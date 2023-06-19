import openai
from audio_transcription import AudioTranscription
from logs import logger
from jinja2 import Environment, FileSystemLoader
from helpers import retry_on_error
import csv
import os
import json


class FactChecker:

    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.audio_transcription = AudioTranscription()

        # Create the Jinja2 environment
        env = Environment(loader=FileSystemLoader('./'))

        # Load the template
        self.template = env.get_template('prompt.txt')

        # CSV file path
        self.csv_file = 'fact_check_results.csv'

        # Check if the CSV file exists, if not, create it with headers
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Statement', 'Answer', 'Explanation'])

    @retry_on_error(max_retries=5, backoff_factor=2)
    def fact_check_with_gpt3(self, text):
        logger.info(f"Sending the transcription to GPT-3 for fact checking")
        rendered_prompt = self.template.render(text=text)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": rendered_prompt},
            ]
        )
        facts = json.loads(completion.choices[0].message.content)
        logger.info(facts)
        # Write the result to the CSV file
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for answer in facts:
                writer.writerow([answer.get('statement'),
                                 answer.get('Answer'), answer.get('Explanation')])
        return answer

    def fact_check_thread(self, q):
        while True:
            # Get the file path from the queue
            file_path = q.get()
            logger.info(f"Received file path from queue: {file_path}")

            # Transcribe the audio
            transcription = self.audio_transcription.transcribe_audio(file_path)

            # Fact-check the transcription with GPT-3
            fact_check_result = self.fact_check_with_gpt3(transcription)

            # Print the result
            logger.info(f'Fact check result: {fact_check_result}')

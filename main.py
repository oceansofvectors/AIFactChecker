import argparse
import queue
import threading
from os import getenv

from audio_transcription import AudioTranscription
from fact_checker import FactChecker

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Process audio from different sources.')
    parser.add_argument('--source', default='microphone',
                        help='The source of the audio. Options are "microphone" or a file path to an audio file.')

    # Parse the arguments
    args = parser.parse_args()

    # Set your API keys
    openai_api_key = getenv("OPENAI_KEY")

    # Create a queue
    q = queue.Queue()

    # Create instances of our classes
    audio_transcription = AudioTranscription(source=args.source)
    fact_checker = FactChecker(openai_api_key)

    # Create the threads
    t1 = threading.Thread(target=audio_transcription.record_thread, args=(q,))
    t2 = threading.Thread(target=fact_checker.fact_check_thread, args=(q,))

    # Start the threads
    t1.start()
    t2.start()

    # Wait for the threads to finish
    t1.join()
    t2.join()

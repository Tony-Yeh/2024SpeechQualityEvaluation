import os
import re
import base64
import requests
import argparse
from openai import OpenAI
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-audio-preview",
        help="Here listed some models that can accept audio input: https://platform.openai.com/docs/models/gpt-4o-realtime",
    )
    parser.add_argument(
        "--high_quality_path",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--low_quality_path",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--groundTruth_path",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="answer.txt",
    )
    parser.add_argument(
        "--wav_folder_path",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    return args

client = OpenAI()

args = parse_args()

high_quality_path = args.high_quality_path
with open(high_quality_path, "rb") as audio_file:
    high_wav_data = audio_file.read()

    
low_quality_path = args.low_quality_path
with open(low_quality_path, "rb") as audio_file:
    low_wav_data = audio_file.read()

high_quality_encoded_string = base64.b64encode(high_wav_data).decode('utf-8')
low_quality_encoded_string = base64.b64encode(low_wav_data).decode('utf-8')

with open(args.output_path, "w") as result:
    result.write("systems,SIG,BAK,OVR\n")

    for root, dirs, files in os.walk(args.wav_folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            # Fetch the audio file and convert it to a base64 encoded string
            with open(file_path, "rb") as audio_file:
                wav_data = audio_file.read()
            encoded_string = base64.b64encode(wav_data).decode('utf-8')

            while True:
                try:
                    completion = client.chat.completions.create(
                        model=args.model,
                        modalities=["text", "audio"],
                        audio={"voice": "alloy", "format": "wav"},
                        messages=[
                            {
                                "role": "user",
                                "content": [{
                                        "type": "text",
                                        "text": "Example 1: This is a Low Quality Audio, its score is\nSIG: [2.60], BAK: [1.00], OVRL: [1.40]"
                                    },
                                    {
                                        "type": "input_audio",
                                        "input_audio": {
                                            "data": low_quality_encoded_string,  # Replace with actual low-quality audio data
                                            "format": "wav"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "Example 2: This is a High Quality Audio, its score is\nSIG: [4.80], BAK: [4.80], OVRL: [5]"
                                    },
                                    {
                                        "type": "input_audio",
                                        "input_audio": {
                                            "data": high_quality_encoded_string,  # Replace with actual high-quality audio data
                                            "format": "wav"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": """
                    The above examples show how the scale you should rate the speech samples. Please rate the quality of another given speech sample based on the following.
                    1. You are an expert rater of speech quality. Remember that you are a very, very strict critic; you will not give out a high score (>4) easily unless the quality is very nice.
                    2. You will be given an audio sample of a person speaking in a possibly noisy environment.
                    3. Please listen to the audio and attend to the speech signal, the background noise, and the overall quality of the audio sample. Any existence of background noise decreases the score greatly.
                    4. For speech signal quality, your answer should be an overall score from 1 to 5, where 1 means the signal is distorted and 5 means the signal is very clear.
                    5. For background noise intrusiveness, your answer should also be scored from 1 to 5, where 1 means the background is very noisy and 5 means very quiet.
                    6. The overall quality is the overall quality of the speech sample affected by the above two factors; your answer should also be scored from 1 to 5, 1 indicating poor quality and 5 indicating excellent quality.
                    7. Your score should use decimal values up to two decimal places.
                    8. Your answer should be in the format "SIG: [X], BAK: [Y], OVRL: [Z]", where X is the score you give about speech signal quality, Y is the score about background noise, and Z is the overall score. Wrap the score in square brackets. You don't need to provide any reason.\n\n"""
                                    },
                                    {
                                        "type": "input_audio",
                                        "input_audio": {
                                            "data": encoded_string,  # Your audio data here
                                            "format": "wav"
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    input_string = completion.choices[0].message.audio.transcript
                    matches = re.findall(r'\[([\d.-]+)\]', input_string)

                    if (len(matches) != 3):
                        raise ValueError("Reply format not match")

                    file_name = file_path.split('/')[-1]
                    remove_extension = file_name.split('.')[0]
                    sound_name = remove_extension.split('-')[-1]
                    
                    float_values = [float(match) for match in matches]
                    x, y, z = float_values
                    result.write(f"{sound_name},{x},{y},{z}\n")
                    break

                except (ValueError, IndexError) as e:
                    print(f"[ERROR] {e}")
                    time.sleep(1)
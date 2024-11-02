import os
import time
import sys
import re
import base64
import argparse
from openai import OpenAI
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-audio-preview",
        help="Here lists some models that can accept audio input: https://platform.openai.com/docs/models/gpt-4o-realtime",
    )
    parser.add_argument(
        "--shot_list",
        nargs="+",
        help="List of WAV files as few-shot learning."
    )
    parser.add_argument(
        "--prompt_list",
        nargs="+",
        help="List of descriptions for each WAV files you provided."
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

def find_scores(file_path, search_str):
    system_id = search_str.split('-')[-1].split('.')[0]
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(system_id):
                _, sig, bak, ovr = line.strip().split(',')
                return float(sig), float(bak), float(ovr)
    print("[ERROR]: Data not found in provided text file.")
    sys.exit(1)


client = OpenAI()

args = parse_args()

few_shot_examples = []
for shot_path in args.shot_list:
    with open(shot_path, "rb") as audio_file:
        wav_data = audio_file.read()
    encoded_string = base64.b64encode(wav_data).decode('utf-8')
    SIG, BAK, OVR = find_scores(args.groundTruth_path, shot_path)
    few_shot_examples.append({
        "SIG": SIG,
        "BAK": BAK,
        "OVR": OVR,
        "encoded_string": encoded_string
    })
    
few_shot_prompt = []
for shot_prompt in args.prompt_list:
    few_shot_prompt.append(shot_prompt)

with open(args.output_path, "w") as result:
    result.write("systems,SIG,BAK,OVR\n")

    for root, dirs, files in os.walk(args.wav_folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            # Fetch the audio file and convert it to a base64 encoded string
            with open(file_path, "rb") as audio_file:
                wav_data = audio_file.read()
            encoded_string = base64.b64encode(wav_data).decode('utf-8')

            few_shot_prompts = []
            for i, example in enumerate(few_shot_examples, start=1):
                few_shot_prompts.extend([
                    {"type": "text", "text": f"Example {i}: {few_shot_prompt[i-1]} Its score is:\nSIG: [{example['SIG']}], BAK: [{example['BAK']}], OVR: [{example['OVR']}]"},
                    {"type": "input_audio", "input_audio": {"data": example["encoded_string"], "format": "wav"}}
                ])
            
            while True:
                try:
                    completion = client.chat.completions.create(
                        model=args.model,
                        modalities=["text"],
                        messages=[
                            {"role": "user", "content": few_shot_prompts + [
                                {"type": "text", "text": """
                    The above examples show how the scale you should rate the speech samples, the audio quality are ranging from great to poor.
                    Please rate the quality of the below given speech sample based on the following.
                    1. You are an expert rater of speech quality. Remember that you are a very, very strict critic, ***you can hear and focus on the details that others may not notice to***; you will not give out a high score easily unless the quality is very nice.
                    2. You will be given an audio sample of a person speaking in a possibly noisy environment.
                    3. Please listen to the audio and attend to the speech signal, the background noise, and the overall quality of the audio sample. Any existence of background noise decreases the score greatly.
                    4. For speech signal quality, your answer should be an overall score from 1 to 5, where 1 means the signal is distorted and 5 means the signal is very clear.
                    5. For background noise intrusiveness, your answer should also be scored from 1 to 5, where 1 means the background is very noisy and 5 means very quiet.
                    6. The overall quality is the overall quality of the speech sample affected by the above two factors; your answer should also be scored from 1 to 5, 1 indicating poor quality and 5 indicating excellent quality.
                    7. Your score should use decimal values up to two decimal places.
                    8. Your answer should be in the format "SIG: [X], BAK: [Y], OVR: [Z]", where X is the score you give about speech signal quality, Y is the score about background noise, and Z is the overall score. Wrap the score in square brackets. You don't need to provide any reason.\n\n"""
                                    },
                                {"type": "input_audio", "input_audio": {"data": encoded_string, "format": "wav"}}
                            ]}
                        ]
                    )
                    # print(completion.usage)   # 計算當次的token count

                    output_string = completion.choices[0].message.content
                    matches = re.findall(r'\[([\d.-]+)\]', output_string)

                    if (len(matches) != 3):
                        raise ValueError("Reply format not match")

                    file_name = file_path.split('/')[-1]
                    remove_extension = file_name.split('.')[0]
                    sound_name = remove_extension.split('-')[-1]
                    
                    float_values = [float(match) for match in matches]
                    x, y, z = float_values
                    result.write(f"{sound_name},{x},{y},{z}\n")
                    
                    print(f"{sound_name},{x},{y},{z}")
                    
                    break

                except (ValueError, IndexError) as e:
                    print(f"[ERROR] {e}")
                    time.sleep(1)
OPENAI_API_KEY="YOUR-API-KEY" \
    python audioAPI.py \
        --model "gpt-4o-audio-preview" \
        --shot_list "data/wav/voicemos2024-track3-p232_sys2_005.wav" "data/wav/voicemos2024-track3-p232_sys4_340.wav" "data/wav/voicemos2024-track3-p232_sys7_328.wav"\
        --prompt_list "This is a perfect high quality audio. It clearly reads the text out loudly and the background is very quiet." "This is a mid quality audio. It is kind of muddy because of the recorder issues, but still can understand what he says." "This is a poor quality audio. There is loud music in the background and the speaker's voice is distorted." \
        --groundTruth_path "eval_mos_list.txt" \
        --output_path "answer.txt" \
        --wav_folder_path "data/wav"
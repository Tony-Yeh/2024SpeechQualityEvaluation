OPENAI_API_KEY="YOUR-API-KEY" \
    python audioAPI.py \
        --model "gpt-4o-audio-preview" \
        --high_quality_path "data/wav/voicemos2024-track3-p257_sys2_287.wav" \
        --low_quality_path "data/wav/voicemos2024-track3-p257_sys6_114.wav" \
        --groundTruth_path "eval_mos_list.txt" \
        --output_path "answer.txt" \
        --wav_folder_path "data/wav"
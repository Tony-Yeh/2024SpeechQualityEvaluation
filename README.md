# 2024SpeechQualityEvaluation
The project utilizes the latest gpt-4o-audio-preview model to evaluate the speech quality and compute the LCC metrics with human labeled ground truth.

## Install Packages
Install requirements in your virtual environment.
```sh
pip install -r requirements.txt
```

## Run the Code
1. Paste an openAI API key into OPENAI_API_KEY="YOUR-API-KEY" in your run_audioAPI.sh file
2. Modify the arguments in the shell script file to meet your needs
3. Run the following command
```sh
sh run_audioAPI.sh
```
4. To calculate LCC with ground truth, you can easily utilize sort.py we provided. This sorts the answers into lexicographic order. Make sure you done this on both eval_mos_list.txt (gound truth) and your answer.txt

5. Run the command to see the result
```sh
sh calc.sh
```

## Reference and Datasets

For the datasets and other concepts, please refer to the following paper:

Wen-Chin Huang, Szu-Wei Fu, Erica Cooper, Ryandhimas E. Zezario, Tomoki Toda, Hsin-Min Wang, Junichi Yamagishi, and Yu Tsao. (2024). *The VoiceMOS Challenge 2024: Beyond Speech Quality Prediction*. arXiv preprint [arXiv:2409.07001](https://arxiv.org/abs/2409.07001)

The dataset is from track 3.

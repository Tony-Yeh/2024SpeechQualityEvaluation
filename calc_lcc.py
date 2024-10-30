import csv
import argparse
from scipy.stats import pearsonr

def read_csv(file_path):
    sig_list, bak_list, ovr_list = [], [], []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            sig_list.append(float(row[1]))
            bak_list.append(float(row[2]))
            ovr_list.append(float(row[3]))
    return sig_list, bak_list, ovr_list

def calculate_lcc(list1, list2):
    lcc, _ = pearsonr(list1, list2)
    return lcc

def main(answer_file, eval_file):
    # Note that we assume the order of the answers (their sample id) in the two files is the same
    answer_sig, answer_bak, answer_ovr = read_csv(answer_file)
    eval_sig, eval_bak, eval_ovr = read_csv(eval_file)

    lcc_sig = calculate_lcc(answer_sig, eval_sig)
    lcc_bak = calculate_lcc(answer_bak, eval_bak)
    lcc_ovr = calculate_lcc(answer_ovr, eval_ovr)

    print(f"LCC for SIG: {lcc_sig:.4f}")
    print(f"LCC for BAK: {lcc_bak:.4f}")
    print(f"LCC for OVR: {lcc_ovr:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate SRCC between answer and evaluation files.")
    parser.add_argument("--answer_file", type=str, required=True)
    parser.add_argument("--eval_file", type=str, required=True)

    args = parser.parse_args()

    main(args.answer_file, args.eval_file)
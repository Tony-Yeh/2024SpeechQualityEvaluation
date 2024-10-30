def sort_systems_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    header = lines[0]
    content = lines[1:]

    sorted_content = sorted(content)

    with open(output_file, 'w') as file:
        file.write(header)
        file.writelines(sorted_content)

input_truth = 'eval_mos_list.txt'
output_truth = 'sorted_eval_mos_list.txt'
input_answer = 'answer.txt'
output_answer = 'sorted_answer.txt'

sort_systems_file(input_truth, output_truth)
sort_systems_file(input_answer, output_answer)

print(f"Sorted data has been produced.")

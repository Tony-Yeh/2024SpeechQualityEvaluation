def sort_systems_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    header = lines[0]
    content = lines[1:]

    sorted_content = sorted(content)

    with open(output_file, 'w') as file:
        file.write(header)
        file.writelines(sorted_content)

input_file = 'eval_mos_list.txt'
output_file = 'sorted_eval_mos_list.txt'

sort_systems_file(input_file, output_file)

print(f"Sorted data has been written to '{output_file}'.")

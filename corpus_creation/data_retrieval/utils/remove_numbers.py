
def reformat_text_file(input_file, output_file):
    # Read the entire file and remove existing newlines
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    formatted_text = ""
    for char in text:
        if not char.isdigit():
            formatted_text += char
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(formatted_text)

# Example usage:
input_file = "C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles Analytica Priora\\input.txt"
output_file = "C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles Analytica Priora\\output.txt"
reformat_text_file(input_file, output_file)
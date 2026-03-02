
def reformat_text_file(input_file, output_file):
    # Read the entire file and remove existing newlines
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Add newlines after '.' or ':'
    cur_chapter=""
    chapter_num=0
    for line in text.splitlines():
        if line.isdigit():
            if chapter_num != 0:
                with open(output_file+str(chapter_num)+"_lat.txt", "w", encoding="utf-8") as f:#TODO: GREEK HERE
                    f.write(cur_chapter+"\n")
                    cur_chapter=""
            chapter_num = int(line)
        else:
            cur_chapter+="\n"+line

    with open(output_file + str(chapter_num) + "_lat.txt", "w", encoding="utf-8") as f:  # TODO: GREEK HERE
        f.write(cur_chapter + "\n")

    for i in range(0, chapter_num+1):
        with open(output_file+str(i)+"_lat.txt", "r", encoding="utf-8") as f:#TODO: GREEK HERE
            text=f.read().replace("\n", " ")
        formatted_text = ""
        whitespace=False
        for char in text:
            if char.isspace() and not whitespace:
                whitespace=True
                formatted_text+=char
            elif not char.isspace():
                if whitespace:
                    whitespace=False
                formatted_text += char
            if char in [".", ";", "·", "?"]:#":",
                formatted_text += "\n"
                whitespace=False

        # Strip leading/trailing spaces from each line
        cleaned_lines = [line.lstrip() for line in formatted_text.splitlines()]
        cleaned_text = "\n".join(cleaned_lines)

        # Save the reformatted text
        with open(output_file+str(i)+"_lat.txt", "w", encoding="utf-8") as f:#TODO: GREEK HERE
            f.write(cleaned_text)



# Example usage:
input_file = "C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles_Med\\de_hypothesibus_planetarum.txt"
output_file = "C:\\Users\\sebas\\Documents\\LMU\\Bachelorarbeit\\Data\\Aristoteles_Med\\"
reformat_text_file(input_file, output_file)
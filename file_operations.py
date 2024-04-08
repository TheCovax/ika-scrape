

def write_to_file(str,filename="tmp.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str)
    file.close()
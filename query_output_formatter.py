# Receive the query results in list and create formatted printing

def formatted_output(result_list):
    if len(result_list) == 0:
        print("Empty set")
    else:
        max_len = 0
        for result in result_list:
            if len(result) > max_len:
                max_len = len(result)

        print("Query Result:")
        line = "+"
        for i in range(max_len):
            line += "-"
        line += "+"
        print(line)
        for result in result_list:
            space_num = max_len - len(result)
            space_str = ""
            for i in range(space_num):
                space_str += " "
            print("|" + result + space_str + "|")
        print(line)



from schemas import CouRow, EmpRow


def inputData(filename):
    f = open('./data/' + filename, 'r')
    table_list = []
    src_data = f.readlines()
    src_data.pop(0)
    if filename == "COURSE.TXT":
        table_name = "course"
        for rows in src_data:
            rows = rows[:-1]
            content = rows.split('|')
            tuples = CouRow(content[0], content[1], content[2], content[3])
            table_list.append(tuples)
        print("Ready")

    elif filename == "EMPLOYEE.TXT":
        table_name = "employee"
        for rows in src_data:
            rows = rows[:-1]
            content = rows.split('|')
            tuples = EmpRow(content[0], content[1], content[2], content[3], content[4])
            table_list.append(tuples)
        print("Ready")

    else:
        print("Wrong file name entered, please try again.")

    return table_name, table_list


# Test code
if __name__ == "__main__":
    tname1, tlst1 = inputData("course.txt")
    tname2, tlst2 = inputData("employee.txt")
    print(tname1)
    for i in range(20):
        tlst1[i].printRow()
    print(tname2)
    for i in range(20):
        tlst2[i].printRow()
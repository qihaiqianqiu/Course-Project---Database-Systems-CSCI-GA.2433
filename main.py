import time
import Query_one
import Query_two
import Query_three
from input import inputData
from BplusTree import Bplus_Tree
"""
print("Usage - Call following commands:")
print("1) INPUT one_string")
print("2) PREPARE one_string")
print("3) Q1 one_string")
print("4) Q1C one_string")
print("5) Q1O one_string")
print("6) Q2 one_string")
print("7) Q2C one_string")
print("8) Q2O one_string")
print("9) Q3 one_string")
print("10) Q3C one_string")
print("11) Q3O one_string")
print("12) QUIT")
print("13) RESULT ON")
print("14) RESULT OFF")
"""


# Default setting
result_printing_flag = True
data = {}

while True:
    input_cmd = input("Enter Command >").upper()
    parsed_cmd = input_cmd.split(" ")

    # RESULT ON/OFF CMD
    if parsed_cmd[0] == "RESULT":
        if parsed_cmd[1] == "ON":
            result_printing_flag = True
            print("Ready")
        if parsed_cmd[1] == "OFF":
            result_printing_flag = False
            print("Ready")

    # QUIT CMD
    if parsed_cmd[0] == "QUIT":
        exit(233)

    # INPUT CMD
    if parsed_cmd[0] == "INPUT":
        table_name, table_list = inputData(parsed_cmd[1])
        data[table_name] = table_list

    # PREPARE CMD
    if parsed_cmd[0] == "PREPARE":
        if parsed_cmd[1] == "CANONICAL":

            # B+tree for Q1C
            time_start_Q1C = time.time()
            Q1C_tree = Bplus_Tree(15)
            for rows in data["employee"]:
                Q1C_tree.insert(rows.Manager, rows)
            time_end_Q1C = time.time()
            print("Canonical indexing(B+tree) time on Q1 is:" + str(time_end_Q1C - time_start_Q1C))

            # B+tree for Q2
            time_start_Q2C = time.time()
            Q2C_tree = Bplus_Tree(15)
            for rows in data["course"]:
                Q2C_tree.insert(rows.EmpID, rows)
            time_end_Q2C = time.time()
            print("Canonical indexing(B+tree) time on Q2 is:" + str(time_end_Q2C - time_start_Q2C))

            # B+tree for Q3
            time_start_Q3C = time.time()
            Q3C_tree = Bplus_Tree(15)
            for rows in data["course"]:
                Q3C_tree.insert(rows.Prof, rows)
            time_end_Q3C = time.time()
            print("Canonical indexing(B+tree) time on Q3 is:" + str(time_end_Q3C - time_start_Q3C))

        elif parsed_cmd[1] == "OPTIMIZED":
            # Optimized for Q1O
            time_start_Q1O = time.time()
            Q1O_tree = Bplus_Tree(15)
            for rows in data["employee"]:
                Q1O_tree.insert(int(rows.Manager), rows)
            time_end_Q1O = time.time()
            print("Optimized preparation time for Q1 is: " + str(time_end_Q1O - time_start_Q1O))

            # Optimized for Q2O
            time_start_Q2O = time.time()
            Q2O_tree_emp = Bplus_Tree(15)
            Q2O_tree_cou = Bplus_Tree(15)
            for row in data["employee"]:
                Q2O_tree_emp.insert(row.Department, row)
            for rows in data["course"]:
                Q2O_tree_cou.insert(rows.EmpID, rows)
            end_time_Q2O = time.time()
            print("Optimized preparation time on Q2 is:" + str(end_time_Q2O - time_start_Q2O))

            # Optimized for Q3
            time_start_Q3O = time.time()
            Q3O_tree = Bplus_Tree(15)
            for rows in data["course"]:
                Q3O_tree.insert(rows.Prof, rows)
            time_end_Q3O = time.time()
            print("Optimized preparation time on Q3 is:" + str(time_end_Q3O - time_start_Q3O))

        else:
            print("Wrong preparation mode entered, please try again.")

        print("Ready")

    # Query CMD:
    else:
        one_string = parsed_cmd[1].lower()
        if parsed_cmd[0] == "Q1":
            Query_one.Q1(data["employee"], one_string, result_printing_flag)
        if parsed_cmd[0] == "Q1C":
            Query_one.Q1C(Q1C_tree, one_string, result_printing_flag)
        if parsed_cmd[0] == "Q1O":
            Query_one.Q1O(Q1O_tree, one_string, result_printing_flag)

        if parsed_cmd[0] == "Q2":
            Query_two.Q2(data["employee"], data["course"], one_string, result_printing_flag)
        if parsed_cmd[0] == "Q2C":
            Query_two.Q2C(data["employee"], Q2C_tree, one_string, result_printing_flag)
        if parsed_cmd[0] == "Q2O":
            Query_two.Q2O(Q2O_tree_emp, Q2O_tree_cou, one_string, result_printing_flag)

        if parsed_cmd[0] == "Q3":
            Query_three.Q3(data["employee"], data["course"], one_string, result_printing_flag)
        if parsed_cmd[0] == "Q3C":
            Query_three.Q3C(data["employee"], Q3C_tree, one_string, result_printing_flag)
        if parsed_cmd[0] == "Q3O":
            Query_three.Q3O(Q3O_tree, one_string, result_printing_flag)

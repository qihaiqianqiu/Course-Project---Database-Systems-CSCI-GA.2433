"""
SELECT ID FROM EMPLOYEE e1
    WHERE e1.department = 'department35' and
    not exists (SELECT * FROM EMPLOYEE e2 WHERE e2.Department = e1.Department
            and e2.salary>e1.salary and
                exists (SELECT * from COURSE c Where c.EmpID=e2.ID));
"""
import time
import query_output_formatter


# Implement loop method
# Current implement equal to simple department match
def Q2(employee_table, course_table, department_id, flag):
    result_set = []
    start_time = time.time()
    for tuple_e1 in employee_table:
        if tuple_e1.Department == department_id:
            outer_not_exist_flag = True
            for tuple_e2 in employee_table:
                if tuple_e2.Department == tuple_e1.Department and int(tuple_e2.Salary) > int(tuple_e1.Salary):
                    for tuple_c in course_table:
                        if tuple_c.EmpID == tuple_e2.ID:
                            # exists return True, e2 be selected
                            outer_not_exist_flag = False
                            break
            if outer_not_exist_flag:
                result_set.append(tuple_e1.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q2: " + str(query_time))


# In canonical method (B+tree)
# Really slow by now, may need further improvement
def Q2C(employee_table, course_tree, department_id, flag):
    result_set = []
    start_time = time.time()
    for tuple_e1 in employee_table:
        if tuple_e1.Department == department_id:
            outer_not_exist_flag = True
            for tuple_e2 in employee_table:
                if tuple_e2.Department == tuple_e1.Department and int(tuple_e2.Salary) > int(tuple_e1.Salary):
                    if not course_tree.search(tuple_e2.ID) is None:
                        # exists return True, e2 be selected
                        outer_not_exist_flag = False
                        break
            if outer_not_exist_flag:
                result_set.append(tuple_e1.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q2C: " + str(query_time))


# Optimized method: multi-column indexing, with optimized exists
# (doesn't scan whole course table, break once found matched record)
def Q2O(employee_tree, course_tree, department_id, flag):
    result_set = []
    start_time = time.time()
    # Search on first tree on Employee(department)
    for tuple_e1 in employee_tree.search(department_id):
        outer_not_exist_flag = True
        # Handle "and" operation in the outer NOT EXISTS command
        for tuple_e2 in employee_tree.search(tuple_e1.Department):
            # Check the salary
            if int(tuple_e1.Salary) < int(tuple_e2.Salary):
                # Search crossing on second tree on course(ID)
                # Also not look up for whole tuples, once there is some records in inner selection, EXISTS returns True
                if not course_tree.search(tuple_e2.ID) is None:
                    # So outer NOT EXISTS returns False
                    outer_not_exist_flag = False
        if outer_not_exist_flag:
            result_set.append(tuple_e1.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q2O: " + str(query_time))



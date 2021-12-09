"""
SELECT e.ID FROM Employee e
WHERE not exists (SELECT * FROM COURSE c1 WHERE c1.prof = “one_string” and
    not exists (SELECT * from COURSE c2 WHERE c2.EmpID=e.ID and c2.courseID=c1.courseID and c2.prof = “one_string”));
"""
import time
import query_output_formatter


# In loop method
def Q3(employee_table, course_table, prof_name, flag):
    result_set = []
    start_time = time.time()
    for tuple_e in employee_table:
        outer_not_exists_flag = True
        for tuple_c1 in course_table:
            if tuple_c1.Prof == prof_name:
                inner_not_exists_flag = True
                for tuple_c2 in course_table:
                    if tuple_c2.EmpID == tuple_e.ID and \
                            tuple_c2.CourseID == tuple_c1.CourseID and tuple_c2.Prof == prof_name:
                        inner_not_exists_flag = False
                if inner_not_exists_flag:
                    outer_not_exists_flag = False
        if outer_not_exists_flag:
            result_set.append(tuple_e.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q3: " + str(query_time))


# Canonical method (B+tree)
def Q3C(employee_table, course_tree, prof_name, flag):
    result_set = []
    start_time = time.time()
    for tuple_e in employee_table:
        outer_not_exists_flag = True
        for tuple_c1 in course_tree.search(prof_name):
            inner_not_exists_flag = True
            for tuple_c2 in course_tree.search(prof_name):
                if tuple_c2.EmpID == tuple_e.ID and tuple_c2.CourseID == tuple_c1.CourseID:
                    # Record c2 exists, not exists return False
                    inner_not_exists_flag = False
            if inner_not_exists_flag:
                outer_not_exists_flag = False
        if outer_not_exists_flag:
            result_set.append(tuple_e.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q3C: " + str(query_time))


"""
Reform another query in another process, by comparing the number of course taken, rather then by EXISTS/NOT EXISTS.
The new logical for the Query3 is implemented as the following SQL:
SELECT c.EmpID from course c
where c.prof = 'one_string' group by c.EmpID
having count(*) = (SELECT count(distinct CourseID) from course c1 where c1.prof = 'one_string');
"""


def Q3O(course_tree, prof_name, flag):
    result_set = []
    start_time = time.time()
    empid_dict = {}
    for tuple_c in course_tree.search(prof_name):
        # Calculate count(*) group by EmpID, record number of courses taken from prof by employees
        if empid_dict.__contains__(tuple_c.EmpID):
            empid_dict[tuple_c.EmpID] += 1
        else:
            empid_dict[tuple_c.EmpID] = 1
    # Calculate number of course the prof offering
    distinct_courseid = []
    for tuple_c1 in course_tree.search(prof_name):
        distinct_courseid.append(tuple_c1.CourseID)
    course_count = len(set(distinct_courseid))
    # Compare number of course taken of each employee with the target value
    for key in empid_dict:
        if empid_dict[key] == course_count:
            # If same, then collect the record
            result_set.append(key)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on Q3O: " + str(query_time))





"""
SELECT ID FROM EMPLOYEE
    WHERE manager=”one_string”;
"""
import time
import query_output_formatter


# In loop method
def Q1(employee_table, manager_id, flag):
    result_set = []
    start_time = time.time()
    for employee_tuple in employee_table:
        if employee_tuple.Manager == manager_id:
            result_set.append(employee_tuple.ID)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        query_output_formatter.formatted_output(result_set)
    print("Time spent on the Q1: " + str(query_time))


# In canonical method (B+Tree)
def Q1C(employee_tree, manager_id, flag):
    start_time = time.time()
    result_set = employee_tree.search(manager_id)
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        result_lst = []
        for item in result_set:
            result_lst.append(item.ID)
        query_output_formatter.formatted_output(result_lst)
    print("Time spent on the Q1C: " + str(query_time))


# In optimized method (B+Tree with int key)
def Q1O(employee_tree, manager_id, flag):
    start_time = time.time()
    # Search for int value of the optimized indexing, rather than the string matching method
    # The optimized indexing tree is also a B+tree, so the data structure itself is sorted when search
    # No more operations needed, just do the search on tree
    result_set = employee_tree.search(int(manager_id))
    end_time = time.time()
    query_time = end_time - start_time
    if flag:
        # Print formatted result
        result_lst = []
        for item in result_set:
            result_lst.append(item.ID)
        query_output_formatter.formatted_output(result_lst)
    print("Time spent on the Q1O: " + str(query_time))


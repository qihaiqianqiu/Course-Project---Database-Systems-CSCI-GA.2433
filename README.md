# Database Systems, CSCI-GA.2433-011 Course Project Assignment

### How the program should be run

The program has a main interface **Main.py**. Run the Python script will call the command line prompet to receiving your commands until an *EXIT* command is received. All possible commands are as follows:

| Command                 | Description                                                  |
| :---------------------- | ------------------------------------------------------------ |
| `INPUT one_string`      | Read data from txt file. one_string should be "employee.txt" or "course.txt" |
| `PREPARE one_string`    | Build index or implement optimized method for Querys. one_string should be "canonical" or "optimized" |
| `Qi/QiC/QiO one_string` | Run Query under `one_string` condition in loop method, canonical method and optimized method |
| `QUIT`                  | Exit the program                                             |
| `RESULT ON`             | Show Query results(Default is ON)                            |
| `RESULT OFF`            | Hide Query results                                           |

When reading commands, all entered characters in prompt will be *converted to upper case string automatically*, so enter upper or lower is not a problem and you also don't need to specificlly add  `' '` or` " "` on your input `one_string`.

### What libraries used

`time` from Python standrad library to calculate execution time

`bisect` from Python standrad librity. 

This module provides support for maintaining a list in sorted order without having to sort the list after each insertion.

In program it is implemented to locate the index when inserting/searching values in a B+ Tree.

### What method is for QiO command

***Q1O***: Because the query is quite simple, I just optimize it with the data type design. Be default, when building B+tree indexing, the key will be handled as a `String` value, which length is not fixed, also cost more to judge for the equality. So in Q1O optimization, I  modify the B+tree indexing to index on `int` value of manager's id specificly, this reduce the execution time from e-05 level into e-06 level on my machine. 

```python
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
```



***Q2O***: I make two B+tree to index on both employee table and course table, when do the searching, I look up the department ID on the first tree, then I jump to the course tree to look up at the EmpID, crossed double indexing makes the query much faster then canonical indexing. Also for the `SELECTION` clause, when it is inside the `NOT EXISTS` or `EXISTS`, I don't scan and examine through the whole record one by one, once I meet a record/tuple that satisfy the condition and be selected out, I will return `True` or `False` value for the clause. I don't change the main query composition and logic for Query2 in optimization.

```python
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
```



***Q3O***: I improve the main query composition and logic for Query3 in optimization. Because calling `NOT EXISTS` inside itself is not very efficient. To find employees taking all course from a professor, we could just count the number of course the professor is offering and compare it with the number of course that a employee is taken from that professor. Also, in order to know the information, we don't need to visit employee table, because the course table has already included EmpID domain, so it is also improved to visit only the course table as the B+tree on course.

```python
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
```

### Additional information

**Q2** and **Q2C** will take some time, other Querys are fast.

Data file in txt should be put into the directory `/project_folder/data` , `course_q3.txt` and `employee_q3.txt` in the folder are for testing the query execution correctness of the Q3. `course.txt` and `employee.txt` are original data in HW3.

No any SQL libraries included.

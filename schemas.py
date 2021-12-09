class EmpRow:
    def __init__(self, id, name, salary, manager, department):
        self.ID = id
        self.Name = name
        self.Salary = salary
        self.Manager = manager
        self.Department = department

    def printRow(self):
        concat = self.ID + "|" + self.Name + "|" + self.Salary + "|" + self.Manager + "|" + self.Department
        print(concat)


class CouRow:
    def __init__(self, empid, courseid, prof, grade):
        self.EmpID = empid
        self.CourseID = courseid
        self.Prof = prof
        self.Grade = grade

    def printRow(self):
        concat = self.EmpID + "|" + self.CourseID + "|" + self.Prof + "|" + self.Grade
        print(concat)


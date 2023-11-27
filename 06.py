def add_employee_to_file(record, path):
    file = open(path, 'a')
    file.write('\n' + record)
    file.close()

record = "Baby Boss,15"
path = 'employees.txt'
print(add_employee_to_file(record, path))
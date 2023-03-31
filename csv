import csv

class ObjectCSVMapper:
    def __init__(self, fields):
        self.fields = fields
        
    def to_csv(self, obj):
        row = []
        for field in self.fields:
            value = getattr(obj, field)
            if isinstance(value, list):
                value = ';'.join(value)
            elif not isinstance(value, str):
                value = str(value)
            row.append(value)
        return row
    
    def from_csv(self, row):
        obj = type('', (), {})()
        for i, field in enumerate(self.fields):
            value = row[i]
            if ';' in value:
                value = value.split(';')
            setattr(obj, field, value)
        return obj
    
    def to_csv_list(self, lst):
        csv_rows = []
        for obj in lst:
            row = self.to_csv(obj)
            csv_rows.append(','.join(row))
        return '\n'.join(csv_rows)
    
    def from_csv_list(self, csv_str):
        lst = []
        rows = csv_str.strip().split('\n')
        for row in rows:
            row_lst = row.split(',')
            obj = self.from_csv(row_lst)
            lst.append(obj)
        return lst
    
    def to_csv_file(self, objs, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.fields)
            for obj in objs:
                writer.writerow(self.to_csv(obj))
                
    def from_csv_file(self, filename):
        objs = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                obj = self.from_csv(row)
                objs.append(obj)
        return objs


class Person:
    def __init__(self, name, age, hobbies):
        self.name = name
        self.age = age
        self.hobbies = hobbies
        
people = [
    Person('Alice', 25, ['reading', 'hiking']),
    Person('Bob', 30, ['gaming', 'cooking']),
    Person('Charlie', 35, ['traveling'])
]

mapper = ObjectCSVMapper(['name', 'age', 'hobbies'])
mapper.to_csv_file(people, 'people.csv')

loaded_people = mapper.from_csv_file('people.csv')
for person in loaded_people:
    print(person.name, person.age, person.hobbies)

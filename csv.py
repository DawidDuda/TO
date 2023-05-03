import csv

class ObjectCSVMapper:
    def __init__(self, fields):
        self.fields = fields
        
    def to_csv(self, obj):
        row = []
        for field in self.fields:
            value = getattr(obj, field)
            if isinstance(value, list) or isinstance(value, set):
                value = ';'.join(map(str, value))
            elif isinstance(value, dict):
                value = ','.join([f"{k}:{v}" for k, v in value.items()])
            elif isinstance(value, tuple):
                value = ','.join(str(x) for x in value)
            elif isinstance(value, Address):
                
                value = "$" + value.a_id + "$"
            else:
                value = str(value)
            row.append(value)
        return row
    
    @classmethod
    def from_csv(cls, row, fields):
        obj = type('', (), {})()
        for i, field in enumerate(fields):
            value = row[i]
            if ';' in value:
                value = value.split(';')
                if len(value) == 1:
                    value = value[0]
            elif ',' in value:
                items = value.split(',')
                if ':' in items[0]:
                    value = {k: v for k, v in [x.split(':') for x in items]}
                else:
                    value = tuple(items)
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
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
            obj = self.from_csv(row_lst, self.fields)
            lst.append(obj)
        return lst
    
    def to_csv_file(self, objs, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.fields)
            for obj in objs:
                row = self.to_csv(obj)
                writer.writerow(row)
                
    def from_csv_file(self, filename):
        objs = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            fields = next(reader)
            for row in reader:
                obj = self.from_csv(row, fields)
                objs.append(obj)
        return objs


class Person:
    def __init__(self, name, age, hobbies, favorite_books, contact_info, address):
        self.name = name
        self.age = age
        self.hobbies = hobbies
        self.favorite_books = favorite_books
        self.contact_info = contact_info
        self.address = address
        
class Address:
    def __init__(self, a_id, street, city):
        self.a_id = a_id
        self.street = street
        self.city = city
        
add = [
       Address("id_1", "Wall st.", "New York"),
       Address("id_2", "Wall st.", "New York"),
       Address("id_3", "Wall st.", "New York"),
       ]
mapper1 = ObjectCSVMapper(["a_id", "street", "city"])

# write the objects to a CSV file
mapper1.to_csv_file(add, "address.csv")

people = [
    Person("John", 25, ["reading", "hiking"], {"fiction": "1984", "non-fiction": "The Art of Thinking Clearly"}, ("john@example.com", "555-1234"), add[0]),
    Person("Jane", 30, ["swimming", "dancing"], {"fiction": "Pride and Prejudice", "non-fiction": "Sapiens"}, ("jane@example.com", "555-5678"), add[1]),
    Person("Bob", 40, ["gardening", "cooking"], {"fiction": "The Great Gatsby", "non-fiction": "Atomic Habits"}, ("bob@example.com", "555-9101"), add[2]),
]
# create an instance of ObjectCSVMapper with the desired fields
mapper = ObjectCSVMapper(["name", "age", "hobbies", "favorite_books", "contact_info", "address"])

# write the objects to a CSV file
mapper.to_csv_file(people, "people.csv")

# read the CSV file back into a list of objects
people_from_csv = mapper.from_csv_file("people.csv")

addresses_from_csv = mapper1.from_csv_file("address.csv")

# print the list of objects
for person in people_from_csv:
    for address in addresses_from_csv:        
        if str( "$" + address.a_id +"$" ) == str(person.address):
            person.address = address
            break

# print the list of objects with addresses included
for person in people_from_csv:
    print(person.name, person.age, person.hobbies, person.favorite_books, person.contact_info, person.address.street, person.address.city)

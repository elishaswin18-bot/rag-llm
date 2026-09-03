# =============================================================
# PYTHON BASICS - LEARNING NOTES
# -------------------------------------------------------------
#  1. Variables & Data Types
#  2. Assignment Styles & Constants
#  3. Input & Type Conversion
#  4. Operators
#  5. Conditionals (if / elif / else)
#  6. Loops (for)
#  7. Lists (ordered, changeable)
#  8. Tuples (ordered, immutable)
#  9. Sets (unique values)
# 10. Dictionaries (key-value pairs)
# 11. Functional Programming
# 12. Type Annotations
# -------------------------------------------------------------
# Lines marked "-> " show the output you get when you
# uncomment and run that line.
# =============================================================

from fastapi import requests
from pytest import mark





# =============================================================
# 5. CONDITIONALS (if / elif / else)
# =============================================================

# . if, elif, and else

# age = int(input('enter your age: '))

# if age>18 and age<40:
#   print('he is adult')
# elif age<18:
#   print('he is child')
# else:
#   print('he is too old')
# -> age = 25 : he is adult
# -> age = 10 : he is child
# -> age = 50 : he is too old

# 2. Using range()
# if age in range(0, 18):
#     print("He is a child")
# elif age in range(18, 40):
#     print("He is an adult")
# elif age >= 40:
#     print("He is 40 or older")
# else:
#     print("Invalid age")
# -> age = 10 : He is a child
# -> age = 25 : He is an adult
# -> age = 50 : He is 40 or older
# -> age = -5 : Invalid age


# 4. Put the logic in a function
# def age_group(age):
#     if age < 0:
#         return "invalid age"
#     if age < 18:
#         return "a child"
#     if age < 40:
#         return "an adult"
#     return "40 or older"


# age = int(input("Enter your age: "))
# print(f"He is {age_group(age)}")
# -> age = 25 : He is an adult
# -> age = 10 : He is a child
# -> age = 50 : He is 40 or older


# =============================================================
# 6. LOOPS (for)
# =============================================================

# for loop
# for i in range(5):
#     print(i)
# -> 0
# -> 1
# -> 2
# -> 3
# -> 4

# for mrk in marks:
#     print(mrk)
# -> 90
# -> 85
# -> 92
# -> 88
# -> 95

# for abc in coordinates:
#     # print(abc)
# -> 10
# -> 20

# myusers = {
#     "name": "Rahul",
#     "age": 25,
#     "is_student": True,
# }

# for key, value in myusers.items():
#     print(f"{key}: {value}")
    # print(abc)
# -> name: Rahul
# -> age: 25
# -> is_student: True


# =============================================================
# 7. LISTS (ordered, changeable)
# =============================================================

#List
# fruits = ['apple', 'mango', 'banana']
# fruits.append('orange')      # -> ['apple', 'mango', 'banana', 'orange']
# fruits[1] = 'red orange'     # -> ['apple', 'red orange', 'banana', 'orange']
# fruits.remove('banana')      # -> ['apple', 'red orange', 'orange']
# print(fruits[-3:])           # -> ['apple', 'red orange', 'orange']
#
# print(fruits)                # -> ['apple', 'red orange', 'orange']

# # LIST CURD - ADD, Delete, Update, Read
fruits = ["apple", "banana", "cherry"]

# # Read
# print(fruits)  # ['apple', 'banana', 'cherry']
# print(fruits[0])  # 'apple'
# print(fruits[1])  # 'banana'
# print(fruits[1:3])  # 'banana', 'cherry'
# print(fruits[-1])  # 'cherry'
# print(fruits[-1:])  # 'cherry'

# for fruit in fruits:
#     print(fruit)
# -> apple
# -> banana
# -> cherry

# # Add
fruits.append("orange")  # Add at the end
# -> ['apple', 'banana', 'cherry', 'orange']
fruits.insert(2, "mango")  # Add at index 2
# -> ['apple', 'banana', 'mango', 'cherry', 'orange']
fruits.extend(["kiwi", "pear"]) # Add multiple items
# -> ['apple', 'banana', 'mango', 'cherry', 'orange', 'kiwi', 'pear']
print(fruits)  #  ['apple', 'banana', 'mango', 'cherry', 'orange', 'kiwi', 'pear']

# # Delete  (each line continues from the list above)
fruits.remove("banana")  # Remove by value
# -> ['apple', 'mango', 'cherry', 'orange', 'kiwi', 'pear']
del fruits[1]  # Remove by index
# -> ['apple', 'cherry', 'orange', 'kiwi', 'pear']
print(fruits)  # ['apple', 'cherry', 'orange', 'kiwi', 'pear']
deleted_fruit = fruits.pop(1)  # Remove and return an item by index
# -> deleted_fruit = 'cherry', fruits = ['apple', 'orange', 'kiwi', 'pear']
last_fruit = fruits.pop() # Remove and return the last item
# -> last_fruit = 'pear', fruits = ['apple', 'orange', 'kiwi']
if "mango" in fruits:
    fruits.remove("mango")
# -> nothing happens, "mango" is already gone: ['apple', 'orange', 'kiwi']

# # Update  (starting again from ['apple', 'banana', 'cherry', 'orange'])
# fruits[1] = "kiwi"  # Update index 1
# -> ['apple', 'kiwi', 'cherry', 'orange']
# fruits[1:3] = ["watermelon", "papaya"]# Update multiple items using slicing
# -> ['apple', 'watermelon', 'papaya', 'orange']
# print(fruits)  # ['apple', 'watermelon', 'papaya', 'orange']

# fruits.clear()# Delete every item
# -> []


# =============================================================
# 8. TUPLES (ordered, immutable)
# =============================================================

# Tuple CRUD
# Tuples are ordered but immutable. This means you cannot directly add, update, or delete individual tuple items.
colors = ("red", "green", "blue")
# print(colors)  # ('red', 'green', 'blue')
# print(colors[0])  # 'red'
# print(colors[1:3])  # ('green', 'blue')
# colors[0] = "pink"  # -> TypeError: 'tuple' object does not support item assignment
temp_colors = list(colors)  # Convert to list to modify
temp_colors.append("yellow")  # Add an item
# -> ['red', 'green', 'blue', 'yellow']
temp_colors[1] = "orange"  # Update an item
# -> ['red', 'orange', 'blue', 'yellow']

# colors = ("red", "green", "blue")
# temp = list(colors)
# temp.append('yellow')
# temp[2] = 'grey'
# print(temp)
# -> ['red', 'green', 'grey', 'yellow']
# temp_tupple = tuple(temp)
# print(temp_tupple)
# -> ('red', 'green', 'grey', 'yellow')


# =============================================================
# 9. SETS (unique values)
# =============================================================
# Sets have no order, so the print order below can differ each run.

# set property
# languages[0]  # Error, Sets do not support indexes:
# -> TypeError: 'set' object is not subscriptable
# Adding a duplicate has no effect:
# languages.add("Python")  # -> {'Java', 'Python', 'C++'}  (unchanged)
# languages.add("JavaScript")
# -> {'Java', 'JavaScript', 'Python', 'C++'}
# languages.update(["Go", "Rust"])
# -> {'Java', 'JavaScript', 'C++', 'Go', 'Python', 'Rust'}
# languages.discard("C++") #Remove the old value
# -> {'Java', 'JavaScript', 'Go', 'Python', 'Rust'}
# languages.discard("PHP")  # -> no error even though "PHP" is not there
# languages.remove("Java") # Raises KeyError if the value does not exist
# -> {'JavaScript', 'Go', 'Python', 'Rust'}
# # Remove and return an arbitrary item
# deleted_language = languages.pop()
# -> deleted_language = 'JavaScript', languages = {'Go', 'Python', 'Rust'}
# languages.clear()# Delete every item
# -> set()
# for language in languages:
#     print(language)
# -> Go
# -> Python
# -> Rust


# =============================================================
# 10. DICTIONARIES (key-value pairs)
# =============================================================

# dic property
#dictionary
user = {
    "name": "Rahul",
    "age": 25,
    "city": "London",
}

# for key in user:
#     print(key)
# -> name
# -> age
# -> city

# for value in user.values():
#     print(value)
# -> Rahul
# -> 25
# -> London

# for key, value in user.items():
#     print(key, value)
# -> name Rahul
# -> age 25
# -> city London

# print(user['city'])
# -> London
# user['city'] = 'New Delhi'
# user.update({
#     "age":40,
#     "name": "Tanmay",
# })
# print(user)
# -> {'name': 'Tanmay', 'age': 40, 'city': 'New Delhi'}

# Nested dictionary update
# API responses frequently contain nested dictionaries:``
# user = {
#     "name": "Rahul",
#     "address": {
#         "city": "London",
#         "postcode": "E1 1AA",
#     },
#     "colors": ["red", "green", "blue"],
# }

# print(user["address"]["city"])       # Read     -> London
# user["address"]["city"] = "Oxford"   # Update   -> address city becomes 'Oxford'
# user["address"]["country"] = "UK"    # Add      -> address gains 'country': 'UK'
# del user["address"]["postcode"]      # Delete   -> 'postcode' is gone
# print(user["colors"])  # Read colors list        -> ['red', 'green', 'blue']
# print(user["colors"][0])  # Read colors first item -> red
# after the 4 lines above, user is:
# -> {'name': 'Rahul',
#     'address': {'city': 'Oxford', 'country': 'UK'},
#     'colors': ['red', 'green', 'blue']}

#safe reading with out error
# print(user["color"])# Error
# -> KeyError: 'color'
# print(user.get("color")) # no error, returns None
# -> None
# print(user.get("color", "Color not found")) # output: Color not found
# -> Color not found


# --- List of dictionaries ---
patientlists = [
    {"id":1, "name":"TANMAY", "age":30},
    {"id":2, "name":"TANMAY1", "age":50},
    {"id":3, "name":"TANMAY2", "age":20},
    {"id":4, "name":"TANMAY3", "age":10},
    {"id":5, "name":"TANMAY3", "age":50},
]

# temp = patientlists[3]
# for value in temp.values():
#     if value == 10:
#         print("value is 10")
# -> value is 10        (patientlists[3] is the one with age 10)

# for patient in patientlists:
#     if patient["id"] == 3:
#         print(patient)
#         break
#     print(patient)
# -> {'id': 1, 'name': 'TANMAY', 'age': 30}
# -> {'id': 2, 'name': 'TANMAY1', 'age': 50}
# -> {'id': 3, 'name': 'TANMAY2', 'age': 20}
#    then break stops the loop, so id 4 and 5 are never printed


# =============================================================
# 11. FUNCTIONAL PROGRAMMING
# =============================================================

# FUNTIONAL PROGRAMMING

# def add_user():
#     print('hello')

# add_user()
# -> hello


# def add_user(name):
#     print(f'hello : {name}')

# add_user('Tanmay')
# -> hello : Tanmay


# def add_user(name, age=20):
#     print(f'hello : {name}, age: {age}')

# add_user('Tanmay', 100)
# -> hello : Tanmay, age: 100
# add_user('Tanmay')
# -> hello : Tanmay, age: 20      (default value is used)


# def add_user(name, age=20):
#    return f'hello : {name}, age: {age}'

# # print(add_user('Tanmay', 100))
# obj = add_user('Tanmay', 100)
# print(obj)
# -> hello : Tanmay, age: 100


# def create_user(name, age, active=True):
#     return {
#         "name": name,
#         "age": age,
#         "active": active,
#     }

# created_user = create_user("Tanmay", 20)
# print(created_user)
# -> {'name': 'Tanmay', 'age': 20, 'active': True}

# for key, value in created_user.items():
#     print(f"{key}: {value}")
# -> name: Tanmay
# -> age: 20
# -> active: True


# def create_user(name, color, *, age, active=True):
#     return {
#         "name": name,
#         "age": age,
#         "active": active,
#     }

# created_user = create_user("Tanmay", "blue", age=20)
# print(created_user)
# -> {'name': 'Tanmay', 'age': 20, 'active': True}
# create_user("Tanmay", "blue", 20)
# -> TypeError: create_user() takes 2 positional arguments but 3 were given
#    (everything after * must be passed by name)

# Any number of positional arguments: *args

# def print_values(*args):
#     for value in args: # this was array
#         print(value)

# print_values("Tanmay", 20, True, None, [90, 85, 92, 88, 95], (10, 20), {1, 2, 3}, {"name": "Rahul", "age": 25})
# -> Tanmay
# -> 20
# -> True
# -> None
# -> [90, 85, 92, 88, 95]
# -> (10, 20)
# -> {1, 2, 3}
# -> {'name': 'Rahul', 'age': 25}


# Any number of keyword arguments: **kwargs - used for passing dictionary as argument
# def create_request(**options):
#     name, age, active = options.get("name"), options.get("age"), options.get("active")
#     print(f"Name: {name}, Age: {age}, Active: {active}")
#     print(options)

# # create_request(name="Tanmay", age=20, active=True)
# -> Name: Tanmay, Age: 20, Active: True
# -> {'name': 'Tanmay', 'age': 20, 'active': True}

# user = {
#     "name": "Tanmay",
#     "age": 20,
#     "active": True,
# }

# create_request(**user)  # unpacking the dictionary into keyword arguments
# -> Name: Tanmay, Age: 20, Active: True
# -> {'name': 'Tanmay', 'age': 20, 'active': True}

# Combining *args and **kwargs
def log_request(endpoint, *messages, **options):
    print("Endpoint:", endpoint)
    print("Messages:", messages)
    print("Options:", options)

# log_request(
#     "/chat",
#     "Hello",
#     "How are you?",
#     model="example-model",
#     timeout=30,
# )
# -> Endpoint: /chat
# -> Messages: ('Hello', 'How are you?')          (*args arrives as a tuple)
# -> Options: {'model': 'example-model', 'timeout': 30}   (**kwargs arrives as a dict)


# =============================================================
# 12. TYPE ANNOTATIONS
# =============================================================

# type annotations - Type annotations document the types that a function expects and returns:
def add_numbers(a: int, b: int) -> int:
    return a + b

# print(add_numbers(5, 3))
# -> 8

def calculate_total(price:float, quantity:int)->float:
   return price * quantity

# calculate_total(12.9, 3)
# -> 38.7      (returns the value, prints nothing without print())

def create_user(name:str, age:int)->dict:
    return {
        "name": name,
        "age": age,
    }

created_user = create_user("Tanmay", 20)
# print(created_user)
# -> {'name': 'Tanmay', 'age': 20}


class Student:
    species = "Canis familiaris"  # Class variable
    def __init__(self, name, age):
      self.name = name
      self.age = age

    def get_user(self):
        return f"The student name is {self.name} and the age is {self.age}"

    def set_city(self):
        return 'retuning from set_user method'
    
    @staticmethod
    def info():
        return 'Student class represents a learner with name and age'

    @classmethod
    def from_string(cls, data: str):
        """Create a Student from a 'name-age' formatted string, e.g. 'Tanmay-20'."""
        name, age = data.split('-')
        cls.species = data
        return cls(name, int(age))

    
# Instance, class, and static methods
obj = Student('Tanmay', 40)
print(obj.get_user())
print(obj.set_city())

# Call the staticmethod
print(Student.info())

# Call the classmethod
student_from_string = Student.from_string("Tanmay-20")
print(student_from_string.get_user())

# Instance method
# - Defined without a decorator; first parameter is conventionally self.
# - Bound to an instance: called on an instance, can read/write instance attributes and also access the class via self.class.
# - Typical use: behavior that depends on per-object state.

# Class method
# Decorated with @classmethod; first parameter is conventionally cls.
# Bound to the class: called on the class or on an instance, receives the class object not the instance.
# Can access/modify class-level state and is commonly used for alternative constructors.

# Static method
# Decorated with @staticmethod; takes no implicit first argument (neither self nor cls).
# Not bound to instance or class: behaves like a regular function placed inside the class namespace.
# Use for utility functions related to the class concept but that don't need instance/class data.

class Customer:
    complay_name = 'DAP Project' #class attribute is shared conceptually by every object
    def __init__(self, name, age, balance=20):
        self.name = name
        self.age = age
        self.skill = []
        self._balance = balance #Private-style attributes _balance

    def add_skill(self, skill):
        self.skill.append(skill)

    def show_skill(self):
        return {
            "name":self.name,
            "age":self.age, 
            "skill":self.skill
        }

    def update_skill(self, new_skill):
        if new_skill == 'TS':
            print('This is cannot be update')
            return 
        self.skill[1] = new_skill

    def delete_skill(self, skill):
        self.skill.remove(skill)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance

    
obj = Customer('Tamnay', 20)
print(obj.show_skill()) #{'name': 'Tamnay', 'age': 20, 'skill': []}
obj.add_skill("Python")
obj.add_skill("SQL")
print(obj.show_skill()) #{'name': 'Tamnay', 'age': 20, 'skill': ['Python', 'SQL']}
obj.update_skill("Java")
print(obj.show_skill()) #{'name': 'Tamnay', 'age': 20, 'skill': ['Python', 'Java']}
obj.delete_skill("Python")
print(obj.show_skill()) #{'name': 'Tamnay', 'age': 20, 'skill': ['Java']}

# Class attributes
print(obj.complay_name) #DAP Project, at instanct level
print(Customer.complay_name) #DAP Project at class level

# Private-style attributes
# Python uses an underscore to indicate an internal attribute:
account = Customer("Rahul", 1000)
account.deposit(500)

print(account.get_balance())  # 1500


# Properties
# A property allows controlled access to an attribute:
# class Person:
#     def __init__(self, age):
#         self.age = age

#     @property
#     def age(self):
#         return self._age
    
#     @age.setter
#     def age(self, value):
#         if value<0:
#             raise ValueError("Age cannot be negative")

#         self._age = value

# obj22= Person(20)
# print(obj22.age)

# Inheritance
# Inheritance allows one class to reuse another class:

# class Persion:
#     def __init__(self, name):
#         self.name = name

#     def intro(self):
#         return f'my name is {self.name}'

# class Student(Persion):
#     def __init__(self, name, course):
#         super().__init__(name)
#         self.course = course

#     def stude(self):
#         return f"{self.name} is studing {self.course}"


# stdObj = Student("Devesh", "Python")
# print(stdObj.intro())
# print(stdObj.stude())

# 12. Special methods
# Special methods have double underscores.
# __str__
# Controls how an object is displayed:

# class Student:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def __str__(self):
#         return f"studunt name is {self.name}, age is {self.age}"


# student = Student("Qraj", 30)
# print(student) # student no need to call the method

# # API Clinet 
# class APIClient:
#     def __init__(self, base_url, api_key):
#         self.base_url = base_url
#         self.api_key = api_key

#     def get_headers(self):
#         return {
#             "Authotization" : f"Bearer {self.api_key}",
#             "Content_type" : "application/json"
#         }

#     def build_url(self, endpoint):
#         return f"{self.base_url}/{endpoint.lstrip("/")}"


# client = APIClient(
#     base_url="https://api.example.com",
#     api_key="secret-key"
# )

# print(client.build_url("/users"))
# print(client.get_headers())

# **. Type annotations
# Add types to constructors, attributes, parameters, and return values:

# class Product:
#     def __init__(self, name:str, price:float, stock:int=0)->None:
#         self.name = name
#         self.price = price
#         self.stock = stock

#     def total_value(self)-> float:
#         return self.price * self.stock

# 2. Validate data immediately
# Do not allow objects to enter an invalid state:   

class Product:
    def __init__(self, name: str, price: float, stock: int = 0) -> None:
        if not name.strip():
            raise ValueError("Product name is required")
        if price < 0:
            raise ValueError("Price cannot be negative")

        if stock < 0:
            raise ValueError("Stock cannot be negative")

        self.name = name.strip()
        self.price = price
        self.stock = stock

prd = Product('rohit', 20.3, 10)
# prd = Product('', 20.3, 10) #ValueError: Product name is required

# print(prd)

# 3. Use custom exceptions
# Custom exceptions make application errors easier to handle:

class ProductError(Exception):
    """Base exception for product errors"""

class InsufficientStock(ProductError):
    pass

class InvalidPriceError(ProductError):
    pass


class ProductEexcptionCls:
    def __init__(self, name:str, price:float, stock:int=0)->None:
        if price<0:
            raise InvalidPriceError("Price cannot be negative")

        self.name= name
        self.price = price
        self.stock = stock

    def sell(self, quantity:int)->None:
        if quantity < 10:
            raise InsufficientStock("Insufficient stock")
        self.stock -= quantity

    def get_stock(self):
        return {
            "stock" : self.stock
        }

# try:
#     prdextcls = ProductEexcptionCls('John', 32.3, 10)
#     # prdextcls = ProductEexcptionCls('John', -3, 10) # error
#     prdextcls.sell(25)
#     print(prdextcls.get_stock())
#     print(prdextcls)
# except InvalidPriceError as error:
#     print(error)
# except InsufficientStock as error:
#     print(error)

# 5. Use dataclasses for data-focused classes

# without dataclass:
# class Person:
#     def __init__(self, name, age):
#         self.name = name  # Initialize the 'name' attribute
#         self.age = age    # Initialize the 'age' attribute

#     def __repr__(self):
#         return f"My name is {self.name} and age is {self.age}"

#     def __eq__(self, other):
#         if not isinstance(other, Person):
#             return False
#         return (self.name == other.name and
#                 self.age == other.age)

# # Creating an instance of Person
# person1 = Person("Alice", 30)
# print(person1.name)  # Output: Alice
# print(person1.age)   # Output: 30

# # The __repr__ method returns a string that represents an object in a developer-friendly format.
# print(repr(person1))


# # Creating two instances of Person, check if thay are equal or not
# person1 = Person("Alice", 30)
# person2 = Person("Alice", 30)
# person3 = Person("Bob", 30)

# print(person1 == person2)  # Output: True
# print(person1 == person3)  # Output: False


# with dataclass:
# Dataclasses are a feature introduced in Python 3.7 that simplify the creation of classes primarily used to store data. 
# They automatically generate special methods like __init__, __repr__, and __eq__ based on the class attributes you define, 
# reducing the amount of boilerplate code you need to write.
print('===USEING DATACLASS===')

# Use an instance attribute:
    # def __init__(self) -> None:
    #     self.permissions: list[str] = []

from dataclasses import dataclass,field

@dataclass
class ProductDataClass:
    name:str
    price:float
    stock: int
    permissions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name is required")

# __init__ method
prduct1 = ProductDataClass('john', 20.2, 30)

# generated __repr__ method
print(prduct1) # Output: Product(name=Laptop, price=999.99, stock=10)

# generated __eq__ method to compare two instances
prduct2 = ProductDataClass('john', 20.2, 30)
print(prduct1 == prduct2)

# product = ProductDataClass("", 50.0, 10)
# print(product) #ValueError: Name is required

# Creating an instance of User without providing a value for 'permissions'
user1 = ProductDataClass('john', 20.2, 30)
print(user1.permissions)  # Output: []

# Creating an instance of User and providing a value for 'permissions'
user2 = ProductDataClass('john', 20.2, 30,permissions=["read", "write"])
print(user2.permissions)  # Output: ['read', 'write']


# Adding logging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(product_name)s')
logger = logging.getLogger(__name__)

class ProductService:
    def create_product(self, name: str) -> None:
        logger.info("Creating product", extra={"product_name": name})

# Create an instance of ProductService and call the method
logs = ProductService()
logs.create_product("indian")


# . Separate responsibilities
# Avoid one large class that performs every operation:
# Too many responsibilities
# class User:
#     def save_to_database(self): ...
#     def send_email(self): ...
#     def process_payment(self): ...
#     def generate_report(self): ...

# class UserRepository:
#     def save(self, user: "User") -> None:
#         ...

# class EmailService:
#     def send_welcome_email(self, user: "User") -> None:
#         ...

user = {
    "devesh1": {"name": "dvesh0", "age": 102},
    "devesh2": {"name": "dvesh1", "age": 101},
    "devesh3": {"name": "dvesh2", "age": 108},
}

# for user_id, details in user.items():
#     print(user_id, ) #devesh1, devesh2, devesh3
#     print(details["name"], details["age"]) #dvesh0 102

# print(user['devesh3']); #{"name": "dvesh2", "age": 108},
# print(user['devesh3']['name']); #dvesh2

# # \\update 
# user["devesh3"]["age"] = 50
# user["devesh3"].update({
#     "name": "John",
#     "age": 50
# })

# # add
# user["devesh4"] = {
#     "name": "David",
#     "age": 40
# }
# user["devesh3"]["city"] = "London"

# # delete
# del user["devesh3"]

# removed_user = user.pop("devesh3")
# print(removed_user)


# add and delte from the front
# Add normally → goes to end
# user["devesh4"] = {"name": "Sam", "age": 30}

# # Add to front → reconstruct dictionary
# user = {"devesh0": {"name": "John", "age": 50}, **user}

# # Delete first
# first_key = next(iter(user))
# del user[first_key]

# user['devesh5'] = {"name": "Sam", "age": 30}
user  = {"devesh9":{"name": "John", "age": 50}, **user}

first_key = next(iter(user)) #moving to the disctionary to loop
print('first_key', first_key)
del user[first_key]

third_key = list(user)[2] # going to 3ed ittrator
print('third_key', third_key)

# ****************lambda***************
# map() = take every item → do something to it → return the changed items
# filter()
# sorted().


# How to do the sorting
sorted_user = dict(
    sorted(user.items(), key=lambda item: item[1]["age"])
)
print(sorted_user)
print(user)

# ------------learn lambda
add = lambda a, b: a + b
# lambda     a, b       :       a + b
#   ↓          ↓                    ↓
# function  parameters           return value
print(add(10, 20))
# ------------learn END lambda


users = [
    {"name": "Devesh", "age": 45},
    {"name": "John", "age": 30},
    {"name": "Sam", "age": 50},
]

numbers = [5, 2, 8, 1, 10]

# fornumla
# map(lambda x: something, collection)
users.sort(key=lambda x:x['age'])
print('users', users)

#1.  map()
results = map(lambda x:x*2, numbers)
print(list(results))

userlist = map(lambda x:x["name"], users)
print(list(userlist))

#2 filter()
result_filter = filter(lambda x:x>4, numbers)
print('result_filter', list(result_filter))

result_filter = filter(lambda x:x['age']>40, users)
print('result_filter', list(result_filter))

#3. sorted()
numbers.sort(key=lambda x:x)
print(numbers)

# error & exception
# try:
#     x = 20/0
#     raise ValueError("ZeroDivisionError in this")
#     # print(x)
# except ValueError as e:
#     print("error is :", e)
# finally:
#     print("always execute")


def withdraw(balance, amount):

    if balance==0:
        raise ValueError("Insufficient balance")
    if amount > balance:
        raise ValueError("amount > then balance")
    return balance - amount

try:
    # result = withdraw(1000, 1500)
    result = withdraw(0, 1500)
    print("Balance:", result)

except ValueError as e:
    print("Transaction failed:", e)


# continue = "not this one, next please."
# break = "I'm done, stop the loop."

# for item in items:
#     if invalid(item):
#         continue       # Skip this one
#     if found(item):
#         break          # Stop everything
#     process(item)


for i in range(1, 6):
    if i == 3:
        continue
    print(i) # here its skip and print 1, 2, 4, 5,6 

users = [
    {"name": "Devesh", "age": 45},
    {"name": "John", "age": None},
    {"name": "Sam", "age": 30},
]

for user in users:
    if user["age"] is None:
        continue
    print(user["name"], user["age"])
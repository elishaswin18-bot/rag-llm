"""Python fundamentals consolidated into one runnable file."""

import asyncio
import json
from dataclasses import dataclass


# 1. Variables and Data Types
name = "Devesh"
age = 35
salary = 100000.50
is_active = True

print(type(name))
print(type(age))


# 2. Collections
users = ["John", "Mary", "Alex"]          # List: ordered, mutable
point = (10, 20)                           # Tuple: ordered, immutable
person = {"age": 10, "name": "Devesh"}   # Dictionary: key-value
skills = {"Python", "React", "FastAPI"}   # Set: unique values
skills.add("LangChain")

print("Users:", users)
print("Point:", point)
print("Person:", person)
print("Skills:", skills)


# 3. List Operations
users = ["name", "age", "gender"]
users[2] = "sex"
users.append("river")
users.append("river_del")
users.remove("river_del")

print(f"User age/value at index 1: {users[1]}")
print(f"User details are: {users}")


# 4. Dictionary Operations
user_address = {
    "add1": "7",
    "add2": "The Marlstone",
    "city": "Swindon",
    "country": "UK",
}

print(user_address["city"])
user_address["capital_new"] = "Delhi"   # Add
user_address["city"] = "London"        # Update
user_address.pop("country", None)       # Delete safely

print(
    "The user address after removing country, adding capital_new "
    f"and updating city is: {user_address}"
)


# 5. Nested Collections
# 5.1 Object inside an array: list of dictionaries
users_list = [
    {"name": "Devesh", "role": "Engineer"},
]

users_list.append({"name": "Anna", "role": "Manager"})
users_list[0]["role"] = "Lead"
del users_list[1]["role"]
print(users_list)

# 5.2 Array inside an object: dictionary containing a list
user_obj = {
    "name": "Devesh",
    "skills": ["Python", "SQL"],
}

user_obj["skills"].append("AWS")
user_obj["skills"][1] = "PostgreSQL"
user_obj["skills"].remove("Python")
print(user_obj)


# 6. Conditionals
person_age = 55

# Corrected ordering: check the highest threshold first.
if person_age >= 60:
    print("Person is senior")
elif person_age >= 18:
    print("Person is adult")
else:
    print("Person is minor")


# 7. Loops
for x in range(2):
    print(x)

for key in user_address:
    print(key)

for key, value in user_address.items():
    print(f"{key}: {value}")

for user_name in ["John", "Mary", "Alex"]:
    print(user_name)

count = 0
while count < 5:
    print(count)
    count += 1


# 8. Functions
def add_numbers(a: int = 100, b: int = 20) -> int:
    """Return the sum of two integers."""
    return a + b


print(add_numbers(1000))
print(add_numbers(30))


# 9. List Comprehensions
numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]
even_numbers = [n for n in numbers if n % 2 == 0]

print(squares)
print(even_numbers)


# 10. Exception Handling
def parse_integer(value: str) -> int | None:
    try:
        return int(value)
    except ValueError as error:
        print(f"Invalid number: {error}")
        return None
    finally:
        print("This always runs")


def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError as error:
        print(f"Error caught: {error}")
        return None


print(parse_integer("abc"))
print(safe_divide(10, 0))


# 11. Classes (OOP)
class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self) -> str:
        return f"Hello {self.name}"


user = User("Devesh")
print(user.greet())


# 12. Inheritance
class Admin(User):
    def delete_user(self, target_user: User) -> str:
        return f"Deleted user: {target_user.name}"


admin = Admin("System Admin")
print(admin.delete_user(user))


# 13. Modules
# In a separate math_utils.py file, this could be:
# def add(a, b):
#     return a + b
#
# Usage:
# from math_utils import add
# print(add(10, 20))
#
# Kept in this file because the request is for one single file.
def add(a: float, b: float) -> float:
    return a + b


print(add(10, 20))


# 14. Ternary Operator
status = "Adult" if person_age >= 18 else "Minor"
print(status)


# 15. Async Programming
async def fetch_data() -> str:
    await asyncio.sleep(1)
    return "Data"


async def async_example() -> None:
    result = await fetch_data()
    print(result)


# 16. Working with JSON
data = {
    "name": "Devesh",
    "role": "Engineer",
}

json_string = json.dumps(data)
print(json_string)

parsed_json = json.loads(json_string)
print(parsed_json)


# 17. Production-Level Python Principles
def calculate_total(price: float, quantity: int) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    return price * quantity


@dataclass(frozen=True, slots=True)
class UserDTO:
    id: int
    name: str


async def get_user(user_id: int) -> UserDTO:
    """Simulate asynchronous database or API I/O."""
    await asyncio.sleep(0.1)
    return UserDTO(id=user_id, name="Devesh")


async def production_example() -> None:
    total = calculate_total(price=19.99, quantity=3)
    user_dto = await get_user(1)
    print("Calculated total:", total)
    print("User DTO:", user_dto)


# 18. Main Entry Point
async def main() -> None:
    await async_example()
    await production_example()


if __name__ == "__main__":
    asyncio.run(main())

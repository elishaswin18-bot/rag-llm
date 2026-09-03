"""
Python interview fundamentals in one runnable file.

Run:
    python python_interview_fundamentals_complete.py

Purpose:
- Covers the most common Python topics for introductory and mid-level interviews.
- Keeps examples small, readable, and production-oriented.
"""

from __future__ import annotations

import asyncio
import json
from abc import ABC, abstractmethod
from collections import Counter, defaultdict, deque
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Generator, Iterable


# ============================================================
# 1. Variables, Data Types, Identity and Mutability
# ============================================================

name: str = "Devesh"
age: int = 35
salary: float = 100000.50
is_active: bool = True
nothing: None = None

print(type(name), type(age), type(salary), type(is_active), type(nothing))

# Equality compares values; identity compares whether references point to the same object.
a = [1, 2]
b = [1, 2]
c = a
print("a == b:", a == b)   # True
print("a is b:", a is b)   # False
print("a is c:", a is c)   # True


# ============================================================
# 2. Strings, Indexing and Slicing
# ============================================================

message = "Python Interview"
print(message.lower())
print(message.upper())
print(message[0])
print(message[-1])
print(message[0:6])
print(message[::-1])
print("Python" in message)
print(f"{name} is preparing for a {message}.")


# ============================================================
# 3. Collections: List, Tuple, Dictionary and Set
# ============================================================

users = ["John", "Mary", "Alex"]
point = (10, 20)
person = {"name": "Devesh", "age": 35}
skills = {"Python", "React", "FastAPI"}

users.append("Anna")
users.extend(["Sam", "Rita"])
users.remove("Sam")
last_user = users.pop()

person["role"] = "Engineer"
person["age"] = 36
removed_role = person.pop("role", None)

skills.add("LangChain")
skills.discard("React")

print(users, last_user)
print(point)
print(person, removed_role)
print(skills)

# Safe dictionary access
print(person.get("city", "Unknown"))

# Set operations
backend = {"Python", "FastAPI", "SQL"}
ai = {"Python", "LangChain", "RAG"}
print("Union:", backend | ai)
print("Intersection:", backend & ai)
print("Difference:", backend - ai)


# ============================================================
# 4. Packing, Unpacking and Swapping
# ============================================================

first, second = point
print(first, second)

head, *middle, tail = [1, 2, 3, 4, 5]
print(head, middle, tail)

x, y = 10, 20
x, y = y, x
print("Swapped:", x, y)


# ============================================================
# 5. Nested Collections
# ============================================================

users_list = [
    {"name": "Devesh", "role": "Engineer"},
    {"name": "Anna", "role": "Manager"},
]

users_list[0]["role"] = "Lead"
users_list[1].pop("role", None)
print(users_list)

user_obj = {"name": "Devesh", "skills": ["Python", "SQL"]}
user_obj["skills"].append("AWS")
user_obj["skills"][1] = "PostgreSQL"
print(user_obj)


# ============================================================
# 6. Conditionals and Truthy/Falsy Values
# ============================================================

person_age = 55

if person_age >= 60:
    age_group = "Senior"
elif person_age >= 18:
    age_group = "Adult"
else:
    age_group = "Minor"

print(age_group)

value = []
if not value:
    print("Empty collections are falsy")

status = "Adult" if person_age >= 18 else "Minor"
print(status)


# ============================================================
# 7. Loops, enumerate, zip, break and continue
# ============================================================

for index, user_name in enumerate(users, start=1):
    print(index, user_name)

technologies = ["Python", "FastAPI", "PostgreSQL"]
levels = ["Advanced", "Intermediate", "Intermediate"]
for technology, level in zip(technologies, levels):
    print(technology, level)

for number in range(1, 6):
    if number == 2:
        continue
    if number == 5:
        break
    print(number)

count = 0
while count < 3:
    print("While:", count)
    count += 1


# ============================================================
# 8. Functions, Scope, *args and **kwargs
# ============================================================

TAX_RATE = 0.20


def add_numbers(a: int = 100, b: int = 20) -> int:
    """Return the sum of two integers."""
    return a + b


def calculate_sum(*numbers: float) -> float:
    """Accept any number of positional arguments."""
    return sum(numbers)


# . *args Example (Positional Arguments)
# Use *args when you do not know how many values a user will pass into the function.

def calculate_total_score(*args):
    # args is treated as a tuple: (90, 85, 92)
    total = sum(args)
    print(f"Total Score: {total}")

# You can pass 3 arguments, 5 arguments, or none at all
calculate_total_score(90, 85, 92)
calculate_total_score(70, 88)

# 2. **kwargs Example (Keyword Arguments)
# Use **kwargs when you want to pass named arguments, like configuration settings or optional profile data.
def build_student_profile(**kwargs):
    # kwargs is treated as a dictionary: {"name": "Rahul", "age": 25}
    for key, value in kwargs.items():
        print(f"{key.capitalize()}: {value}")

# You can pass any number of key-value pairs
build_student_profile(name="Rahul", age=25, city="Swindon")


def build_profile(name: str, **details: Any) -> dict[str, Any]:
    """Accept flexible keyword arguments."""
    return {"name": name, **details}


def calculate_net_salary(gross_salary: float) -> float:
    """Read a module-level constant without modifying it."""
    return gross_salary * (1 - TAX_RATE)


print(add_numbers(10, 20))
print(calculate_sum(1, 2, 3, 4))
print(build_profile("Devesh", role="Engineer", city="Swindon"))
print(calculate_net_salary(100000))


# ============================================================
# 9. Lambda, map, filter and sorted
# ============================================================

numbers = [1, 2, 3, 4, 5]
print(list(map(lambda number: number * 2, numbers)))
print(list(filter(lambda number: number % 2 == 0, numbers)))

employees = [
    {"name": "Anna", "salary": 80000},
    {"name": "Devesh", "salary": 95000},
]
print(sorted(employees, key=lambda employee: employee["salary"], reverse=True))


# ============================================================
# 10. Comprehensions
# ============================================================

squares = [number**2 for number in numbers]
even_numbers = [number for number in numbers if number % 2 == 0]
square_map = {number: number**2 for number in numbers}
unique_lengths = {len(user_name) for user_name in users}

print(squares)
print(even_numbers)
print(square_map)
print(unique_lengths)


# ============================================================
# 11. Exception Handling and Custom Exceptions
# ============================================================

class InvalidPriceError(ValueError):
    """Raised when a price is invalid."""


def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError as error:
        print(f"Cannot divide by zero: {error}")
        return None


def calculate_total(price: float, quantity: int) -> float:
    if price < 0:
        raise InvalidPriceError("Price cannot be negative")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    return price * quantity


print(safe_divide(10, 0))

try:
    print(calculate_total(-10, 2))
except InvalidPriceError as error:
    print(error)


# ============================================================
# 12. Classes, Encapsulation, Properties and Class Methods
# ============================================================

class User:
    user_count = 0

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self._email = email
        User.user_count += 1

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid email address")
        self._email = value

    def greet(self) -> str:
        return f"Hello {self.name}"

    @classmethod
    def from_string(cls, value: str) -> User:
        name_value, email_value = value.split(",")
        return cls(name_value.strip(), email_value.strip())

    @staticmethod
    def is_valid_email(value: str) -> bool:
        return "@" in value and "." in value


user = User("Devesh", "devesh@example.com")
second_user = User.from_string("Anna, anna@example.com")
print(user.greet())
print(second_user.email)
print(User.user_count)
print(User.is_valid_email("test@example.com"))

# -------------------------------------------
class User:
    def __init__(self, name:str, age:int)->None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string string configuration.")

        if not isinstance(age, int):
            raise TypeError("should in be integer")

        if not (0 <= age <= 25):
            raise ValueError(
                f"age {age} this is the value"
            )

        self.name = name
        self.age=age

    @property
    def age(self)->int:
        return self.age

    def get_name(self):
        return f'hello - {self.name}'

try:
    tst = User('Devesh', 199)
    print(tst.get_name())
except (ValueError, TypeError) as error:
    print(f"Failed to initialise user structural runtime: {error}")   


# ============================================================
# 13. Inheritance, Polymorphism and Abstract Base Classes
# ============================================================

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        raise NotImplementedError


class EmailNotifier(Notifier):
    def send(self, message: str) -> str:
        return f"Email sent: {message}"


class SmsNotifier(Notifier):
    def send(self, message: str) -> str:
        return f"SMS sent: {message}"


def notify(notifier: Notifier, message: str) -> None:
    print(notifier.send(message))


notify(EmailNotifier(), "Interview scheduled")
notify(SmsNotifier(), "Interview reminder")


# ============================================================
# 14. Dataclasses and Enum
# ============================================================

class Role(str, Enum):
    ENGINEER = "engineer"
    MANAGER = "manager"


@dataclass(frozen=True, slots=True)
class UserDTO:
    id: int
    name: str
    role: Role


user_dto = UserDTO(id=1, name="Devesh", role=Role.ENGINEER)
print(user_dto)
print(asdict(user_dto))


# ============================================================
# 15. Iterators and Generators
# ============================================================


def generate_even_numbers(limit: int) -> Generator[int, None, None]:
    """Yield values lazily instead of building a full list."""
    for number in range(limit):
        if number % 2 == 0:
            yield number


print(list(generate_even_numbers(10)))

iterator = iter(["Python", "FastAPI"])
print(next(iterator))
print(next(iterator))


# ============================================================
# 16. Decorators
# ============================================================


def log_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}")
        result = function(*args, **kwargs)
        print(f"Finished {function.__name__}")
        return result

    return wrapper


@log_call
def multiply(a: int, b: int) -> int:
    return a * b


print(multiply(4, 5))


# ============================================================
# 17. Context Managers and File Handling
# ============================================================

@contextmanager
def managed_resource():
    print("Opening resource")
    try:
        yield "resource"
    finally:
        print("Closing resource")


with managed_resource() as resource:
    print("Using", resource)

file_path = Path("python_example.txt")
file_path.write_text("Python interview preparation", encoding="utf-8")
print(file_path.read_text(encoding="utf-8"))
file_path.unlink(missing_ok=True)


# ============================================================
# 18. JSON Serialization and Deserialization
# ============================================================

payload = {
    "name": "Devesh",
    "role": "Engineer",
    "skills": ["Python", "FastAPI"],
}

json_string = json.dumps(payload, indent=2)
parsed_json = json.loads(json_string)
print(json_string)
print(parsed_json)


# ============================================================
# 19. Useful Standard Library Collections
# ============================================================

word_counts = Counter(["python", "api", "python", "fastapi"])
print(word_counts)

grouped_users: defaultdict[str, list[str]] = defaultdict(list)
grouped_users["engineering"].append("Devesh")
print(dict(grouped_users))

queue = deque(["task-1", "task-2"])
queue.append("task-3")
print(queue.popleft())


# ============================================================
# 20. Async Programming and Concurrency
# ============================================================

async def fetch_data(source: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"Data from {source}"


async def fetch_all() -> list[str]:
    """Run independent I/O operations concurrently."""
    return await asyncio.gather(
        fetch_data("database", 0.2),
        fetch_data("api", 0.1),
    )


# ============================================================
# 21. Dependency Injection Style
# ============================================================

class UserRepository:
    async def get_by_id(self, user_id: int) -> UserDTO:
        await asyncio.sleep(0.05)
        return UserDTO(id=user_id, name="Devesh", role=Role.ENGINEER)


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_user(self, user_id: int) -> UserDTO:
        if user_id <= 0:
            raise ValueError("user_id must be positive")
        return await self.repository.get_by_id(user_id)


# ============================================================
# 22. Common Interview Utility Functions
# ============================================================


def remove_duplicates(values: Iterable[int]) -> list[int]:
    """Remove duplicates while preserving input order."""
    return list(dict.fromkeys(values))


def is_palindrome(value: str) -> bool:
    normalized = "".join(character.lower() for character in value if character.isalnum())
    return normalized == normalized[::-1]


def count_characters(value: str) -> dict[str, int]:
    return dict(Counter(value))


print(remove_duplicates([1, 2, 2, 3, 1]))
print(is_palindrome("A man, a plan, a canal: Panama"))
print(count_characters("python"))


# ============================================================
# 23. Main Entry Point
# ============================================================

async def main() -> None:
    results = await fetch_all()
    print(results)

    service = UserService(UserRepository())
    fetched_user = await service.get_user(1)
    print(fetched_user)


if __name__ == "__main__":
    asyncio.run(main())

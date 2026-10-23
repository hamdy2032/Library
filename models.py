import re
from enum import Enum
from datetime import datetime

class ReadingStatus(Enum):
    BORROWED = "Borrowed"
    COMPLETED = "Completed"

class Book:
    def __init__(self, book_id, title, author, category, available_copies):
        self.id = book_id
        self.title = title
        self.author = author
        self.category = category
        self._available_copies = available_copies
        self.ratings = []

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        if value < 0:
            raise ValueError("Available copies cannot be negative.")
        self._available_copies = value

    def add_rating(self, user_id, score, review):
        if not (1 <= score <= 10):
            raise ValueError("Rating must be between 1 and 10.")
        self.ratings.append({"user_id": user_id, "score": score, "review": review})

    def calculate_average_rating(self):
        if not self.ratings:
            return 0.0
        total_score = sum(rating['score'] for rating in self.ratings)
        return round(total_score / len(self.ratings), 2)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available_copies": self.available_copies,
            "ratings": self.ratings
        }

class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.set_email(email)
        self.reading_history = []

    def set_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format.")
        self.email = email

    def add_reading_history(self, book_id, status):
        if status not in ReadingStatus:
            raise ValueError("Invalid reading status.")
        self.reading_history.append({
            "book_id": book_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status.value
        })

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "reading_history": self.reading_history
        }

class Recommendation:
    def __init__(self, user_id, book_id, reason, score):
        self.user_id = user_id
        self.book_id = book_id
        self.reason = reason
        self.score = score
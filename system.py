import json
from collections import Counter
from models import User, Book, Recommendation, ReadingStatus

class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.books = {}

    def add_user(self, user_id, name, email):
        if user_id in self.users:
            raise ValueError("User ID already exists.")
        self.users[user_id] = User(user_id, name, email)

    def add_book(self, book_id, title, author, category, available_copies):
        if book_id in self.books:
            raise ValueError("Book ID already exists.")
        self.books[book_id] = Book(book_id, title, author, category, available_copies)

    def borrow_book(self, user_id, book_id):
        user = self.users.get(user_id)
        book = self.books.get(book_id)
        
        if not user or not book:
            raise ValueError("User or Book not found.")
        
        if any(history['book_id'] == book_id for history in user.reading_history):
            print("User has already borrowed or completed this book.")
            return

        if book.available_copies > 0:
            book.available_copies -= 1
            user.add_reading_history(book_id, ReadingStatus.BORROWED)
            print(f"Book '{book.title}' borrowed successfully by {user.name}.")
        else:
            print("No available copies.")

    def recommend_books(self, user_id):
        user = self.users.get(user_id)
        if not user or not user.reading_history:
            return []

        read_book_ids = [rh['book_id'] for rh in user.reading_history]
        categories = [self.books[bid].category for bid in read_book_ids if bid in self.books]
        
        if not categories:
            return []
            
        favorite_category = Counter(categories).most_common(1)[0][0]

        recommendations = []
        for book in self.books.values():
            if book.id not in read_book_ids and book.category == favorite_category:
                avg_rating = book.calculate_average_rating()
                if avg_rating >= 7:
                    rec = Recommendation(user_id, book.id, f"Matches favorite category: {favorite_category}", avg_rating)
                    recommendations.append(rec)
        return recommendations

    def save_data(self, filename="library_data.json"):
        data = {
            "users": {uid: user.to_dict() for uid, user in self.users.items()},
            "books": {bid: book.to_dict() for bid, book in self.books.items()}
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Data saved successfully.")

    def load_data(self, filename="library_data.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for uid, u_data in data.get("users", {}).items():
                    user = User(u_data['id'], u_data['name'], u_data['email'])
                    user.reading_history = u_data['reading_history']
                    self.users[int(uid)] = user
                    
                for bid, b_data in data.get("books", {}).items():
                    book = Book(b_data['id'], b_data['title'], b_data['author'], b_data['category'], b_data['available_copies'])
                    book.ratings = b_data['ratings']
                    self.books[int(bid)] = book
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("Data file not found. Starting with an empty system.")
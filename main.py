from system import LibrarySystem

def main():
    system = LibrarySystem()
    
    system.load_data()
    
    if not system.books:
        system.add_book(1, "Clean Code", "Robert C. Martin", "Programming", 5)
        system.add_book(2, "Python Crash Course", "Eric Matthes", "Programming", 3)
        system.add_user(1, "Ahmed Hamdy", "ahmedhamdy8472@gmail.com")
    
    try:
        system.borrow_book(1, 1)
        system.books[1].add_rating(1, 9, "Great book!")
    except ValueError as e:
        print(f"Error: {e}")
    
    recs = system.recommend_books(1)
    for rec in recs:
        book_title = system.books[rec.book_id].title
        print(f"Recommended for you: {book_title} - Reason: {rec.reason}")
    
    system.save_data()

if __name__ == "__main__":
    main()
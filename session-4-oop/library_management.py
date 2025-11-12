from abc import ABC, abstractmethod


class LibraryItem(ABC):
    _id_counter = 0
    def __init__(self, title, creator, copies):
        # self increment of cls id, shared within instance
        LibraryItem._id_counter += 1

        self.id = LibraryItem._id_counter
        self.title = title
        self.creator = creator
        self.total_copies = copies
        self.available_copies = copies # init from copies
    
    def is_available(self):
        return self.available_copies > 0
    
    def borrow(self):
        if self.is_available():
            self.available_copies -= 1
            return True
        return False
    
    def return_item(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False
    
    @abstractmethod
    def get_item_info(self):
        pass # filled by subcls method 
    
    @abstractmethod
    def get_item_type(self):
        pass
    
    def __str__(self):
        return f"{self.title},{self.creator}"
    
    def __eq__(self, other):
        if isinstance(other, LibraryItem):
            return self.id == other.id
        return False


class Book(LibraryItem):
    def __init__(self, title, author, copies, isbn, num_pages):
        super().__init__(title, author, copies)
        self.author = author
        self.isbn = isbn
        self.num_pages = num_pages
    
    def get_item_type(self): # override 
        return "Book"
    
    def get_item_info(self):
        return f"{self.title}\n {self.author}\n {self.isbn}\n {self.num_pages}\n"


class DVD(LibraryItem):
    def __init__(self, title, director, copies, duration_minutes, genre):
        super().__init__(title, director, copies)
        self.director = director
        self.duration_minutes = duration_minutes
        self.genre = genre
    
    def get_item_type(self):
        return "DVD"
    
    def get_item_info(self):
        return f"Title: {self.title}\nDirector: {self.director}\nDuration: {self.duration_minutes} minutes\nGenre: {self.genre}\nType: DVD"


class Member:
    _id_counter = 0
    
    def __init__(self, name, email):
        Member._id_counter += 1
        self.member_id = Member._id_counter
        self.name = name
        self.email = email
        self.borrowed_items = []
        self.notifications = []
    
    def can_borrow(self):
        return len(self.borrowed_items) < self.get_max_borrow_limit()
    
    def borrow_item(self, item_id):
        self.borrowed_items.append(item_id)
        return True
    
    def return_item(self, item_id):
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)
            return True
        return False
    
    def get_borrowed_count(self):
        return len(self.borrowed_items)
    
    def get_max_borrow_limit(self):
        return 0
    
    def update(self, message):
        self.notifications.append(message)
    
    def get_notifications(self):
        return self.notifications
    
    def clear_notifications(self):
        self.notifications = []
    
    def __str__(self):
        return f"{self.name} ({self.member_id})"


class RegularMember(Member):
    MAX_BORROW_LIMIT = 3
    
    def get_max_borrow_limit(self):
        return self.MAX_BORROW_LIMIT


class PremiumMember(Member):
    MAX_BORROW_LIMIT = 5
    
    def __init__(self, name, email, membership_expiry=None):
        super().__init__(name, email)
        self.membership_expiry = membership_expiry
    
    def get_max_borrow_limit(self):
        return self.MAX_BORROW_LIMIT


class Library:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.items = {}
            self.members = {}
            self.waiting_list = {}
            self._initialized = True
    
    def add_item(self, item):
        self.items[item.id] = item
        return True
    
    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False
    
    def add_member(self, member):
        self.members[member.member_id] = member
        return True
    
    def remove_member(self, member_id):
        if member_id in self.members:
            del self.members[member_id]
            return True
        return False
    
    def borrow_item(self, member_id, item_id):
        if member_id not in self.members or item_id not in self.items:
            return False
        
        member = self.members[member_id]
        item = self.items[item_id]
        
        if not member.can_borrow():
            return False
        
        if item.borrow():
            member.borrow_item(item_id)
            return True
        return False
    
    def return_item(self, member_id, item_id):
        if member_id not in self.members or item_id not in self.items:
            return False
        
        member = self.members[member_id]
        item = self.items[item_id]
        
        if member.return_item(item_id):
            item.return_item()
            self.notify_waiting_members(item_id)
            return True
        return False
    
    def search_items(self, query):
        results = []
        for item in self.items.values():
            if query.lower() in item.title.lower() or query.lower() in item.creator.lower():
                results.append(item)
        return results
    
    def display_all_items(self):
        for item in self.items.values():
            print(f"ID: {item.id}, {item}")
    
    def display_all_members(self):
        for member in self.members.values():
            print(member)
    
    def join_waiting_list(self, member_id, item_id):
        if member_id not in self.members or item_id not in self.items:
            return False
        
        if item_id not in self.waiting_list:
            self.waiting_list[item_id] = []
        
        member = self.members[member_id]
        if member not in self.waiting_list[item_id]:
            self.waiting_list[item_id].append(member)
        return True
    
    def leave_waiting_list(self, member_id, item_id):
        if item_id in self.waiting_list:
            member = self.members.get(member_id)
            if member in self.waiting_list[item_id]:
                self.waiting_list[item_id].remove(member)
                return True
        return False
    
    def get_waiting_list(self, item_id):
        return self.waiting_list.get(item_id, [])
    
    def notify_waiting_members(self, item_id):
        if item_id in self.waiting_list:
            item = self.items[item_id]
            for member in self.waiting_list[item_id]:
                member.update(f"'{item.title}' is now available!")
    
    def __len__(self):
        return len(self.items)


def main():
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=" * 50)
    
    library = Library()
    
    book1 = Book("Python Crash Course", "Eric Matthes", 2, "978-1593279288", 544)
    book2 = Book("Clean Code", "Robert Martin", 2, "978-0132350884", 464)
    dvd1 = DVD("The Matrix", "Wachowski Brothers", 2, 136, "Sci-Fi")
    dvd2 = DVD("Inception", "Christopher Nolan", 1, 148, "Thriller")
    
    library.add_item(book1)
    library.add_item(book2)
    library.add_item(dvd1)
    library.add_item(dvd2)
    
    alice = RegularMember("Alice", "alice@email.com")
    bob = PremiumMember("Bob", "bob@email.com")
    charlie = RegularMember("Charlie", "charlie@email.com")
    
    library.add_member(alice)
    library.add_member(bob)
    library.add_member(charlie)
    
    print(f"\nTotal items: {len(library)}")
    
    library.borrow_item(alice.member_id, book1.id)
    library.borrow_item(alice.member_id, dvd1.id)
    library.borrow_item(alice.member_id, book2.id)
    print(f"Alice borrowed: {alice.get_borrowed_count()}/{alice.get_max_borrow_limit()}")
    
    result = library.borrow_item(alice.member_id, dvd2.id)
    print(f"Alice 4th borrow: {result}")
    
    library.borrow_item(bob.member_id, dvd2.id)
    print(f"Bob borrowed: {bob.get_borrowed_count()}/{bob.get_max_borrow_limit()}")
    
    result = library.borrow_item(charlie.member_id, dvd2.id)
    print(f"Charlie borrow (unavailable): {result}")
    
    library.join_waiting_list(charlie.member_id, dvd2.id)
    print(f"Charlie joined waiting list")
    
    library.return_item(bob.member_id, dvd2.id)
    print(f"Bob returned DVD")
    print(f"Charlie notifications: {charlie.get_notifications()}")
    
    results = library.search_items("Python")
    print(f"\nSearch 'Python': {len(results)} result(s)")
    
    print("\nAll items:")
    library.display_all_items()
    
    print("\nSingleton test:")
    library2 = Library()
    print(f"Same instance: {library is library2}")
    
    print("\nPolymorphism test:")
    print(book1.get_item_info())
    print()
    print(dvd1.get_item_info())


if __name__ == "__main__":
    main()
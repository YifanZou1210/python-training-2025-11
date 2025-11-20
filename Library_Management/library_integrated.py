from datetime import date
import db_manager as db # db customized method interface

# business logic layer 
class Book:
    def __init__(self, title, author, copies, isbn, num_pages):
        self.id = db.add_book(title, author, copies, isbn, num_pages)
        self._title = title
        self._author = author
        self._isbn = isbn
        self._num_pages = num_pages
    
    @property # transfer method to attribute, access it through self.attri
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def num_pages(self):
        return self._num_pages
    
    @property
    def available_copies(self):
        item = db.get_item_by_id(self.id)
        return item.available_copies if item else 0
    
    @property
    def total_copies(self):
        item = db.get_item_by_id(self.id)
        return item.total_copies if item else 0
    
    def get_item_type(self):
        return "Book"
    
    def get_item_info(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nPages: {self.num_pages}\nType: Book"
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
class DVD:
    def __init__(self, title, director, copies, duration_minutes, genre):
        self.id = db.add_dvd(title, director, copies, duration_minutes, genre)
        self._title = title
        self._director = director
        self._duration = duration_minutes
        self._genre = genre
    
    @property
    def title(self):
        return self._title
    
    @property
    def director(self):
        return self._director
    
    @property
    def duration_minutes(self):
        return self._duration
    
    @property
    def genre(self):
        return self._genre
    
    @property
    def available_copies(self):
        item = db.get_item_by_id(self.id)
        return item.available_copies if item else 0
    
    @property
    def total_copies(self):
        item = db.get_item_by_id(self.id)
        return item.total_copies if item else 0
    
    def get_item_type(self):
        return "DVD"
    
    def get_item_info(self):
        return f"Title: {self.title}\nDirector: {self.director}\nDuration: {self.duration_minutes} min\nGenre: {self.genre}\nType: DVD"
    
    def __str__(self):
        return f"{self.title} by {self.director}"



# Member 

class Member:
    
    def __init__(self, name, email, membership_type, borrow_limit, expiry=None):
        self.member_id = db.add_member(name, email, membership_type, borrow_limit, expiry)
        self.name = name
        self.email = email
    
    def get_borrowed_count(self):
        items = db.get_member_borrowed_items(self.member_id)
        return len(items)
    
    def can_borrow(self):
        return self.get_borrowed_count() < self.get_max_borrow_limit()
    
    def get_max_borrow_limit(self):
        membership = db.get_membership(self.member_id)
        return membership.borrow_limit if membership else 0
    
    def borrow_item(self, item_id):
        if self.can_borrow():
            return db.borrow_item(self.member_id, item_id)
        return False
    
    def return_item(self, item_id):
        return db.return_item(self.member_id, item_id)
    
    def get_notifications(self):
        notifications = db.get_member_notifications(self.member_id)
        return [n.message for n in notifications]
    
    def update(self, message):
        db.create_notification(self.member_id, message)
    
    def clear_notifications(self):
        db.mark_all_notifications_read(self.member_id)
    
    def __str__(self):
        return f"{self.name} ({self.member_id})"


# RegularMember

class RegularMember(Member):
    
    def __init__(self, name, email):
        super().__init__(name, email, 'regular', 3, None)


# PremiumMember

class PremiumMember(Member):
    
    def __init__(self, name, email, expiry_str=None):
        expiry = None
        if expiry_str:
            y, m, d = map(int, expiry_str.split('-'))
            expiry = date(y, m, d)
        super().__init__(name, email, 'premium', 5, expiry)

# Library 类（单例）

class Library:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        db.init_database()
        self._initialized = True
    
    # Item Operations
    def add_item(self, item):
        return True
    
    def remove_item(self, item_id):
        return db.remove_item(item_id)
    
    def get_item_by_id(self, item_id):
        return db.get_item_by_id(item_id)
    
    def search_items(self, query):
        return db.search_items(query)
    
    def get_all_items(self):
        return db.get_all_items()
    
    def display_all_items(self):
        items = db.get_all_items()
        for item in items:
            print(f"ID: {item.id}, {item.title} by {item.creator} ({item.item_type})")
    
    # Member Operations
    def add_member(self, member):
        return True
    
    def remove_member(self, member_id):
        return db.remove_member(member_id)
    
    def get_member_by_id(self, member_id):
        return db.get_member_by_id(member_id)
    
    def get_all_members(self):
        return db.get_all_members()
    
    def display_all_members(self):
        members = db.get_all_members()
        for m in members:
            membership = db.get_membership(m.id)
            type_str = membership.membership_type if membership else 'none'
            limit = membership.borrow_limit if membership else 0
            print(f"{m.name} ({m.id}) - {type_str} (limit: {limit})")
    
    # Borrowing Operations
    def borrow_item(self, member_id, item_id):
        return db.borrow_item(member_id, item_id)
    
    def return_item(self, member_id, item_id):

        return db.return_item(member_id, item_id)
    
    def get_member_borrowed_items(self, member_id):
        return db.get_member_borrowed_items(member_id)
    
    def get_item_borrow_history(self, item_id):
        return db.get_item_borrow_history(item_id)
    
    # Waiting List Operations
    def join_waiting_list(self, member_id, item_id):
        return db.join_waiting_list(member_id, item_id)
    
    def leave_waiting_list(self, member_id, item_id):
        return db.leave_waiting_list(member_id, item_id)
    
    def get_waiting_list(self, item_id):
        return db.get_waiting_list(item_id)
    
    def notify_waiting_members(self, item_id):
        return db.notify_waiting_members(item_id)
    
    # Magic Methods
    def __len__(self):
        return len(db.get_all_items())

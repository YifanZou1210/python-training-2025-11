from abc import ABC, abstractmethod
from typing import Optional
class LibraryItem(ABC):
  _id_counter = 0 # cls attribute
  def __init__(self, title, creator, copies):
    LibraryItem._id_counter+=1 # use cls.attri
    self.id = LibraryItem._id_counter
    self.title = title 
    self.creator = creator
    self.total_copies = copies 
    self.available_copies = copies 

  def is_available(self)->bool:
    if self.available_copies>0:
      return True 
    return False 
  
  # available copies to borrow 
  def borrow(self)->bool:
    if self.available_copies>0:
      self.available_copies-=1
      return True 
    else:
      return False 
  
  def return_item(self)->bool:
    if self.available_copies<self.total_copies:
      self.available_copies+=1
      return True 
    else:
      return False 
  
  @abstractmethod
  def get_item_info(self)->str:
    pass

  @abstractmethod
  def get_item_type(self)->str:
    pass

  def __str__(self):
    return f'{self.title} by {self.creator} with {self.available_copies} available copies'
  
  def __eq__(self, other)->bool:
    # if self.id!=other:
    #   return False 
    if not isinstance(other, LibraryItem):
      return False
    return True 
  
class Book(LibraryItem):
  def __init__(self, title, author, copies, isbn, num_pages):
    super().__init__(title, author, copies)
    self.isbn = isbn 
    self.pages = num_pages
  
  def get_item_info(self):
    return f"{self.title} by {self.creator} with {self.isbn}, {self.pages}"
  
  def get_item_type(self):
    return "Books"

class DVD(LibraryItem):
  def __init__(self, title, director, copies, duration_minutes, genre):
    super().__init__(title, director, copies)
    self.duration = duration_minutes
    self.genre = genre 
  
  def get_item_info(self):
    return f'{self.title} by {self.creator} with {self.duration}, {self.genre}'
  
  def get_item_type(self):
    return "DVD"
  
class Member(ABC):
  _id_counter = 0 
  def __init__(self, name, email):
    Member._id_counter+=1
    self.member_id = Member._id_counter
    self.name = name 
    self.email = email 
    self.borrowed_items = []
    self.notifications = []
    self.max_borrow_limit = 0
  
  def can_borrow(self)->bool:
    if len(self.borrowed_items)>=self.max_borrow_limit:
      return False 
    return True 
  
  def borrow_item(self, item_id)->bool:
    if self.can_borrow():
      self.borrowed_items.append(item_id)
      return True 
    else:
      return False 
  
  def return_item(self, item_id)->bool:
    # if self.borrowed_items>0:
    #   self.borrowed_items.remove(item_id)
    #   return True 
    if item_id in self.borrowed_items:  # ✅ 检查 ID 是否在列表中
      self.borrowed_items.remove(item_id)
      return True
    else:
      print('no items in borrowed list')
      return False 
  
  def get_borrowed_count(self)->int:
    return len(self.borrowed_items)

  @abstractmethod
  def get_max_borrow_limit(self):
    pass
  @abstractmethod
  def update(self,message):
    pass

  def get_notifications(self):
    return self.notifications
  
  def clear_notifications(self):
    self.notifications.clear()
  
  def __str__(self):
    return "Member"
  
class RegularMember(Member):
  def __init__(self, name, email):
    super().__init__(name, email)
    self.max_borrow_limit = 3
  
  def get_max_borrow_limit(self):
    return self.max_borrow_limit
  def update(self, message):
    self.notifications.append(message)

class PremiumMember(Member):
  def __init__(self, name, email,membership_expiry = None ): # optional args
    super().__init__(name, email)
    self.membership_expiry = membership_expiry
    self.max_borrow_limit = 5 
  
  def get_max_borrow_limit(self):
    return self.max_borrow_limit
  def update(self, message):
    self.notifications.append(message)

class Library():
  _instance = None 
  def __new__(cls):
    """
    singleton pattern inplementation
    1. if no shared instance exist, create one 
    2. 
    """
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance._initialized = False
    return cls._instance 
  
  def __init__(self):
    """initialization only once 
    """
    if self._initialized:
      return
    self.items = {} # dict[int, libraryItem] like 1:book
    self.members = {} 
    self.waiting_list = {} 
    self._initialized = True 

  def add_item(self, item:LibraryItem):
    self.items[item.id] = item 
    return True 
  
  def remove_item(self, item_id):
    if item_id in self.items:
      self.items.pop(item_id)
      return True 
    else:
      return False
  
  def add_member(self, member:Member):
    self.members[member.member_id] = member 
    return True 
  
  def remove_member(self, member_id)->bool:
    if member_id in self.members:
      del self.members[member_id]
      return True 
    else:
      return False 
    
  def borrow_item(self, member_id, item_id)->bool:
    member: Member = self.members.get(member_id)
    item: LibraryItem = self.items.get(item_id)
    if not member or not item:
      return False 
    if not member.can_borrow():
      return False 
    if item.borrow():
      member.borrow_item(item_id)
      return True 
    else:
      return False 
  
  def return_item(self,member_id, item_id)->bool:
    member:Member = self.members.get(member_id)
    item:LibraryItem = self.items.get(item_id)
    if not member or not item:
      return False 
    if member.return_item(item_id):
      # if other user return books, notify waiting list 
      item.return_item()
      self.notify_waiting_members(item_id)
      return True 
    return False
  
  def search_items(self, query):
    """
    1. traverse all library items with title and creator
    2. search target creator and title, append them in res 
    """
    res = [] 
    for item in self.items.values(): # traverse all libraryitems 
      if query.lower() in item.title.lower() or query.lower() in item.creator.lower():
        res.append(item)
    return res 
  
  def display_all_items(self):
    for item in self.items.values():
      print(f'{item.id} with {item}')
  
  def display_all_members(self):
    for member in self.members.values():
      print(f'{member.member_id} with {member}')
    
  def join_waiting_list(self, member_id, item_id)->bool:
    member = self.members.get(member_id)
    if not member:
      return False 
    if item_id not in self.waiting_list:
      self.waiting_list[item_id] = [] 
    if member not in self.waiting_list[item_id]:
      self.waiting_list[item_id].append(member)
    return True 
  
  def leave_waiting_list(self, member_id, item_id)->bool:
    member = self.members.get(member_id)
    item = self.items.get(item_id)
    if not member or not item:
      return False 
    if not item_id in self.waiting_list:
      return False 
    if not member in self.waiting_list[item_id]:
      return False 
    self.waiting_list[item_id].remove(member)
    return True 
  
  def get_waiting_list(self, item_id):
    return self.waiting_list.get(item_id, []) 
  
  def notify_waiting_members(self, item_id)->None:
    if item_id not in self.waiting_list:
      return 
    item = self.items[item_id]
    message = f"{item.title} is now ok "
    for member in self.waiting_list[item_id]:
      member.update(message)

  def __len__(self)->int:
    return len(self.items)


def main():
  print("=" * 70)
  print("LIBRARY MANAGEMENT SYSTEM - DEMO")
  print("=" * 70)
  
  # Create library (Singleton)
  library = Library()
  
  # Add books and DVDs
  book1 = Book("Python Crash Course", "Eric Matthes", 2, "978-1593279288", 544)
  book2 = Book("Clean Code", "Robert Martin", 2, "978-0132350884", 464)
  dvd1 = DVD("The Matrix", "Wachowski Brothers", 2, 136, "Sci-Fi")
  dvd2 = DVD("Inception", "Christopher Nolan", 1, 148, "Thriller")
  
  library.add_item(book1)
  library.add_item(book2)
  library.add_item(dvd1)
  library.add_item(dvd2)
  
  print(f"\n--- Added Items ---")
  print(f"Book: {book1} (ID: {book1.id})")
  print(f"DVD: {dvd1} (ID: {dvd1.id})")
  print(f"Total items: {len(library)}")
  
  # Demonstrate Polymorphism - get_item_info()
  print(f"\n--- Polymorphism Demo: get_item_info() ---")
  print(book1.get_item_info())
  print(f"\n{dvd1.get_item_info()}")
  
  # Add members
  alice = RegularMember("Alice", "alice@email.com")
  bob = PremiumMember("Bob", "bob@email.com")
  charlie = RegularMember("Charlie", "charlie@email.com")
  
  library.add_member(alice)
  library.add_member(bob)
  library.add_member(charlie)
  
  print(f"\n--- Added Members ---")
  print(f"{alice} - Max: {alice.get_max_borrow_limit()} items")
  print(f"{bob} - Max: {bob.get_max_borrow_limit()} items")
  
  # Regular member borrows items (max 3)
  print(f"\n--- Regular Member Borrowing (Max 3) ---")
  library.borrow_item(alice.member_id, book1.id)
  library.borrow_item(alice.member_id, dvd1.id)
  library.borrow_item(alice.member_id, book2.id)
  print(f"Alice borrowed: {alice.get_borrowed_count()}/{alice.get_max_borrow_limit()} items")
  
  # Try to exceed limit
  success = library.borrow_item(alice.member_id, dvd2.id)
  print(f"Alice trying 4th item: {success} (exceeded limit)")
  
  # Premium member borrows items (max 5)
  print(f"\n--- Premium Member Borrowing (Max 5) ---")
  library.borrow_item(bob.member_id, dvd2.id)
  print(f"Bob borrowed: {bob.get_borrowed_count()}/{bob.get_max_borrow_limit()} items")
  print(f"'{dvd2.title}' available: {dvd2.available_copies}")
  
  # Waiting list and Observer pattern
  print(f"\n--- Waiting List & Observer Pattern ---")
  success = library.borrow_item(charlie.member_id, dvd2.id)
  print(f"Charlie trying to borrow '{dvd2.title}': {success} (unavailable)")
  
  library.join_waiting_list(charlie.member_id, dvd2.id)
  print(f"Charlie joined waiting list")
  print(f"Waiting list size: {len(library.get_waiting_list(dvd2.id))}")
  
  # Return item - triggers notification
  print(f"\nBob returns '{dvd2.title}'...")
  library.return_item(bob.member_id, dvd2.id)
  print(f"Charlie's notifications: {charlie.get_notifications()}")
  
  # Search functionality
  print(f"\n--- Search Items ---")
  results = library.search_items("Python")
  print(f"Search 'Python': {len(results)} result(s)")
  
  results = library.search_items("Matrix")
  print(f"Search 'Matrix': {len(results)} result(s)")
  
  # Display final state
  print(f"\n--- Final State ---")
  print(f"Total items: {len(library)}")
  library.display_all_items()
  
  print("\n" + "=" * 70)
  print("DEMO COMPLETED!")
  print("=" * 70)

if __name__ == "__main__":
  main()
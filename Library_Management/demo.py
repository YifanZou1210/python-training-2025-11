"""
Complete Demo - All Features
"""
from library_integrated import Library, Book, DVD, RegularMember, PremiumMember
import db_manager as db


def main():
    print("="*70)
    print("LIBRARY MANAGEMENT SYSTEM - DATABASE INTEGRATION DEMO")
    print("="*70)
    
    # 1. 初始化数据库
    print("\n--- Database Initialization ---")
    db.reset_database()
    
    # 2. 创建 Library
    library = Library()
    
    # 3. 添加物品
    print("\n--- Adding Items ---")
    book1 = Book("Python Crash Course", "Eric Matthes", 2, "978-1593279288", 544)
    book2 = Book("Clean Code", "Robert Martin", 1, "978-0132350884", 464)
    dvd1 = DVD("The Matrix", "Wachowski Brothers", 1, 136, "Sci-Fi")
    dvd2 = DVD("Inception", "Christopher Nolan", 1, 148, "Thriller")
    
    library.add_item(book1)
    library.add_item(book2)
    library.add_item(dvd1)
    library.add_item(dvd2)
    
    print(f"Total items: {len(library)}")
    
    # 4. 多态演示
    print("\n--- Polymorphism Demo ---")
    print(book1.get_item_info())
    print()
    print(dvd1.get_item_info())
    
    # 5. 添加会员
    print("\n--- Adding Members ---")
    alice = RegularMember("Alice", "alice@email.com")
    bob = PremiumMember("Bob", "bob@email.com", "2025-12-31")
    charlie = RegularMember("Charlie", "charlie@email.com")
    
    library.add_member(alice)
    library.add_member(bob)
    library.add_member(charlie)
    
    print(f"Alice (Regular): Max {alice.get_max_borrow_limit()} items")
    print(f"Bob (Premium): Max {bob.get_max_borrow_limit()} items")
    
    # 6. 借阅测试
    print("\n--- Borrowing Operations ---")
    library.borrow_item(alice.member_id, book1.id)
    library.borrow_item(alice.member_id, dvd1.id)
    library.borrow_item(alice.member_id, book2.id)
    
    print(f"Alice borrowed: {alice.get_borrowed_count()}/{alice.get_max_borrow_limit()}")
    print(f"Book1 available: {book1.available_copies}/{book1.total_copies}")
    
    # 超限测试
    success = library.borrow_item(alice.member_id, dvd2.id)
    print(f"Alice trying 4th item: {success} (exceeded limit)")
    
    # 7. Premium 会员
    print("\n--- Premium Member Borrowing ---")
    library.borrow_item(bob.member_id, dvd2.id)
    print(f"Bob borrowed: {bob.get_borrowed_count()}/{bob.get_max_borrow_limit()}")
    print(f"DVD2 '{dvd2.title}' available: {dvd2.available_copies}")
    
    # 8. 等待列表
    print("\n--- Waiting List & Observer Pattern ---")
    success = library.borrow_item(charlie.member_id, dvd2.id)
    print(f"Charlie trying to borrow '{dvd2.title}': {success} (unavailable)")
    
    library.join_waiting_list(charlie.member_id, dvd2.id)
    print("Charlie joined waiting list")
    
    waiting = library.get_waiting_list(dvd2.id)
    print(f"Waiting list size: {len(waiting)}")
    
    # 9. 归还触发通知
    print("\nBob returns '{}'...".format(dvd2.title))
    library.return_item(bob.member_id, dvd2.id)
    
    print(f"DVD2 available: {dvd2.available_copies}")
    
    notifications = charlie.get_notifications()
    print(f"Charlie's notifications: {notifications}")
    
    # 10. 搜索
    print("\n--- Search Items ---")
    results = library.search_items("Python")
    print(f"Search 'Python': {len(results)} result(s)")
    
    results = library.search_items("Matrix")
    print(f"Search 'Matrix': {len(results)} result(s)")
    
    # 11. 显示状态
    print("\n--- Final State ---")
    print(f"Total items: {len(library)}")
    
    print("\nAll items:")
    library.display_all_items()
    
    print("\nAll members:")
    library.display_all_members()
    
    # 12. 单例测试
    print("\n--- Singleton Pattern ---")
    library2 = Library()
    print(f"library is library2: {library is library2}")
    
    # 13. 数据持久化
    print("\n--- Data Persistence ---")
    print("Creating new Library instance...")
    library3 = Library()
    print(f"Items still in DB: {len(library3)}")
    
    items = library3.get_all_items()
    print(f"Item titles: {[i.title for i in items]}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    main()

from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from datetime import datetime, date , timedelta
from engine import engine 
from typing import List
from models import (
    Base, LibraryItemModel, BookModel, DVDModel, MemberModel, MembershipModel, BorrowedItemModel, WaitingListModel, NotificationModel
)

"""
Initialize DB 
"""

def init_database():
    Base.metadata.create_all(engine)
    print('db initialized')

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('db reset')

""" 
Item Operations 
"""

def add_book(title, author, copies, isbn, num_pages)->BookModel:
    # open context manager Session, ensure auto commit/rollback
    with Session(engine) as session:
        # start transaction, ensure itomicity 
        with session.begin():
            # create libraryitem instance 
            item = LibraryItemModel(
                title = title,
                creator = author, 
                item_type = 'book', # type as book 
                total_copies = copies,
                available_copies = copies
            )
            session.add(item) # register instance into session, no write in db 
            session.flush() # flush execute sql, add item.id in advance, no transaction commit 
            # create bookmodel instance, share same item.id 
            book = BookModel(
                id = item.id,
                isbn = isbn, 
                num_pages = num_pages 
            )
            session.add(book)

            print(f'added book : {title} with {item.id}')
            return book.id 
def add_dvd(title, director, copies, duration, genre)->DVDModel:
    with Session(engine) as session:
        with session.begin():
            item = LibraryItemModel(
                title = title, 
                creator = director, 
                item_type = 'dvd',
                total_copies = copies, 
                available_copies = copies
            )
            session.add(item)
            session.flush()
            dvd = DVDModel(
                id = item.id,
                duration_minutes = duration, 
                genre = genre 
            )
            session.add(dvd)
            session.flush()
        return dvd.id

def remove_item(item_id):
    with Session(engine) as session:
        with session.begin():
            item = session.get(LibraryItemModel, item_id)
            if item:
                session.delete(item)
                return True
            return False

# only read operation no need transaction 
def get_item_by_id(item_id:int):
    with Session(engine) as session:
        stmt = select(LibraryItemModel).where(LibraryItemModel.id == item_id)
        return session.execute(stmt).scalar() 
def search_items(query:str)->List[LibraryItemModel]:
    with Session(engine) as session:
        stmt = select(LibraryItemModel).where(
            or_( # used in multi-condition block 
                LibraryItemModel.title.ilike(f'%{query}%'), # ilike - fuzzy query
                LibraryItemModel.creator.ilike(f'%{query}%')
            )
        )
        return session.execute(stmt).scalars().all()
def get_all_items()->List[LibraryItemModel]:
    with Session(engine) as session:
        stmt = select(LibraryItemModel)
        return session.execute(stmt).scalars().all() 

""" 
Member Operations
"""
def add_member(name, email, membership_type, borrow_limit, expiry = None)-> MemberModel:
    with Session(engine) as session:
        with session.begin():
            member = MemberModel(
                name = name, 
                email = email
            )
            session.add(member)
            session.flush()

            membership = MembershipModel(
                member_id = member.id,
                membership_type = membership_type, 
                borrow_limit = borrow_limit,
                expiry_date = expiry
            )

            session.add(membership)
            return member.id 
def remove_member(member_id):
    with Session(engine) as session:
        with session.begin():
            member = session.get(MemberModel, member_id)
            if member:
                session.delete(member)
                return True
            return False

def get_member_by_id(member_id):
    with Session(engine) as session:
        stmt = select(MemberModel).where(MemberModel.id == member_id)
        return session.execute(stmt).scalar()

def get_all_members():
    with Session(engine) as session:
        stmt = select(MemberModel)
        return session.execute(stmt).scalars().all()

""" 
Membership Operations
"""
def create_membership(member_id, membership_type, borrow_limit, expiry = None)->MembershipModel:
    with Session(engine) as session:
        with session.begin():
            membership = MembershipModel(
                member_id = member_id, 
                membership_type=membership_type,
                borrow_limit=borrow_limit,
                expiry_date=expiry
            )
            session.add(membership)
            return membership.id
def update_membership(member_id, membership_type=None, borrow_limit=None, expiry=None):
    with Session(engine) as session:
        with session.begin():
            stmt = select(MembershipModel).where(MembershipModel.member_id == member_id)
            membership = session.execute(stmt).scalar()
            if not membership:
                return False
            if membership_type:
                membership.membership_type = membership_type
            if borrow_limit:
                membership.borrow_limit = borrow_limit
            if expiry:
                membership.expiry_date = expiry
            
            membership.updated_at = datetime.now()
            return True
def renew_membership(member_id, days):
    with Session(engine) as session:
        with session.begin():
            stmt = select(MembershipModel).where(MembershipModel.member_id == member_id)
            membership = session.execute(stmt).scalar()
            if not membership:
                return False
            if membership.expiry_date:
                membership.expiry_date = membership.expiry_date + timedelta(days=days)
            else:
                membership.expiry_date = date.today() + timedelta(days=days)
            membership.updated_at = datetime.now()
            return True
def get_membership(member_id):
    with Session(engine) as session:
        stmt = select(MembershipModel).where(MembershipModel.member_id == member_id)
        return session.execute(stmt).scalar()
def check_membership_expiry(member_id):
    membership = get_membership(member_id)
    if not membership:
        return True
    if membership.expiry_date is None:
        return False
    return date.today() > membership.expiry_date

"""Borrowing Operations"""
def borrow_item(member_id, item_id):
    with Session(engine) as session:
        with session.begin():
            member = session.get(MemberModel, member_id)
            item = session.get(LibraryItemModel, item_id)
            if not member or not item:
                return False
            borrowed_count = len([b for b in member.borrowed_records if b.status == 'borrowed'])
            if borrowed_count >= member.membership.borrow_limit:
                return False
            if item.available_copies <= 0:
                return False
            record = BorrowedItemModel(
                member_id=member_id,
                item_id=item_id,
                status='borrowed'
            )
            session.add(record)
            item.available_copies -= 1
            return True


def return_item(member_id, item_id):
    with Session(engine) as session:
        with session.begin():
            stmt = select(BorrowedItemModel).where(
                BorrowedItemModel.member_id == member_id,
                BorrowedItemModel.item_id == item_id,
                BorrowedItemModel.status == 'borrowed'
            )
            record = session.execute(stmt).scalar()
            
            if not record:
                return False
            record.status = 'returned'
            record.return_date = datetime.now()
            item = session.get(LibraryItemModel, item_id)
            item.available_copies += 1
            # notify waiter 
            _notify_waiting_in_transaction(session, item_id)
            
            return True


def get_member_borrowed_items(member_id):
    with Session(engine) as session:
        stmt = select(BorrowedItemModel).where(
            BorrowedItemModel.member_id == member_id,
            BorrowedItemModel.status == 'borrowed'
        )
        records = session.execute(stmt).scalars().all()
        
        item_ids = [r.item_id for r in records]
        if not item_ids:
            return []
        
        items_stmt = select(LibraryItemModel).where(LibraryItemModel.id.in_(item_ids))
        return session.execute(items_stmt).scalars().all()


def get_item_borrow_history(item_id):
    with Session(engine) as session:
        stmt = select(BorrowedItemModel).where(
            BorrowedItemModel.item_id == item_id
        ).order_by(BorrowedItemModel.borrow_date.desc())
        
        return session.execute(stmt).scalars().all()



# Waiting List Operations


def join_waiting_list(member_id, item_id):
    with Session(engine) as session:
        with session.begin():
            stmt = select(WaitingListModel).where(
                WaitingListModel.member_id == member_id,
                WaitingListModel.item_id == item_id
            )
            existing = session.execute(stmt).scalar()
            
            if existing:
                return False
            
            waiting = WaitingListModel(member_id=member_id, item_id=item_id)
            session.add(waiting)
            return True


def leave_waiting_list(member_id, item_id):
    with Session(engine) as session:
        with session.begin():
            stmt = select(WaitingListModel).where(
                WaitingListModel.member_id == member_id,
                WaitingListModel.item_id == item_id
            )
            waiting = session.execute(stmt).scalar()
            
            if waiting:
                session.delete(waiting)
                return True
            return False


def get_waiting_list(item_id):
    with Session(engine) as session:
        stmt = select(WaitingListModel).where(
            WaitingListModel.item_id == item_id
        ).order_by(WaitingListModel.joined_at)
        
        waiting_records = session.execute(stmt).scalars().all()
        
        member_ids = [w.member_id for w in waiting_records]
        if not member_ids:
            return []
        
        members_stmt = select(MemberModel).where(MemberModel.id.in_(member_ids))
        return session.execute(members_stmt).scalars().all()


def notify_waiting_members(item_id):
    with Session(engine) as session:
        with session.begin():
            _notify_waiting_in_transaction(session, item_id)


def _notify_waiting_in_transaction(session, item_id):
    stmt = select(WaitingListModel).where(WaitingListModel.item_id == item_id)
    waiting_records = session.execute(stmt).scalars().all()
    
    if not waiting_records:
        return
    
    item = session.get(LibraryItemModel, item_id)
    message = f"'{item.title}' is now available!"
    
    for waiting in waiting_records:
        notification = NotificationModel(
            member_id=waiting.member_id,
            message=message
        )
        session.add(notification)



# Notification Operations

def create_notification(member_id, message):
    with Session(engine) as session:
        with session.begin():
            notification = NotificationModel(
                member_id=member_id,
                message=message
            )
            session.add(notification)
            return notification.id


def get_member_notifications(member_id, unread_only=False):
    with Session(engine) as session:
        stmt = select(NotificationModel).where(
            NotificationModel.member_id == member_id
        )
        
        if unread_only:
            stmt = stmt.where(NotificationModel.is_read == False)
        
        stmt = stmt.order_by(NotificationModel.created_at.desc())
        return session.execute(stmt).scalars().all()


def mark_notification_read(notification_id):
    with Session(engine) as session:
        with session.begin():
            notification = session.get(NotificationModel, notification_id)
            if notification:
                notification.is_read = True
                return True
            return False


def mark_all_notifications_read(member_id):
    with Session(engine) as session:
        with session.begin():
            stmt = select(NotificationModel).where(
                NotificationModel.member_id == member_id,
                NotificationModel.is_read == False
            )
            notifications = session.execute(stmt).scalars().all()
            
            for n in notifications:
                n.is_read = True
            
            return len(notifications)

        
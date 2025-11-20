"""
SQLAlchemy 2.x ORM Models
"""
from typing import List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy import String, Integer, Boolean, DateTime, Date, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class LibraryItemModel(Base):
    __tablename__ = 'library_items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    creator: Mapped[str] = mapped_column(String(255))
    item_type: Mapped[str] = mapped_column(String(20))
    total_copies: Mapped[int] = mapped_column(Integer, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    book: Mapped[Optional["BookModel"]] = relationship(back_populates="library_item", cascade="all, delete-orphan")
    dvd: Mapped[Optional["DVDModel"]] = relationship(back_populates="library_item", cascade="all, delete-orphan")
    borrowed_records: Mapped[List["BorrowedItemModel"]] = relationship(back_populates="item", cascade="all, delete-orphan")
    waiting_members: Mapped[List["WaitingListModel"]] = relationship(back_populates="item", cascade="all, delete-orphan")


class BookModel(Base):
    __tablename__ = 'books'
    
    id: Mapped[int] = mapped_column(ForeignKey('library_items.id', ondelete='CASCADE'), primary_key=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    num_pages: Mapped[int] = mapped_column(Integer)
    
    library_item: Mapped["LibraryItemModel"] = relationship(back_populates="book")


class DVDModel(Base):
    __tablename__ = 'dvds'
    
    id: Mapped[int] = mapped_column(ForeignKey('library_items.id', ondelete='CASCADE'), primary_key=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(50))
    
    library_item: Mapped["LibraryItemModel"] = relationship(back_populates="dvd")


class MemberModel(Base):
    __tablename__ = 'members'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    membership: Mapped[Optional["MembershipModel"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    borrowed_records: Mapped[List["BorrowedItemModel"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    waiting_items: Mapped[List["WaitingListModel"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    notifications: Mapped[List["NotificationModel"]] = relationship(back_populates="member", cascade="all, delete-orphan")


class MembershipModel(Base):
    __tablename__ = 'memberships'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id', ondelete='CASCADE'), unique=True)
    membership_type: Mapped[str] = mapped_column(String(20))
    borrow_limit: Mapped[int] = mapped_column(Integer)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    member: Mapped["MemberModel"] = relationship(back_populates="membership")


class BorrowedItemModel(Base):
    __tablename__ = 'borrowed_items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id', ondelete='CASCADE'))
    item_id: Mapped[int] = mapped_column(ForeignKey('library_items.id', ondelete='CASCADE'))
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    return_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='borrowed')
    
    member: Mapped["MemberModel"] = relationship(back_populates="borrowed_records")
    item: Mapped["LibraryItemModel"] = relationship(back_populates="borrowed_records")


class WaitingListModel(Base):
    __tablename__ = 'waiting_list'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id', ondelete='CASCADE'))
    item_id: Mapped[int] = mapped_column(ForeignKey('library_items.id', ondelete='CASCADE'))
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    member: Mapped["MemberModel"] = relationship(back_populates="waiting_items")
    item: Mapped["LibraryItemModel"] = relationship(back_populates="waiting_members")
    
    __table_args__ = (UniqueConstraint('member_id', 'item_id'),)


class NotificationModel(Base):
    __tablename__ = 'notifications'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id', ondelete='CASCADE'))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    member: Mapped["MemberModel"] = relationship(back_populates="notifications")
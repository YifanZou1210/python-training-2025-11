-- Library_Items Table 
CREATE TABLE if not exists library_items (
    -- primary key
    id serial INT PRIMARY KEY, -- item id 
    title VARCHAR(255) NOT NULL, -- item title 
    creator VARCHAR(255) NOT NULL, -- author or director 
    item_type VARCHAR(255) NOT NULL, -- book or dvd 
    total_copies VARCHAR(20) NOT NULL DEFAULT 1, -- total copies
    available_copies INTEGER NOT NULL DEFAULT 1, -- available copies 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- creation time 
)

CREATE TABLE if not exists books (
    id serial INTEGER PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE, 
    num_pages INTEGER NOT NULL, 
    Foreign Key (id) REFERENCES library_items(id) ON DELETE CASCADE
)

CREATE Table dvds(
    id serial INTEGER PRIMARY KEY,
    duration_minutes INTEGER NOT NULL, 
    genre VARCHAR(50) NOT NULL, 
    Foreign Key (id) REFERENCES library_items(id) 
        On DELETE CASCADE
)



CREATE TABLE members (
    id serial PRIMARY KEY, 
    name VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT Null UNIQUE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)


CREATE Table membership (
    id serial PRIMARY KEY, 
    member_id integer NOT NULL UNIQUE,
    membership_type VARCHAR(20) NOT NULL,
    borrow_limit INTEGER NOT NULL,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Foreign Key (member_id) REFERENCES members(id) on delete CASCADE
)

CREATE Table borrowed_items (
    id INTEGER PRIMARY KEY serial,
    member_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'borrowed',
    Foreign Key (member_id) REFERENCES  members(id) on delete CASCADE,
    Foreign Key (item_id) REFERENCES library_items(id) on delete CASCADE
)

CREATE Table waiting_list (
    id INTEGER PRIMARY KEY serial,
    member_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Foreign Key (member_id) REFERENCES members(id) on delete CASCADE
    Foreign Key (item_id) REFERENCES library_items(id) on delete CASCADE
    UNIQUE(member_id, item_id)      
)

CREATE Table notifications (
    id INTEGER serial primary key, 
    member_id INTEGER not null,
    message text not null,
    is_read boolean default false,
    created_at TIMESTAMP DEFAULT current_timestamp,
    Foreign Key (member_id) REFERENCES members(id) delete CASCADE
)
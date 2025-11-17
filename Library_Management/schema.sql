-- Library_Items Table 
CREATE TABLE if not exists library_items (
    -- primary key
    id serial INT PRIMARY KEY, -- item id 
    title VARCHAR(255) NOT NULL, -- item title 
    creator VARCHAR(255) NOT NULL, -- author or director 
    iterm_type VARCHAR(255) NOT NULL, -- book or dvd 
    total_copies VARCHAR(20) NOT NULL DEFAULT 1, -- total copies
    available_copies INTEGER NOT NULL DEFAULT 1, -- available copies 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- creation time 
)

CREATE TABLE if not exists books (
    id serial INTEGER PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL UNIQUE, 
    null_pages INTEGER NOT NULL, 
    Foreign Key (id) REFERENCES library_items(id)
        ON DELETE CASCADE
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
    membership_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Foreign Key (membership_id) REFERENCES membership(id)
)


CREATE Table membership (
    id serial PRIMARY KEY, 
    member_id 
)
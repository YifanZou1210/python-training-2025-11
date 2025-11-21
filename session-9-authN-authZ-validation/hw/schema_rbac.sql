-- RBAC Table design 
-- user -> role -> permission 
DROP Table if EXISTS role_permissions cascade
DROP TABLE if EXISTS users cascade
DROP TABLE if EXISTS permissions cascade
DROP TABLE if EXISTS roles cascade

-- permission
CREATE Table permission (
    id serial integer primary key,
    name VARCHAR(255) not null UNIQUE, -- permission name like view_customers 
    description TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
)

-- Insert all required permissions 
INSERT INTO permissions (name, description) VALUES
('view_customers', 'View customer list and details'),
('create_customers', 'Create new customers'),
('update_customers', 'Update customer information'),
('delete_customers', 'Delete customers'),
('view_orders', 'View order list and details'),
('create_orders', 'Create new orders'),
('update_orders', 'Update order information'),
('delete_orders', 'Delete orders'),
('manage_users', 'Register new users and assign roles');

-- Role 
CREATE Table roles (
    id serial primary key integer,
    name VARCHAR(50) not null unique,
    description text,
    created_at TIMESTAMP DEFAULT current_timestamp
)

INSERT INTO roles (name, description) VALUES
('Admin', 'Full system access including user management'),
('Sales', 'Can manage customers and orders, but cannot delete or manage users'),
('Viewer', 'Read-only access to customers and orders');

-- Role-Permission Injunction 
CREATE Table role_permissions (
    id serial primary key,
    role_id integer not null,
    permission_id integer not null,
    created_at TIMESTAMP DEFAULT current_timestamp,

    Foreign Key (role_id) REFERENCES roles(id) delete cascade,
    Foreign Key (permission_id) REFERENCES permissions(id) delete cascade

    UNIQUE(role_id, permission_id)
)

-- assign all permissions to admin role
INSERT INTO role_permissions (role_id, permission_id) 
SELECT 1, id from permissions 

-- assign 6 permissions to sales role 
INSERT INTO role_permissions (role_id, permission_id)
SELECT 2, id FROM permissions 
WHERE name IN (
    'view_customers', 'create_customers', 'update_customers',
    'view_orders', 'create_orders', 'update_orders'
);

-- assign 2 permissions to viewer roles 
INSERT INTO role_permissions (role_id, permission_id)
SELECT 3, id FROM permissions 
WHERE name IN ('view_customers', 'view_orders');

-- User
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,         
    password_hash VARCHAR(255) NOT NULL, -- Hashed password
    name VARCHAR(100) NOT NULL,
    role_id INTEGER NOT NULL, -- one user only have one role 
    is_active BOOLEAN DEFAULT TRUE,             
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Create initial admin user
-- Password: 'Admin123' (hashed with bcrypt)
-- Note: This is a placeholder hash, will be replaced by seed script
INSERT INTO users (email, password_hash, name, role_id) VALUES
('admin@example.com', '$2b$12$placeholder', 'System Admin', 1);


--- view all roles with perssions 
SELECT r.name as role, array_agg(p.name) as permissions 
-- aggregate to one array group 
from roles r left join role_permissions rp 
on r.id = rp.role_id
left join permissions 
p on rp.permission_id = p.id -- foreign key = refered primary key 
group by r.id, r.name
order by r.id 


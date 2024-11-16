-- init.sql

-- Drop tables if they already exist (useful for resetting the database)
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;

-- Create the users table
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
);

-- Create the products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock_quantity INTEGER
);

-- Insert dummy data into users table
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'Admin'),  -- password: "password"
('user', 'user123', 'User');   -- password: "password"

-- Insert dummy data into products table
INSERT INTO products (product_id, name, category, price, stock_quantity) VALUES
(1, 'Product A', 'Category1', 10.00, 100),
(2, 'Product B', 'Category2', 15.50, 200),
(3, 'Product C', 'Category1', 20.75, 150),
(4, 'Product D', 'Category3', 30.00, 50),
(5, 'Product E', 'Category2', 25.00, 75);
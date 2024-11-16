import streamlit as st
import sqlite3
from hashlib import sha256
import pandas as pd


# Database setup
class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('inventory.db')


    def init_db(self):
        conn = self.conn
        cursor = conn.cursor()

        # Initialize database tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock_quantity INTEGER
            )
        ''')

        conn.commit()

    def get_db_connection(self):
        try:
            conn = sqlite3.connect('inventory.db')
            print("Databse connected")
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def add_user(self, username, password, role):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", (username, self.hash_password(password), role))
        conn.commit()

    # Add default admin and user
    def add_dummy_data(self):
        self.add_user("admin", "admin123", "Admin")
        self.add_user("user", "user123", "User")

# Streamlit GUI Components
class authenticate:

    def __init__(self) -> None:
        self.conn = sqlite3.connect('inventory.db')
    
  # Helper functions
    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def role(self, username, password):
        try:
            conn = self.conn
            if conn is None:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, self.hash_password(password)))
            return cursor.fetchone()
        
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None



    def authenticate_user(self, username, password):
        try:
            conn = self.conn
            if conn is None:
                return None

            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Error authenticating user: {e}")
            return None
        

    def login(self):
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = self.role(username, password)
            if user:
                st.session_state['username'] = username
                st.session_state['role'] = user[0]
                st.sidebar.success(f"Logged in as {st.session_state['role']}")
            else:
                st.sidebar.error("Invalid credentials")

    def logout(self):
        st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())
        self.conn.close()



class Products():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('inventory.db')
    
    def add_dummy_data(self, product_id, product_name, category, price, stock_quantity):
        try:
            conn = self.conn
            if conn is None:
                return None

            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (product_id, name, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)",
                           (product_id, product_name, category, price, stock_quantity))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")
            return None


    def add_data(self):
        self.add_dummy_data(1, "Milk", "dairy", 50, 30)
        self.add_dummy_data(2, "Juice", "drinks", 30, 70)
        self.add_dummy_data(11, "Corn flakes", "snacks", 67, 33)
        self.add_dummy_data(21, "cake", "bakery", 30, 45)


    def view_inventory(self):
        """
        Display all products in the inventory in table format.
        """
        try:
            conn = self.conn
            cursor = conn.cursor()
            
            # Fetch all products from the database
            cursor.execute("SELECT product_id, name, category, price, stock_quantity FROM products")
            products = cursor.fetchall()
            
            # Define table column names
            columns = [ "Product ID", "Name", "Category", "Price", "Stock Quantity"]

            # Convert data into a pandas DataFrame
            df = pd.DataFrame(products, columns=columns)

            if df.empty:
                st.warning("No products found in the inventory.")
            else:
                st.subheader("Product Inventory")
                st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while fetching the inventory: {e}")


    def add_product(self):
        if st.session_state['role'] == 'Admin':
            product_id = st.number_input("Product ID", step=1)
            name = st.text_input("Product Name")
            category = st.text_input("Category")
            price = st.number_input("Price")
            stock_quantity = st.number_input("Stock Quantity", step=1)
            if st.button("Add Product"):
                try:
                    conn = self.conn
                    if conn is None:
                        return None

                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO products (product_id, name, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)",
                           (product_id, name, category, price, stock_quantity))
                    conn.commit()
                    st.success("Product added successfully.")
                except sqlite3.Error as e:
                    print(f"Error adding product: {e}")
                    return None
        else:
            st.warning("Admin access required to add products.")

    def edit_product(self):
        if st.session_state['role'] == 'Admin':
            product_id = st.number_input("Product ID")
            new_price = st.number_input("New Price")
            new_stock = st.number_input("New Stock Quantity")
            if st.button("Update Product"):
                try:
                    conn = self.conn
                    if conn is None:
                        return None

                    cursor = conn.cursor()
                    cursor.execute("UPDATE products SET price=?, stock_quantity=? WHERE product_id=?", (new_price, new_stock, product_id))
                    conn.commit()
                    st.success("Product updated successfully.")
                except sqlite3.Error as e:
                    print(f"Error updating product: {e}")
                    return None
               
        else:
            st.warning("Admin access required to edit products.")

    def delete_product(self):
        if st.session_state['role'] == 'Admin':
            product_id = st.number_input("Product ID to delete", step=1)
            if st.button("Delete Product"):
                try:
                    conn = self.conn
                    if conn is None:
                        return None

                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM products WHERE product_id=?", (product_id,))
                    conn.commit()
                    st.success("Product deleted successfully.")
                except sqlite3.Error as e:
                    print(f"Error deleting product: {e}")
                    return None
                # finally:
                #     if conn:
                #         conn.close()
        else:
            st.warning("Admin access required to delete products.")

    def inventory_menu(self):
        # After successful login, display different tabs based on role
        st.title("Inventory Management System")

        tab1, tab2, tab3, tab4 = st.tabs([
                            "View All Products",
                            "Add Product",
                            "Update Product",
                            "Delete Product"
                            ])

        with tab1:
            st.header("All Products")
            self.view_inventory()
        with tab2:
            st.header("Add Products")
            self.add_product()
        with tab3:
            st.header("Update Products")
            self.edit_product()    
        with tab4:
            st.header("Delete Products")
            self.delete_product() 


def main():
    d = Database()

    auth_user = authenticate()
    
    P = Products()

    d.init_db()
    d.get_db_connection()

    if 'username' not in st.session_state:
        auth_user.login()
    else:
        st.sidebar.success(f"Welcome, {st.session_state['username']}")
        P.add_data()
        P.inventory_menu()
        auth_user.logout()





# Main app logic
if __name__ == "__main__":
    main()



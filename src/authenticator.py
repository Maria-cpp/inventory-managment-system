import streamlit as st


# class in process


def signUp():
    st.title("User Authentication with Streamlit and SQL")

    menu = ["Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if register_user(new_user, new_password):
                st.success("You have successfully created an account.")
            else:
                st.error("Username already exists. Please choose a different one.")

    elif choice == "Login":
        st.subheader("Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome, {username}!")
                # Load main application page here
            else:
                st.error("Incorrect username or password.")
import streamlit as st

from streamlit_option_menu import option_menu
# 
import user, home, products

st.set_page_config(
    page_title = "Inventory Managment System"
)

st.title("streamlit Docker Dev test")

st.write("This is a test app")
 
class MultiApp:
    def __init__(self):
        self.apps = []
    # 
    def add_app(self, title, function):
        self.apps.append({
            "title":title,
            "function": function
        })
    # 
    def run():
           # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Tabs',
                options=['Home','Account','Products'],
                icons=['house-fill','person-circle','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                )    
        if app == 'Home':
            home.app()
        if app == 'Account':
            user.app()
        if app == "Products":
            products.app()
    
    run()
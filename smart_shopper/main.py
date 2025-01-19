import streamlit as st

def main():
    st.title("Smart Shopper")

    with st.form(key='email_form'):
        email = st.text_input("Enter your email:")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write(f"Email submitted: {email}")

if __name__ == "__main__":
    main()
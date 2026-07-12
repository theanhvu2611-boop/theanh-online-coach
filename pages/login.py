import streamlit as st
from supabase_client import supabase

st.title("Đăng nhập")

email = st.text_input("Email")

password = st.text_input(
    "Mật khẩu",
    type="password"
)

if st.button("Đăng nhập"):

    try:

        result = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email

        st.success("Đăng nhập thành công")

        st.write(st.session_state)

    except Exception as e:

        st.error(str(e))

if st.button("Đăng xuất"):

    st.session_state.clear()

    st.rerun()
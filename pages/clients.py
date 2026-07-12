import streamlit as st
from supabase_client import supabase

# Phải đăng nhập
if not st.session_state.get("logged_in"):

    st.error("Bạn phải đăng nhập")

    st.stop()

# Chỉ admin
ADMIN_EMAIL = "theanhvu2611@gmail.com"

if st.session_state.get("user_email") != ADMIN_EMAIL:

    st.error(
        "Bạn không có quyền truy cập"
    )

    st.stop()

st.title("Quản lý học viên")

clients = (
    supabase
    .table("clients")
    .select("*")
    .order("name")
    .execute()
)

data = clients.data

# ====================
# DANH SÁCH HỌC VIÊN
# ====================

for client in data:

    st.write(
        f"""
👤 {client['name']}

📧 {client['email']}

📅 Hết hạn:
{client['package_expiry']}

✅ Active:
{client['active']}
"""
    )

    if client["active"]:

        if st.button(
            f"🔒 Khóa {client['name']}",
            key=f"disable_{client['id']}"
        ):

            supabase.table(
                "clients"
            ).update(
                {
                    "active": False
                }
            ).eq(
                "id",
                client["id"]
            ).execute()

            st.rerun()

    else:

        if st.button(
            f"🔓 Mở khóa {client['name']}",
            key=f"enable_{client['id']}"
        ):

            supabase.table(
                "clients"
            ).update(
                {
                    "active": True
                }
            ).eq(
                "id",
                client["id"]
            ).execute()

            st.rerun()

    st.divider()

st.header("Thêm học viên")

new_name = st.text_input(
    "Tên học viên"
)

new_email = st.text_input(
    "Email"
)

expiry = st.date_input(
    "Ngày hết hạn"
)

if st.button("Thêm học viên"):

    try:

        supabase.table(
            "clients"
        ).insert(
            {
                "name": new_name,
                "email": new_email,
                "package_expiry": str(expiry),
                "active": True
            }
        ).execute()

        st.success(
            "Đã thêm học viên"
        )

        st.rerun()

    except Exception as e:

        st.error(str(e))
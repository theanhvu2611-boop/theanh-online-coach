import streamlit as st
from supabase_client import supabase
from datetime import date

# =========================
# KIỂM TRA ĐĂNG NHẬP
# =========================

if not st.session_state.get("logged_in"):

    st.error("Bạn phải đăng nhập")

    st.stop()

ADMIN_EMAIL = "theanhvu2611@gmail.com"

if st.session_state.get("user_email") != ADMIN_EMAIL:

    st.error(
        "Bạn không có quyền truy cập"
    )

    st.stop()
    
# =========================
# CHỈ ADMIN ĐƯỢC TRUY CẬP
# =========================

ADMIN_EMAIL = "theanhvu2611@gmail.com"

if st.session_state.get("user_email") != ADMIN_EMAIL:

    st.error("Bạn không có quyền truy cập")

    st.stop()

# =========================
# DASHBOARD
# =========================

st.title("🏋️ Coach Dashboard")

selected_date = st.date_input(
    "Xem lịch ngày",
    value=date.today()
)

# =========================
# LẤY BOOKING
# =========================

bookings = (
    supabase
    .table("bookings")
    .select("*")
    .eq("booking_date", str(selected_date))
    .order("booking_time")
    .execute()
)

data = bookings.data

# =========================
# KHÔNG CÓ LỊCH
# =========================

if not data:

    st.info(
        "Không có lịch trong ngày này"
    )

# =========================
# HIỂN THỊ LỊCH
# =========================

else:

    st.subheader(
        f"📅 {selected_date} ({len(data)} ca)"
    )

    for item in data:

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write(
                f"🕒 {item['booking_time']} - {item['student_name']}"
            )

        with col2:

            if st.button(
                "❌",
                key=f"delete_{item['id']}"
            ):

                supabase.table(
                    "bookings"
                ).delete().eq(
                    "id",
                    item["id"]
                ).execute()

                st.success(
                    "Đã xóa lịch"
                )

                st.rerun()

# =========================
# THỐNG KÊ
# =========================

st.divider()

st.metric(
    "Tổng số lịch trong ngày",
    len(data)
)

# =========================
# ĐĂNG XUẤT
# =========================

if st.button("Đăng xuất"):

    st.session_state.clear()

    st.rerun()
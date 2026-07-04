import streamlit as st
from supabase_client import supabase
from datetime import date

st.title("Coach Dashboard")

# Chọn ngày muốn xem
selected_date = st.date_input(
    "Xem lịch ngày",
    value=date.today()
)

# Lấy booking theo ngày
bookings = (
    supabase
    .table("bookings")
    .select("*")
    .eq("booking_date", str(selected_date))
    .order("booking_time")
    .execute()
)

data = bookings.data

# Hiển thị lịch
if not data:

    st.info("Không có lịch trong ngày này")

else:

    st.subheader(
        f"📅 {selected_date} ({len(data)} ca)"
    )

    for item in data:

        col1, col2 = st.columns([4, 1])

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

                st.success("Đã xóa lịch")

                st.rerun()
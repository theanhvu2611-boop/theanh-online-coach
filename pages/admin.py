import streamlit as st
from supabase_client import supabase

st.title("Coach Dashboard")

bookings = (
    supabase
    .table("bookings")
    .select("*")
    .order("booking_date")
    .execute()
)

st.dataframe(bookings.data)
booking_id = st.number_input(
    "ID cần xóa",
    step=1
)

if st.button("Xóa lịch"):

    supabase.table("bookings").delete().eq(
        "id",
        booking_id
    ).execute()

    st.success("Đã xóa")
import streamlit as st
from datetime import datetime, timedelta
from supabase_client import supabase
from telegram_bot import send_telegram

st.title("Thế Anh Fitness")

st.write("Website Booking Coaching")

# Nhập tên học viên
name = st.text_input("Tên học viên")

# Chọn ngày
date = st.date_input("Ngày")

# Lấy booking của ngày đã chọn
bookings = (
    supabase
    .table("bookings")
    .select("booking_time")
    .eq("booking_date", str(date))
    .execute()
)

# Danh sách giờ đã đặt
booked_times = []

for item in bookings.data:
    booked_times.append(item["booking_time"])

# Danh sách giờ bị khóa
blocked_times = []

for booked_time in booked_times:

    # Khóa chính giờ đã đặt
    blocked_times.append(booked_time)

    # Khóa thêm 30 phút tiếp theo
    time_str = booked_time.replace(" - VN", "")

    dt = datetime.strptime(time_str, "%H:%M")

    next_slot = dt + timedelta(minutes=30)

    blocked_times.append(
        next_slot.strftime("%H:%M") + " - VN"
    )

# Tạo toàn bộ khung giờ
all_times = []

current = datetime.strptime("01:00", "%H:%M")
end = datetime.strptime("22:00", "%H:%M")

while current <= end:

    all_times.append(
        current.strftime("%H:%M") + " - VN"
    )

    current += timedelta(minutes=30)

# Chỉ lấy giờ còn trống
available_times = []

for t in all_times:

    if t not in blocked_times:
        available_times.append(t)

# Nếu hết giờ
if len(available_times) == 0:

    st.warning("Ngày này đã kín lịch")

    st.stop()

# Chọn giờ
time = st.selectbox(
    "Khung giờ",
    available_times
)

# Đặt lịch
if st.button("Đặt lịch"):

    if not name:

        st.error("Vui lòng nhập tên học viên")

    else:

        try:

            supabase.table("bookings").insert({
                "student_name": name,
                "booking_date": str(date),
                "booking_time": time
            }).execute()

            send_telegram(
                f"""
🔥 BOOKING MỚI

👤 Học viên: {name}

📅 Ngày: {date}

🕒 Giờ: {time}
"""
            )

            st.success(
                f"Đặt lịch thành công: {date} lúc {time}"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Có lỗi xảy ra: {str(e)}"
            )
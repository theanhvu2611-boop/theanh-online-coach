import streamlit as st
from datetime import datetime, timedelta, date
from supabase_client import supabase
from telegram_bot import send_telegram

# =========================
# KIỂM TRA ĐĂNG NHẬP
# =========================

if not st.session_state.get("logged_in"):

    st.error(
        "Vui lòng đăng nhập tại trang Login"
    )

    st.stop()

user_email = st.session_state.get(
    "user_email"
)

st.title("Thế Anh Fitness")

st.write("Website Booking Coaching")

client = (
    supabase
    .table("clients")
    .select("*")
    .eq("email", user_email)
    .execute()
)

if len(client.data) == 0:

    st.error(
        "Tài khoản chưa được kích hoạt"
    )

    st.stop()

student_name = client.data[0]["name"]

expiry = client.data[0]["package_expiry"]

if expiry:

    expiry_date = date.fromisoformat(
        expiry
    )

    if date.today() > expiry_date:

        st.error(
            "Gói coaching đã hết hạn"
        )

        st.stop()
        
st.success(
    f"Xin chào {student_name}"
)
st.info(
    f"Gói coaching hết hạn: {expiry}"
)

if st.button("Đăng xuất"):

    st.session_state.clear()

    st.rerun()

# Chọn ngày
selected_date = st.date_input("Ngày")

# Lấy booking của ngày đã chọn
bookings = (
    supabase
    .table("bookings")
    .select("booking_time")
    .eq("booking_date", str(selected_date))
    .execute()
)

# Danh sách giờ đã đặt
booked_times = []

for item in bookings.data:

    booked_times.append(
        item["booking_time"]
    )

# Tạo toàn bộ khung giờ
all_times = []

current = datetime.strptime(
    "01:00",
    "%H:%M"
)

end = datetime.strptime(
    "22:00",
    "%H:%M"
)

while current <= end:

    all_times.append(
        current.strftime("%H:%M") + " - VN"
    )

    current += timedelta(
        minutes=30
    )

# Chỉ lấy giờ không bị trùng
# với buổi PT 60 phút

available_times = []

for t in all_times:

    slot_start = datetime.strptime(
        t.replace(" - VN", ""),
        "%H:%M"
    )

    slot_end = (
        slot_start
        + timedelta(minutes=60)
    )

    conflict = False

    for booked_time in booked_times:

        booked_start = datetime.strptime(
            booked_time.replace(
                " - VN",
                ""
            ),
            "%H:%M"
        )

        booked_end = (
            booked_start
            + timedelta(minutes=60)
        )

        if (
            slot_start < booked_end
            and
            slot_end > booked_start
        ):

            conflict = True
            break

    if not conflict:

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

    try:

        supabase.table("bookings").insert({
            "student_name": student_name,
            "booking_date": str(selected_date),
            "booking_time": time
        }).execute()

        send_telegram(
            f"""
🔥 BOOKING MỚI

👤 Học viên: {student_name}

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
import streamlit as st
import time
from Chat import chat

st.title('Chatbot GERTY')  # Đặt tiêu đề cho ứng dụng

# Kiểm tra và khởi tạo session_state nếu cần
if "messages" not in st.session_state:
    st.session_state.messages = []  # Khởi tạo danh sách tin nhắn trong session_state nếu chưa có

# Hiển thị tin nhắn có trong session_state
for message in st.session_state.messages:
    with st.chat_message(message['role']):  # Tạo phần hiển thị tin nhắn theo vai trò (user hoặc assistant)
        st.markdown(message['content'])  # Hiển thị nội dung tin nhắn

# Lấy dữ liệu từ chat_input và xử lý
if prompt := st.chat_input("Hãy nhập vào yêu cầu?"):
    # Thêm tin nhắn của người dùng vào session_state
    st.session_state.messages.append(
        {
            "role": 'user',  # Vai trò của tin nhắn là 'user'
            "content": prompt  # Nội dung tin nhắn
        }
    )

    # Hiển thị tin nhắn người dùng vừa nhập trong giao diện Streamlit.
    with st.chat_message('user'):
        st.markdown(prompt)

    # Tạo một phần tin nhắn mới với vai trò là 'assistant'.
    with st.chat_message('assistant'):
        full_res = ""
        holder = st.empty()  # Tạo một chỗ trống để hiển thị tin nhắn dần dần
        
        # Gọi hàm chat và xử lý kết quả
        response = chat(prompt)
        
        # Chạy animation tạo cảm giác trả lời của bot
        for word in response.split():
            full_res += word + " "
            time.sleep(0.05)  # Tạm dừng 0.05 giây giữa các từ
            holder.markdown(full_res + "█")  # Hiển thị từ mới thêm vào với dấu nháy để mô phỏng gõ chữ
            
        # Hiển thị ra câu trả lời đầy đủ
        holder.markdown(full_res)

    # Thêm tin nhắn của bot vào session_state
    st.session_state.messages.append(
        {
            "role": "assistant",  # Vai trò của tin nhắn là 'assistant'
            "content": full_res  # Nội dung tin nhắn
        }
    )

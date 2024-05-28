import random
import json
import torch
import os
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from getWeather import weather
from unidecode import unidecode
from tom_tat import tom_tat_van_ban
from acronym.stand_words import normalize_text, dictions

# Chọn thiết bị chạy mô hình PyTorch (GPU nếu có, ngược lại sử dụng CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

intents = {"intents": []}

# Lặp qua tất cả các file JSON trong thư mục "stories" và mở các file json trong đó
folder_path = "stories"
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):  # Kiểm tra file có định dạng .json
        file_path = os.path.join(folder_path, file_name)  # Tạo đường dẫn đầy đủ tới file
        with open(file_path, 'r', encoding='utf-8') as file:  # Mở file với mã hóa utf-8
            intents_data = json.load(file)  # Đọc dữ liệu JSON từ file
            intents["intents"].extend(intents_data["intents"])  # Thêm các intent vào danh sách intents

FILE = "data.pth"
data = torch.load(FILE)  # Tải dữ liệu mô hình đã được lưu

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Khởi tạo mô hình NeuralNet và tải trạng thái đã lưu
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # Chuyển mô hình sang chế độ đánh giá (evaluation)

bot_name = "TIMI"
waiting_for_summary = False  # Biến trạng thái chờ tóm tắt

def chat(user_input):
    global waiting_for_summary
    # Xử lý input từ người dùng
    processed_input = unidecode(user_input).lower()  # Chuyển đổi input thành chữ thường và loại bỏ dấu
    processed_input = normalize_text(processed_input, dictions)  # Chuẩn hóa văn bản
    processed_input = tokenize(processed_input)  # Tách từ

    X = bag_of_words(processed_input, all_words)  # Chuyển đổi input thành bag of words
    X = X.reshape(1, X.shape[0])  # Định hình lại tensor
    X = torch.from_numpy(X).to(device)  # Chuyển đổi thành tensor PyTorch

    output = model(X)  # Dự đoán từ mô hình
    _, predicted = torch.max(output, dim=1)  # Lấy nhãn có xác suất cao nhất

    tag = tags[predicted.item()]  # Lấy tag tương ứng với nhãn dự đoán

    probs = torch.softmax(output, dim=1)  # Tính xác suất của các nhãn
    prob = probs[0][predicted.item()]  # Xác suất của nhãn được dự đoán

    # Nếu đang trong trạng thái chờ tóm tắt
    if waiting_for_summary:
        if prob.item() > 0.92:  # Kiểm tra xác suất dự đoán
            waiting_for_summary = False  # Thay đổi trạng thái chờ tóm tắt
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])  # Trả về phản hồi ngẫu nhiên
        summary = tom_tat_van_ban(user_input)  # Gọi hàm tóm tắt văn bản
        waiting_for_summary = False  # Thay đổi trạng thái chờ tóm tắt
        return summary  # Trả về kết quả tóm tắt

    # Nếu xác suất dự đoán cao hơn ngưỡng (0.85), chọn phản hồi tương ứng
    if prob.item() > 0.8:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "tom_tat":
                    waiting_for_summary = True  # Đặt trạng thái chờ tóm tắt
                    return random.choice(intent['responses'])  # Trả về phản hồi ngẫu nhiên
                elif tag == 'weather':
                    return weather(user_input)  # Gọi hàm lấy thời tiết
                else:
                    return random.choice(intent['responses'])  # Trả về phản hồi ngẫu nhiên
    else:
        # Nếu không tìm thấy intent phù hợp, trả về phản hồi mặc định
        intent = next((i for i in intents['intents'] if i["tag"] == "khong_hieu"), None)
        if intent:
            return random.choice(intent['responses'])  # Trả về phản hồi ngẫu nhiên
        else:
            return "I do not understand..."  # Trả về thông báo không hiểu


# while True:
#     a = input("Nhập: ")
#     if a == 'q': break
#     b = chat(a)
#     print(b)
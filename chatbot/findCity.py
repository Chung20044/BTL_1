import spacy

def detect_city(text):
    # Tải mô hình ngôn ngữ tiếng Anh của spaCy
    nlp = spacy.load("en_core_web_sm")
    # Xử lý văn bản đầu vào
    doc = nlp(text)
    cities = []  # Khởi tạo danh sách để lưu tên các thành phố hoặc quốc gia
    # Duyệt qua các thực thể nhận dạng trong văn bản
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Kiểm tra nếu thực thể là "GPE" (Địa danh: thành phố, quốc gia, v.v.)
            cities.append(ent.text)  # Thêm tên thực thể vào danh sách
    if not cities:  # Nếu không tìm thấy thành phố hoặc quốc gia nào
        return "Không tìm thấy thành phố hoặc quốc gia nào."
    return cities  # Trả về danh sách các thành phố hoặc quốc gia

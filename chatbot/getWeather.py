import requests
import spacy

DEFAULT_API_KEY = "1cc33c70b27901c6919c8f891ebff70c"  # API key mặc định cho OpenWeatherMap

def weather(text):
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
        return weather_api('Hanoi')  # Mặc định lấy thời tiết của Hà Nội
    else:
        return weather_api(cities[0])  # Lấy thời tiết của thành phố đầu tiên được tìm thấy

def weather_api(city, api_key=DEFAULT_API_KEY):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"  # URL cơ bản để tìm kiếm tọa độ địa lý của thành phố
    params = {
        'q': f"{city}",  # Thành phố cần tìm kiếm
        'limit': 1,  # Giới hạn kết quả trả về là 1
        'appid': api_key  # API key để xác thực
    }

    try:
        response = requests.get(base_url, params=params)  # Gửi yêu cầu HTTP GET tới API
        response.raise_for_status()  # Kiểm tra phản hồi có lỗi không
        
        data = response.json()  # Chuyển phản hồi thành dữ liệu JSON

        if response.status_code == 200 and data:
            latitude = data[0]['lat']  # Lấy vĩ độ của thành phố
            longitude = data[0]['lon']  # Lấy kinh độ của thành phố
            
            weather_result = get_weather(city, latitude, longitude, api_key)  # Gọi hàm lấy thông tin thời tiết
            return weather_result
        else:
            return "Không thể lấy dữ liệu thời tiết. Vui lòng thử lại sau."  # Trường hợp không có dữ liệu phù hợp
    
    except requests.RequestException:
        return "Không thể lấy dữ liệu thời tiết. Vui lòng thử lại sau."  # Trường hợp lỗi yêu cầu HTTP

def get_weather(city, lat, lon, api_key=DEFAULT_API_KEY):
    base_url = "https://api.openweathermap.org/data/2.5/weather"  # URL cơ bản để lấy thông tin thời tiết
    params = {
        'lat': lat,  # Vĩ độ của thành phố
        'lon': lon,  # Kinh độ của thành phố
        'appid': api_key,  # API key để xác thực
        'units': 'metric'  # Đơn vị nhiệt độ là độ C
    }

    try:
        response = requests.get(base_url, params=params)  # Gửi yêu cầu HTTP GET tới API
        response.raise_for_status()  # Kiểm tra phản hồi có lỗi không
        
        data = response.json()  # Chuyển phản hồi thành dữ liệu JSON

        if response.status_code == 200:
            temperature = data['main']['temp']  # Lấy nhiệt độ từ dữ liệu thời tiết
            return f"Nhiệt độ hiện tại tại {city}: {temperature} °C"  # Trả về chuỗi thông tin thời tiết
        else:
            return "Không thể lấy dữ liệu thời tiết. Vui lòng thử lại sau."  # Trường hợp không có dữ liệu phù hợp
    
    except requests.RequestException:
        return "Không thể lấy dữ liệu thời tiết. Vui lòng thử lại sau."  # Trường hợp lỗi yêu cầu HTTP

# while True: 
#     a = input('Nhập: ')
#     if a == 'q': break
#     print(weather(a))
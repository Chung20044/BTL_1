import torch
import torch.nn as nn

# Định nghĩa lớp NeuralNet kế thừa từ nn.Module
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        # Gọi hàm khởi tạo của lớp cha nn.Module
        super(NeuralNet, self).__init__()
        # Định nghĩa lớp Linear (fully connected layer) đầu tiên với kích thước đầu vào và đầu ra tương ứng
        self.l1 = nn.Linear(input_size, hidden_size)
        # Định nghĩa lớp Linear thứ hai với kích thước đầu vào và đầu ra tương ứng
        self.l2 = nn.Linear(hidden_size, hidden_size)
        # Định nghĩa lớp Linear thứ ba với kích thước đầu vào là hidden_size và đầu ra là num_classes
        self.l3 = nn.Linear(hidden_size, num_classes)
        # Định nghĩa hàm kích hoạt ReLU
        self.relu = nn.ReLU()

    def forward(self, x):
        # Tính toán giá trị tại lớp Linear đầu tiên
        out = self.l1(x)
        # Áp dụng hàm kích hoạt ReLU
        out = self.relu(out)
        # Tính toán giá trị tại lớp Linear thứ hai
        out = self.l2(out)
        # Áp dụng hàm kích hoạt ReLU
        out = self.relu(out)
        # Tính toán giá trị tại lớp Linear thứ ba
        out = self.l3(out)
        # Trả về kết quả đầu ra
        return out

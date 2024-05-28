from underthesea import ner, sent_tokenize
import numpy as np
import nltk
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.cluster import KMeans

def tom_tat_van_ban(content):
    # Chuyển văn bản thành chữ thường và loại bỏ khoảng trắng ở đầu và cuối
    content_parsed = content.lower().strip()
    # Tách văn bản thành các câu
    sentences = sent_tokenize(content_parsed)

    # Số lượng câu trong văn bản
    num_sent = len(sentences)

    # Sử dụng Named Entity Recognition (NER) để lấy từ được gắn nhãn
    word_labels = []
    for sentence in sentences:
        # Lấy nhãn từ của câu hiện tại
        sentence_labels = ner(sentence)
        # Thêm từ vào danh sách word_labels
        word_labels.extend([label[0] for label in sentence_labels])

    # Lọc bỏ các từ có nhãn không phải là tên người, địa điểm hoặc tổ chức
    filtered_words = [word for word in word_labels if word not in ['B-PER', 'I-PER', 'B-LOC', 'I-LOC', 'B-ORG', 'I-ORG']]

    # Biểu diễn vector cho mỗi câu
    X = []
    for sentence in sentences:
        # Tách các từ trong câu
        words = nltk.word_tokenize(sentence)
        # Tạo vector độ dài bằng số lượng từ đã lọc và gán giá trị ban đầu là 0
        sentence_vec = np.zeros((len(filtered_words)))
        # Gán giá trị 1 cho từ có trong câu
        for idx, word in enumerate(filtered_words):
            if word in words:
                sentence_vec[idx] = 1
        # Thêm vector của câu vào danh sách X
        X.append(sentence_vec)

    # Tính số cụm cho K-means
    n_clusters = int(num_sent * (35/100))
    if n_clusters >= (num_sent - 1):
        return 'Văn bản quá ngắn! Nhập văn bản dài hơn để tôi có thể tóm tắt giúp bạn'
    else:
        # Áp dụng K-means
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        kmeans = kmeans.fit(X)

        # Tính trung bình vị trí của các câu trong mỗi cụm
        avg = []
        for j in range(n_clusters):
            idx = np.where(kmeans.labels_ == j)[0]
            avg.append(np.mean(idx))

        # Tìm câu gần nhất với trung tâm của mỗi cụm
        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
        # Sắp xếp thứ tự các câu tóm tắt
        ordering = sorted(range(n_clusters), key=lambda k: avg[k])
        # Tạo văn bản tóm tắt bằng cách ghép các câu gần trung tâm nhất theo thứ tự
        summary = ' '.join([sentences[closest[idx]] for idx in ordering])
        return f'{summary}'

# Ví dụ sử dụng hàm tom_tat_van_ban
# content = input("Nhập vào văn bản: ")
# print(tom_tat_van_ban(content))

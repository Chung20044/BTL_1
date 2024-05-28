import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
from unidecode import unidecode

# Khởi tạo Porter Stemmer
stemmer = PorterStemmer()

# Hàm tách các từ thành token (các từ riêng lẻ)
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Hàm giảm từ về gốc, chuyển thành chữ thường và loại bỏ dấu
def stem(word):
    # Loại bỏ dấu và chuyển thành chữ thường
    normalized_word = unidecode(word).lower()
    # Giảm từ về gốc
    return stemmer.stem(normalized_word)

# Hàm biểu diễn từ dưới dạng bag-of-words
def bag_of_words(tokenized_sentence, all_words):
    # Stem các từ trong tokenized_sentence
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    # Tạo mảng bằng độ dài all_words và gán giá trị ban đầu là 0.0
    bag = np.zeros(len(all_words), dtype=np.float32)

    # Lặp từng từ trong all_words, nếu từ đó có trong tokenized_sentence thì gán giá trị 1.0 cho vị trí tương ứng
    for idx, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[idx] = 1.0
    return bag

# Ví dụ minh họa cách sử dụng hàm bag_of_words
# tokenized_sentence = ["hello", "world", "hello"]
# all_words = ["hello", "world", "goodbye"]
# Kết quả mong đợi: [1.0, 1.0, 0.0]

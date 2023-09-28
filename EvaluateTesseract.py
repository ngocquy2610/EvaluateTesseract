import difflib
import pytesseract
from PIL import Image, ImageEnhance
import os
import json

# Path to the Tesseract executable (change this if needed)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\ADMIN\\Desktop\\nnquy\\FSOFT\\Tesseract\\tesseract.exe'


def calculate_cer(text_ref, text_pred):

    # So sánh từng ký tự trong hai văn bản.
    diff = list(difflib.ndiff(text_ref, text_pred))

    # Đếm số ký tự bị nhận dạng sai.
    num_errors = len([x for x in diff if x[0] != " "])

    # Tính tỷ lệ lỗi ký tự.
    cer = num_errors / len(text_ref)
    if cer > 1:
        cer = 1

    return cer

def calculate_wer(text_ref, text_pred):

    # Phân tách hai văn bản thành các từ.
    text_ref_words = text_ref.split()
    text_pred_words = text_pred.split()

    # Tạo một bản đồ từ các từ tham chiếu đến các từ được nhận dạng.
    map_words = {}
    for i, word in enumerate(text_ref_words):
        map_words[word] = text_pred_words[i]

    # Tạo một danh sách các từ bị nhận dạng sai.
    list_errors = []
    for i, word in enumerate(text_ref_words):
        if word != map_words[word]:
            list_errors.append(i)

    # Tính số từ bị nhận dạng sai.
    num_errors = len(list_errors)

    # Tính tỷ lệ lỗi từ.
    wer = num_errors / len(text_ref_words)

    return wer

def evaluate_detection(images_folder, labels_file):
    
    with open(labels_file) as f:
        labels = json.load(f)

    results = []
    images = os.listdir(images_folder)
    n = 1
    for image in images:
        image_path = os.path.join(images_folder, image)
        img = Image.open(image_path)

        text_pred = pytesseract.image_to_string(img)
        text_ref = labels[image]['data']

        if text_pred == '':
            acc = 0

        else:
            cer = calculate_cer(text_ref, text_pred)
            wer = calculate_wer(text_ref, text_pred)
            acc = (1-cer) * (1-wer)

        results.append(acc) 
        print(f'done {n} image')
        n += 1
    
    accuracy = sum(results) / len(results)

    return accuracy

images_folder = 'C:\\Users\\ADMIN\\Desktop\\nnquy\\FSOFT\\1_Text Extraction\\2_Text Recognition\\data2\\images'
labels_file = 'C:\\Users\\ADMIN\\Desktop\\nnquy\\FSOFT\\1_Text Extraction\\2_Text Recognition\\data2\\labels.json'

accuracy = evaluate_detection(images_folder, labels_file)

print(accuracy)

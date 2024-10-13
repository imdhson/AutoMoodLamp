import math
import tensorflow as tf
import csv

def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding to score vector."""
    class_names = []
    if tf.io.gfile.exists(class_map_csv_text):
        with open(class_map_csv_text, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                class_names.append(row['display_name'])
    else:
        print(f"File not found: {class_map_csv_text}")
    return class_names

def is_conversation(class_idx):
    speech_arr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 25, 26, 27, 28, 29, 30, 31, 32, 63, 64, 65}
    #대화와 연관된 클래스의 집합
    if class_idx in speech_arr:
        return True
    return False

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
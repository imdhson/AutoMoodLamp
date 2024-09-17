def is_conversation(class_idx):
    speech_arr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 25, 26, 27, 28, 29, 30, 31, 32, 63, 64, 65}
    if class_idx in speech_arr:
        return True
    return False


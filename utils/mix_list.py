import random

def mix_list(list_original):
    # Создаем копию, поскольку мы не должны изменять оригинал
    list = list_original[:]
    # Цикл от 0 до длины списка -1
    list_length = len(list)
    for i in range(list_length):
        # Получение случайного индекса
        index_aleatory = random.randint(0, list_length - 1)
        # Замена
        temp = list[i]
        list[i] = list[index_aleatory]
        list[index_aleatory] = temp
    # Возвращаем список
    return list


if __name__ == '__main__':
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    mixed_list = mix_list(list)
    print("Исходный список: ")
    print(list)
    print("Перемешанный список: ")
    print(mixed_list)
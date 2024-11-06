from csv import DictReader


def get_clients(path_file_csv: str, delimiter: str):
    """
    Получаем список клиентов из csv-файла
    :param path_file_csv: путь к csv-файлу
    :param delimiter: разделитель
    :return:
    """
    with open(path_file_csv, encoding='utf-8') as file:
        file_reader = DictReader(file, delimiter=delimiter)
        list_numbers = list()
        # for i, row in enumerate(file_reader):
        for row in file_reader:
            # if i == 0:
            #     continue
            try:
                list_numbers.append(row['Мобильный номер'])
            except KeyError:
                break

        return list_numbers

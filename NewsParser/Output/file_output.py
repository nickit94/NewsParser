import os


def generate_path(url):
    """
    Генерирование пути и имени файла в соответствии с "Усложнение задачи №1"
    :param url: url
    :return: полный путь
    """
    path_list = url.split('/')

    if path_list[-1] != '':
        filename = path_list[-1] + ".txt"
        path = os.getcwd() + "/".join(path_list[1:-1])
    else:
        filename = path_list[-2] + ".txt"
        path = os.getcwd() + "/".join(path_list[1:-2])

    if not os.path.exists(path):
        os.makedirs(path)

    return path + '/' + filename


class FileOutput:
    """
    Вывод данных парсера в файл.
    """
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def generate_output(self):
        full_path = generate_path(self.url)

        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(self.text)

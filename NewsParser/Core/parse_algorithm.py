import os
import bs4
import configparser
from textwrap import fill
from .parse_algorithm_helper import *


class ParseAlgorithm:
    """
    Реализация парсинга данных с помощью библиотеки beautifulSoup4.

    Алгоритм строится на следующих этапах:
        - Поиск всех универсальных тегов, которые могут содержать текст статьи (@list_text_tags)
        - Поиск из предыдущего списка всех наиболее вероятных тегов, в которых может быть полный текст
        статьи и заголовок
        - Утверждение какого-то одного тега из предыдущего пункта, в котором с максимальной вероятностью есть
        полный текст статьи и заголовок, а также минимальное количество мусора
        - Проход по всем дочерним элементам найденного главного тега в поисках тегов, содержащих текст
        - Фильтрация найденных тегов (второй проход для вычищения мусора) через регулярное выражение и форматирование
        итоговой строки (ссылки, списки, код)
    """

    def __init__(self, request):
        self.soup = bs4.BeautifulSoup(request.text, 'lxml')
        self.config = configparser.ConfigParser()
        self.config.read(os.path.dirname(__file__) + '/../config.ini', encoding="utf-8")
        self.wrap = int(self.config['text']['wrap'])

    def __filtering_and_formatting_text(self, tag):
        """
        Метод, который реализует более детальную фильтрацию элементов, а также основное форматирование текста
        :param tag: текущий тег для проверки
        :return: отформатированная строка, если содержимое тега не является мусором
        """
        # Форматирование для кодовых тегов
        if 'code' in [child1.name for child1 in tag.contents]:
            return wrapper_code_tag(tag.text.strip())

        # Форматирование для заголовков
        for header in header_tag_list:
            if header in tag.name:
                return '\n' + tag.text.strip().upper()

        # Форматирование для всех остальных тегов
        text = tag.text.replace('\n', '').strip()
        if re.findall(regex, text):

            # Форматирование для списков
            if tag.parent.name == 'li':
                text = ' • ' + text

            for child in tag.contents:
                # Форматирование для ссылок
                if child.name and child.name == 'a':
                    indx = text.find(child.text) + len(child.text)
                    text = text[:indx] + " [{}]".format(child.get('href')) + text[indx:]

            return '\n' + fill(text, width=self.wrap) + ('\n' if tag.parent.name != 'li' else '')

        return ""

    def __map_to_probable_main_tag_list(self):
        """
        Фильтрация всех тегов страницы и получение списка вероятных тегов, в которых содержится полный текст
        статьи и заголовок
        :return: список вероятных тегов с текстом и заголовком
        """

        list_probable_main_tag = []
        list_all_text_tags = self.soup.findAll(text_tag_list)

        # Рекурсивный проход по дочерним элементам каждого найденного тэга и подсчет всех ключевых параметров
        # (кол-во дочерних элементов, кол-во точек в тексте)
        for cur_tag in list_all_text_tags:
            count_child, count_dot, is_h1 = 0, 0, False

            for child in cur_tag.descendants:

                if child.name in tag_white_list:
                    count_child += 1

                if child.name == 'h1':
                    is_h1 = True

                if is_navigable_string(child):
                    count_dot += child.count('.')

            if is_h1:
                list_probable_main_tag.append([cur_tag, count_child, count_dot])

        return list_probable_main_tag

    def parse(self):
        # Поиск всех вероятных тэгов, которые могут содержать текст статьи и заголовок
        list_probable_main_tag = self.__map_to_probable_main_tag_list()

        # Поиск одного главного тэга, в котором находится вся статья с заголовком с меньшим мусором
        tag_with_article = find_main_tag_with_article(list_probable_main_tag)

        # Выборка из дочерних тегов главного тега по наличию текста
        list_tag_with_text = tag_with_article.findAll(find_all_tag_with_text)

        # Дополнительная фильтрация текста через регулярку. На выходе - чистая статья
        result_text = self.soup.title.text.strip().upper() + '\n'
        for tag_with_text in list_tag_with_text:
            format_text = self.__filtering_and_formatting_text(tag_with_text)
            if format_text:
                result_text += format_text

        return result_text

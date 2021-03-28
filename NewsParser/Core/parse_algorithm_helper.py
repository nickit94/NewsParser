import re
from bs4.element import NavigableString, Script, Stylesheet

# Основные теги для поиска статьи
text_tag_list = ['div', 'article']
# Теги заголовков для повышения регистра
header_tag_list = ['h1', 'h2', 'h3', 'h4']
# Белый список тегов для поиска полезного текста
tag_white_list = ['div', 'span', 'p', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
# Черный список тегов для исключения мусора
tag_black_list = ['noindex', 'footer', 'svg', 'label', 'input', 'meta', 'link', 'script', 'picture', 'img',
                  'noscript', 'figure', 'figcaption', 'iframe']
# Разрешенные вложенные теги для форматирования текста
text_formatter_tag_list = ['a', 'strong', 'em', 'mark', 'b', 'i', 's', 'small', 'sup', 'sub', 'dfn', 'q',
                           'blockquote', 'cite', 'code', 'samp', 'kbd', 'var', 'time']

# Регулярное выражение для отсеивания мусора в тексте тегов
regex = re.compile(r'.*[a-zA-Zа-яА-ЯёЁ]+.*[\.!?:;]$')


def is_navigable_string(bs4_element):
    """
    Вернет True, если данный элемент является строкой, но при этом не является скриптом и стилем
    :param bs4_element: bs4 element
    :return: Bool
    """
    return (isinstance(bs4_element, NavigableString) and not isinstance(bs4_element, Script)
            and not isinstance(bs4_element, Stylesheet))


def find_all_tag_with_text(tag):
    """
    Функция, которая передается как условие для поиска элементов в bs4.findAll.
    Специальное многосоставное условие, которое помогает отсеить большую часть мусора из разметки страницы.
    :param tag: текущий тег для проверки
    :return: Bool
    """
    return (tag.name and tag.name in tag_white_list
            and ((isinstance(tag.next_element, NavigableString) and tag.next_element != '\n')
                 or tag.next_element.name in text_formatter_tag_list)
            and not tag.find_parent(tag_black_list))


def find_main_tag_with_article(list_tag):
    """
    Поиск тега со статьей из списка вероятных тегов. В дальнейшем алгоритм можно улучить,
    поэтому ему выделен отдельный метод
    :param list_tag: список вероятных тегов
    :return: главный тег со статьей
    """
    # Подсчет среднего кол-ва точек во всех найденных тегах
    avg_count_dot = sum(item[2] for item in list_tag) / len(list_tag)
    list_tag.reverse()

    for tag in list_tag:
        if tag[2] > avg_count_dot / 2:
            return tag[0]


def wrapper_code_tag(code_text):
    """
    Обертка кодового тега
    """
    return '\n\n------------ CODE START ------------\n' + \
           code_text + \
           '\n------------- CODE END -------------\n'

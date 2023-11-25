"""
Скрыпт для падліку частаты ўжывання словаформаў ў тэксце
Імя тэкставага файлу для апрацоўкі можа падавацца ў камандным радку
альбо, пры адсутнасці, уводзіцца ў дыялогу пасля запыту праграмы.
# assert a==b, f'{a} ! = {b}' - карысная рэч на ўспамін

"""
import sys
import re
from itertools import filterfalse
import locale
locale.setlocale(locale.LC_COLLATE, "be_BY.UTF-8")

def get_words(text):
    """Ачыстка ад пунктуыцыі, сартыроўка тэксту, падрыхтоўка яго да падлікаў
    """
    spec_chars = '.,?!№@#$%~_—+–«»<>():;…0123456789\*\"\/\[\]'
    text = "".join([i for i in text if i not in spec_chars])
    text = text.lower()

    text = text.replace("\n", " ").replace("'", "ʼ").replace("’", "ʼ")\
               .replace("- ", " ").replace(" - ", " ").replace(" -", " ")\
               .replace("\xa0", " ").replace("\t", " ")

    # перадача тэксту ў функцыю для выдалення небеларускай лексікі,
    # і некаторай з "клясычнага" правапісу
    text = cleen_foreign_words(text)
    text = text.replace(" ў", " у")

    # канвертацыя радка ў спіс
    words = text.split()

    # стоп-словы
    be_rm = ['а', 'аб', 'ад', 'аж', 'але', 'б', 'без', 'бо', 'бы',
             'было', 'быў', 'быць', 'ва', 'вам', 'вас', 'вось', 'вы',
             'гэтага', 'гэтай', 'гэтую', 'гэты', 'гэтым', 'гэтыя',
             'да', 'дзе', 'для', 'ды', 'дык', 'ёй', 'ён', 'ёю', 'ж',
             'жа', 'з', 'за', 'і', 'ім', 'імі', 'іх', 'к', 'каб',
             'каго', 'калі', 'мае', 'мая', 'мне', 'мой', 'мы', 'мяне',
             'на', 'над', 'нам', 'нас', 'наш', 'не', 'небудзь', 'ну',
             'ні', 'нібы', 'па', 'пад', 'пра', 'праз', 'пры', 'раз',
             'са', 'сабе', 'сам', 'сама', 'свае', 'сваё', 'сваім',
             'сваіх', 'сваю', 'свой', 'сябе', 'табе', 'таго', 'тады',
             'так', 'такі', 'такія', 'такое', 'такой', 'там', 'таму',
             'тая', 'то', 'тое', 'той', 'толькі', 'туды', 'тут', 'ты',
             'тым', 'тых', 'тыя', 'у', 'ў', 'увесь', 'ужо', 'усе', 'усё',
             'усім', 'усю', 'хоць', 'хто', 'цябе', 'ці', 'чаго', 'чым',
             'што', 'я', 'яго', 'яе', 'як', 'якая', 'які', 'якім', 'якія',
             'якога', 'якое', 'якой', 'якую', 'яму', 'яна', 'яно', 'яны',
             'яшчэ', 'тую', 'гэтых', 'гэта', 'з-пад', 'такая', 'якіх',
             'й', 'ня', 'кг', 'см']
    ru_rm = ['автор', 'американский', 'армия', 'белый', 'близкий', 'более', 'больше', 'больше',
             'большой', 'борьба', 'бояться', 'брать', 'бывать', 'бывший', 'быстро', 'быть', 'важный',
             'вдруг', 'ведь', 'ведь', 'великий', 'верить', 'вернуться', 'вести', 'весь', 'вечер',
             'вещь', 'взгляд', 'взять', 'вид', 'видеть', 'власть', 'вместе', 'внимание', 'внутренний',
             'вода', 'военный', 'воздух', 'возможность', 'война', 'войти', 'вообще', 'вопрос',
             'вполне', 'впрочем', 'время', 'все', 'все', 'все-таки', 'всегда', 'вспомнить', 'встреча',
             'всякий', 'второй', 'выйти', 'высокий', 'выходить', 'где', 'главный', 'глаз', 'глядеть',
             'говорить', 'голова', 'голос', 'город', 'гость', 'государственный', 'государство',
             'готовый', 'гражданин', 'группа', 'давать', 'давно', 'даже', 'даже', 'далее', 'далекий',
             'данные', 'данный', 'дать', 'дверь', 'движение', 'девочка', 'девушка', 'действие',
             'действительно', 'делать', 'дело', 'день', 'деньги', 'держать', 'десять', 'деятельность',
             'директор', 'довольно', 'документ', 'долго', 'должен', 'доллар', 'дорога', 'дорогой',
             'достаточно', 'думать', 'его', 'единственный', 'если', 'ехать', 'ещё', 'её', 'ждать',
             'же', 'жена', 'женщина', 'живой', 'жизнь', 'жить', 'забыть', 'заметить', 'заниматься',
             'затем', 'зачем', 'здесь', 'земля', 'знать', 'значение', 'значит', 'и', 'игра', 'играть',
             'идея', 'идти', 'из', 'известный', 'или', 'именно', 'иметь', 'имя', 'иногда', 'иной',
             'институт', 'интерес', 'информация', 'искать', 'искусство', 'использование', 'использовать',
             'исследование', 'история', 'их', 'каждый', 'казаться', 'как', 'как', 'как-то', 'какой',
             'какой-то', 'картина', 'качество', 'квартира', 'класс', 'книга', 'ко', 'когда',
             'количество', 'комната', 'компания', 'конец', 'конечно', 'который', 'красный', 'кровь',
             'кроме', 'крупный', 'кстати', 'кто', 'кто-то', 'куда', 'купить', 'легкий', 'лежать', 'ли',
             'либо', 'лицо', 'лишь', 'лучший', 'любить', 'любовь', 'любой', 'маленький', 'мальчик',
             'материал', 'мать', 'машина', 'между', 'международный', 'местный', 'место', 'минута', 'мир',
             'мировой', 'мнение', 'многий', 'много', 'может', 'можно', 'молодой', 'момент', 'московский',
             'мочь', 'мужчина', 'наверное', 'надо', 'назвать', 'называть', 'найти', 'наконец', 'написать',
             'например', 'народ', 'настоящий', 'наука', 'находиться', 'начало', 'начальник', 'начать',
             'начаться', 'начинать', 'небо', 'небольшой', 'неделя', 'некоторый', 'нельзя', 'необходимый',
             'несколько', 'нет', 'нет', 'ни', 'ни', 'никакой', 'никогда', 'никто', 'ничто', 'новый',
             'нога', 'номер', 'ночь', 'нужно', 'нужный', 'об', 'оба', 'область', 'образ', 'образование',
             'общество', 'общий', 'объект', 'огромный', 'один', 'один', 'однако', 'оказаться', 'окно',
             'около', 'он', 'она', 'они', 'оно', 'опыт', 'опять', 'организация', 'основа', 'основной',
             'особенно', 'особый', 'оставаться', 'оставить', 'остаться', 'ответ', 'ответить', 'отвечать',
             'отец', 'открыть', 'относиться', 'отношение', 'очень', 'очередь', 'партия', 'первый', 'перед',
             'период', 'писать', 'письмо', 'пить', 'плечо', 'плохой', 'по', 'подобный', 'подойти',
             'подумать', 'позволять', 'пойти', 'пока', 'пока', 'показать', 'политика', 'политический',
             'полный', 'положение', 'получать', 'получить', 'помнить', 'помочь', 'помощь', 'понимать',
             'понять', 'попасть', 'порядок', 'поскольку', 'последний', 'посмотреть', 'поставить', 'потом',
             'потому', 'похожий', 'почему', 'почти', 'поэтому', 'появиться', 'правда', 'правило',
             'правительство', 'право', 'предложить', 'предприятие', 'представитель', 'представить',
             'представлять', 'президент', 'при', 'привести', 'приехать', 'прийти', 'прийтись', 'пример',
             'принимать', 'принцип', 'принять', 'приходить', 'причина', 'про', 'проблема', 'провести',
             'программа', 'продолжать', 'проект', 'производство', 'произойти', 'происходить', 'пройти',
             'просить', 'просто', 'простой', 'против', 'процесс', 'пусть', 'путь', 'пытаться', 'пять',
             'работать', 'равный', 'развитие', 'разговор', 'различный', 'разный', 'район', 'ранний',
             'рассказать', 'рассказывать', 'ребенок', 'результат', 'речь', 'решение', 'решить', 'роль',
             'российский', 'рубль', 'русский', 'рынок', 'ряд', 'рядом', 'самый', 'связь', 'сделать', 'себя',
             'сегодня', 'сейчас', 'семья', 'сердце', 'сидеть', 'сила', 'сильный', 'система', 'ситуация',
             'сказать', 'сколько', 'скорый', 'следовать', 'следующий', 'слишком', 'словно', 'слово',
             'случай', 'слушать', 'слышать', 'смерть', 'смотреть', 'смочь', 'смысл', 'сначала', 'снова',
             'со', 'собираться', 'собственный', 'событие', 'совершенно', 'совет', 'советский', 'современный',
             'совсем', 'создание', 'создать', 'состав', 'состояние', 'социальный', 'спать', 'спина',
             'спрашивать', 'спросить', 'сразу', 'среди', 'средство', 'срок', 'становиться', 'старый',
             'стать', 'статья', 'стена', 'стоить', 'сторона', 'стоять', 'страна', 'судьба', 'существовать',
             'счет', 'считать', 'также', 'театр', 'тело', 'тема', 'теперь', 'территория', 'тип', 'товарищ',
             'тогда', 'тоже', 'только', 'тот', 'точка', 'требовать', 'третий', 'три', 'труд', 'туда',
             'тяжелый', 'увидеть', 'удаться', 'уж', 'уже', 'узнать', 'уйти', 'улица', 'управление', 'уровень',
             'условие', 'успеть', 'утро', 'уходить', 'участие', 'федеральный', 'федерация', 'фильм',
             'характер', 'ходить', 'хороший', 'хорошо', 'хотеть', 'хотеться', 'хоть', 'хотя', 'целый',
             'цель', 'цена', 'центр', 'часто', 'часть', 'человек', 'человеческий', 'чем', 'через', 'черный',
             'четыре', 'число', 'читать', 'что', 'что', 'что-то', 'чтобы', 'чувство', 'чувствовать', 'чуть',
             'широкий', 'экономический', 'это', 'это', 'этот', 'являться', 'меня', 'хочу', 'эта', 'был',
             'твой', 'твоя', 'твою', 'него', 'нему']

    # выдаленне стоп-словаў
    words  = list(filterfalse(set(be_rm + ru_rm).__contains__, words))
    words = sorted(words, key=locale.strxfrm)
    return words

def cleen_foreign_words(text):
    """Выдаленне небеларускай лексікі, і некаторай з "клясычнага" правапісу
    """

    reguldict = [
            r'\b\w*?[^а-зй-шьыэюяіўёʼ\-\ ]\w*?\b',
            r'\b\w*?[ищъ]\w*?\b',
            r'\b\w*?[^злнсц]ь\w*?\b',
            r'\b\w*?[джртчш][еёюя]\w*?\b',
            r'\b\w*?[ёе][джртхчш][еёйюя]\w*?\b',
            r'\b\w*?[еою][джртчш][еёюя]\w*?\b',
            r'\b\w*?[о][бвджзйлмпрстфхцчш][ёйо]\w*?\b',
            r'\b\w*?ч[зфш]\w*?\b',
            r'\b\w*?в[бвгджзкмнпрстфхцчш]\w*?\b',
            r'\b\w*?[вжзклнпсфх]ый\b',
            r'\b\w*?о[^дгн]о\w*?\b',
            r'\b\w+?ого\b',
            r'\b\w*?(ов|нно)\b',
            r'\b\w*?\-+?[аоэ]\-+?\w*?\b',
            r'\b\w*?[аеоуэюя]ет\b'
            ]

    regex = re.compile('|'.join(reguldict))
    text = regex.sub(' ', text)
    return text

def get_words_freq(words):
    """Падлік частаты ўжывання словаформаў
    """
    words_freq = {}
    for word in words:
        if word in words_freq:
            words_freq[word] = words_freq[word] + 1
        else:
            words_freq[word] = 1
    words_freq_sorted = sorted(words_freq.items(), key=lambda item:(-item[1], locale.strxfrm(item[0])))
    return words_freq, words_freq_sorted

def file_oper(text, file_result):

    words = get_words(text)
    words_freq, words_freq_sorted = get_words_freq(words)
    with open(file_result,"w", encoding='utf-8') as file_f:
        file_f.write(f'Агульная колькасць слоў: {str(len(words)).rjust(12)}\n')
        file_f.write(f'Колькасць унікальных слоў: {str(len(words_freq)).rjust(10)}\n\n')
        file_f.write(f'Частата выкарыстання:\n\n')

        for j in words_freq_sorted:
            line = str(str(j[1]).rjust(5)) + '   ' + (j[0].ljust(len(j)) + '\n')
            file_f.writelines(line)

def input_filename():
    """Увядзіце імя файлу з тэкстам для падліку частаты ўжывання словаформаў.
       Вывад вынікаў у файл {inputfilename}.freq.txt.
    """
    try:
        filename = input('Імя файлу з неапрацаваным тэкстам: ')
        with open(filename, encoding="utf8") as textfile:
            text = textfile.read()
        file_result = (f'{filename}.freq.txt')

        file_oper(text, file_result)

        print(f'Success! Вынікі запісаныя ў файл {file_result}.')

    except FileNotFoundError:
        print(f'Памылка! Такога файлу - "{filename}" не існуе. Праграма спынена!')

def main():
    """Апрацоўка імя файлу з тэкстам для падліку з каманднага радку.
       Вывад вынікаў у файл {inputfilename}.freq.txt.
    """
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as textfile:
                text = textfile.read()

            file_result = (f'{sys.argv[1]}.freq.txt')

            file_oper(text, file_result)

            print(f'Success! Вынікі запісаныя ў файл {file_result}.')

        except FileNotFoundError:
            print(f'Файл "{sys.argv[1]}" не знодзены.\nПадайце слушнае імя файлу ў наступным радку:')
            input_filename()

    else:
        print(f'Запуск праграмы без аргументаў.\nПадайце слушнае імя файлу ў наступным радку:')
        input_filename()

if __name__ == "__main__":
    main()

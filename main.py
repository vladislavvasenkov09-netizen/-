# викторина Quiz-Master по самым разным темам

from pathlib import Path
import json
import random
from time import sleep
from datetime import datetime
from sys import exit

path_quest = Path('questions.json')
path_user = Path('user.json')

# кол-вол очков за правильные вопросы на все категории
points_py = 0
points_geo = 0
points_inf = 0

class Question:
    """В обьекте класса хранится только один вопрос"""

    def __init__(self, id, text, options, correct_answer, category):
        self.id = id
        self.text = text
        self.options = options
        self.correct_answer = correct_answer
        self.category = category

    def check_answer(self):
        """Проверка ответов"""

        try:
            answer = int(input('\nВаш ответ: '))
        except ValueError:
            print('Нужно вводить число!')
            print('Штраф! Вопрос пропускаем!')
            sleep(1)
            return

        if answer == self.correct_answer:
            print("Правильно, +1 балл, идем дальше!")
            sleep(1)
            return True
        else:
            print('Неверно!')
            sleep(1)
            return False

    def show_question(self, order):
        """Вывод одного вопроса"""

        print(f'\nКатегория: {self.category}')
        print(f'Вопрос {order} из 10')
        print(f'\n{self.text}')
        num = 1
        for option in self.options:
            print(f'{num}. {option}')
            num += 1

class QuizGame:
    """Вся работа 'под капотом' игры"""
    def __init__(self):
        pass

    def calculate_result(self, points):
        """Подсчет всех результатов и вывод"""

        print('\nРЕЗУЛЬТАТЫ ЗА ЭТОТ РАУНД:')
        print(f'\tОтвечено правильно на {points} ответов из 10.')
        print(f'\tТочность: {points * 10}%')

        if points <= 3:
            print('\nУжасно, тебе стоит лучше учиться.')
        elif points <= 5:
            print('\nПлохо, но с некоторыми заданиями ты справляешься!')
        elif points <= 7:
            print('\nДостаточно хорошо, ты достаточно умён, но есть куда расти!')
        elif points <= 9:
            print('\nХорошо! Ты почти полностью справился!')
        else:
            print('\nОтлично! Ты просто гений!')

        sleep(2)

    def start(self, p_py, p_geo, p_inf):
        """Запуск раунда викторины"""

        points = 0
        order = 1

        categorys = [
            "1. Python",
            "2. География",
            "3. Информатика"
        ]

        print('Категории:')
        for category in categorys:
            print(f'\t{category}')

        try:
            answer_category = int(input('\nВыберите категорию вопросов: '))
        except ValueError:
            print('Нужно вводить число!')
            print('Попробуйте еще раз.')
            sleep(1)
            return p_py, p_geo, p_inf

        # читаем файл один раз
        contents = path_quest.read_text(encoding='utf-8')
        questions_list = json.loads(contents)

        if answer_category == 1:
            target_category = 'Python'
        elif answer_category == 2:
            target_category = 'География'
        elif answer_category == 3:
            target_category = 'Информатика'
        else:
            print('Такой категории нет!')
            return p_py, p_geo, p_inf

        filtered_questions = [i for i  in questions_list if i.get('category') == target_category]

        questions_random = random.sample(filtered_questions, k=len(filtered_questions))

        for q_data in questions_random:
            question = Question(**q_data)
            question.show_question(order)

            if question.check_answer():
                if answer_category == 1:
                    p_py += 1
                elif answer_category == 2:
                    p_geo += 1
                elif answer_category == 3:
                    p_inf += 1
                points += 1

            order += 1

        self.calculate_result(points)

        return p_py, p_geo, p_inf

    def safe_record(self, answer_safe, string):
        if answer_safe == 1:
            # если файла нет или он пуст то прост выводим рекорды текущей игры
            if path_user.exists() == False or path_user.stat().st_size == 0:
                print('Файла с рекордами не существует! Данные берутся из текущей игры.')
                print(f'\nПравильных ответов в категории Python: {points_py}')
                print(f'Правильных ответов в категории География: {points_geo}')
                print(f'Правильных ответов в категории Информатика: {points_inf}')
        
            # если же файл есть и в нем что то есть то подгружаем все в словарь и выводим
            elif path_user.exists() and path_user.stat().st_size > 0:       
                read = path_user.read_text()
                load = json.loads(read)
        
                print(f'\nДата последних рекордов: {load['date']}')
                for key, value in load.items():
                    if key != 'date':
                        print(f'Категория: {key}. Кол-во правильных ответов: {value}')
        
        # ну а тут сохранения именно НОВЫХ рекордов
        elif answer_safe == 2:
            user = {
                'date': string,
                'Python': points_py,
                'География': points_geo,
                'Информатика': points_inf
            }

            # если файла не существует или он пуст то автоматом создаем его и записываем рекорды
            if path_user.exists() == False or path_user.stat().st_size == 0:
                dump = json.dumps(user, ensure_ascii=False, indent=4)
                path_user.write_text(dump, encoding='utf-8')
                print('\nПервые рекорды успешно сохранены!')

            else:
                read = path_user.read_text()
                load = json.loads(read)

                record_beaten = False

                if points_py > load.get('Python', 0):
                    load['Python'] = points_py
                    record_beaten = True
                if points_geo > load.get('География', 0):
                    load['География'] = points_geo
                    record_beaten = True
                if points_inf > load.get('Информатика', 0):
                    load['Информатика'] = points_inf
                    record_beaten = True
                if record_beaten:
                    load['date'] = string

                    # записываем весь обновленный словарь
                    dump = json.dumps(load, ensure_ascii=False, indent=4)
                    path_user.write_text(dump, encoding='utf-8')
                    print('\nЛучшие рекорды сохранены!')

                    print(f'\nДата актульных рекордов: {load['date']}')
                    for key, value in load.items():
                        if key != 'date':
                            print(f'Категория: {key}. Кол-во правильных ответов: {value}')
                else:
                    print('\nРекорды текущей игры меньше или равны прошлым.')
        
        else:
            print('Такой операции не существует!')
            return

    def add_quest(self, text, options, correct_answer):
        categorys = [
            "1. Python",
            "2. География",
            "3. Информатика"
        ]

        print('\nКатегории:')
        for categor in categorys:
            print(f'\t{categor}')

        try:
            answer_category = int(input('К какой категории отнести вопрос? '))
        except ValueError:
            print('\nНужно вводить число!"')
            print('Попробуйте еще раз!')
            return

        contents = path_quest.read_text(encoding='utf-8')
        load = json.loads(contents)

        if answer_category == 1:
            question = {
                'id': random.randint(30, 100),
                'text': text,
                'options': options,
                'correct_answer': correct_answer,
                'category': 'Python'
            }

            load.append(question)
            questions = json.dumps(load, ensure_ascii=False, indent=4)
            path_quest.write_text(questions, encoding='utf-8')

        elif answer_category == 2:
            question = {
                'id': random.randint(30, 100),
                'text': text,
                'options': options,
                'correct_answer': correct_answer,
                'category': 'География'
            }

            load.append(question)
            questions = json.dumps(load, ensure_ascii=False, indent=4)
            path_quest.write_text(questions, encoding='utf-8')

        elif answer_category == 3:
            question = {
                'id': random.randint(30, 100),
                'text': text,
                'options': options,
                'correct_answer': correct_answer,
                'category': 'Информатика'
            }

            load.append(question)
            questions = json.dumps(load, ensure_ascii=False, indent=4)
            path_quest.write_text(questions, encoding='utf-8')

        print('\nВопрос успешно сохранен!')
        sleep(2)

try:                    
    while True:
        # обьект всей игры
        game = QuizGame()
        # главный экран
        print('\n====== QUIZ-GAME ======')

        main_screen = [
            '\n1. Начать викторину',
            "2. Просмотреть категории",
            "3. Просмотреть и сохранить рекорды",
            "4. Добавить вопрос",
            "0. Выход"
        ]
        for screen in main_screen:
            print(screen)

        # обработка ошибок и работа всей игры
        try:
            answer_main = int(input('\nВведите операцию: '))
        except ValueError:
            print('\nНужно вводить число!')
            print('Попробуйте еще раз!')
            continue

        # один раунд викторины
        if answer_main == 1:
            points_py, points_geo, points_inf = game.start(points_py, points_geo, points_inf)

        # вывод всех категорий вопросов
        elif answer_main == 2:
            categorys = [
                "1. Python",
                "2. География",
                "3. Информатика"
            ]
        
            print('Категории:')
            for category in categorys:
                print(f'\t{category}')

            input('\nНажмите Enter чтобы вернутся в главное меню...')

        # сохранение рекордов в файл
        elif answer_main == 3:
            # сохраняем текущее время в переменных
            datetime_record = datetime.now()
            string = datetime_record.strftime('%d.%m.%Y %H:%M')

            # два пути что бы было более логично
            print('\nЧто вам нужно?')
            print('\t1. Просмотреть прошлые рекорды')
            print('\t2. Сохранить рекорды')

            try:
                answer_safe = int(input('\nОтвет: '))
            except ValueError:
                print('Нужно вводить число!')
                sleep(2)
                continue

            game.safe_record(answer_safe, string)
        
            input('\nНажмите Enter чтобы вернутся в главное меню...')

        elif answer_main == 4:
            text = input('\nВведите текст вопроса: ')

            try:
                num_options = int(input('\nСколько вариантов ответа у вас будет? '))
            except ValueError:
                print('\nНужно вводить число!')
                print('Попробуйте еще раз!')
                sleep(2)
                continue
            options = []

            for i in range(num_options):
                option = input('\tВведите вариант ответа: ')
                options.append(option)

            try:
                correct_answer = int(input('\nВведите номер правильного ответа: '))
            except ValueError:
                print('\nНужно вводить число!')
                continue

            if correct_answer > len(options):
                print('Правильный ответ больше кол-ва вариантов!')
                sleep(2)
                continue
            elif correct_answer < 1:
                print('Правильный ответ меньше кол-ва вариантов')
                sleep(2)
                continue

            game.add_quest(text, options, correct_answer)

        # выход
        elif answer_main == 0:
            print('\nУвидимся в следующий раз!')
            break

        else:
            print('Такой операции не существует!')
            sleep(2)

except KeyboardInterrupt:
    print('\nРабота викторины была экстренно прервана!')
    exit()

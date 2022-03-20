#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import pathlib
import logging

"""
Выполнить индивидуальное задание 1 лабораторной работы 2.19, добавив возможность работы
с исключениями и логгирование.
"""

class MyStudents:
    def __init__(self, line):
        self.line = line

    def select_student(self, students):
        """
        Выбрать cтудентов с заданной оценкой.
        """
        print(self.line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(self.line)
        # Инициализировать счетчик.
        count = 0
        # Проверить сведения студентов из списка.
        for student in students:
            grade = list(map(int, student.get('grade', '').split()))
            if sum(grade) / max(len(grade), 1) >= 4.0:
                count += 1
                print(
                    '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                        count,
                        student.get('name', ''),
                        student.get('group', ''),
                        student.get('grade', 0)
                    )
                )
        print(self.line)
        if count == 0:
            print("Студенты с баллом 4.0 и выше не найдены.")
        print(self.line)

    def display(self, students):
        """
        Отобразить список студентов.
        """
        print(self.line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"))
        print(self.line)
        for idx, student in enumerate(students, 1):
            print(
                '| {:<4} | {:<30} | {:<20} | {:<15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('grade', 0)
                )
            )
        print(self.line)

    def add_student(self, students, name, group, grade):
        students.append(
            {
                'name': name,
                'group': group,
                'grade': grade,
            }
        )
        return students

    def save_student(self, file_name, students):
        with open(file_name, "w", encoding="utf-8") as file_out:
            json.dump(students, file_out, ensure_ascii=False, indent=4)
        logging.info(f"Данные сохранены в файл: {file_name}")

    def load_student(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f_in:
            return json.load(f_in)


def main(command_line=None):
    logging.basicConfig(
        filename='students.log',
        level=logging.INFO
    )

    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    st = MyStudents(line)

    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
    )
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser]
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
    )
    add.add_argument(
        "-g",
        "--group",
        type=int,
        action="store"
    )
    add.add_argument(
        "-gr",
        "--grade",
        action="store",
        required=True,
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
    )
    args = parser.parse_args(command_line)

    is_dirty = False
    name = args.filename
    home = pathlib.Path.cwd() / name

    try:
        students = st.load_student(home)
        logging.info("Файл найден")
    except FileNotFoundError:
        students = []
        logging.warning("Файл не найден, создается новый")

    if args.command == "add":
        students = st.add_student(students, args.name, args.group, args.grade)
        is_dirty = True
        logging.info("Добавлен студент")
    elif args.command == 'display':
        st.display(students)
        logging.info("Отображён список студентов")
    elif args.command == "select":
        st.select_student(students)
        logging.info("Выбраны студенты с нужными оценками")

    if is_dirty:
        st.save_student(args.filename, students)


if __name__ == '__main__':
    main()
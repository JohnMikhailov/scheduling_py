from src import input_output
import random


class Generator:

    def __init__(self, path):
        self.settings = input_output.read(path)
        self.professors = tuple([i + 1 for i in range(self.settings[0])])
        self.classes = tuple([i + 1 for i in range(self.settings[1])])
        self.classrooms = tuple([i + 1 for i in range(self.settings[2])])
        self.groups = tuple([i + 1 for i in range(self.settings[3])])
        self.groups_amount = self.settings[3]
        self.classes_in_each_group = self.settings[4]
        self.classes_per_day_max = self.settings[5]
        self.classes_each_day_max = self.settings[6]
        self.days = tuple([day + 1 for day in range(self.settings[9])])

        self.professor_min_classes = self.settings[7]
        self.professor_max_classes = self.settings[8]
        self.days_max = self.settings[9]
        self.hours = {}

        self.classes_type = {}

        self.evaluation_time = {}
        self.evaluation_place = {}
        self.group_classes = {}  # ключ - номер группы, значение - список предметов

        self.generate_inputs()

    def generate_evaluation_time(self):  # можно упростить
        days = tuple([day for day in range(self.days_max)])  # воскресенье (7й день) - выходной
        pairs = tuple([i for i in range(self.classes_each_day_max)])  # пары; максимум = 8
        for professor in self.professors:
            day_eval = []
            for _ in days:
                pair_eval = []
                for _ in pairs:
                    pair_eval.append(round(random.uniform(0, 1), 1))
                day_eval.append(tuple(pair_eval))
            self.evaluation_time[professor] = tuple(day_eval)
        # в результате получается так: evaluation_time[1][2][3] - оценка преподавателя 1 для третей пары во вторник

    def generate_evaluation_place(self):
        for professor in self.professors:
            class_eval = []
            for _ in self.classes:
                classroom_eval = []
                for _ in self.classrooms:
                    classroom_eval.append(round(random.uniform(0, 1), 1))
                class_eval.append(tuple(classroom_eval))
            self.evaluation_place[professor] = tuple(class_eval)
        # в результате поучается так: evaluation_place[1][2][3] - оценка преподавателя 1 для проведения лекции
        # (практики) 2 в аудитории 3

    def generate_group_classes(self):  # предметы должны повторяться!
        borders = range(0, len(self.classes) + 1, self.classes_in_each_group)
        self.group_classes = {
            group: self.classes[borders[number-1]:borders[number]]
            for number, group in enumerate(self.groups, 1)
        }

    #  скорее всего, это избыточно
    def generate_classes_type(self):  # True - практика, False - лекция
        self.classes_type = {
            class_: random.choice([True, False])
            for class_ in self.classes
        }

    # возможно, избыточный метод
    def generate_hours(self):  # назначение часов работы каждому преподавателю
        self.hours = {
            professor: random.randint(self.professor_min_classes, self.professor_max_classes)
            for professor in self.professors
        }

    def generate_inputs(self):
        self.generate_evaluation_time()
        self.generate_evaluation_place()
        self.generate_group_classes()
        self.generate_classes_type()

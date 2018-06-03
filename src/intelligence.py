import random as rm
import itertools
from src.generator import Generator

'''
                                ******************** УСЛОВИЯ ********************

                        1 У каждой группы ВСЕ предметы различны
                        2 НЕТ потоковых лекций (следует из 1)
                        3 Лекция по предмету N и практика по предмету N - два разных предмета (мотивирую тем,
                          что лекция и практика проводятся в различное время и в различных местах)
                        4 НЕТ ситуаций, когда один преподаватель ведет у одной и той же гурппы более
                        одного занятия в день
'''


class Engine:

    def __init__(self, data: Generator):
        self.__data = data

    def __calculate_classes_per_day_max(self, gc):
        return self.__data.classes_per_day_max if len(gc) >= self.__data.classes_per_day_max else len(gc)

    def __time(self, temp_classes):
        first_class = rm.randint(1, self.__data.classes_each_day_max - len(temp_classes))
        last_class = first_class + len(temp_classes)
        return tuple(range(first_class, last_class))

    def __professors(self, time):
        return tuple(rm.sample(self.__data.professors, len(time)))

    def __classrooms(self, time):
        return tuple(rm.sample(self.__data.classrooms, len(time)))

    def __distribute_data(self, group):
        """раcпределяет информацию для группы group на каждый день"""
        """{группа: {день: ((предмет1, предмет2), (первая_пара, вторая_пара), (препод1, препод2)"""
        """(аудитория1, аудитория2))}}"""
        dist = {}
        group_classes = set(self.__data.group_classes[group])
        days = list(self.__data.days)
        rm.shuffle(days)
        classes_p_day_min = len(group_classes) // self.__data.days_max  # столько в среднем будет каждый день
        for day in days:
            classes_p_day_max = self.__calculate_classes_per_day_max(group_classes)
            if classes_p_day_max <= classes_p_day_min:  # предметы закончились, можно выходить
                break
            classes = tuple(rm.sample(group_classes, rm.randint(classes_p_day_min, classes_p_day_max)))
            group_classes = group_classes.difference(set(classes))
            time = self.__time(classes)
            professors = self.__professors(time)
            classrooms = self.__classrooms(time)
            dist[day] = (classes, time, professors, classrooms)
        return dist

    def scheduling(self):
        """ключ - номер группы, значение - словарь с расписанием занятий для гурппы на неделю"""
        return {
            group: self.__distribute_data(group)
            for group in self.__data.groups
        }

    def mutate(self, schedule: dict):
        new_schedule = {}
        for group, day_sch in schedule.items():
            temp = {}
            for day, sch in day_sch.items():
                classes = list(sch[0])
                professors = list(sch[2])
                places = list(sch[3])
                rm.shuffle(classes)
                rm.shuffle(professors)
                rm.shuffle(places)
                classes = tuple(classes)
                professors = tuple(professors)
                places = tuple(places)
                temp[day] = classes, sch[1], professors, places
            new_schedule[group] = temp
        return new_schedule

    def is_valid(self, schedule: dict):
        for group_a, group_b in itertools.combinations(self.__data.groups, 2):
            in_common_days = set(schedule[group_a].keys()).intersection(set(schedule[group_b].keys()))
            for day in in_common_days:
                if self.__have_collision(schedule[group_a][day], schedule[group_b][day]):
                    return False
        return True

    @staticmethod
    def __have_collision(group_a: tuple, group_b: tuple):
        group_a_sel = set(zip(group_a[1], group_a[2], group_a[3]))
        group_b_sel = set(zip(group_b[1], group_b[2], group_b[3]))
        return True if group_a_sel.intersection(group_b_sel) else False

    def evaluation(self, schedule: dict):
        return self.__evaluation_time(schedule) + self.__evaluation_place(schedule)

    def __evaluation_time(self, schedule: dict):
        estimate = 0
        for group_day_sch in schedule.values():
            for day in group_day_sch:
                for time, professor in zip(group_day_sch[day][1], group_day_sch[day][2]):
                    estimate += self.__data.evaluation_time[professor][day - 1][time - 1]
        return estimate

    def __evaluation_place(self, schedule: dict):
        estimate = 0
        for group_day_sch in schedule.values():
            for i in group_day_sch.values():
                for class_, professor, place in zip(i[0], i[2], i[3]):
                    estimate += self.__data.evaluation_place[professor][class_ - 1][place - 1]
        return estimate

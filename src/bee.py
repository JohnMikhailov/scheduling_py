from src.intelligence import Engine


class Bee:

    def __init__(self, engine: Engine):
        self.__engine = engine
        self.schedule = None
        self.value = None

    def search_schedule(self):  # поиск расписания
        self.schedule = self.__engine.scheduling()

    def estimate(self):
        self.value = self.__engine.evaluation(self.schedule)

    def __extract(self):  # модификация расписания
        return self.__engine.mutate(self.schedule)

    def is_valid(self):  # проверка расписания
        return self.__engine.is_valid(self.schedule)

    def mutate_schedule(self):  # генерирует новые расписания из текущего а количесвте workers
        return self.__engine.mutate(self.schedule)

from src.bee import Bee
from src.generator import Generator
from src.intelligence import Engine

'''

        This file contains modified bee colony algorithm.
        Specifically: input parameters - inputs coming from parameters, not from file

'''


class BCA:

    def __init__(self, description, path_to_settings):
        self.description = description
        self.path_to_generator = path_to_settings
        data = Generator(self.path_to_generator)
        self.intelligence = Engine(data)

    def bca(self, *args):
        best_amount = args[3]
        steps = args[0]
        scouts = [Bee(self.intelligence) for _ in range(args[1])]
        workers = [Bee(self.intelligence) for _ in range(args[2])]
        hive = []
        for step in range(steps):
            for scout in scouts:
                scout.search_schedule()  # скауты находят решения
                scout.estimate()
            solutions = []
            for scout in range(best_amount):
                for worker in workers:
                    worker.schedule = scouts[scout].mutate_schedule()  # рабочие пчелы обрабатывают решения
                    worker.estimate()
                    solutions.append(worker)
            valid = [solution for solution in solutions if solution.is_valid()]  # филтрация решений
            valid.sort(key=lambda x: x.value, reverse=True)
            if len(hive) == 0:
                hive = valid
            n = len(hive) if len(hive) <= len(valid) else len(valid)
            for i in range(n):
                if hive[i].value < valid[i].value:
                    hive[i] = valid[i]
        return [(hive[i].schedule, hive[i].value) for i in range(len(hive) // args[3])]

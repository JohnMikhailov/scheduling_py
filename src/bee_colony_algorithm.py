from src.bee import Bee
from src.generator import Generator
from src.intelligence import Engine
from src import input_output


def __collect_data(bca_inputs='bee_colony_inputs.txt', generator_inputs='settings.txt'):
    settings = input_output.read(bca_inputs)
    data = Generator(generator_inputs)
    intelligence = Engine(data)
    scouts = [Bee(intelligence) for _ in range(settings[0])]
    workers = [Bee(intelligence) for _ in range(settings[1])]
    steps = settings[2]
    hive = []
    return steps, scouts, workers, hive


def bca(bca_inputs='bee_colony_inputs.txt', generator_inputs='settings.txt'):
    steps, scouts, workers, hive = __collect_data(bca_inputs, generator_inputs)
    for step in range(steps):
        for scout in scouts:
            scout.search_schedule()  # скауты находят решения
            scout.estimate()
        solutions = []
        for scout in scouts:
            for worker in workers:
                worker.schedule = scout.mutate_schedule()  # рабочие пчелы обрабатывают решения
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
    return [(hive[i].schedule, hive[i].value) for i in range(len(hive) // 5)]

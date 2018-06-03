def read(input_file):
    with open(input_file, 'r') as input_file:
        input_ = filter(lambda x: x.isdecimal(), input_file.read().split())
    return tuple(map(int, input_))
#

def write(schedule, output_file='output.txt'):
    with open(output_file, 'w') as output_file:
        for group in schedule:
            output_file.write('\n' + 'Группа ' + str(group) + '\n')
            output_file.write('\n')
            for day in schedule[group]:
                output_file.write(('Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')[day] + ': ' + '\n')
                for i in zip(schedule[group][day][0], schedule[group][day][1], schedule[group][day][2],
                             schedule[group][day][3]):
                    output_file.write(f'{i[1]}-я Пара: Предмет {i[0]}, Преподаватель {i[2]}, Аудитория {i[3]}' + '\n')
                output_file.write('\n')



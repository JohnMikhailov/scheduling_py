def __get_day_name(number):
    return ('Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')[number]


def print_like_group_day_schedule(schedule):
    for group in schedule:
        print('\n'+'Группа '+str(group)+' '+'\n')
        for day in schedule[group]:
            print(__get_day_name(day) + ': ' + '\n')
            for i in zip(schedule[group][day][0], schedule[group][day][1], schedule[group][day][2], schedule[group][day][3]):
                __description(i)
            print()


def __description(i):
    print('{}-я Пара: Предмет {}, Преподаватель {}, Аудитория {}'.format(i[1], i[0], i[2], i[3]))
#
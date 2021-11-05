from datetime import datetime

def func_for_decor(path):
    def decor(my_function):
        def log_writer(*args, **kwars):
            time_start = str(datetime.today())
            func_time_start_ = time_start.split('.')
            func_time_start = str(func_time_start_[0])
            result = my_function(*args, **kwars)
            time_end = str(datetime.today())
            func_time_end_ = time_end.split('.')
            func_time_end = str(func_time_end_[0])
            func_name = my_function.__name__
            arguments_1 = str(args)
            arguments_2 = str(kwars)
            log = func_time_start + '\n' + func_name + '\n' + arguments_1 + '\n' + arguments_2 + '\n' + func_time_end + '\n' + '\n'
            with open(path, "a") as f:
                f.write(log)
            return result
        return log_writer
    return decor

@func_for_decor('C:/Users/VedNA/PycharmProjects/pythonProject/decorators/loggs.txt')

def define_your_star(day: object, month: object) -> object:
    if month == 'январь':
      if day in range(1, 20):
        print("козерог")
      else:
        print('водолей')
    elif month == 'февраль':
      if day in range(1, 20):
        print('водолей')
      else:
        print('рыбы')
    elif month == 'март':
      if day in range(1, 21):
        print('рыбы')
      else:
        print('овен')
    elif month == 'апрель':
      if day in range(1, 21):
        print('овен')
      else:
        print('телец')
    elif month == 'май':
      if day in range(1, 21):
        print('телец')
      else:
        print('близнецы')
    elif month == 'июнь':
      if day in range(1, 22):
        print('близнецы')
      else:
        print('рак')
    elif month == 'июль':
      if day in range(1, 23):
        print('рак')
      else:
        print('лев')
    elif month == 'август':
      if day in range(1, 23):
        print('лев')
      else:
        print('девы')
    elif month == 'сентябрь':
      if day in range(1, 23):
        print('девы')
      else:
        print('весы')
    elif month == 'октябрь':
      if day in range(1, 23):
        print('весы')
      else:
        print('скорпион')
    elif month == 'ноябрь':
      if day in range(1, 22):
        print('скорпион')
      else:
        print('стрелец')
    else:
      if day in range(1, 21):
        print('стрелец')
      else:
        print('козерог')
    return day

if __name__ == '__main__':
    print('Введите день')
    my_day = int(input())

    print('Введите месяц')
    my_month = input()
    define_your_star(my_day, my_month)
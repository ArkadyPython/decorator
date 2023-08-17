import os
import datetime


def logger(path):

    def __logger(old_f):
        def new_function(*args, **kwargs):
            datet = datetime.datetime.now()
            name = old_f.__name__
            arg = f'{args}, {kwargs}'
            result = old_f(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                cont = f'{datet}\n{name}\n{arg}\n{result}\n'
                file.writelines(cont)
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world()
        result = summator(2, 2)
        assert isinstance(result, int)
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path)

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content


if __name__ == '__main__':
    test_2()
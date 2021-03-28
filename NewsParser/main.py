import sys
from time import time
from DataSource.from_url_data_source import FromUrlDataSource
from Core.parse_algorithm import ParseAlgorithm
from Output.file_output import FileOutput

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Введено неверное кол-во параметров. Необходимо ввести 1 параметр: URL")
        raise SystemExit(-1)

    time_start = time()
    url = sys.argv[1]

    request = FromUrlDataSource(url=url).get_data()
    if not request:
        raise SystemExit(-2)

    parse_result = ParseAlgorithm(request=request).parse()
    file_output = FileOutput(text=parse_result, url=url).generate_output()

    print("Done!")
    print(f"Время выполнения: {time() - time_start} сек")

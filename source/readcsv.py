import pandas as pd
from pathlib2 import Path

class ReadCsvData():

    def __init__(self, file_path):
        self.__file_path = file_path

    @property
    def file_path(self):
        return self.__file_path

    def replace_none_with_empty(self):
        df = Path(r"%s" % self.__file_path)

        data = df.read_text()
        data = data.replace("brak", "")
        data = data.replace('"""', '"')
        data = data.replace('"brak"', "")

        df.write_text(data)

    def read_schedule_csv(self):
        df = pd.read_csv(r"%s" % self.__file_path,
            delimiter = ",",
            usecols = ["Typ", "Tytuł", "Uwaga", "Pierwszy dzień", "Ostatni dzień", "Ogłoszony początek", "Ogłoszony koniec", "Miejsce"],
            dtype = None)
        
        return df
from datetime import datetime, timedelta
import pandas as pd
from pathlib2 import Path


def replace_none_with_empty():
    df = Path(r"source/events.csv")

    data = df.read_text()
    data = data.replace("brak", "")

    df.write_text(data)

replace_none_with_empty()

df = pd.read_csv(r"source/events.csv",
    delimiter = ",",
    usecols = ["Typ", "Tytuł", "Uwaga", "Pierwszy dzień", "Ostatni dzień", "Ogłoszony początek", "Ogłoszony koniec", "Miejsce"],
    dtype = None)

class_type_list = df["Typ"].values.tolist()
subject_list = df["Tytuł"].values.tolist()
notes_list = df["Uwaga"].values.tolist()
start_days = df["Pierwszy dzień"].values.tolist()
end_days = df["Ostatni dzień"].values.tolist()
start_time = df["Ogłoszony początek"].values.tolist()
end_time = df["Ogłoszony koniec"].values.tolist()
location = df["Miejsce"].values.tolist()

current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
current_date_str = datetime.now().strftime("%d/%m/%Y")
current_time = datetime.now()
current_date = datetime.strptime(current_date_str, "%d/%m/%Y")
tomorrow_str = datetime.strftime(current_time + timedelta(days=1, hours=10), "%d/%m/%Y")
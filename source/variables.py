from datetime import datetime, timedelta
from .readcsv import *


rc1 = ReadCsvData("source/events.csv")

rc1.replace_none_with_empty()
df = rc1.read_schedule_csv()

class_type_list = df["Typ"].values.tolist()
subject_list = df["Tytuł"].values.tolist()
start_days = df["Pierwszy dzień"].values.tolist()
end_days = df["Ostatni dzień"].values.tolist()
start_time = df["Ogłoszony początek"].values.tolist()
end_time = df["Ogłoszony koniec"].values.tolist()
location = df["Miejsce"].values.tolist()

current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
current_date_str = datetime.now().strftime("%d/%m/%Y")
current_time = datetime.now()
current_date = datetime.strptime(current_date_str, "%d/%m/%Y")
tomorrow_time_str = datetime.strftime(
    current_time + timedelta(days=1, hours=10), "%d/%m/%Y"
)

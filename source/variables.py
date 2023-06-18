from datetime import datetime, timedelta

current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
current_date_str = datetime.now().strftime("%d/%m/%Y")
current_time = datetime.now()
current_date = datetime.strptime(current_date_str, "%d/%m/%Y")
tomorrow_time_str = datetime.strftime(
    current_time + timedelta(days=1, hours=10), "%d/%m/%Y"
)

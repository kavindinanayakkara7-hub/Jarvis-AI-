import datetime
import psutil


def get_system_info():

    cpu = psutil.cpu_percent(
        interval=1
    )

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    return (
        f"CPU usage is {cpu:.0f} percent. "
        f"Memory usage is {memory.percent:.0f} percent. "
        f"Disk usage is {disk.percent:.0f} percent."
    )


def get_current_time():

    now = datetime.datetime.now()

    return (
        "The current time is "
        + now.strftime("%I:%M %p")
    )


def get_current_date():

    now = datetime.datetime.now()

    return (
        "Today is "
        + now.strftime("%A, %B %d, %Y")
    )
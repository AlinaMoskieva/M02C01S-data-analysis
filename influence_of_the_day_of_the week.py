import csv
from datetime import datetime
import matplotlib.pyplot as plt

DIAGRAM_TITLE = "Влияние дня недели на вероятность отказа от корзины"
HORIZONTAL_TITLE = "Вероятность отказа"
VERTICAL_TITLE = "Дни недели"
PATH_TO_DATA = "files/train.csv"

DIAGRAM_NAME = "graphs/influence_of_the_day_of_the week"

IMAGE_FORMAT = "png"
COLOR = "#B0E0E6"
MARKER_SIZE = 10


def set_diagram_titles(ax):
    ax.set_title(DIAGRAM_TITLE)
    ax.set_xlabel(HORIZONTAL_TITLE)
    ax.set_ylabel(VERTICAL_TITLE)


def scatterplot(x_data, y_data):
    _, ax = plt.subplots()

    ax.scatter(x_data, y_data, s=MARKER_SIZE, color=COLOR)

    set_diagram_titles(ax)
    plt.savefig("{}".format(DIAGRAM_NAME), fmt=IMAGE_FORMAT)


def weekday(date):
    return datetime.strptime(date, "%d/%m/%Y").weekday()


def csv_reader(file_obj):
    reader = csv.reader(file_obj, delimiter=" ")

    week_days = []
    cancel_flags = []
    prev = 1

    for row in reader:
        s = " ".join(row)
        splitted_rows = s.split(",")
        order_num = splitted_rows[5]

        if order_num != prev:
            week_days.append(weekday(splitted_rows[2]))

            cancel_flags.append(splitted_rows[9])
        prev = order_num

    scatterplot(cancel_flags, week_days)


if __name__ == "__main__":
    with open(PATH_TO_DATA, "r", encoding="ISO-8859-1") as f_obj:
        csv_reader(f_obj)

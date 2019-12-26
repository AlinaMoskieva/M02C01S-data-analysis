import csv
from collections import Counter
import matplotlib.pyplot as plt

DIAGRAM_TITLE = "Зависимость отказа от количества заказываемых единиц"
HORIZONTAL_TITLE = "Вероятность отказа"
VERTICAL_TITLE = "Количество заказанных товаров"
PATH_TO_DATA = "files/train.csv"

NAME_FOR_SCATTERPLOT = "graphs/dependence_on_quantity_of_units_ordered"
NAME_FOR_LINEPLOT = "graphs/dependence_on_quantity_of_units_ordered_lineplot"

IMAGE_FORMAT = "png"
COLOR = "#B0E0E6"


def set_diagram_titles(ax):
    ax.set_title(DIAGRAM_TITLE)
    ax.set_xlabel(HORIZONTAL_TITLE)
    ax.set_ylabel(VERTICAL_TITLE)


def scatterplot(x_data, y_data):
    _, ax = plt.subplots()
    ax.scatter(x_data, y_data, s=10, color=COLOR)

    set_diagram_titles(ax)
    plt.savefig("{}".format(NAME_FOR_SCATTERPLOT), fmt=IMAGE_FORMAT)


def lineplot(x_data, y_data):
    _, ax = plt.subplots()
    ax.plot(x_data, y_data, lw=2, color=COLOR)

    set_diagram_titles(ax)
    plt.savefig("{}".format(NAME_FOR_LINEPLOT), fmt=IMAGE_FORMAT)


def csv_reader(file_obj):
    reader = csv.reader(file_obj, delimiter=" ")
    orders = []
    cancel_flags = []
    prev = 1
    for row in reader:
        s = " ".join(row)
        splitted_rows = s.split(",")

        order_num = splitted_rows[5]
        orders.append(order_num)

        if order_num != prev:
            cancel_flags.append(splitted_rows[9])
        prev = order_num

    order_data = dict(Counter(orders)).values()

    lineplot(cancel_flags, list(order_data))
    scatterplot(cancel_flags, list(order_data))


if __name__ == "__main__":
    with open(PATH_TO_DATA, "r", encoding="ISO-8859-1") as f_obj:
        csv_reader(f_obj)

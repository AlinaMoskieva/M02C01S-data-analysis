import csv
import itertools

import matplotlib.pyplot as plt

DIAGRAM_TITLE = "Влияние времени суток на отказ"
HORIZONTAL_TITLE = "Колиество отказов"
HORIZONTAL_TITLE_BASED_ON_PERCENTAGE = " Вероятность отказа"
VERTICAL_TITLE = "Период дня"
PATH_TO_DATA = "files/train.csv"

BASED_ON_CANCELLED_AMOUNT_NAME = "graphs/influence_of_the_part_of_the_day"
BASED_ON_CANCELLED_AMOUNT_NAME_LINEPLOT = "graphs/influence_of_the_part_of_the_day_lineplot"

BASED_ON_CANCELLED_PERCENTAGE_NAME = "graphs/influence_of_the_part_of_the_day_based_on_percentage"
BASED_ON_CANCELLED_PERCENTAGE_NAME_LINEPLOT = "graphs/influence_of_the_part_of_the_day_lineplot__based_on_percentage"

IMAGE_FORMAT = "png"
COLOR = "#B0E0E6"
MARKER_SIZE = 10
PART_OF_DAY = ["утро", "день", "вечер"]


def set_diagram_titles(ax, horizontal_title):
    ax.set_title(DIAGRAM_TITLE)
    ax.set_xlabel(horizontal_title)
    ax.set_ylabel(VERTICAL_TITLE)


def scatterplot(x_data, y_data, diagram_name, horizontal_title):
    _, ax = plt.subplots()

    ax.scatter(x_data, y_data, s=10, color=COLOR)

    set_diagram_titles(ax, horizontal_title)

    plt.savefig("{}".format(diagram_name), fmt=IMAGE_FORMAT)


def lineplot(x_data, y_data, diagram_name, horizontal_title):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw=2, color=COLOR)

    set_diagram_titles(ax, horizontal_title)

    plt.savefig('{}'.format(diagram_name), fmt=IMAGE_FORMAT)


def the_order_was_cancelled(data):
    return data[9] == "1"


def the_order_was_at_the_morning(time_interval):
    return time_interval.startswith("06") or time_interval.startswith("08") or time_interval.startswith("10")


def the_order_was_at_the_middle_day(time_interval):
    return time_interval.startswith("12") or time_interval.startswith("14") or time_interval.startswith("16")


def count_orders_by_part_of_the_day(total_amount_of_cancelled_orders, total_amount_of_not_cancelled_orders):
    return [x + y for x, y in
            itertools.zip_longest(total_amount_of_cancelled_orders, total_amount_of_not_cancelled_orders, fillvalue=0)]


def count_percentge_of_cancelled_orders(total_amount_of_cancelled_orders, total):
    return [(x / y) * 100 for x, y in itertools.zip_longest(total_amount_of_cancelled_orders, total)]


def collect_data(morning_data, day_data, evening_data):
    data = []

    data.append(morning_data)
    data.append(day_data)
    data.append(evening_data)

    return data


def csv_reader(file_obj):
    reader = csv.reader(file_obj, delimiter=' ')

    cancel_flags = []
    prev = 1

    amount_of_cancelled_orders_at_morning = 0
    amount_of_cancelled_orders_at_middle_day = 0
    amount_of_cancelled_orders_at_evening = 0

    amount_of_not_cancelled_orders_at_morning = 0
    amount_of_not_cancelled_orders_at_middle_day = 0
    amount_of_not_cancelled_orders_at_evening = 0

    for row in reader:
        s = " ".join(row)
        splitted_row = s.split(',')
        order_num = splitted_row[5]

        if order_num != prev:
            time_interval = splitted_row[0]

            if the_order_was_cancelled(splitted_row):
                if the_order_was_at_the_morning(time_interval):
                    amount_of_cancelled_orders_at_morning += 1
                elif the_order_was_at_the_middle_day(time_interval):
                    amount_of_cancelled_orders_at_middle_day += 1
                else:
                    amount_of_cancelled_orders_at_evening += 1
            else:
                if the_order_was_at_the_morning(time_interval):
                    amount_of_not_cancelled_orders_at_morning += 1
                elif the_order_was_at_the_middle_day(time_interval):
                    amount_of_not_cancelled_orders_at_middle_day += 1
                else:
                    amount_of_not_cancelled_orders_at_evening += 1
            cancel_flags.append(int(splitted_row[9]))
        prev = order_num

    total_amount_of_cancelled_orders = collect_data(amount_of_cancelled_orders_at_morning,
                                                    amount_of_cancelled_orders_at_middle_day,
                                                    amount_of_cancelled_orders_at_evening)

    total_amount_of_not_cancelled_orders = collect_data(amount_of_not_cancelled_orders_at_morning,
                                                        amount_of_not_cancelled_orders_at_middle_day,
                                                        amount_of_not_cancelled_orders_at_evening)

    total = count_orders_by_part_of_the_day(total_amount_of_cancelled_orders, total_amount_of_not_cancelled_orders)
    percentage = count_percentge_of_cancelled_orders(total_amount_of_cancelled_orders, total)

    generate_diagrams(total_amount_of_cancelled_orders, percentage)


def generate_diagrams(total_amount_of_cancelled_orders, percentage):
    lineplot(total_amount_of_cancelled_orders, PART_OF_DAY, BASED_ON_CANCELLED_AMOUNT_NAME_LINEPLOT, HORIZONTAL_TITLE)
    scatterplot(total_amount_of_cancelled_orders, PART_OF_DAY, BASED_ON_CANCELLED_AMOUNT_NAME, HORIZONTAL_TITLE)

    lineplot(percentage, PART_OF_DAY, BASED_ON_CANCELLED_PERCENTAGE_NAME, HORIZONTAL_TITLE_BASED_ON_PERCENTAGE)
    scatterplot(percentage, PART_OF_DAY, BASED_ON_CANCELLED_PERCENTAGE_NAME_LINEPLOT,
                HORIZONTAL_TITLE_BASED_ON_PERCENTAGE)


if __name__ == "__main__":
    with open(PATH_TO_DATA, "r", encoding="ISO-8859-1") as f_obj:
        csv_reader(f_obj)

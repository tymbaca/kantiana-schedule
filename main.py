import html_parser
import schedule_baker
import xlsx_generator

from settings import *

start_date = "01.01.2023"
day_count = 180
groups = [1, 2, 3]


def main():
    groups_html_lists = []
    groups_schedule_lists = []

    for group in groups:
        html_list = html_parser.get_html_list(start_date=start_date, group=group, day_count=day_count)
        groups_html_lists.append(html_list)

    for html_list in groups_html_lists:
        schedule_list = schedule_baker.bake_schedules(html_list)
        groups_schedule_lists.append(schedule_list)

    xlsx_generator.generate(groups_schedule_lists, "testing.xlsx")


if __name__ == '__main__':
    main()

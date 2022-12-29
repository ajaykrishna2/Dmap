from crontab import CronTab
my_cron = CronTab(user='ajay')
job = my_cron.new(command='python /home/ajay/PycharmProjects/pythonProject/tasks/email4.py')
job.hour.every(13)
print('hi')
my_cron.write()

# def main():
#     from crontab import CronTab
#
#     cron = CronTab()
#
#     job = cron.new(command='python3.8 /home/ajay/PycharmProjects/pythonProject/tasks/email4.py')
#     job.minute.on(2)
#     job.hour.on(12)
#
#     cron.write()
#
# if __name__ == "__main__":
#   main()
import sys
from datetime import datetime


def main(args):
    ans = 1
    for arg in args[1:]:
        ans *= int(arg)
    print("calculated result as: {} on: {} ".format(ans,
                                                    datetime.now()))


if __name__ == '__main__':
    main(sys.argv)
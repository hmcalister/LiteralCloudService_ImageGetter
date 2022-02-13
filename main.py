import os, datetime

logs_path=f"logs/{str(datetime.date.today())}.log"
if os.path.exists(logs_path):
    os.remove(logs_path)

from testing import wgetTester
wgetTester.test_time_wget()
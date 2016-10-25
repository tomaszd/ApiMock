# warning psuedocode! Note the retries could be done via faili APIresult objects
# for fututre this should be added as periodic task to celery or as cron job
import re
path_to_logfile = "logfile.log"


def get_latest_failing_calls(path_to_log):
    """parse logs to get proper failing calls"""
    debug_calls = open(path_to_logfile, "r")
    failing_calls = []
    for line in failing_calls:
        if re.match("_status=False"):
            failing_calls.append(line)
    return failing_calls


def retry_new_calls(sure=True, erase_old=True):
    """here should be the logic to create call from log params
        #as for now there is URL/ METHOD / params so should be easy
        with erase_old -the old status=False are deleted to not be repetead"""

    for failing_call in get_latest_failing_calls(path_to_log=path_to_logfile):
        pass

retry_new_calls(sure=True)

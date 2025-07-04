#!/usr/bin/env python3
#
# logMaintenance.py

"""
Documentation:
  logMaintenance.py enters the arguments into the life.log with format:
  YYYY-MM-DD HH:MM:SS|[logMaintenance.main]|<string>
"""

import sys

sys.path.append('/home/ubuntu/TB5-WaLI/plib')
import lifeLog

from time import sleep


def main():
    args = sys.argv
    if (len(args) == 1):
          print('USAGE: ./logMaintenance.py "log this message to life.log"')
    else:
          strToLog = "** " + args[1] + " **"
          lifeLog.logger.info(strToLog)
          print("'{}' added to life.log".format(strToLog))
    sleep(1)


if (__name__ == '__main__'):  main()

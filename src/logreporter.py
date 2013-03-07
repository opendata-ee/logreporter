#!/usr/bin/env python

"""
logreporter is a simple app that, given a list of log files to check
will read each log file and report on the number of ERROR entries within
a given time period, 24 hours by default.  Once it has built a list of
error messages, it tries to group them and then generate a report that
is emailed to one or more email addresses.
"""
import os, sys
import datetime
import itertools
import smtplib
import argparse
from email.mime.text import MIMEText
from socket import gethostname

from reporter import check_log_file, filter_date
from dateutil import parser as date_parser
from template import (generate_header, generate_block, generate_footer)

def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logs",
                        help="comma-separated list of log files")
    parser.add_argument("-s", "--sender",
                        help="email address of sender")
    parser.add_argument("-r", "--recipients",
                        help="comma-separated list of recipients")
    parser.add_argument("--server",
                        help="The address:port of the mail server")
    parser.add_argument("--hours", type=int, default=24,
                        help="Accepts log from the previous X hours")

    return parser.parse_args()


if __name__ == "__main__":
    args = load_config()
    if not args.logs:
        print "Log files required, specify a comma-separated list as -l"
        sys.exit(0)
    if not args.recipients:
        print "No recipients specified, provide a comma-separated list to -r"
        sys.exit(0)

    text_blocks = []

    hostname = gethostname()
    rundate = datetime.datetime.now()

    for logfile in args.logs.split(','):
        if not os.path.exists(logfile):
            print "Failed to find file: {f}".format(f=logfile)
            continue

        with open(logfile, 'r') as f:
            items = check_log_file(f)
            items = itertools.ifilter(filter_date(args.hours, now=rundate), items)
            block = generate_block(logfile, list(items))
            text_blocks.append(block)

    header = generate_header(rundate, server=hostname)
    footer = generate_footer()

    sender = args.sender if args.sender else "root@{0}".format(hostname)
    msg = MIMEText("".join([header] + text_blocks + [footer]))
    msg['Subject'] = "[LOG REPORT] {0}".format(hostname)
    msg['From'] = sender
    msg['To'] = args.recipients

    s = smtplib.SMTP(args.server or "localhost:1025")
    s.sendmail(sender, args.recipients.split(','), msg.as_string())
    s.quit()

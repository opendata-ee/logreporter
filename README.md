# logreporter

Getting emails with every single occurrence of an error is a bit of a pain.

LogReporter is a simple script that scans a list of log files looking for specific types of messages.  Currently this involves looking for messages that are logged in a specific format and for specific tags.

Once the logs have been checked, the script will then email a report of the found errors (if any) to a list of recipients as a plain text email.

## Installation

    git clone git://github.com/<username>/logreporter.git
    cd logreporter
    virtualenv .
    . bin/activate
    pip install -r requirements.txt
    

## Running the script

Rather than have a config file (for the moment) the script it managed by a collection of command line arguments that specify what is expected of the script.

The arguments accepted by the script are:

  * __--logs__ - A comma separated list of log files to check
  * __--sender__ - email address for the sender (defaults to root@{servername})
  * __--recipients__ - A comma separated list of people to receive the email.
  * __--server__ - the host:ip of the smtp server if it is not localhost:25
  * __--hours__ - The number of hours in the past (from right now) to look back in the log file.

An example command line might be:

    LOGROOT=/var/log/ckan
    src/logreporter.py --logs $LOGROOT"/ckan.log" \
        --server localhost:1025 \
        --recipients ross@localhost.local \
        --hours 2400
    
In the example above, the SMTP server is set to localhost:1025 for testing and you can set up a test email server by using:

    python -m smtpd -n -c DebuggingServer localhost:1025


## TODO

  * Group errors together with a count of how many times, and over what time period they occurred.
  * Accept more than one logging level
  * Provide a way of specifying how to match a log entry.
#!/usr/bin/env python3


import datetime as dt
import dateutil.parser as dp
import itertools as it
import os
import os.path as path
import re
import shutil as sh
import subprocess as sp
import sys


class HandledError(Exception):
    def __init__(self, fmt=None, *args):
        if fmt:
            self.message = fmt.format(*args)
        else:
            self.message = None


class InternalError(HandledError):
    pass


class UserError(HandledError):
    pass


class UserCancelled(HandledError):
    pass


def parse_date(date_string=None):
    complaint = UserError("invalid date: '{}'", date_string)
    if not date_string:
        return dt.date.today()
    if date_string[0] in "+-":
        try:
            number_of_days = int(date_string)
        except ValueError:
            raise complaint
        return dt.date.today() + dt.timedelta(days=number_of_days)
    elts = date_string.split("-")
    if len(elts) not in (1, 2, 3):
        raise complaint
    for elt in elts:
        try:
            if int(elt) <= 0:
                raise complaint
        except ValueError:
            raise complaint
    try:
        return dp.parse(date_string, parserinfo=dp.parserinfo(
            dayfirst=False, yearfirst=True))
    except ValueError:
        raise complaint


REPO_PATH = os.getenv("DIARY_LOCATION")
if not REPO_PATH:
    print("diary: you need to set DIARY_LOCATION")
    sys.exit(1)


ENTRIES_PATH = path.join(REPO_PATH, "entries")


def get_entry_dates():
    dates = []
    for entry in sorted(os.listdir(ENTRIES_PATH)):
        if re.fullmatch(r"[0-9]{4}-"
                        r"(0[1-9]|1[012])-"
                        r"(0[1-9]|[12][0-9]|3[01])-"
                        r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
                        r".md.gpg",
                    entry):
            date = entry[:len(entry)-len(".md.gpg")]
            dates.append(date)
    return dates


def tabulate(strings, sep="    "):
    column_width = max(len(string) for string in strings)
    terminal_size = sh.get_terminal_size(fallback=None)
    if terminal_size:
        column_count = terminal_size.columns // (column_width + len(sep))
    else:
        column_count = 1
    columns = [[] for i in range(column_count)]
    column_length = ((len(strings) - 1) // column_count) + 1
    for i, string in enumerate(strings):
        columns[i // column_length].append(string)
    for row in it.zip_longest(*columns):
        print(sep.join(
            item.ljust(column_width)
            for item in row if item is not None))


def task_ls(*args):
    if args:
        raise UserError("'ls' takes no arguments")
    dates = get_entry_dates()
    entry_count = len(dates)
    if entry_count == 0:
        print("No entries")
    elif entry_count == 1:
        print("1 entry")
    elif entry_count < 10:
        print("{} entries".format(entry_count))
    else:
        tabulate(dates)
        first_date = dates[0]
        last_date = dates[-1]
        print()
        print("{} entries from {} to {}".format(entry_count,
                                                first_date,
                                                last_date))


EDITOR = ["emacsclient", "--alternate-editor=", "-nw"]


DATE_FORMAT = "%Y-%m-%d-%a"


def format_date(date):
    return date.strftime(DATE_FORMAT)



def entry_filepath(date):
    date_string = format_date(date)
    filename = "{}.md.gpg".format(date_string)
    filepath = os.path.join(ENTRIES_PATH, filename)
    return filepath


def run(*args):
    return sp.call(args, cwd=REPO_PATH) == 0


ONE_DAY = dt.timedelta(days=1)


def file_contents(filepath):
    if path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    return None


def task_edit(*args):
    if len(args) > 1:
        raise UserError("'edit' only takes one argument")
    date = parse_date(*args)
    if not args and get_entry_dates():
        adjusted_date = date
        days_without_entries = 0
        while not path.exists(entry_filepath(adjusted_date - ONE_DAY)):
            adjusted_date -= ONE_DAY
            days_without_entries += 1
        if days_without_entries >= 1:
            if days_without_entries == 1:
                print("You have no entry for yesterday!")
            else:
                print("You have no entries for the last {} days!"
                      .format(days_without_entries))
            user_response = input("Make entry for {} instead? [Y/n/q] "
                                  .format(format_date(adjusted_date)))
            if user_response and user_response[0] in "qQ":
                raise UserCancelled
            if not user_response or user_response[0] not in "nN":
                date = adjusted_date
    date_string = format_date(date)
    filepath = entry_filepath(date)
    old_contents = file_contents(filepath)
    if run(*EDITOR, filepath):
        new_contents = file_contents(filepath)
        if new_contents != old_contents:
            if not run("git", "add", filepath):
                raise InternalError
            if not run("git", "commit", "-m",
                       ("Edit entry for {}" if old_contents
                        else "Create entry for {}").format(date_string)):
                raise InternalError
        else:
            print("No changes.")
    else:
        print("Edit aborted.")
        new_contents = file_contents(filepath)
        if new_contents != old_contents:
            user_response = input("Revert changes to entry for {}? [y/N] "
                                  .format(date_string))
            if user_response and user_response in "yY":
                if not run("git", "checkout", filepath):
                    raise InternalError


def task_rm(*args):
    if len(args) > 1:
        raise UserError("'rm' only takes one argument")
    date = parse_date(*args)
    date_string = format_date(date)
    filepath = entry_filepath(date)
    if path.exists(filepath):
        user_response = input("Delete entry for {}? [y/N] "
                              .format(date_string))
        if user_response and user_response[0] in "yY":
            if not run("git", "rm", filepath):
                raise InternalError
            if not run("git", "commit", "-m",
                       "Delete entry for {}".format(date_string)):
                raise InternalError
        else:
            raise UserCancelled
    else:
        raise UserError("no entry for {}".format(date_string))


def task_mv_or_cp(*args, task=None):
    assert task in ("mv", "cp")
    user_readable_task = "Move" if task == "mv" else "Copy"
    if not args:
        raise UserError("'{}' needs an argument", task)
    elif len(args) == 1:
        old_date = parse_date()
        new_date = parse_date(args[0])
    elif len(args) == 2:
        old_date = parse_date(args[0])
        new_date = parse_date(args[1])
    else:
        raise UserError("'{}' only takes two arguments", task)
    old_date_string = format_date(old_date)
    new_date_string = format_date(new_date)
    old_filepath = entry_filepath(old_date)
    new_filepath = entry_filepath(new_date)
    user_response = input("{} entry for {} to {}? [Y/n] "
                          .format(user_readable_task,
                                  old_date_string, new_date_string))
    if not user_response or user_response[0] not in "nN":
        if path.exists(new_filepath):
            user_response = input("Overwrite existing entry for {}? [y/N] "
                                  .format(new_date_string))
            if not user_response or user_response[0] not in "yY":
                raise UserCancelled
        if not run(task, old_filepath, new_filepath):
            raise InternalError
        if not run("git", "add", old_filepath, new_filepath):
            raise InternalError
        if not run("git", "commit", "-m",
                   "{} entry for {} to {}"
                   .format(user_readable_task,
                           old_date_string, new_date_string)):
            raise InternalError
    else:
        raise InternalError


def task_mv(*args):
    return task_mv_or_cp(*args, task="mv")


def task_cp(*args):
    return task_mv_or_cp(*args, task="cp")


def task_run(*args):
    if not args:
        raise UserError("'run' needs an argument")
    if not run(*args):
        raise InternalError


def task_git(*args):
    return task_run("git", *args)


def task_push(*args):
    return task_git("push", *args)


USAGE_MESSAGE = """\
usage:
    diary ls
    diary [ edit ] [ <date> ]
    diary rm [ <date> ]
    diary mv [ <old-date> ] <new-date>
    diary cp [ <old-date> ] <new-date>
    diary run [ <shell-command> ... ]
    diary git [ <git-args> ... ]
    diary push [ <git-push-args> ... ]
    diary help

date format:
    [+-]<number-of-days>
    <day-of-month>
    <month>-<day-of-month>
    <year>-<month>-<day-of-month>\
"""


def task_help(*args):
    print(USAGE_MESSAGE)


TASKS = ("ls", "edit", "rm", "mv", "cp", "run", "git", "push", "help")


def main(*args):
    if not args:
        task = "edit"
    elif args[0] in TASKS:
        task, *args = args
    elif len(args) == 1 and not re.search(r"[a-z]", args[0]):
        task = "edit"
    else:
        raise UserError("invalid task '{}'", args[0])
    try:
        task_function = eval("task_{}".format(task))
    except NameError:
        raise InternalError("task '{}' is not implemented yet", task)
    task_function(*args)


if __name__ == "__main__":
    try:
        main(*sys.argv[1:])
        sys.exit(0)
    except UserCancelled:
        sys.exit(1)
    except HandledError as e:
        if e.message:
            print("diary: {}".format(e.message))
        sys.exit(1)

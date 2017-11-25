**`diary-manager`**: if you want your diary on the command line.

<!-- toc -->

- [TL;DR](#tldr)
  * [What is it](#what-is-it)
  * [How do I get it](#how-do-i-get-it)
- [Installation](#installation)
  * [Install dependencies](#install-dependencies)
    + [macOS](#macos)
  * [Install `diary-manager`](#install-diary-manager)
- [Usage](#usage)
- [Configuration](#configuration)
- [Version control](#version-control)
- [Encryption](#encryption)
- [Development](#development)

<!-- tocstop -->

## TL;DR

### What is it

`diary-manager` is a simple tool for managing (possibly encrypted,
possibly version-controlled) diary entries on the command line.

### How do I get it

    $ pip3 install git+https://github.com/raxod502/diary-manager.git

## Installation

### Install dependencies

#### macOS

Install the Xcode Command Line Tools:

    $ xcode-select --install

Install [Homebrew]:

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install [Python 3][python]:

    $ brew install python3

### Install `diary-manager`

    $ pip3 install git+https://github.com/raxod502/diary-manager.git

## Usage

First, create your diary repository (any directory will work; it only
has to be a Git repository if you want version control support):

    $ mkdir diary
    $ cd diary
    $ git init

Then export the environment variable `$DIARY_LOCATION` to this
directory, or some subdirectory. This is the directory inside which
diary entries will be placed.

You can make an entry for the current day with:

    $ diary

For more information, refer to the usage message:

    usage:
        diary ls
        diary [ edit ] [ <date> ]
        diary rm [ <date> ]
        diary mv [ <old-date> ] <new-date>
        diary cp [ <old-date> ] <new-date>
        diary run [ <shell-command> ... ]
        diary git [ <git-args> ... ]
        diary help

    date format:
        [+-]<number-of-days>
        <day-of-month>
        <month>-<day-of-month>
        <year>-<month>-<day-of-month>

Note that if you don't specify the month (or year), `diary-manager`
assumes you mean a day in the past (rather than the future).

## Configuration

By default, entries are edited in `$EDITOR` (or `vi`, by default). You
can override this by exporting `$DIARY_EDITOR`.

By default, entries are created in the format `<date>.md`. You can
customize the `<date>` format by exporting `$DIARY_DATE_FORMAT`, which
defaults to `%Y-%m-%d-%a`. This is parsed by [`strftime`][strftime]
(note that no validation is done by `diary-manager` so be careful).
You can customize the file extension (defaults to `.md`) by exporting
`$DIARY_ENTRY_EXTENSION`.

## Version control

`diary-manager` automatically creates a Git commit on every edit if
the `$DIARY_LOCATION` directory is inside a Git repository and Git is
installed on the system. Otherwise, it does nothing. Using Git is
recommended, since then you have no chance of data loss.

## Encryption

For encrypted diary entries, using [Emacs]
with [EasyPG Assistant][epa] is recommended. Here is the
`diary-manager` configuration:

    $ export DIARY_EDITOR='emacsclient --alternate-editor= -nw'
    $ export DIARY_ENTRY_EXTENSION='.md.gpg'

Then put a file `.dir-locals.el` in your `$DIARY_LOCATION` with the
following contents (where `<your name>` matches your GPG key; to
encrypt to multiple keys you can just use a list of strings instead of
a single string):

    ((nil . ((epa-file-encrypt-to . "<your name>"))))

You may wish to install package [markdown-mode], or choose a different
file extension than `.md`.

## Development

    $ git clone https://github.com/raxod502/diary-manager.git
    $ cd diary-manager
    $ pip3 install --editable .

This will install a symlink to `diary` in your system's binary
directory.

[emacs]: https://www.gnu.org/software/emacs/
[epa]: https://www.gnu.org/software/emacs/manual/html_mono/epa.html
[git]: https://git-scm.com/
[homebrew]: https://brew.sh/
[markdown-mode]: https://github.com/jrblevin/markdown-mode
[python]: https://www.python.org/
[strftime]: http://strftime.org/

**Maintenance notice:** This project is not actively maintained, but
pull requests will be reviewed and accepted, and security patches will
be applied.

**`diary-manager`**: simple command-line tool and Emacs package for
managing diary entries.

<!-- longlines-start -->

<!-- toc -->

- [TL;DR](#tldr)
- [Command-line tool](#command-line-tool)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Configuration](#configuration)
- [Emacs package](#emacs-package)
  * [Installation](#installation-1)
  * [Usage](#usage-1)
  * [Configuration](#configuration-1)
- [Contributor guide](#contributor-guide)
- [FAQ](#faq)
  * [How can I encrypt my diary entries?](#how-can-i-encrypt-my-diary-entries)
  * [How is this different from `diary-lib`?](#how-is-this-different-from-diary-lib)

<!-- tocstop -->

<!-- longlines-stop -->

## TL;DR

`diary-manager` is a way for you to maintain a collection of daily
diary entries. It comes with a command-line tool and an Emacs package;
both expose the same functionality. You can install the command-line
tool with [Pip]:

    $ pip3 install git+https://github.com/radian-software/diary-manager.git

You can install the Emacs package with [`straight.el`][straight.el]:

    (straight-use-package 'diary-manager)

To get started, create a directory to hold your diary entries. You can
put it in a Git repository if you want a version-controlled diary. For
the command-line tool, export the environment variable
`$DIARY_LOCATION` to this directory. The Emacs package will use this
environment variable by default, but you can also set the Emacs user
option `diary-manager-location`.

Using the command-line tool, make a diary entry for the current day as
follows:

    $ diary

This will open the editor configured in the environment variable
`$DIARY_EDITOR`, or `$EDITOR`, or as a fallback `vi(1)`. When you are
finished, save the file and exit your editor. If your
`$DIARY_LOCATION` is in a Git repository, a commit will automatically
be created.

Using the Emacs package, make a diary entry for the current day as
follows:

    M-x diary-manager-edit

When you are finished, press `C-c C-c` to save the entry, making a
commit if `$DIARY_LOCATION` is in a Git repository, and kill the
buffer.

## Command-line tool
### Installation

First, you will need to install [Python 3][python] and [Pip]. Then,
you may run the following command to install the command-line tool:

    $ pip3 install git+https://github.com/radian-software/diary-manager.git

This will install a binary named `diary`.

### Usage

The commands are mostly self-explanatory:

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

If a date is omitted, it defaults to the current date. Otherwise, you
can specify an offset in days from the current date, or give a full or
partial date in year-month-day format. (Partial dates are interpreted
as dates in the past; if you wish to specify a future date, either
give a full date or use an offset.)

`diary run` and `diary git` just change working directory to
`$DIARY_LOCATION` and then run the command provided.

### Configuration

Before doing anything, you must set `$DIARY_LOCATION` to an existing
directory, which will hold your diary entries.

In this directory, the filenames of entries are determined by
concatenating the date and an extension. The date is formatted using
[strftime] with `$DIARY_DATE_FORMAT` (defaults to `%Y-%m-%d-%a`). The
extension is given by `$DIARY_ENTRY_EXTENSION` (defaults to `.md`).

Entries are edited in `$DIARY_EDITOR`, `$EDITOR`, or `vi(1)` in
decreasing order of preference.

## Emacs package
### Installation

`diary-manager` [is available on MELPA][melpa]. The easiest way to
install it is using [`straight.el`][straight.el]:

    (straight-use-package 'diary-manager)

However, you may install `diary-manager` using any other Emacs package
manager if you prefer.

### Usage

The commands are mostly self-explanatory:

* `M-x diary-manager-edit`
* `M-x diary-manager-find-file`
* `M-x diary-manager-edit-mode`
* `M-x diary-manager-remove`
* `M-x diary-manager-move`
* `M-x diary-manager-copy`
* `M-x diary-manager-browse`

The equivalent to the command-line tool's `diary edit` is `M-x
diary-manager-edit`. This requires `$DIARY_LOCATION` or
`diary-manager-location` to be set. However, you can also edit an
arbitrary file as a diary entry using `M-x
diary-manager-find-file`. In fact, you can enable `M-x
diary-manager-edit-mode` from any buffer. This is probably not very
useful in most cases, however.

`M-x diary-manager-browse` opens Dired on `diary-manager-location`.

### Configuration

The same environment variables are used, but they may be overridden by
setting Emacs Lisp variables:

* `$DIARY_LOCATION` becomes `diary-manager-location`
* `$DIARY_DATE_FORMAT` becomes `diary-manager-date-format`
* `$DIARY_ENTRY_EXTENSION` becomes `diary-manager-entry-extension`
* `$DIARY_TEMPLATE` (not available in the Python version) becomes
  `diary-manager-template`

If you don't change the extension from `.md`, you will probably want
to install the package [markdown-mode]. This can be done
with [`straight.el`][straight.el]:

    (straight-use-package 'markdown-mode)

Diary templates are a feature unique to the Emacs version. See
docstring for the user option, but the short version is that they
allow you to have custom text inserted by default into each new diary
entry before you start editing it.

## Contributor guide

Please see [the contributor guide for my
projects](https://github.com/radian-software/contributor-guide).

To work on the command-line tool, start by creating a virtualenv and
then run

    $ pip install -e .

from inside this repository. That will install a `diary` binary to
your virtualenv, which automatically picks up changes to the `diary`
script in this repository.

To work on the Emacs package, just install it via `straight.el` and
hack away. Changes to `diary-manager.el` will take effect without
further intervention.

## FAQ
### How can I encrypt my diary entries?

The easiest way is to use Emacs with [EasyPG Assistant][epa]. Start by
creating a GPG key. In your `$DIARY_LOCATION`, create a file called
`.dir-locals.el` with the following contents (where `<your key>`
matches your GPG key; to encrypt to multiple keys instead just use a
list of strings instead of a single string):

    ((nil . ((epa-file-encrypt-to . "<your key>"))))

Use the following configuration for `diary-manager`:

    $ export DIARY_EDITOR='emacsclient --alternate-editor= -nw'
    $ export DIARY_ENTRY_EXTENSION='.md.gpg'

### How is this different from `diary-lib`?

[`diary-lib`][diary-lib] is a package which comes bundled with
Emacs. [Org] has integration with this package.

The word "diary" can mean either an appointment book, or a personal
journal. `diary-lib` provides a way to keep an appointment book, while
`diary-manager` provides a way to keep a personal journal.

* `diary-lib` has all diary entries in the same file, while
  `diary-manager` uses a separate file for each entry.
* `diary-lib` has specific support for entering and processing
  structured data relating to appointments and calendar events,
  whereas `diary-manager` allows you to enter free-form text with no
  special features.
* `diary-lib` is approximately 2,500 lines of code, and
  `diary-manager` is approximately 600.

[borg]: https://github.com/emacscollective/borg
[diary-lib]: https://www.gnu.org/software/emacs/manual/html_node/emacs/Diary.html
[el-get]: https://github.com/dimitri/el-get
[epa]: https://www.gnu.org/software/emacs/manual/html_mono/epa.html
[markdown-mode]: https://github.com/jrblevin/markdown-mode
[melpa]: https://melpa.org/#/diary-manager
[org]: https://orgmode.org/
[pip]: https://pip.pypa.io/en/stable/
[python]: https://www.python.org/
[quelpa]: https://github.com/quelpa/quelpa
[straight.el]: https://github.com/raxod502/straight.el
[strftime]: http://strftime.org/

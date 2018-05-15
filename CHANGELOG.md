# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog].

## 1.1.2 (released 2018-05-15)
### Fixed
* Previously, `dm-save-entry` would erroneously attempt to kill the
  buffer when there was an error. This has now been fixed.

## 1.1.1 (released 2018-03-13)
### Fixed
* Previously, a message was not shown when saving a diary entry with
  Git. This has been fixed.

## 1.1 (released 2018-03-13)
### Added
* Emacs package
    * User options
        * `dm-diary-location`
        * `dm-diary-date-format`
        * `dm-diary-entry-extension`
        * `dm-enable-git-integration`
        * `dm-read-date-function`
        * `dm-error-buffer-name`
        * `dm-edit-mode-map`
        * `dm-edit-mode-message`
    * Interactive functions
        * `dm-edit`
        * `dm-find-file`
        * `dm-edit-mode`
        * `dm-remove`
        * `dm-move`
        * `dm-copy`
        * `dm-browse`

## 1.0 (released 2017-11-24)
### Added
* Python command-line utility for making diary entries
    * `diary ls`
    * `diary edit`
    * `diary rm`
    * `diary mv`
    * `diary cp`
    * `diary run`
    * `diary git`
    * `diary help`
* Distribution configuration in `setup.py`
* Documentation in README
* MIT license
* Changelog

[keep a changelog]: http://keepachangelog.com/

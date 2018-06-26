# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog].

## 2.0.1 (released 2018-06-26)
### Python script
#### Bugs fixed
* The `diary-manager` package now correctly depends on the
  `python-dateutil` package and not the unrelated (but confusingly
  named) `dateutils` package.

## 2.0 (released 2018-06-05)
### Emacs package
#### Breaking changes
* Many functions and variables have been renamed in order to clarify
  which should be considered public and to change the prefix from
  `dm-` to `diary-manager-` as per standard packaging conventions.
  Note that internal functions and variables will not be documented
  further in this changelog.
  * User options
    * `dm-diary-location` -> `diary-manager-location`
    * `dm-diary-date-format` -> `diary-manager-date-format`
    * `dm-enable-git-integration` ->
      `diary-manager-enable-git-integration`
    * `dm-read-date-function` -> `diary-manager-read-date-function`
    * `dm-error-buffer-name` -> `diary-manager-error-buffer-name`
    * `dm-edit-mode-map` -> `diary-manager-edit-mode-map`
    * `dm-edit-mode-message` -> `diary-manager-edit-mode-message`
  * Public functions
    * `dm-read-date` -> `diary-manager-read-date`
  * Interactive functions
    * `dm-save-entry` -> `diary-manager-save-entry`
    * `dm-discard-entry` -> `diary-manager-discard-entry`
    * `dm-edit` -> `diary-manager-edit`
    * `dm-find-file` -> `diary-manager-find-file`
    * `dm-remove` -> `diary-manager-remove`
    * `dm-move` -> `diary-manager-move`
    * `dm-copy` -> `diary-manager-copy`
    * `dm-browse` -> `diary-manager-browse`
  * Minor modes
    * `dm-edit-mode` -> `diary-manager-edit-mode`
  * Internal variables
    * `dm-buffer-date`
    * `dm-buffer-original-contents`
    * `dm-buffer-saved-contents`
    * `dm-buffer-dedicated`
  * Internal functions
    * `dm-ensure-dm-diary-location-set`
    * `dm-ensure-org-read-date-defined`
    * `dm-error-popup`
    * `dm-call-process`
    * `dm-format-process-error`
    * `dm-validate-process`
    * `dm-validator-program-found`
    * `dm-validator-command-succeeded`
    * `dm-run-process`
    * `dm-check-process`
    * `dm-git-enabled-p`
    * `dm-git-file-exists-in-index`
    * `dm-git-modified-p`
    * `dm-git-file-exists-in-head`
    * `dm-git-rm`
    * `dm-update-saved-buffer-contents`
    * `dm-ensure-buffer-visiting-diary-entry`
    * `dm-move-or-copy`

#### Internal changes
* `diary-manager.el` now uses lexical binding.
* `diary-manager.el` is now tested on Travis CI.

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


[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/pyimage2pdf/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/pyimage2pdf/tree/master)
[![PyPI version](https://badge.fury.io/py/pyimage2pdf.svg)](https://badge.fury.io/py/pyimage2pdf)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Introduction

```

# Overview

The basic command structure is:

```bash
    Usage: image2pdf [OPTIONS]
    
      This command converts input image files to pdf;  If
      you omit the output file name the command deduces the name
      based on the input file name
    
    Options:
      --version               Show the version and exit.
      -i, --input-file PATH   The input image file name to convert.  [required]
      -o, --output-file PATH  The output pdf file name.
      --help                  Show this message and exit.

```


A simple example:

```bash
image2pdf -i tests/resources/images/CompactImageDump.png
```
produces the following output:

```bash

Using input file name as base for output file name
Output file name is: CompactImageDump.pdf

```
# Installation

```bash
pip install pyimage2pdf
```

___

Written by <a href="mailto:email@humberto.a.sanchez.ii@gmail.com?subject=Hello Humberto">Humberto A. Sanchez II</a>  (C) 2025


## Note
For all kind of problems, requests, enhancements, bug reports, etc.,
please drop me an e-mail.


------


![Humberto's Modified Logo](https://raw.githubusercontent.com/wiki/hasii2011/gittodoistclone/images/SillyGitHub.png)

I am concerned about GitHub's Copilot project



I urge you to read about the [Give up GitHub](https://GiveUpGitHub.org) campaign from [the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that
a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue
to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done
without my permission.  I do not consent to GitHub's use of this project's code in Copilot.

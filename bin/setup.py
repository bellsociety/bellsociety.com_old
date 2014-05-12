#!/usr/bin/env python
"""
Checks out the gh-pages branch to _site/ dir
as a separate repo.
Allows for fancy-pants deploys, a   la
https://gist.github.com/chrisjacob/825950

To be used with the sibling deploy script

Author: Alex Rattray <rattray.alex@gmail.com>
"""

import os
import sys
import time
import subprocess
import datetime
from clint.textui import puts, colored, indent


def cyan(msg):
  return puts(colored.cyan(msg))


def red(msg):
  return puts(colored.red(msg))


def shell(cmd, *args, **kwargs):
  # tell the user what's about to go out
  puts(colored.blue("-> {}".format(cmd)))

  try:
    out = subprocess.check_output(cmd, shell=True, *args, **kwargs)
  except subprocess.CalledProcessError as e:
    # puts(colored.red(traceback.format_exc()))
    red("Command failed! (exit code {})".format(e.returncode))
    with indent(4):
      red("Failed cmd: {}".format(e.cmd))
      red("Exit code: {}".format(e.returncode))
      red("Output:")

    out = e.output
    raise e

  finally:
    with indent(4):
      puts(out)

  return out


def main():

  shell('rm -rf _site/')
  shell('git clone git@github.com:bellsociety/bellsociety.com.git _site')
  # go to _site, which is an entirely different git checkout
  os.chdir('_site')
  puts('now in folder {}'.format(os.getcwd()))
  shell('git checkout gh-pages')
  time.sleep(1)
  shell('git branch -D master')

if __name__ == '__main__':
  puts(os.getcwd())
  if 'bin/' not in sys.argv[0]:
    red('must be run as bin/setup.py! from projectroot!')
    sys.exit()

  main()

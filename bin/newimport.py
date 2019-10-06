#!/usr/bin/env python

import argparse
import yaml
import os
import urllib

import tablib
import requests
from clint.textui import puts, indent
from clint.textui.colored import green, red
from django.utils.text import slugify

import csv


def read_jekyll_file(filepath):
  """
  Reads a file with the following format:
  ```
  ---
  front: matter
  ---
  # Body Text as *Markdown* or <em>whatever</em>
  ```
  and returns:
    front_matter, body_text
  """

  front_matter = None
  body_text = ''

  try:
    with open(filepath, 'r') as f:
      contents = f.read()
      split_contents = contents.split('---\n', 2)
      front_matter_text = split_contents[1]

      # print 'found existing front-matter: ', front_matter_text
      front_matter = yaml.load(front_matter_text)
      # print 'python formatted: ', front_matter

      body_text = split_contents[2]
      if body_text:
        puts(u'existing body_text: {}'.format(body_text))

  except IOError:
    puts(green('file does not yet exist, will create...'))
  except IndexError:
    puts(red('file does not have front-matter yet, will overwrite...'))

  return front_matter, body_text


def create_front_matter(row, old_front_matter=None, accept=False):
  data = {}
  for key, value in row.items():
    if key == 'year':
      value = int(value)
    elif not value:
      value = None
    else:
      value = unicode(value).strip()
    data[key] = value

  data['layout'] = 'member_page'
  data['slug'] = unicode(slugify(row['name']))

  new_front_matter = recursively_check_conflicts(
    data, old_front_matter, accept=accept)

  new_front_matter_text = yaml.safe_dump(
    new_front_matter, default_flow_style=False)

  return new_front_matter_text


def recursively_check_conflicts(new, old, accept=False):
  puts(u'checking {}'.format(new))
  if hasattr(new, 'name'):
    puts(u'Person: {}'.format(new['name']))

  with indent(2, quote=" | "):

    if old is None:
      return new

    if new == old:
      return new

    # check if, eg 1990 == '1990' == u'1990'
    u_new = unicode(new)
    u_old = unicode(old)
    if u_new == u_old:
      return new

    puts(green('GREEN (FROM EXCEL):'))
    puts(green(u_new))
    puts(red('RED (FROM OLD VERSION OF DOCUMENT):'))
    puts(red(u_old))

    if accept:
      puts(green('accepting Excel version (green)'))
      return new

    while True:
      selection = raw_input(
        'Should we keep [G]REEN, [R]ED? \n'
        'Or should we [C]ONTINUE recursing, '
        'so you can make a more granular decision? \n'
        'OR Would you prefer to enter some [O]THER value (will be text)? \n'
        '[g/r/c/o]: '
      ).lower()[0]
      if selection in ['g', 'r', 'c', 'o']:
        if selection == 'o':
          new = raw_input('enter a new value: \n')
          puts('Do you confirm the following?')
          puts(new)
          if raw_input('[y/n]: ').lower().startswith('y'):
            return new
        else:
          break
      else:
        puts('-> You must enter g, r, c, or o!')

    if selection == 'g':
      return new
    elif selection == 'r':
      return old
    elif selection == 'c':

      if isinstance(new, dict) and isinstance(old, dict):
        checked = []
        for k, v in new.items():
          new[k] = recursively_check_conflicts(v, old.get(k, None))
          checked.append(k)
        for k, v in old.items():
          if k in checked:
            continue
          v = recursively_check_conflicts(new.get(k, None), v)
          if v:
            new[k] = v

      elif isinstance(new, list) and isinstance(old, list):
        for i, item in enumerate(new):
          if item in old:
            continue
          else:
            new[i] = recursively_check_conflicts(item, old[i])
        for i, item in enumerate(old):
          if item in new:
            continue
          else:
            item = recursively_check_conflicts(new[i], item)
            if item:
              new.append(item)

      else:  # int, str, or unicode (probably)
        if selection == 'c':
          puts(red('-> You cannot recurse further. Try again.'))
          return recursively_check_conflicts(new, old)

      return new


def write_jekyll_file(filepath, new_front_matter, body_text=''):

  # ensure dir exists.
  try: os.makedirs(os.path.dirname(filepath))
  except: pass

  with open(filepath, 'w') as f:
    new_file_contents = "---\n{}\n---\n{}".format(new_front_matter, body_text)
    f.write(new_file_contents)


def save_profile_image(image_url, filepath):
  image_url = image_url.strip()
  print(image_url)
  if not image_url:
    puts('No image url; skipping.')
    return

  if os.path.exists(filepath):
    puts('Image already exists, so skipping. '
      'If you want to update it, delete the existing file.')
    return

  puts('Will save profile photo: {}'.format(filepath.split('/')[-1]))

  # ensure dir exists.
  try: os.makedirs(os.path.dirname(filepath))
  except: pass

  # try:
  download = urllib.URLopener()
  download.retrieve(image_url, filepath)
  print("File {} downloaded to {}".format(image_url, filepath))

  # except urllib.error.URLError as e:
  #   print("Error downloading image '{}': {}".format(iamge_url, e))
  # except urllib.error.HTTPError as e:
  #   print("HTTP Error download image '{}': {!s}".format(image_url, e))

  puts('done saving photo')
  return

# Creates jekyll page for each individual member
def process_entry(row, dest, accept=False):

  # Turns names from "Krishna Bharathala" to "krishna-bharathala"
  slug = slugify(row['name'])
  filename = '{}/{}/index.md'.format(dest, slug)
  jekyll_filepath = os.path.abspath(filename)

  year = int(dest.split('/')[-1])
  photo_filename = 'images/members/{year}/{slug}.jpg'.format(
    year=year, slug=slug)
  photo_filepath = os.path.abspath(photo_filename)

  old_front_matter, body_text = read_jekyll_file(jekyll_filepath)

  new_front_matter = create_front_matter(row, old_front_matter, accept=accept)

  write_jekyll_file(jekyll_filepath, new_front_matter, body_text)

  # Requires internet, comment this out if you don't have internet
  save_profile_image(row['headshot_jpg_url'], photo_filepath)


def process_year(overall, year, accept):
  dest = '_members/{}'.format(year)

  # write the people
  for row in overall:
    process_entry(row, dest, accept)

  # write board file
  board_front_matter = yaml.safe_dump(
    {
      'layout': 'board',
      'year': year
    },
    default_flow_style=False)
  board_filepath = '{}/board.md'.format(dest)
  write_jekyll_file(board_filepath, board_front_matter, '')

  # write index file
  index_front_matter = yaml.safe_dump(
    {
      'layout': 'member_year',
      'year': year
    },
    default_flow_style=False)
  index_filepath = '{}/index.md'.format(dest)
  write_jekyll_file(index_filepath, index_front_matter, '')


# Parses the CSV File
# Puts information into a list of dicts for each member.
def parse_file(filename, accept=False):

  # Makes sure that the file name is a number.
  try:
    year = int(filename.split(".")[0].split("/")[-1])
  except:
    puts(red(
      'CSV name is not a number: {}'.format(filename.split(".")[0].split("/")[-1])
    ))

  with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    l = list(reader)
    overall = []

    # Ignoring the header row.
    for row in l[1:]:
      temp_dict = {}
      for i in xrange(len(row)):
        # Creating a dictionary with format:
        # {"name": "krishna bharathala", "email": "kbharathala@gmail.com"}
        temp_dict[l[0][i]] = row[i]
      overall.append(temp_dict)

  process_year(overall, year, accept)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='bin/newimport.py')
  parser.add_argument('csv_file', action='store',
    help="must be csv file with each year has the file name. eg. 2018.csv")

  parser.add_argument('--accept', action='store_true',
    help="Accept all changes from the excel doc "
    "(overwrite everything in old jekyll file)")
  args = parser.parse_args()

  parse_file(args.csv_file, accept=args.accept)


#!/usr/bin/env python

import argparse
import yaml
import os

import tablib
import requests
from clint.textui import puts, indent
from clint.textui.colored import green, red
from django.utils.text import slugify


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

  with open(filepath, 'wb') as file_:
    r = requests.get(image_url, stream=True)
    for chunk in r.iter_content(chunk_size=1024):
      if chunk: # filter out keep-alive new chunks
        file_.write(chunk)
        file_.flush()

  puts('done saving photo')
  return


def process_entry(row, dest, accept=False):

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
  save_profile_image(row['headshot_jpg_url'], photo_filepath)


def process_year(sheet, year, accept):
  year = int(year)
  dest = '_members/{}'.format(year)

  # write the people
  for row in sheet.dict:
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



def main(input_xls, dest, accept=False):
  with open(input_xls, 'rb') as f:
    sheet = tablib.import_set(f.read())

  for row in sheet.dict:
    process_entry(row, dest, accept=accept)


def import_years(input_xls, accept=False):
  with open(input_xls, 'rb') as f:
    databook = tablib.import_book(f.read())

  for sheet in databook.sheets():
    try:
      year = int(sheet.title)
    except:
      puts(red(
        'ignoring sheet because it is not an int: {}'
        .format(sheet.title)
      ))
      continue

    process_year(sheet, year, accept=accept)



if __name__ == '__main__':

  parser = argparse.ArgumentParser(prog='bin/import.py')
  parser.add_argument('excel_file', action='store',
    help="must be xls (not xlsx!) file with each year in its own sheet.")
  # parser.add_argument('destination_directory', action='store')
  parser.add_argument('--accept', action='store_true',
    help="Accept all changes from the excel doc "
    "(overwrite everything in old jekyll file)")
  args = parser.parse_args()

  if str(args.excel_file)[-4:] != '.xls':
    puts(red('must be .xls file!'))
    exit()

  # main(args.excel_file, args.destination_directory, accept=args.accept)
  import_years(args.excel_file, accept=args.accept)


import csv
import sys
import os
import requests

if __name__ == '__main__':

    def get_index(n, l):
        try:
            return l.index(n)
        except ValueError:
            print 'Error: CSV incorrectly formatted. Ensure there is a ' +\
            '"{}" column.'.format(n)


    # def save_profile_image(image_url, filepath):
    #     image_url = image_url.strip()
    #     if not image_url:
    #         print ('No image url; skipping.')
    #         return
    #
    #     if os.path.exists(filepath):
    #         print ('Image already exists, so skipping. ' + \
    #             'If you want to update it, delete the existing file.')
    #         return
    #
    #     print ('Will save profile photo: {}'.format(filepath.split('/')[-1]))
    #
    #     # ensure dir exists.
    #     try: os.makedirs(os.path.dirname(filepath))
    #     except: pass
    #
    #     with open(filepath, 'wb') as file_:
    #         r = requests.get(image_url, stream=True)
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk: # filter out keep-alive new chunks
    #                 file_.write(chunk)
    #                 file_.flush()
    #
    #     print ('done saving photo')
    #     return


    if len(sys.argv) < 3:
        print 'Error: Please provide <CSV File> <Members Directory>'
        sys.exit()


    members = {}
    titles = []

    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        titles = reader.next()
        year = get_index('year', titles)

        for line in reader:
            if line[year] not in members:
                members[line[year]] = []
            members[line[year]].append(line)


    _members = sys.argv[2]

    for year in members:
        if not os.path.exists('{}/{}'.format(_members, year)):
            print 'Creating new class directory: {}'.format(year)
            os.makedirs(_members + year)
        else:
            print 'Class directory "{}" exists'.format(year)

        for member in members[year]:
            name = member[get_index('name', titles)]
            slug = name.lower().replace(' ', '-')
            path = '{}/{}/{}'.format(_members, year, slug)

            if not os.path.exists(path):

                confirm = raw_input('Member "{}" does not exist.'.format(name)+\
                ' Create? (y/n)\n')
                if confirm.lower() != 'y':
                    continue

                os.makedirs(path)
                with open((path + '/index.md'), 'w') as f:
                    f.write('---\n')

                    f.write('layout: member_page\n')
                    f.write('slug: {}\n'.format(slug))

                    for i in range(len(titles)):
                        f.write('{}: {}\n'.format(titles[i], member[i] or 'null'))

                    f.write('\n---\n')

                print 'Created member: "{}"'.format(name)

                # photo_filename = 'images/members/{year}/{slug}.jpg'.format(
                #   year=year, slug=slug)
                # save_profile_image(member[get_index('headshot_jpg_url', titles)], photo_filename)

import csv
import sys
import os

if __name__ == '__main__':

    def get_index(n, l):
        try:
            return l.index(n)
        except ValueError:
            print 'Error: CSV incorrectly formatted. Ensure there is a ' +\
            '"{}" column.'.format(n)

    if len(sys.argv) < 2:
        print 'Error: Please provide a csv file for processing'
        sys.exit()


    members = {}
    titles = []

    with open(sys.argv[1], 'r') as f:
        titles = f.next().split(',')

        year = get_index('year', titles)

        for line in f:
            l = line.split(',')
            if l[year] not in members:
                members[l[year]] = []
            members[l[year]].append(l)


    _members = '../_members'

    for year in members:
        if not os.path.exists('{}/{}'.format(_members, year)):
            print 'Creating new class directory: {}'.format(year)
            os.makedirs(_members + year)
        else:
            print 'Class directory "{}" exists'.format(year)

        for member in members[year]:
            name = member[get_index('name', titles)]

            if not os.path.exists(_members + year):

                confirm = raw_input('Member "{}" does not exist.'.format(name)+\
                ' Create? (y/n)\n')
                if confirm.lower() != 'y':
                    continue

                slug = name.lower().replace(' ', '-')
                path = '{}/{}/{}'.format(_members, year, slug)
                os.makedirs(path)
                with open((path + '/index.md'), 'w') as f:
                    f.write('---\n')

                    for i in range(len(titles)):
                        f.write('{}: {}'.format(titles[i], member[i] or 'null'))

                    f.write('\n---\n')

                print 'Created member: "{}"'.format(name)

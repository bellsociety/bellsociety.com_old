
# BellSociety.com

This is a guide on how to update the information on this site. We use [Jekyll](http://jekyllrb.com/); please familiarize yourself with the framework if you're planning to perform maintenance. It's a simple system and should take about an hour to get up to speed with if you know the computers.

---

# Getting Started with Development

Development requires Ruby and Python. Ruby for the site and Python for the sweet-ass script that generates all the boilerplate.

To get started with Ruby is easy. Run `bundle install` and it should just work.
If it doesn't work, you probably need to change your gems source to http instead of https.

Python isn't hard either. First you'll need pip. If you don't have it, [install it](http://python-packaging-user-guide.readthedocs.org/en/latest/installing/#install-pip-setuptools-and-wheel). Then run `pip install -r bin/requirements.txt`.

---

### To add a new Year's worth of Members:

1. Add the year (eg. `2018`) to the `collections: members: years:` list in `_config.yaml`. It'll make sense when you look.
2. Change the `current_year` in `_config.yaml` to the current year. This one was a toughie.
3. Tell members to add themselves to [the google spreadsheet](https://docs.google.com/spreadsheets/d/1vTla34lK53UFgDouSKHVU4uz2mYWKU7Ib8KsNG7ARu4/edit#gid=0). You'll need a new sheet for your year (eg; `2018`). NOTE: Make sure pictures links are imgur. Drive links require more work than necessary.
4. Download the year's sheet as a `csv` Save it to (eg) `_data/2018.csv`.
5. Run `bin/newimport.py _data/2018.csv`.
5. Ring many bells with jubilation.

---

### To develop:

`bundle exec jekyll serve --watch`

---

### To deploy an updated version:


```sh
git add .
git commit -m "My description of changes"
git checkout gh-pages
git merge master
git commit --allow-empty -m "Deploying to Github Pages at `date`"
git push
git checkout master
```

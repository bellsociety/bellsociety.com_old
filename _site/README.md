
# BellSociety.com

This is a guide on how to update the information on this site. We use [Jekyll](http://jekyllrb.com/); please familiarize yourself with the framework if you're planning to perform maintenance. It's a simple system and should take about an hour to get up to speed with if you know the computers.

---

### To add a new Year's worth of Members:

I will use the example year `2032` (ie; you graduate in 2032) with two members, `Will Jahbs` and `Stephen Gaits`. Hopefully this adds clarity.

1. Add a folder named `2032` to the `_members` folder.
2. Add a folder named `2032` to the `images/members` folder.
3. Copy `_members/2014/index.md` into `_members/2032`. Update the year to `2032`.
4. Add `2032` to the `collections: members: years:` list in `_config.yaml`. It'll make sense when you look.
5. Change the `current_year` in `_config.yaml` to the current year. This one was a toughie.
6. Tell members to add themselves (below).
 - Not sure how to manage github access. This might be an unnecessary pain. You may need to do the brunt of this work yourself. In fact, you almost definitely should.
7. Ring many bells with jubilation.

---

### To add yourself as a member:

I will use the example graduating year of `2032` and pretend your name is `Will Jahbs`. Hopefully this adds clarity.

1. In the folder `_members/2032`, add a file called `will_jahbs.md`.
  - You can do this through the github web interface: go to this link (**replacing 2032**):
  [`https://github.com/bellsociety/bellsociety.com/new/master/_members/2032`](https://github.com/bellsociety/bellsociety.com/new/master/_members/2032).
2. Copy the contents of [_members/2014/alex_rattray.md](https://raw.githubusercontent.com/bellsociety/bellsociety.com/master/_members/2014/alex_rattray.md) into it.
3. Customize! Replace Alex's stuff with your own. You may leave things blank.
  - (For the curious, the stuff between the `---`'s at the top is yaml, and below that is markdown)
4. If you'd like, add a custom bio down below the lower `---`. Write in Markdown (it's easy!!!).
5. Add a jpeg of your pretty face to `images/members/2032` with a filename of `will_jahbs.jpeg`
  - The file format must be `.jpeg`, not `.jpg` or `.png` or `.anythingelse`.
  - The file name must otherwise exactly match the `will_jahbs.md` in `_members/year/2032`.
  - (This is because Alex, the original creator, was feeling hacky. You could fix this if you felt like it, but consistency can be nice sometimes.)
  - Uploading images isn't possible through the github website =( so you'll probably want to email/dropbox/whatever your photo to someone who has admin privileges, and make them upload it with git. Thank them with a big hug.
6. Ring many bells with jubilation.


---

### To develop:

1. `gem install jekyll`
2. `jekyll serve --watch`
3. Go to `localhost:4000` in your browser.

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
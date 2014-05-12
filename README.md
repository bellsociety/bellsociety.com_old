
# BellSociety.com

This is a guide on how to update the information on this site. We use [Jekyll](http://jekyllrb.com/); please familiarize yourself with the framework if you're planning to perform maintenance. It's a simple system and should take about an hour to get up to speed with if you know the computers.

---

### To add a new Year's worth of Members:

I will use the example `2032` with two members, `Will Jawbs` and `Stephen Gaits`. Hopefully this adds clarity.

1. Add a folder named `2032` to the `_members` folder.
2. Add a folder named `2032` to the `images/members` folder.
3. Copy `_members/2014/index.md` into `_members/2032`. Update the year to `2032`.
4. Add `2032` to the `collections: members: years:` list in `_config.yaml`. It'll make sense when you look.
5. Tell members to add themselves (below) `.md` files to add whatever content they feel like, html-style. Not sure how to manage github access. This might be an unnecessary pain.
6. Ring many bells with jubilation.

---

### To add yourself as a member:

I will use the example `2032` and pretend your name is `Will Jawbs`. Hopefully this adds clarity.

1. In the folder `_members/2032`, add a file called `will_jawbs.md`.
2. Copy the contents of `_members/2014/alex_rattray.md` into it, and delete everything that follows a colon in the stuff at the top (between the `---`'s). Except `layout` and `is_member`. Leave that stuff as is.
3. Replace all those blank slots with your info, dude!
4. If you'd like, add a custom bio down below the lower `---`.
  - It's in Markdown or HTML. You can write Markdown or HTML, right? (If not, just write words and it'll be fine. Or ask a friend. Then it'll definitely be fine).
2. Add a jpeg of your pretty face to `images/members/2032` with a filename of `will_jawbs.jpeg`. The file format must be `jpeg`, not `jpg` or `png` or `anythingelse`. The file name must otherwise exactly match the `will_jawbs.md` in `_members/year/2032`.
  - (This is because Alex, the original creator, was feeling hacky. You could fix this if you felt like it, but consistency can be nice sometimes.)




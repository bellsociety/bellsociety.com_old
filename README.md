
# BellSociety.com

This is a guide on how to update the information on this site. We use [Jekyll](http://jekyllrb.com/); please familiarize yourself with the framework if you're planning to perform maintenance. It's a simple system and should take about an hour to get up to speed with if you know the computers.

---

### To add a new Year's worth of Members:

I will use the example `2032` with two members, `Will Jawbs` and `Stephen Gaits`. Hopefully this adds clarity.

1. Add a folder named `2032` to the `_members` folder.
2. Add a folder named `2032` to the `images/members` folder.
3. Copy `_members/2014/index.md` into `_members/2032`. Update the year to `2032`.
4. Add a file for each member into `_members/2032`, with the format `stephen_gaits.md`. Each should be a copy of `_members/2014/alex_rattray.md`. Update their information, and clear the html (the part below the second `---` at the top). Members update this themselves.
5. Add a jpeg of each member into `images/members/2032` with a name formatted as `stephen_gaits.jpeg`. The file format must be `jpeg`, not `jpg` or `png` or `anythingelse`. This is because Alex, the original creator, was feeling hacky. You could fix this if you felt like it, but consistency can be nice sometimes.
6. Tell members to modify their `.md` files to add whatever content they feel like, html-style. Not sure how to manage github access. This might be an unnecessary pain.
7. Add `2032` to the `collections: members: years:` list in `_config.yaml`.




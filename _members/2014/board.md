---
layout: default
is_member: false
year: 2014
---

<h1 class="cover-heading">
  Bell {{ page.year }} Board Members
</h1>
<br>

<div class="row">
  {% for member in site.members %}
    {% if member.year == page.year and member.board_position %}
      <div class="col-xs-6 col-md-3">
        {% assign size = 'small' %}
        {% include profile.html %}
      </div>
    {% endif %}
  {% endfor %}
</div>
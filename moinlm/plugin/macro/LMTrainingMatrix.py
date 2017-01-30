"""LMTrainingMatrix

Macro for displaying days elapsed since users have documented that
they have read specified pages.

Options:

* pattern - a regular expression limiting the list of pages to be displayed
* users - name of a Group page specifying a set of users to display
* show_missing - if 'yes', diplay pages that have been deleted or renamed
* max_days - number of days within which a page should have been read
* show_help - if 'yes', print this help text

"""

from operator import attrgetter
import re

from jinja2 import Template
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from moinlm.training import read_training_log
from moinlm.utils import pivot

Dependencies = ["time"]


def decorate(request, table, show_missing=False):
    for row in table:
        page = Page(request, row[0])
        if show_missing or page.exists():
            row[0] = page.link_to(request)
            yield row


def group_from_page(request, pagename):
    page = Page(request, pagename)
    if not page.exists():
        raise ValueError('The page "{}" does not exist'.format(pagename))
    return {line.split()[-1]
            for line in page.get_body().splitlines()
            if line.strip().startswith('*')}


def main(macro, pattern=None, users=None, show_missing=False, max_days=365,
         show_help=False):

    if show_help:
        return '<pre>{}</pre>'.format(__doc__)

    request = macro.request

    fields, rows = read_training_log(request)
    if pattern:
        rows = [row for row in rows if re.search(r'' + pattern, row.pagename)]

    if users:
        colnames = group_from_page(request, users)
        user_page_link = Page(request, users).link_to(request)
    else:
        colnames = None
        user_page_link = None

    try:
        max_days = int(max_days)
    except ValueError:
        raise ValueError('max_days must be an integer')

    table = pivot(rows,
                  rowattr='pagename',
                  colattr='user',
                  cellfun=attrgetter('elapsed_days'),
                  nullval='',
                  colnames=colnames)

    header = next(table)
    table = decorate(request, table, show_missing=show_missing)

    def highlight(val):
        if not val:
            return 'missing'
        elif val > max_days:
            return 'old'
        else:
            return 'ok'

    template = Template("""
{% set cell_width = '1em' %}
<style>
  table.training {
  }
  th.rotate {
  -webkit-transform: rotate(90deg);
  -moz-transform: rotate(90deg);
  -ms-transform: rotate(90deg);
  -o-transform: rotate(90deg);
  transform: rotate(90deg) translatex(-6.75em) translatey(2.1em);
  transform-origin: left bottom;
  height: 6em;
  font-family: "Lucida Console", Monaco, monospace;
  }
  div.rotate {
  max-width: {{ cell_width }};
  min-width: {{ cell_width }};
  }
  td.training {
  max-width: {{ cell_width }};
  min-width: {{ cell_width }};
  font-size: 75%;
  }
  td.training-odd {
  opacity: 0.6;
  }
  td.missing { background-color: #d2d4d8;}
  td.ok {color: white; background-color: green;}
  td.old {color: yellow; background-color: yellow;}
</style>
<div>
  <ul>
    <li>Each cell shows the elapsed time in days since each page was read</li>
    {% if pattern %}
      <li>Pages listed below match the pattern <strong>"{{ pattern }}"</strong></li>
    {% endif %}
    {% if user_page_link %}
      <li>Only users listed in {{ user_page_link | safe}} are shown</li>
    {% endif %}
    <li>Pages that <strong>no longer exist</strong> are
      {% if show_missing %}
	<strong>included</strong> (gray links)
      {% else %}
	<strong>excluded</strong>
      {% endif %}
    </li>
    <li>Cells are green when a page has been read within
      <strong>{{ max_days }}</strong> days</li>
  </ul>

  <table class="training">
    <tr>
      <th style="width: 30em;"></th>
      {% for name in header[1:] %}
	<th class="rotate"><div class="rotate" >{{ name }}</div></th>
      {% endfor %}
    </tr>

    {% for row in rows %}
      <tr>
	<td nowrap>{{ row[0] }}</td>
	{% for val in row[1:] %}
	  <td class="training {{ highlight(val) }} {% if loop.index is divisibleby(2) %} training-odd{% endif %}">
	    {{ val }}
	  </td>
	  {% endfor %}
      </tr>
    {% endfor %}
  </table>
</div>
    """)

    msg = template.render(
        header=header,
        rows=table,
        user_page_link=user_page_link,
        pattern=pattern,
        show_missing=show_missing,
        highlight=highlight,
        max_days=max_days,
    )
    return msg


def execute(macro, argstr):
    try:
        args, kwargs, trailing = wikiutil.parse_quoted_separated(argstr or u'')
        if trailing:
            raise ValueError('trailing arguments are not allowed')
        return main(macro, *args, **kwargs)
    except Exception, err:
        return macro.request.formatter.text(
            "<<LMTrainingMatrix: %s>>" % err.args[0], style="color:red")

"""

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


def main(macro, pattern=None, users=None, show_missing=False):
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

    table = pivot(rows,
                  rowattr='pagename',
                  colattr='user',
                  cellfun=attrgetter('elapsed_days'),
                  nullval='',
                  colnames=colnames)

    header = next(table)
    table = decorate(request, table, show_missing=show_missing)

    template = Template("""
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
  </ul>
  <table>
    <tr>
      {% for name in header %}
	<th>{{ name }}</th>
      {% endfor %}
    </tr>

    {% for row in rows %}
      <tr>
	<td nowrap>{{ row[0] }}</td>
	{% for val in row[1:] %}
	  <td>{{ val }}</td>
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

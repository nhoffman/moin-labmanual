"""

"""

from operator import attrgetter

from jinja2 import Template
from MoinMoin import wikiutil
from moinlm.training import read_training_log
from moinlm.utils import pivot

Dependencies = ["time"]


def main(macro, pattern):
    request = macro.request

    fields, rows = read_training_log(request)
    table = pivot(rows,
                  rowattr='pagename',
                  colattr='user',
                  cellfun=attrgetter('elapsed_days'),
                  nullval='')

    header = next(table)

    template = Template("""
<table>
  <tr>
    {% for name in header %}
      <th>{{ name }}</th>
    {% endfor %}
  </tr>

  {% for row in rows %}
    <tr>
      <td>{{ row[0] }}</td>
      {% for val in row[1:] %}
	<td>{{ val }}</td>
      {% endfor %}
    </tr>
  {% endfor %}
</table>
    """)

    msg = template.render(header=header, rows=table)
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

"""Functions for recording and displaying attestation of training.

"""

from os import path
import sqlite3
from itertools import groupby
from operator import itemgetter

from jinja2 import Template

TRAINING_DB_NAME = 'training_log.sqlite3'


class TrainingDB(object):
    def __init__(self, request, db_path=None):
        self.db_path = db_path or path.join(request.cfg.data_dir, TRAINING_DB_NAME)
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.create_db()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.close()

    def create_db(self):
        sql = """
        create table if not exists training
        (pagename text,
         rev integer,
         user text,
         timestamp DATE DEFAULT CURRENT_TIMESTAMP)
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def add_record(self, **kwargs):
        keys, values = zip(*kwargs.items())
        sql = 'insert into training ({}) values ({})'.format(
            ', '.join(keys),
            ', '.join(['?'] * len(keys))
        )
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()

    def get_records(self, pagename=None):
        template = Template("""
        select
          {% if not pagename %}pagename, {% endif %}
          date(datetime(timestamp, "localtime")) as date,
          cast(round(0.499999 + julianday('now') - julianday(timestamp)) as integer)
            as elapsed_days,
          rev as revision,
          user
        from training
        {% if pagename %}where pagename = ?{% endif %}
        order by user, timestamp desc
        """)

        sql = template.render(pagename=pagename)
        cur = self.conn.cursor()

        if pagename:
            cur.execute(sql, (pagename,))
        else:
            cur.execute(sql)

        header = [col[0] for col in cur.description]
        return header, list(cur.fetchall())


def read_training_log(request, pagename=None):
    """Return (header, rows) for all training records, or for those
    matching pagename if provided.

    """
    with TrainingDB(request) as db:
        header, rows = db.get_records(pagename=pagename)
        most_recent = [next(grp) for user, grp in groupby(rows, itemgetter(-1))]
        return header, sorted(most_recent)


def record_training(request, **kwargs):
    with TrainingDB(request) as db:
        db.add_record(**kwargs)

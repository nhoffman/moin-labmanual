"""Functions for recording and displaying attestation of training.

"""

from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor

traininglog_fields = ['pagename', 'rev', 'user', 'timestamp']
traininglog_delim = ';'
traininglog_name = u"TrainingLog"


def read_training_log(request, pagename=None):
    logpage = Page(request, traininglog_name)
    lines = logpage.getlines()

    for line in lines:
        if not line.strip() or line.startswith('#'):
            continue

        d = dict(zip(traininglog_fields, line.split(traininglog_delim)))
        if not pagename:
            yield d
        elif d.get('pagename') == pagename:
            yield d


def record_training(request, page_info):
    editor = PageEditor(request, traininglog_name, do_revision_backup=0)
    raw_body = editor.get_raw_body_str()
    new_line = traininglog_delim.join(page_info[f] for f in traininglog_fields)
    editor.saveText(newtext=raw_body.strip() + '\n' + new_line, rev=0)

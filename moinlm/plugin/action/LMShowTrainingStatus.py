# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action reads tabular data in the page TrainingLog and shows
    lines matching the current page.
"""

from MoinMoin.Page import Page
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget

from moinlm.training import read_training_log


def execute(pagename, request):

    _ = request.getText

    fields, loglines = read_training_log(request, pagename)

    if loglines:
        logtd = TupleDataset()
        logtd.columns = [
            Column(field, label=_(field, formatted=False), align='left')
            for field in fields
        ]

        for line in loglines:
            logtd.addRow(line)

        log_table = DataBrowserWidget(request)
        log_table.setData(logtd)

        msg = """
        <p>The <strong>most recent</strong> record for each user is shown</p>
        """

        request.theme.add_msg(msg + log_table.render())
    else:
        request.theme.add_msg(_('No training records for this page'))

    Page(request, pagename).send_page()

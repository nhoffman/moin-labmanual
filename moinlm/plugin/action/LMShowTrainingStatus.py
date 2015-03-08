# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action reads tabular data in the page TrainingLog and shows
    lines matching the current page.

    @copyright: 2008 Noah Hoffman <ngh2@u.washington.edu>
    @license: UW Free Fork
"""

import os, re
from MoinMoin import config, wikiutil
from MoinMoin.Page import Page
from MoinMoin.util import timefuncs
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget
from MoinMoin.widget import html

from lmWriteTrainingLog import read_training_log, traininglog_fields

def execute(pagename, request):

    _ = request.getText
    user = request.user

    loglines = list(read_training_log(request, pagename))

    if loglines:
        logtd = TupleDataset()
        logtd.columns = []
        for field in traininglog_fields:
            logtd.columns.append(
                Column(field, label=_(field, formatted=False), align='left')
                )

        for line in loglines:
            logtd.addRow(tuple(line[f] for f in traininglog_fields))

        log_table = DataBrowserWidget(request)
        log_table.setData(logtd)
        request.theme.add_msg(log_table.render())
    else:
        request.theme.add_msg(_('No training records for this page'))


    Page(request, pagename).send_page()


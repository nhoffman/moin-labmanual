from MoinMoin.search.Xapian.search import XapianSearch
from MoinMoin.search.builtin import MoinSearch
import logging


def _search_no_attachment(self):
    """Search using Xapian

    Get a list of pages using fast xapian search and
    return moin search in those pages if needed.

    replaces MoinMoin.search.Xapian.search.XapianSearch._search() and
    removes attachments.

    """

    clock = self.request.clock
    index = self.index

    clock.start('_xapianSearch')
    clock.start('_xapianQuery')
    search_results = index.search(self.query, sort=self.sort,
                                  historysearch=self.historysearch)
    clock.stop('_xapianQuery')
    logging.debug("_xapianSearch: finds: %r" % search_results)

    # Note: .data is (un)pickled inside xappy, so we get back exactly what
    #       we had put into it at indexing time (including unicode objects).
    pages = [{'uid': r.id,
              'wikiname': r.data['wikiname'][0],
              'pagename': r.data['pagename'][0],
              'attachment': r.data['attachment'][0],
              'revision': r.data.get('revision', [0])[0]}
             for r in search_results]

    # remove pages representing attachments from results
    pages = [page for page in pages if not page['attachment']]

    try:
        if not self.query.xapian_need_postproc():
            # xapian handled the full query
            clock.start('_xapianProcess')
            try:
                _ = self.request.getText
                return self._getHits(pages), \
                    (search_results.estimate_is_exact and '' or _('about'),
                     search_results.matches_estimated)
            finally:
                clock.stop('_xapianProcess')
    finally:
        clock.stop('_xapianSearch')

    # some postprocessing by MoinSearch is required
    return MoinSearch(self.request, self.query, self.sort, self.mtime,
                      self.historysearch, pages=pages)._search()


def monkey_patch_xapian_search():
    """Apply the patch to suppress listing of attchments. Add this line to
    the wiki config:

    moinlm.monkey_patches.monkey_patch_xapian_search()

    """

    XapianSearch._search = _search_no_attachment

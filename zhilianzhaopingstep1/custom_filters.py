from scrapy.dupefilters import RFPDupeFilter
import os
import logging
#from scrapy import loging
# from scrapy.utils.job import job_dir
# from scrapy.utils.request import request_fingerprint

class CustomURLFilter(RFPDupeFilter):
    """ 只根据url去重"""

    def __init__(self, path=None, debug=False):
        self.urls_seen = set()
        #self.debug = debug
        #RFPDupeFilter.__init__(self, path)
        self.file = None
        #self.fingerprints = set()
        self.logdupes = True
        self.debug = debug
        if path:
            self.file = open(os.path.join(path, 'requestsurl.seen'), 'a+')
            self.urls_seen.update(x.rstrip() for x in self.file)

    def request_seen(self, request):
        # if request.url in self.urls_seen:
        #     return True
        # else:
        #     self.urls_seen.add(request.url)

        #fp = self.request_fingerprint(request)
        if request.url in self.urls_seen:
            return True
        self.urls_seen.add(request.url)
        if self.file:
            self.file.write(request.url + os.linesep)

        def close(self, reason):
            if self.file:
                self.file.close()

        def log(self, request, spider):
            if self.debug:
                fmt = "Filtered duplicate request: %(request)s"
                log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)
            elif self.logdupes:
                fmt = ("Filtered duplicate request: %(request)s"
                       " - no more duplicates will be shown"
                       " (see DUPEFILTER_DEBUG to show all duplicates)")
                log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)
                self.logdupes = False

       # spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
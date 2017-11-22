from __future__ import print_function
import os
import logging
import re
import time

from scrapy.utils.job import job_dir
from scrapy.utils.request import request_fingerprint


class BaseDupeFilter(object):

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        return False

    def open(self):  # can return deferred
        pass

    def close(self, reason):  # can return a deferred
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass


class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path=None, debug=False):
        self.file = None
        self.fileurl = None
        self.fingerprints = set()
        self.urls_seen = set()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if path:
            self.file = open(os.path.join(path, 'requests.seen'), 'a+')
            self.fileurl = open(os.path.join(path,'requestsurl.seen'),'a+')
            self.file.seek(0)
            self.fingerprints.update(x.rstrip() for x in self.file)
            # self.urls_seen.update(x.rstrip() for x in self.fileurl)

    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(job_dir(settings), debug)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if re.findall('sou.zhaopin.com',request.url):
            if self.file:
                self.file.write(os.linesep)
                self.fileurl.write(os.linesep)
        else:
            if self.file:
                self.file.write(fp + os.linesep)
                self.fileurl.write(request.url + os.linesep)

        # self.urls_seen.add(request.url)
        # if re.findall('sou.zhaopin.com',request.url):
            # if self.fileurl:
               # self.fileurl.write(os.linesep)
        # else:
            # if self.fileurl:
                # self.fileurl.write(request.url + os.linesep)
                # self.fileurl.write(request.url + os.linesep)

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def close(self, reason):
        if self.file:
            self.file.write(time.strftime('----------%Y-%m-%d %H:%M:%S---------',time.localtime(time.time())) + os.linesep)
            self.fileurl.write(time.strftime('----------%Y-%m-%d %H:%M:%S---------',time.localtime(time.time())) + os.linesep)
            self.file.close()

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

from __future__ import print_function

import requests
from w3lib.encoding import html_to_unicode
from htmls import DomTreeBuilder
from mdr import MiningDataRegion, MiningDataRecord, MiningDataField,Region



class Depta(object):
    def __init__(self, threshold=0.7, k=5):
        self.threshold = threshold
        self.k = k
    def extract(self, html='', **kwargs):
        Region.now=0
        
        """
        extract data field from raw html or from a url.
        """
        if not html and 'url' in kwargs:
            url=kwargs.pop('url')
            r = requests.get(url)
            Region.url=url
            _, html = html_to_unicode(r.headers.get('content-type'), r.content)

        builder = DomTreeBuilder(html)
        root = builder.build()

        region_finder = MiningDataRegion(root, self.k, self.threshold)
        regions = region_finder.find_regions(root)

        record_finder = MiningDataRecord(self.threshold)
        field_finder = MiningDataField()

        for region in regions:
            #print (region)
            records = record_finder.find_records(region)
            items, _ = field_finder.align_records(records)
            region.items = items
            # print (items)
            if 'verbose' in kwargs:
                print(region)
                for record in records:
                    print('\t', record)

        return regions


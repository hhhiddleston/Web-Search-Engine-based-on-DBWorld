from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.qparser.dateparse import DateParserPlugin
import sys

class DBworldSearcher:

    def __init__(self, indexdir, fieldlist=["subject", "content"]):
        self.indexdir = indexdir
        ix = open_dir(indexdir)

        #self.parser = QueryParser("subject", self.ix.schema)
        self.parser = MultifieldParser(fieldlist, ix.schema)
        self.parser.add_plugin(DateParserPlugin())
        self.searcher = ix.searcher()

    def search(self, querytext, limit):
        myquery = self.parser.parse(querytext)
        results = self.searcher.search(myquery, limit=limit)
        return results

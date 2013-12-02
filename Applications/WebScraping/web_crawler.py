""" TODO:
add __init__ params: (note: some of these are \problems to write for students)
    allowed_domains
    seed_urls
    index_fxn
find better seed url (create a sandbox?)
make it a polite bot? (i.e. reads robots.txt, avoids bot traps)
comment stuff
"""
from pprint import pprint
import re
import itertools as itt


class WebCrawler:
    """ A very basic but functional web crawler.
    Indexes webpages by the words they contain.
    """
    def __init__(self):
        self.index = {}
        self.urls_crawled = set()

    def crawl(self, seed_url, max_depth):
        assert max_depth is not None and max_depth <= 3, "Your max_depth is dangerously (i.e., arbitrarily) large. Calm down."
        next_level = set([seed_url])
        depth_counter = xrange(max_depth+1) if max_depth != None else itt.count()
        for _ in depth_counter:
            if not next_level: # quit early if we have no links left to follow
                break
            next_level = self._crawl_one_deep(next_level) 

    def _crawl_one_deep(self, urls_to_index):
        next_level = set()
        for url in (urls_to_index - self.urls_crawled):
            print "Crawling URL:", url
            page = self.get_page(url)
            next_level.update(set(self.gen_all_links(page)))
            self.update_index(url, page)
            self.urls_crawled.add(url)
        return next_level

    def get_page(self, url):
        """ Takes in a URL and returns a string composed of that URL's HTML text.
            Returns an empty string if the webpage could not be retrieved.
        """
        try:
            import urllib
            return urllib.urlopen(url).read()
        except:
            print
            print "*** Error opening URL '%s'. ***" % url
            print
            return ""

    def get_content(self, page): # TODO probably make this fxn the default param for index_fxn
        for word in re.split(r"\W", page): # TODO improve this word finder; maybe anything not in tags?
            if word:
                yield word.lower()

    def update_index(self, url, page):
        for word in self.get_content(page):
            try:
                # print "Updating word:", repr(word), url
                self.index[word].update(set([url]))
            except KeyError:
                # print "Adding new word:", word
                self.index[word] = set([url])

    def gen_all_links(self, page):
        """ Given a string page, generates all urls that are linked from this page
            page should be an HTML text file, not a URL.
        """
        pos = -1
        try:
            while True:
                start_link = page.index('<a href=', pos+1)
                url_start = page.index('"', start_link)+1
                pos = url_end = page.index('"', url_start)
                yield page[url_start:url_end]
        except ValueError: # we've found all the links found
            pass


crawler = WebCrawler()
crawler.crawl("http://students.cs.byu.edu/~ahuff44/testing", max_depth=1)

pprint(crawler.index)

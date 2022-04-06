import urllib.parse
import urllib.request
import json

def words(context):
    """ Convert word array to string. """
    return " ".join(context['word'])

def search(cqlQuery):
    """ Search and show hits. """
    url = "http://opensonar.ato.inl.nl/blacklab-server" + \
        "/zeebrieven/hits?patt=" + urllib.parse.quote_plus(cqlQuery) + \
        "&outputformat=json&wordsaroundhit=3"
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    hits = response['hits']
    docs = response['docInfos']
    for hit in hits:
        # Show the document title and hit information
        doc = docs[hit['docPid']]
        print ('%25s  %-15s %-25s (%s)' % \
            (words(hit['left']), words(hit['match']), words(hit['right']),\
            doc['title']))

# "Main program"
search('[pos="PRN"] "schip"')

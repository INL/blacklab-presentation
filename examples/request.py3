from urllib.parse import quote_plus as urlencode
from urllib.request import urlopen
import json

def words(context):
    """ Convert word array to string. """
    return " ".join(context['word'])

def make_url(corpus, req_type, param):
    """ Build a BLS URL. """
    paramparts = [urlencode(k) + "=" + urlencode(str(v)) for (k, v) in param.items() if v is not None]
    urlpar = "&".join(paramparts)
    return "http://opensonar.ato.inl.nl/blacklab-server" + \
        "/" + corpus + "/" + req_type + "?" + urlpar

def request(corpus, req_type, param):
    """ Make a request to BLS and return the JSON structure. """
    if 'outputformat' not in param:
        param['outputformat'] = 'json'
    url = make_url(corpus, req_type, param)
    #print(url)
    f = urlopen(url)
    return json.loads(f.read().decode('utf-8'))

def concordances(cql_query):
    """ Show concordances (KWICs) for CQL query. """
    response = request("zeebrieven", "hits", {
        'patt': cql_query,
        'wordsaroundhit': '3'
    })
    hits = response['hits']
    docs = response['docInfos']
    print('Concordances for ' + cql_query + ':')
    for hit in hits:
        # Show the document title and hit information
        doc = docs[hit['docPid']]
        print ('%25s  %-15s %-25s (%s)' % \
            (words(hit['left']), words(hit['match']), words(hit['right']),\
            doc['title']))
    print()

def group(title, cql_query, group_by, param = {}):
    """ Show frequency lists for alternative matches. """
    
    # If a CQL query was specified, this is a hits request;
    # otherwise, it's a docs request.
    is_hits = cql_query is not None
    req_type = "hits" if is_hits else "docs"
    result_el = "hitGroups" if is_hits else "docGroups"

    if is_hits:
        param['patt'] = cql_query
    param['group'] = group_by
    if 'number' not in param:
        param['number'] = 10   # limit to 10 groups unless specified
    response = request("zeebrieven", req_type, param)
    groups = response[result_el]
    if is_hits:
        print('%s - %s' % (title, cql_query) )
    else:
        print(title)
    for group in groups:
        print ('  %-20s %4d' % (group['identityDisplay'], group['size']))
    print()

# Find concordances (KWICs) for a CQL query
concordances('[pos="PRN"] "schip"')
concordances('[lemma="groot"] [pos="NOU"]')

""" Show frequency lists for alternative matches. """
group('Spelling variations', '[lemma="water"]', "hit:word:i")
group('Starts with...', '[word="sch(ee?|i)p.*"]', "hit:word:i")
group('Adjectives for a word', '[pos="ADJ"] [lemma="schip"]', "hit:lemma:i")
group('Who\'s the sweetest?', '[lemma="lief"]', "wordright:lemma:i")
group('Documents by year', None, "field:witnessYear_from", {'number': 100, 'sort': 'identity'})

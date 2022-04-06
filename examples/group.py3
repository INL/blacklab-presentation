import urllib.parse
import urllib.request
import json

def words(context):
    """ Convert word array to string. """
    return " ".join(context['word'])

def group(title, cqlQuery, groupBy):
    """ Search and show hits. """
    url = "http://opensonar.ato.inl.nl/blacklab-server" + \
        "/zeebrieven/hits?group=" + groupBy + "&patt=" + \
        urllib.parse.quote_plus(cqlQuery) + "&outputformat=json"
    f = urllib.request.urlopen(url)
    response = json.loads(f.read().decode('utf-8'))
    groups = response['hitGroups']
    print(title)
    for group in groups[0:10]:
        print ('  %-20s %4d' % (group['identityDisplay'], group['size']))
    print()

# "Main program"
group('Spellingvariatie water', '[lemma="water"]',             "hit:word:i")
group('Begint met schip/scheep','[word="sch(ee|i)p.*"]',       "hit:word:i")
group('Adjectieven bij schip',  '[pos="ADJ"] [lemma="schip"]', "hit:lemma:i")
group('Wie is lief?',           '[lemma="lief"] [pos="NOU"]',  "hit:lemma:i")

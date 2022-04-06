# Webserviceontwerp: BlackLab

---

# SOAP of REST?

SOAP:
- ingewikkeld, zwaar, veel features
- weinig gebruikt in publieke APIs, veel gebruikt in grote bedrijven (Oracle, SAP, IBM)
- "opdracht"-model: doe A met X, doe B met Y, doe C met Z.

REST:
- simpel, licht, weinig features
- zeer populair (75% +) in publieke APIs, open source en
  kleinere organisaties
- "resource"-model: URLs komen overeen met resources die je opvraagt, wijzigt, toevoegt en verwijdert.

Wij hebben gekozen voor RESTful webservices.

---

# Wat maakt een webservice RESTful?

URLs zijn paden naar resources.

Dus niet:  
>`http://api.inl.nl/org?view=project&name=Molechaser`

Maar:  
>`http://api.inl.nl/org/projects/Molechaser`

---

# Wat maakt een webservice RESTful?

Logische URLs retourneren logische resultaten.

Lijst beschikbare corpora:
>`http://api.inl.nl/bls/`

Informatie over het CHN (grootte, velden, etc):
>`http://api.inl.nl/bls/chn`

Informatie over het veld auteur in het CHN:
>`http://api.inl.nl/bls/chn/fields/author`

---

# Wat maakt een webservice RESTful?

Zoek-URLs werken met GET-variabelen.

Alle documenten in het CHN:
>`http://api.inl.nl/bls/chn/docs/`

Gefilterde lijst van documenten:
>`http://api.inl.nl/bls/chn/docs/?author=Kluun`

Hits van het woord "schip":
>`http://api.inl.nl/bls/chn/hits/?patt="schip"`

Hits van het woord "schip":
>`http://api.inl.nl/bls/chn/hits/?patt="schip"`

---

# Wat maakt een webservice RESTful?

HTTP methods bepalen de uit te voeren aktie.

        POST    Resource maken, retourneert de nieuwe URI

        PUT     Resource maken/wijzigen, client geeft de URI op

        GET     Resource opvragen

        DELETE  Resource verwijderen

---

# Wat maakt een webservice RESTful?

## Voorbeelden HTTP methods (1)

Creeer een nieuw corpus:
>`POST   http://api.inl.nl/bls/chn`<br>

Informatie over corpus:
>`GET    http://api.inl.nl/bls/chn`

Verwijder corpus:
>`DELETE http://api.inl.nl/bls/chn`

---

# Operaties in BlackLab Server

## Voorbeelden HTTP methods (2)

Voeg documenten toe:
>`PUT    http://apis.inl.nl/bls/chn/docs/`

Verwijder documenten:
>`DELETE http://apis.inl.nl/bls/chn/docs/?author=Kluun`

Verwijder document:
>`DELETE http://apis.inl.nl/bls/chn/docs/123`

Update document:
>`POST   http://apis.inl.nl/bls/chn/docs/123`

---

# Wat maakt een webservice RESTful?

HTTP Accept header bepaalt wat er geretourneerd wordt (bijv. JSON of XML)

<table>
<tr><th>Formaat</th><th>HTTP Accept</th></tr>
<tr><td>XML</td><td>application/xml</td></tr>
<tr><td>JSON</td><td>application/json</td></tr>
<tr><td>JSONP</td><td>application/javascript</td></tr>
</table>

**N.B.** er bestaan andere MIME types voor JSON/XML; het is verstandig om te matchen op string "xml", "json" of "javascript".

Handig: ondersteun ook "outputformat" parameter voor clients die geen HTTP Accept header kunnen zetten.

---

# Wat maakt een webservice RESTful?

Stateless.

Niet:
>`http://.../bls/chn/hits?resultset=93485&first=50`<br>
(niet bookmarkable want tijdelijk)

Maar:
>`http://.../bls/chn/hits?patt="schip"&filter=author:Kluun&first=50`<br>

---

# XML vs. JSON

XML:
- XSLT, Xpath, XML Schema, etc.
- Veel tools beschikbaar

JSON:
- Makkelijk in code te gebruiken
- Mapt triviaal naar native datastructures

Beiden hebben voordelen; waarom kiezen?

---

# Webservice + single-page application

- Herlaadt de pagina niet, maar doet AJAX requests naar de webservice.
- Werkt de pagina steeds bij aan de hand van het JSON/XML antwoord.
- Simpel: alleen HTML, CSS & Javascript.
- Belangrijk: history.pushState() voor bookmarkability!
- Betere gebruikerservaring, minder zwaar voor server, beter onderhoudbaar.

---

# EINDE DEEL 1

---


---

# Hoe output genereren?

Print statements / template system:
- Je vergeet makkelijk values te escapen
- Vrij omslachtig voor hierarchische structuren
- Te breekbaar voor grotere projecten

Object serialization (bijv. Jersey):
- Zet automagisch classes om in XML/JSON
- Je moet dus wel classes hebben voor alle te retourneren data.
- Als data uit database komt, moet je dus ORM doen

BLS aanpak:
- eenvoudig te customizen per geval
- geen ORM/classes nodig als tussenvorm, wel output code
- met nieuwe aanpak (DataStream) geen tussentijdse datastructuur nodig

---

# Security

## "Default deny" / "Whitelisting"

Niet:
>"alles mag tenzij het er verdacht uitziet"

Maar:
>"niks mag tenzij ik zeker weet dat het onschuldig is"

---

# Security

## User Input == Devil Input. Valideer zo strikt mogelijk.

Niet:
>"een naam mag geen slashes of pipe symbols bevatten"

Maar:
>"een naam mag alleen letters, cijfers of streepjes bevatten" <br>
(je kunt de eisen later altijd relaxen, strikter maken is lastiger)

---

# Security

## Check autorisatie op elke actie.

Anders is de voordeur gebarricadeerd, maar <br>
de achterdeur staat wagenwijd open.

---

# Security

## Injection attacks (1)

Die treden op als je strings met user input aan elkaar plakt zonder escaping toe te passen.

Kwetsbare code:
>`stmt = "SELECT * FROM person WHERE ID = " + devilInput;`

SQL injection:
>`devilInput == "1; DROP TABLE person"`

Correcte code:
>`stmt = prepare("SELECT * FROM person WHERE ID = ?");<br>
stmt.bind(1, devilInput);

---

# Security

## Injection attacks (2)

Kwetsbaar:
>`print("<p>Viewing person" + devilInput + "</p>");`

HTML injection:
>`devilInput == " Jan<script src="http://ha.xxx/evil.js"></script>"`

Correct:
>`print("<p>Viewing person" + htmlescape(devilInput) + "</p>");`

---

# Security

## Denial of service

Stel limieten in om [unintentional] denial of service attacks te voorkomen.

Dus niet:
>user mag vrij files uploaden

Maar:
>user mag maximaal 10 files uploaden van max. 10MB per stuk

---

# Same Origin Policy problematiek

- AJAX requests moeten in principe naar dezelfde hostname gaan,
  anders houdt de browser ze tegen.

- JSONP biedt uitkomst. Service antwoordt bijv.:
  `jsonp({ "results": [1, 2, 3, 4, 5] });`

- Moderne optie: CORS (Cross-Origin Resource Sharing)
  De webservice geeft aan welke domeinen 'm mogen benaderen.

---

# Character encoding.

Alles in UTF-8:
- HTML pagina's UTF-8 encoding in META tag zetten
- Tomcat (of PHP, ...) configureren voor UTF-8 URLs.
- Databasecommunicatie in UTF-8.
- OutputStream openen met UTF-8 encoding.
- HTTP header Content-Type zetten met UTF-8 encoding.

---

# Diversen

- Gotcha HTTP DELETE: IE7/8 ondersteunt dit niet!
  Als IE7/8-support gewenst is een alternatief bieden (bijv. POST met parameter action=DELETE)
  (maar DELETE zelf ook altijd ondersteunen, dit is de standaard en de toekomst)
- Cache headers: Expires, Cache-Control en evt. Pragma no-cache.
  Tijd in BLS instelbaar. Sommige operaties moeten uiteraard niet cacheable zijn
  (sowieso alleen GET, maar GET van een status die vaak verandert weer niet)
- File uploads. AJAX file upload tegenwoordig ook mogelijk.
- Langere operaties (bijv. indexeren): start, status, abort.
  Evt. zelfs signaal wanneer klaar (bijv. via email)
  BLS: "polling advice" voor applicatie
- Handig voor debuggen: prettyprinting optie
- Diverse performance instellingen


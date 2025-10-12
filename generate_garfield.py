from feedgen.feed import FeedGenerator
from datetime import datetime, timezone, timedelta

print("Script gestart: Ophalen van klassieke C&H strip via GoComics asset server.")

# --- Stap 1: Bepaal welke klassieke strip we vandaag tonen ---

# De strip liep van 18 november 1985 tot 31 december 1995.
start_datum_strip = datetime(1985, 11, 18)
eind_datum_strip = datetime(1995, 12, 31)
totaal_dagen_strip = (eind_datum_strip - start_datum_strip).days + 1

# We gebruiken een vast startpunt om de cyclus voorspelbaar te maken.
start_punt_cyclus = datetime(2020, 1, 1)
vandaag = datetime.now()
dagen_verstreken = (vandaag - start_punt_cyclus).days

# Bereken welke dag in de strip-cyclus het vandaag is.
cyclus_dag_index = dagen_verstreken % totaal_dagen_strip
huidige_strip_datum = start_datum_strip + timedelta(days=cyclus_dag_index)

# Formatteer de datum voor de URL
jaar = huidige_strip_datum.strftime('%Y')
maand = huidige_strip_datum.strftime('%m')
dag = huidige_strip_datum.strftime('%d')
datum_code = huidige_strip_datum.strftime('%y%m%d') # Geeft YYMMDD

# --- NIEUWE LOGICA: Bepaal de juiste bestandsextensie ---
# weekday() geeft 6 terug voor Zondag.
if huidige_strip_datum.weekday() == 6:
    extensie = 'jpg'
    print("Info: De stripdatum is een zondag, dus .jpg wordt gebruikt.")
else:
    extensie = 'gif'
    print("Info: De stripdatum is geen zondag, dus .gif wordt gebruikt.")

# Bouw de correcte, werkende URL op naar de GoComics asset server
# Voorbeeld: https://assets.gocomics.com/comics/ch/1985/11/ch851118.gif
image_url = f"https://assets.gocomics.com/comics/ch/{jaar}/{maand}/ch{datum_code}.{extensie}"

print(f"SUCCES: De URL voor de strip van {huidige_strip_datum.strftime('%Y-%m-%d')} is: {image_url}")


# --- Stap 2: Bouw de RSS-feed ---

# We linken naar de GoComics pagina voor die specifieke datum
comic_page_url = f"https://www.gocomics.com/calvinandhobbes/{jaar}/{maand}/{dag}"

fg = FeedGenerator()
fg.id(comic_page_url)
fg.title('Calvin and Hobbes Strip')
fg.link(href='https://www.gocomics.com/calvinandhobbes', rel='alternate')
fg.description('Een dagelijkse klassieke Calvin and Hobbes strip.')
fg.language('en')

datum_titel = huidige_strip_datum.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url)
fe.title(f'Calvin and Hobbes - {datum_titel}')
fe.link(href=comic_page_url)
# De publicatiedatum in de feed is vandaag, ook al is de strip oud.
fe.pubDate(vandaag.replace(hour=8, minute=0, second=0, microsecond=0).astimezone(timezone.utc))
fe.description(f'<img src="{image_url}" alt="Calvin and Hobbes Strip voor {datum_titel}" />')


# --- Stap 3: Schrijf het XML-bestand weg ---

try:
    fg.rss_file('calvinandhobbes.xml', pretty=True)
    print("SUCCES: 'calvinandhobbes.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)
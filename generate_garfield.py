from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

print("Script gestart: Genereren van de Garfield RSS-feed op basis van datum.")

# --- Stap 1: Genereer de URL voor de strip van vandaag ---

# Haal de huidige datum op
nu = datetime.now(timezone.utc)

# Formatteer de datum naar de structuur die de URL vereist (YYMMDD)
# Voorbeeld: 10 oktober 2025 wordt '251010'
datum_code = nu.strftime('%y%m%d')
jaar = nu.strftime('%Y')

# Bouw de volledige URL op
# Voorbeeld: http://picayune.uclick.com/comics/ga/2025/ga251010.gif
image_url = f"http://picayune.uclick.com/comics/ga/{jaar}/ga{datum_code}.gif"
comic_page_url = f"https://www.gocomics.com/garfield/{jaar}/{nu.strftime('%m')}/{nu.strftime('%d')}"

print(f"SUCCES: De URL voor vandaag is gegenereerd: {image_url}")

# --- Stap 2: Bouw de RSS-feed ---

fg = FeedGenerator()
fg.id(comic_page_url)
fg.title('Garfield Strip')
fg.link(href='https://www.gocomics.com/garfield', rel='alternate')
fg.description('De dagelijkse Garfield strip.')
fg.language('en')

# Formatteer de datum voor de titel van de feed-entry (YYYY-MM-DD)
datum_titel = nu.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url)
fe.title(f'Garfield - {datum_titel}')
fe.link(href=comic_page_url)
fe.pubDate(nu)
fe.description(f'<img src="{image_url}" alt="Garfield Strip voor {datum_titel}" />')

# --- Stap 3: Schrijf het XML-bestand weg ---

try:
    # We noemen het bestand nu 'garfield.xml'
    fg.rss_file('garfield.xml', pretty=True)
    print("SUCCES: 'garfield.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)
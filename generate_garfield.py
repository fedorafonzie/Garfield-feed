from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

print("Script gestart: Genereren van de Garfield RSS-feed op basis van datum.")

# --- Stap 1: Genereer de URL voor de strip van vandaag ---

nu = datetime.now(timezone.utc)

if nu.weekday() == 6:
    extensie = 'jpg'
    mime_type = 'image/jpeg'
    print("INFO: Het is zondag, de extensie wordt .jpg")
else:
    extensie = 'gif'
    mime_type = 'image/gif'
    print(f"INFO: Het is geen zondag (dag {nu.weekday() + 1}), de extensie wordt .gif")

datum_code = nu.strftime('%y%m%d')
jaar = nu.strftime('%Y')

# OPLOSSING 1: Wijzig http naar https in de URL
image_url = f"https://picayune.uclick.com/comics/ga/{jaar}/ga{datum_code}.{extensie}"
comic_page_url = f"https://www.gocomics.com/garfield/{jaar}/{nu.strftime('%m')}/{nu.strftime('%d')}"

print(f"SUCCES: De URL voor vandaag is gegenereerd: {image_url}")

# --- Stap 2: Bouw de RSS-feed ---

fg = FeedGenerator()
fg.id(comic_page_url)
fg.title('Garfield Strip')
fg.link(href='https://www.gocomics.com/garfield', rel='alternate')
fg.description('De dagelijkse Garfield strip.')
fg.language('en')

datum_titel = nu.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url)
fe.title(f'Garfield - {datum_titel}')
fe.link(href=comic_page_url)
fe.pubDate(nu)

# OPLOSSING 2: Gebruik een enclosure voor de afbeelding (standaard RSS specificatie)
fe.enclosure(image_url, 0, mime_type)

# OPLOSSING 3: Gebruik fe.content met type='html' voor de img-tag in plaats van description
fe.content(f'<img src="{image_url}" alt="Garfield Strip voor {datum_titel}" />', type='html')
fe.description(f'Garfield Strip voor {datum_titel}') # Platte tekst als fallback

# --- Stap 3: Schrijf het XML-bestand weg ---

try:
    fg.rss_file('garfield.xml', pretty=True)
    print("SUCCES: 'garfield.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)
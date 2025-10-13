import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

print("Script gestart: Ophalen van de Garfield strip via ArcaMax.")

# De URL van de ArcaMax pagina voor Garfield
COMIC_PAGE_URL = "https://www.arcamax.com/thefunnies/garfield/"
image_url = None

try:
    # --- Stap 1: Haal de pagina op en extraheer de image URL ---
    print(f"Pagina ophalen: {COMIC_PAGE_URL}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    response = requests.get(COMIC_PAGE_URL, headers=headers)
    response.raise_for_status()

    # Gebruik BeautifulSoup om de HTML te parsen
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Zoek naar de <img> tag met id="comic-zoom"
    img_tag = soup.find('img', id='comic-zoom')
    
    if img_tag and img_tag.has_attr('src'):
        image_url = img_tag['src']
        print(f"SUCCES: Afbeelding URL gevonden: {image_url}")
    else:
        raise ValueError("Kon de <img> tag met id='comic-zoom' niet vinden.")

except (requests.exceptions.RequestException, ValueError) as e:
    print(f"FOUT: Kon de afbeelding niet ophalen. Foutdetails: {e}")
    exit(1)

# --- Stap 2: Bouw de RSS-feed ---

fg = FeedGenerator()
fg.id(COMIC_PAGE_URL)
fg.title('Garfield Comic Strip')
fg.link(href=COMIC_PAGE_URL, rel='alternate')
fg.description('De dagelijkse Garfield strip.')
fg.language('en')

nu = datetime.now(timezone.utc)
datum_titel = nu.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url)
fe.title(f'Garfield - {datum_titel}')
fe.link(href=COMIC_PAGE_URL)
fe.pubDate(nu)
fe.description(f'<img src="{image_url}" alt="Garfield Strip voor {datum_titel}" />')

# --- Stap 3: Schrijf het XML-bestand weg ---

try:
    fg.rss_file('garfield.xml', pretty=True)
    print("SUCCES: 'garfield.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)
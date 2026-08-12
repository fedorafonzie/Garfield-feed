import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

print("Script gestart: Genereren van de Garfield RSS-feed.")

# --- Stap 1: Bepaal de URL van de webpagina van vandaag ---

nu = datetime.now(timezone.utc)
jaar = nu.strftime('%Y')
maand = nu.strftime('%m')
dag = nu.strftime('%d')

comic_page_url = f"https://www.gocomics.com/garfield/{jaar}/{maand}/{dag}"
print(f"INFO: Zoeken naar strip op {comic_page_url}")

# --- Stap 2: Scrape de webpagina om de afbeeldings-URL te vinden ---

# We gebruiken een User-Agent omdat sommige websites scripts blokkeren
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(comic_page_url, headers=headers)
    response.raise_for_status() # Controleer of de pagina succesvol is geladen
    
    # Parse de HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # GoComics plaatst de strip in een 'picture' tag met de class 'item-comic-image'
    comic_element = soup.select_one('.item-comic-image img')
    
    if comic_element and comic_element.has_attr('src'):
        image_url = comic_element['src']
        print(f"SUCCES: Afbeeldings-URL gevonden: {image_url}")
    else:
        print("FOUT: Kon de afbeelding niet vinden op de pagina. De HTML-structuur is mogelijk gewijzigd.")
        exit(1)
        
except requests.exceptions.RequestException as e:
    print(f"FOUT: Kon de GoComics pagina niet laden. Melding: {e}")
    exit(1)

# --- Stap 3: Bouw de RSS-feed ---

fg = FeedGenerator()
fg.id('https://www.gocomics.com/garfield')
fg.title('Garfield Strip')
fg.link(href='https://www.gocomics.com/garfield', rel='alternate')
fg.description('De dagelijkse Garfield strip.')
fg.language('en')

datum_titel = nu.strftime("%Y-%m-%d")

fe = fg.add_entry()
fe.id(image_url) # Gebruik de dynamisch gevonden afbeeldings-URL
fe.title(f'Garfield - {datum_titel}')
fe.link(href=comic_page_url)
fe.pubDate(nu)

# Omdat de url geen standaard extensie meer heeft, gebruiken we image/jpeg als veilige aanname
fe.enclosure(image_url, 0, 'image/jpeg')

# De afbeelding tonen in de feed
fe.content(f'<img src="{image_url}" alt="Garfield Strip voor {datum_titel}" />', type='html')
fe.description(f'Garfield Strip voor {datum_titel}') 

# --- Stap 4: Schrijf het XML-bestand weg ---

try:
    fg.rss_file('garfield.xml', pretty=True)
    print("SUCCES: 'garfield.xml' is aangemaakt met de strip van vandaag.")
except Exception as e:
    print(f"FOUT: Kon het bestand niet wegschrijven. Foutmelding: {e}")
    exit(1)
import re
import requests
from bs4 import BeautifulSoup
import webbrowser

def handle_web_command(command, tts, config):
    if command.startswith("search the web for ") or command.startswith("look up "):
        if command.startswith("search the web for "):
            query = command.replace("search the web for ", "").strip()
        else:
            query = command.replace("look up ", "").strip()
        # Use webbrowser to open search
        url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        webbrowser.open(url)
        tts.speak(f"Searching the web for {query}.")
        return True
    if command.startswith("scrape "):
        match = re.match(r'scrape (\S+)( for (.+))?', command)
        if match:
            url = match.group(1)
            arg = match.group(3) if match.group(3) else None
            extract_type = None
            selector = None
            if arg:
                if arg in ['table', 'list', 'images', 'download']:
                    extract_type = arg
                else:
                    selector = arg
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                if extract_type == 'table':
                    tables = soup.find_all('table')
                    if tables:
                        for i, table in enumerate(tables[:1], 1):
                            rows = table.find_all('tr')
                            for row in rows[:5]:
                                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                                tts.speak(f"Row: {', '.join(cols)}")
                    else:
                        tts.speak("No tables found on the page.")
                elif extract_type == 'list':
                    lists = soup.find_all(['ul', 'ol'])
                    if lists:
                        for i, l in enumerate(lists[:1], 1):
                            items = l.find_all('li')
                            for item in items[:5]:
                                text = item.get_text(strip=True)
                                tts.speak(f"List item: {text}")
                    else:
                        tts.speak("No lists found on the page.")
                elif extract_type == 'images':
                    images = soup.find_all('img')
                    if images:
                        for i, img in enumerate(images[:5], 1):
                            src = img.get('src')
                            tts.speak(f"Image {i}: {src}")
                    else:
                        tts.speak("No images found on the page.")
                elif extract_type == 'download':
                    filename = url.split('/')[-1] or 'downloaded_content.html'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    tts.speak(f"Content downloaded as {filename}.")
                elif selector:
                    elements = soup.select(selector)
                    if elements:
                        for i, el in enumerate(elements[:3], 1):
                            text = el.get_text(strip=True)
                            tts.speak(f"Result {i}: {text}")
                    else:
                        tts.speak("No elements found for that selector.")
                else:
                    tts.speak("Here is the page title: " + soup.title.string)
            except Exception as e:
                tts.speak("Sorry, I couldn't scrape that website.")
            return True
    return False 
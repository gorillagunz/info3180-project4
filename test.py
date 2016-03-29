import requests
import BeautifulSoup
import urlparse

def get_images(url):
    images = []
    result = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(result.text)
    og_image = (soup.findAll('meta', property='og:image') or
                        soup.findAll('meta', attrs={'name': 'og:image'}))
    # if og_image and og_image['content']:
    print og_image
    
    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        print thumbnail_spec['href']
    
    image = """<img src="%s"><br />"""
    for img in soup.findAll("img", src=True):
       if "sprite" not in img["src"]:
           images += [image % urlparse.urljoin(url, img["src"])]
    return images
print get_images("http://www.imdb.com/list/ls072815691/")
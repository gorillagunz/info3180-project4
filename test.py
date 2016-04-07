import requests
import BeautifulSoup
import urlparse

def get_images(url):
    images = []
    result = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(result.text)
    og_image = (soup.findAll('meta', property='og:image') or
                        soup.findAll('meta', attrs={'name': 'og:image'}))
    if og_image:
        for img in og_image:
            images += [img['content']]
    #print images 
    thumbnail_spec = soup.findAll('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        for img in og_image:
            images += [str(img['href'])]
    
    for img in soup.findAll("img", src=True):
        if "sprite" not in img["src"]:
            images += [str(img["src"])]
    return images
print get_images("http://www.amazon.com/gp/product/B004FSE52C/ref=ox_sc_act_title_2?ie=UTF8&psc=1&smid=A1XBPHGHAXLHDG")
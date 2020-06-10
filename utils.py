from bs4 import BeautifulSoup
import requests

def news_scrapper(url):
  try:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get headline
    title = soup.find('h1').get_text()
    
    # Get body news
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    article = ' '.join(sentence_list)

    return title, article
  except:
    pass
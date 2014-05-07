from bs4 import BeautifulSoup
import requests
import tweepy
import json
import ast


def link_aggregator():
  url = "http://blog.jntuworld.com"
  response = requests.get(url)
  soup = BeautifulSoup(response.text)  
  sub = "JNTU-HYD"
  img_tags = []
  links = []  
  img_tags = soup.find_all('img', alt="Latest News")  
  for tag in img_tags:
    try:
      link = tag.next_element.get('href')
    except AttributeError:
      print "Tag doesn't contain link"
      continue
    try:
      if sub in link:
	links.append(link)
    except TypeError:
      print "Text not present"
      continue

  return links
	
def file_writer(links):
  with open("links.txt","w") as f:
    for link in links:
      f.write(link + "\n")

def url_shortner(url):
  headers = {'content-type' : 'application/json'}
  payload = {'longUrl' : url}
  response = requests.post("https://www.googleapis.com/urlshortener/v1/url", data=json.dumps(payload), headers=headers)
  return response.text

def main():
  links = link_aggregator()
  link = links[0]
  file_writer(links)
  dictionary = ast.literal_eval(url_shortner(link))
  short_url = dictionary["id"]
  print short_url

if __name__ == "__main__":
  main()


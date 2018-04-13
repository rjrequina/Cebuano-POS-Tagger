try:
    from urllib.request import urlopen
    from urllib import parse as urlparse
except ImportError:
    from urllib2 import urlopen, urlparse

from bs4 import BeautifulSoup
from utilities import write_file, read_file


'''
Scrapes news links and store it to a file
Stores the news links in news-links.txt
'''
def scrape_news_links():
    links = read_file('data/scraped/news-links.txt')
    if len(links) == 500:
        print("Status: Finished!\n")
        return

    url = "http://www.sunstar.com.ph/superbalita-cebu/balita"
    main_url = urlparse.urlparse(url).scheme + '://' + urlparse.urlparse(url).hostname
    stop_scraping_process = False
    i = 0
    limit = 500
    while i <  limit and not stop_scraping_process:
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        titles = soup.findAll('h3', {'class': 'title'})
        for title in titles:
            child = title.findChildren()[0]
            write_file("data/scraped/news-links.txt", contents=[main_url + child.get('href')], mode="a")
            print(main_url + child.get('href'))
            print("\n")
            i += 1
            if i == limit:
                break

        next_page = soup.find('a', {'title': 'Go to next page'})
        if next_page:
            url = main_url + next_page.get('href')
        else:
            stop_scraping_process = True

'''
Scrapes news contents from links stored in news-links.txt
Stores the news contents in news-raw.txt
'''
def scrape_news_contents():
    checkpoint = read_file("data/scraped/cp/news-links-cp.txt")
    start = int(checkpoint[0])
    if start == 501:
        print("Status: Finished!")
        return

    urls = read_file("data/scraped/news-links.txt", start=start)
    contents = []
    for idx, url in enumerate(urls):
        start += 1
        print("Link [" + str(start) + "]: "  + url)
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        div = soup.find('div', {'class': 'field-item even', 'property': 'content:encoded'})
        for child in div.findChildren():
            contents.append(child.getText())
        write_file("data/scraped/news-raw-nc.txt", contents=contents, per_line=True, mode="a")
        contents = []
        endpoints = [
            str(start + 1)
        ]

        write_file("data/scraped/cp/news-links-cp.txt", contents=endpoints, mode="w")


if __name__ == "__main__":
    # scrape_news_links()
    # scrape_news_contents()
    pass

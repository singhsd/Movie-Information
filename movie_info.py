import requests
from bs4 import BeautifulSoup

def main():
    # find query
    name = raw_input("Enter the query: ")
    queries = name.split(' ')
    base = "https://www.imdb.com"
    link = base + "/find?ref_=nv_sr_fn&q="
    for word in queries:
        link = link + word + "+"
    # generate search url
    link = link[:len(link)-1] + "&s=all"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # find all results
    for link in soup.find_all("td", class_="result_text"):
        get_info(base+link.a["href"])
        break;
    # remove ^ break above to get information about all the entries of search results. Currently, only the first result will be searched

def get_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    print "Title: ", soup.title.contents[0].encode("utf8")
    print "Rating: ", soup.find("div", class_="ratingValue").strong.span.contents[0].encode("utf8")
    print "Users Rated: ", soup.find("div", class_="imdbRating").a.span.contents[0].encode("utf8")
    element = soup.find("div", class_="subtext")#.contents[0].encode("utf8")
    print "Runtime: ", element.time.contents[0][25:33]
    genre = ""
    for link in element.find_all("a"):
        if "genre" in link["href"]:
            genre = genre + link.contents[0].encode("utf8")+ ", "
        else:
            print "Release Date: ", link.contents[0].encode("utf8")
    print "Genre: ", genre[:-2]
    print "Summary: ", soup.find("div", class_="summary_text").contents[0][21:-13].encode("utf8")
    element = soup.find_all("div", class_="credit_summary_item")

    for i in range(len(element)):
        director = ""
        for link in element[i].find_all("a"):
            director = director + link.contents[0].encode("utf8") + ", "
        print element[i].h4.contents[0].encode("utf8"), director[:-2]
    '''
        end = -1;
        writer = ""
        for link in element[1].find_all("a"):
            writer = writer + link.contents[0].encode("utf8") + ", "
        if "more credit" in writer:
            end = -17
        print "Writer(s): ", writer[:end]

        starcast = ""
        for link in element[2].find_all("a"):
            starcast = starcast + link.contents[0].encode("utf8") + ", "
        if "See full cast" in starcast:
            end = -24
        print "Star Cast: ", starcast[:end]
    '''

if __name__ == '__main__':
    main()

# pyright: reportMissingModuleSource=false
import requests
import pandas
import bs4
import tabulate

# link can lay du lieu
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating%27'


def get_page_content(url):
    page = requests.get(url, headers={"Accept-Language": "en-US"})
    return bs4.BeautifulSoup(page.text, "html.parser")


soup = get_page_content(url)
titles = []
release = []
certificate = []
runtime = []
genre = []
rates = []
for movie in soup.findAll('div', class_='lister-item-content'):
    if ((not movie.findAll('h3', class_='lister-item-header'))):
        continue
    titles.append('' if not [tl.text for tl in movie.findAll('h3', class_='lister-item-header')] else
                  [tl.text for tl in movie.find('h3', class_='lister-item-header').findAll('a')][0])
    release.append('' if not [rl.text for rl in movie.findAll('span', class_='lister-item-year text-muted unbold')] else
                   [rl.text for rl in movie.findAll('span', class_='lister-item-year text-muted unbold')][0].replace("(", "").replace(")", ""))
    certificate.append('' if not [ce.text for ce in movie.findAll('span', class_='certificate')] else
                       [ce.text for ce in movie.findAll('span', class_='certificate')][0])
    runtime.append('' if not [rt.text for rt in movie.findAll('span', class_='runtime')] else
                   [rt.text for rt in movie.findAll('span', class_='runtime')][0])
    genre.append('' if not [gr.text for gr in movie.findAll('span', class_="genre")] else
                 [rt.text for rt in movie.findAll('span', class_='genre')][0])
    rates.append('' if not [rt.text for rt in movie.findAll('div', class_='inline-block ratings-imdb-rating')] else
                 [rt.text for rt in movie.find('div', class_='inline-block ratings-imdb-rating').findAll('strong')][0])

df = pandas.DataFrame({'titles': titles,
                       'release': release,
                       'certificate': certificate,
                       'runtime': runtime,
                       'genre': genre,
                       'rates': rates})
print(df.to_markdown())

# pyright: reportMissingModuleSource=false
import urllib3
import requests
import pandas
import bs4
import tabulate
import matplotlib.pyplot as plt
import numpy as np

# link can lay du lieu
url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating%27'


def get_page_content(url):
    # su dung lib urllib3
    page = urllib3.PoolManager()
    page = page.request('GET', url)
    return bs4.BeautifulSoup(page.data, "html.parser")

    # su dung lib request
    # page = requests.get(url, headers={"Accept-Language": "en-US"})
    # return bs4.BeautifulSoup(page.text, "html.parser")


soup = get_page_content(url)
titles = []
release = []
certificate = []
runtime = []
genre = []
rates = []
imgs_urls = []
for movie in soup.findAll('div', class_='lister-item mode-advanced'):
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
# get link file anh
img_tags = soup.find_all('img')
for img in img_tags:
    imgs_urls.append(img['loadlate'])

lib = {'titles': titles,
       'release': release,
       'certificate': certificate,
       'runtime': runtime,
       'genre': genre,
       'rates': rates, 'img_url': imgs_urls}
i = 0
# Tai image ve may
# for img in imgs_urls:
#     img_data = requests.get(img).content
#     file_name = titles[i]+".jpg"
#     with open(file_name, 'wb') as handler:
#         handler.write(img_data)
#     i += 1

# xu ly du lieu nam release
release_y = []
for y in lib["release"]:
    release_year = [int(year)
                    for year in y.split() if year.isdigit()]
    release_y.append(release_year[0])
lib["release"] = release_y

run_time_category = []
for rt in lib["runtime"]:
    rt = [int(run_time)
          for run_time in rt.split() if run_time.isdigit()]
    if rt[0] < 100:
        run_time_category.append("short")
    elif rt[0] < 160:
        run_time_category.append("medium")
    else:
        run_time_category.append("long")
lib["runtime_cat"] = run_time_category
df = pandas.DataFrame(lib)

# genre main category
main_genres = {'Action': 0, 'Comedy': 0,
               'Drama': 0, 'Adventure': 0, 'Horror': 0}
for genre in df['genre']:
    for main_genre in main_genres.keys():
        if genre.find(main_genre) != -1:
            main_genres[main_genre] += 1

# phan loai so film theo thoi gian 
df_cnt_runtime = df.groupby('runtime_cat').size().reset_index(name='counts')
print(df_cnt_runtime.to_markdown())

# dem so film theo tung nam
df_cnt_year = df.groupby('release').size().reset_index(name='counts')

# tao bang ve gom 4 (2x2) bang con
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
#bang con 1
axs[0, 0].barh(df_cnt_runtime["runtime_cat"], df_cnt_runtime["counts"], color=[
               '#F0F8FF', '#E6E6FA', '#B0E0E6', '#7B68EE', '#483D8B'])
#bang con 2               
axs[1, 0].pie(np.array(list(main_genres.values())), labels=np.array(list(main_genres.keys())),
              colors=['#F0F8FF', '#E6E6FA', '#B0E0E6', '#7B68EE', '#483D8B'])
#bang con 3
plt.scatter(df_cnt_year['release'], df_cnt_year['counts'], alpha=0.5)
# Show the plot
plt.show()

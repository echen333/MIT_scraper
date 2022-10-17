import requests
from bs4 import BeautifulSoup

URL = "https://mitadmissions.org/blogs/page/"
PAGE_LIMIT = 10
ITER_PER = 5
SORT_BY = "date" # date, title, comments, responses


s = requests.Session()

for iter in range(ITER_PER):
    blogs = []
    blog_links = []
    outside_links = []
    num_comments = []
    num_responses = []

    for i in range(1, PAGE_LIMIT + 1):
        page = s.get(URL + str(iter*PAGE_LIMIT + i))
        print("Page " + str(iter*PAGE_LIMIT + i) + " status: " + str(page.status_code))

        soup = BeautifulSoup(page.content, "lxml")

        results = soup.find_all("a", {"class": "post-tease__h__link"})

        for result in results:
            blogs.append(result.get_text())
            blog_links.append(result["href"])

    print(blogs)
    print(blog_links)

    for i in range(len(blog_links)):
        page = s.get(blog_links[i])

        soup = BeautifulSoup(page.content, "lxml")

        results = soup.find_all("a")

        for result in results:
            outside_links.append(result["href"])

    outside_links = list(set(outside_links))
    outside_links.sort()

    f = open(f"blogs_{iter}.txt", "w")
    for i in range(len(blogs)):
        f.write(blogs[i] + "\n")
        f.write(blog_links[i])
    f.close()

    f = open(f"outside_links_{iter}.txt", "w")
    for link in outside_links:
        f.write(link + "\n")
    f.close()



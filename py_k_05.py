from bs4 import BeautifulSoup
import requests
import time

# 爬取58同城租房信息

# 58租房信息列表所在的url
urls = ["http://bj.58.com/chuzu/{}".format("pn" + str(i) if i>1 else "") for i in range(1,30)]

# 爬取的各个房屋详情的url
house_detail_urls = []

def get_soup(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    }

    # proxies = {"http": "153.149.158.189:3128"}

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_house_list(url):
    soup = get_soup(url)

    one_page_house_href_list = soup.select("tr > td.t > a")

    for house_href in one_page_house_href_list:
        href = house_href.get("href")
        if(len(href)>0):
            house_detail_urls.append(href)

    time.sleep(2)
    return house_detail_urls

def get_house_detail(url):
    soup = get_soup(url)

    title = soup.select("h1.main-title")[0]
    house_img = soup.select("#smainPic")[0]
    price = soup.select("em.house-price")[0]
    house_style = soup.select("div.house-type")[0]
    house_at = soup.select("div.xiaoqu")[0]
    # house_detail = soup.select("ul.house-primary-content")
    addr = soup.select("ul.house-primary-content > li.house-primary-content-li > div")[3]
    ower_phone = soup.select(".tel")[0]

    house_info_id = soup.select("ul.mtit_con_ul > li > a.cb7")[1].get("href").split("=")[-1]
    house_review_count_html = requests.get("http://jst1.58.com/counter?infoid={}".format(str(house_info_id)))
    review_count = house_review_count_html.text.split("=")[-1]

    data = {
        "title" : title.get_text(),
        "house_img" : house_img.get("src"),
        "price" : price.get_text(),
        "house_style" : house_style.get_text(),
        "house_at" : list(house_at.stripped_strings),
        # "house_detail" : list(house_detail.stripped_strings),
        "addr" : addr.get_text(),
        "ower_phone" : list(ower_phone.stripped_strings),
        "review_count" : review_count
    }

    if(int(data["review_count"]) > 0):
        print("______" , data ,sep="##########")
    else:
        print(data)


def main_function():
    for url in urls:
        for detail_url in get_house_list(url):
            try:
                get_house_detail(detail_url)
            except:
                pass
            # get_house_detail(detail_url)
# get_house_detail(get_house_list(urls[0])[0])

if __name__ == "__main__":
    main_function()


"""
http://bj.58.com/chuzu/
http://bj.58.com/chuzu/pn2/

li.house-primary-content-li:nth-child(4) > div:nth-child(2)
"""
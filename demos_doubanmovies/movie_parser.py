# _*_ coding: utf-8 _*_

import spider
import sys
from bs4 import BeautifulSoup

class MovieParser(spider.Parser):
    fail_count = 0
    index_count = 0
    parse_count = 0
    def htm_parse(self, priority, url, keys, deep, content):
        url_list, save_list = [], []
        soup = BeautifulSoup(content, "html5lib")

        if keys[0] == "index":
            # 获取列表页中所有的电影页面Url
            div_movies = soup.find_all("a", class_="nbg", title=True)
            print(url, "div_movies len:", len(div_movies))
            url_list.extend([(item.get("href"), ("detail", keys[1]), 0) for item in div_movies])
            self.index_count = self.index_count + 20
            if self.index_count % 100 == 0:
                print("index_count:", self.index_count, ",parse_count:", self.parse_count)

            # 获取列表页的下一页

            if len(div_movies) > 0:
                urllist = url.split('&')
                if len(urllist) == 2 :
                    ids = urllist[1].split('=')

                    if len(ids) == 2:
                        id = int(ids[1]) + 20
                        url_list.append(('https://movie.douban.com/tag/2015?type=O&start=' + str(id), ("index", keys[1]), 1))
        else:
            movie = [url]
            self.parse_count = self.parse_count + 1
            try:
                content = soup.find("div", id="content")

                # 标题
                name_and_year = [item.get_text() for item in content.find("h1").find_all("span")]
                name, year = name_and_year if len(name_and_year) == 2 else (name_and_year[0], "")
                movie.append(name.strip())
                movie.append(year.strip("()"))

                # info
                content_left = soup.find("div", class_="subject clearfix")

                nbg_soup = content_left.find("a", class_="nbgnbg").find("img")
                movie.append(nbg_soup.get("src") if nbg_soup else "")

                info = content_left.find("div", id="info").get_text()
                info_dict = dict([line.strip().split(":", 1) for line in info.strip().split("\n") if line.strip().find(":") > 0])

                movie.append(info_dict.get("导演", "").replace("\t", " "))
                movie.append(info_dict.get("编剧", "").replace("\t", " "))
                movie.append(info_dict.get("主演", "").replace("\t", " "))
                movie.append(info_dict.get("类型", "").replace("\t", " "))
                movie.append(info_dict.get("制片国家/地区", "").replace("\t", " "))
                movie.append(info_dict.get("语言", "").replace("\t", " "))
                movie.append(info_dict.get("上映日期", "").replace("\t", " "))
                movie.append(info_dict.get("季数", "").replace("\t", " "))
                movie.append(info_dict.get("集数", "").replace("\t", " "))
                movie.append(info_dict.get("片长", "").replace("\t", " "))
                movie.append(info_dict.get("又名", "").replace("\t", " "))
                movie.append(info_dict.get("官方网站", "").replace("\t", " "))
                movie.append(info_dict.get("IMDb链接", "").replace("\t", " "))


                # score & rating num
                rating_wrap = soup.find("div", class_="rating_wrap clearbox")
                if rating_wrap and rating_wrap.find("strong", class_="ll rating_num"):
                    movie.append(rating_wrap.find("strong", class_="ll rating_num").get_text())
                else :
                    movie.append("")

                rating_sum = None
                if rating_wrap:
                    rating_sum = rating_wrap.find("a", class_="rating_people")
                if rating_sum and rating_sum.find("span") and len(rating_sum.find("span").get_text()) > 0:
                    movie.append(rating_sum.find("span").get_text())
                else :
                    movie.append("")

                #summary
                summary = soup.find("div", id="link-report")
                if summary and len(summary.get_text().replace("\t", "").replace("\n", "").strip()) > 0:
                    movie.append(summary.get_text().replace("\t", "").replace("\n", "").strip())
                else :
                    movie.append("")

                #likes
                likes = soup.find("div", class_="recommendations-bd")

                if likes and likes.findAll("dd"):
                    like_lists = []
                    for l in likes.findAll("dd") :
                        like_lists.append(l.find("a").get_text().replace("\t", "").replace("\n", "").strip())
                    if len(like_lists) > 0 :
                        movie.append(",".join(like_lists))
                    else:
                        movie.append("")
                else :
                    movie.append("")

                #tags
                tags = None
                if soup.find("div", class_="tags-body"):
                    tags = soup.find("div", class_="tags-body").findAll("a")
                if tags :
                    tags_lists = []
                    for t in tags :
                        tags_lists.append(t.get_text())
                    if len(tags_lists) > 0 :
                        movie.append(",".join(tags_lists))
                else :
                    movie.append("")

                #doulist
                dou = None
                if soup.find("div", id="subject-doulist"):
                    dou = soup.find("div", id="subject-doulist").findAll("a")
                if dou :
                    dou_lists = []
                    for d in dou :
                        dou_lists.append(d.get_text())
                    if len(dou_lists) > 0 :
                        movie.append(",".join(dou_lists))
                    else:
                        movie.append("")
                else :
                    movie.append("")

                assert len(movie) == 23, "length of movie is invalid"
                save_list.append(movie)
            except:
                print(++self.fail_count, "Unexpected error when fetching:", url, " ", sys.exc_info(), movie, "\n\n")
                if (len(movie) < 2):
                    print("page", soup.prettify())
        return 1, url_list, save_list

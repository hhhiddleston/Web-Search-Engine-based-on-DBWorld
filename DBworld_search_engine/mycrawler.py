from selenium import webdriver
import os
import json
from datetime import datetime
import progressbar
import time
from multiprocessing import Pool, cpu_count, current_process

DEBUG_INIT = True
DEBUG_MENU = False
DEBUG_SAVE = True

class DBworldCrawler:

    def __init__(self, menu_url="https://research.cs.wisc.edu/dbworld/browse.html", output_dir="messages"):
        self.menu_url = menu_url
        self.output_dir = output_dir
        # load browser driver
        opt = webdriver.FirefoxOptions()
        # no display mode
        opt.add_argument('--headless')
        self.browser = webdriver.Firefox(firefox_options=opt)
        if DEBUG_INIT:   print "Driver loaded."

        # make a new dir to store jsons
        self.new_dir_path = "{}/{}".format(self.output_dir, datetime.now().strftime("%Y%m%d%H%M%S"))
        os.mkdir(self.new_dir_path)

    def crawl_menu_url(self):
        self.browser.get(self.menu_url)
        msgs = self.browser.find_elements_by_tag_name("TBODY")
        # process all messages, table contents
        p = progressbar.ProgressBar()
        p.start()
        print "Crawling messages from {}".format(self.menu_url)
        total_num = len(msgs)

        for idx, msg in enumerate(msgs):
            TDs = msg.find_elements_by_tag_name("TD")
            Sent = TDs[0].text
            Type = TDs[1].text
            Author = TDs[2].text
            Subject = TDs[3].text
            tmp = TDs[3].find_element_by_tag_name("A")
            Detail_href = tmp.get_attribute("HREF")
            Deadline = TDs[4].text
            try:
                WebPage_href = TDs[5].find_element_by_tag_name("A").get_attribute("HREF")
            except Exception as e:
                WebPage_href = ""
            if DEBUG_MENU : print "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(Sent,Type,Author,Subject,Detail_href,Deadline,WebPage_href)

            # save as json
            out_path = "{}/{}.json".format(self.new_dir_path, idx)
            out_dict = {
                "sent": Sent,
                "type": Type,
                "author": Author,
                "subject": Subject,
                "href": Detail_href,
                "deadline": Deadline,
                "webpage": WebPage_href
            }

            with open(out_path,"w") as out_file:
                out_file.write(json.dumps(out_dict))

            p.update(idx*100 / total_num)

        p.finish()


    def crawl_detail_url(self):
        jsondir=self.new_dir_path
        total_num = len(os.listdir(jsondir))
        p = progressbar.ProgressBar()
        p.start()
        print "Crawling detail contents of messages."
        for idx in range(total_num):
            # load json
            jsonpath = "{}/{}.json".format(jsondir, idx)
            with open(jsonpath, "r") as in_file:
                buf = in_file.read()
                dic_data = json.loads(buf)
                url = dic_data["href"]
                try:
                    self.browser.get(url)
                    content = self.browser.find_element_by_tag_name("PRE").text
                except Exception:
                    content = ""

            with open("{}/{}.txt".format(self.new_dir_path, idx), "w") as out_file:
                out_file.write(content.encode("utf-8"))

            p.update(idx*100 / total_num)
        p.finish()


if __name__=="__main__":
    dbworldcrawler = DBworldCrawler()
    s_time = time.time()
    dbworldcrawler.crawl_menu_url()
    e_time = time.time()
    print "Finished in {} s".format(e_time-s_time)
    dbworldcrawler.crawl_detail_url()
    e2_time = time.time()
    print "Finished in {} s".format(e2_time - e_time)

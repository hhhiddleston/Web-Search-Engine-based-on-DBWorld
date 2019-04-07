# DBworld Search Engine #

developed by yuanmu

2018-10

---

## Crawling Information ##

A message of dbworld is just raw text without any fixed format. So we need Natural Language Processing to extract information that we cares about.

Based on the requirements of this lab assignment, we need to extract the following information:
* Submission deadline
* Conference start-end date
* Conference place
* Conference topic
* Message content

The implemented `mycrawler.py` can crawl all messages from the menu url https://research.cs.wisc.edu/dbworld/browse.html .

It will create a new directory, named by the current date, e.g. 20181010082508 `format "%Y%m%d%H%M%S"`

And it will store two kind of files in the directory:
* xxx.json `xxx is the sequence number of message` contains metadata of message, format:
```
	out_dict = {
                "sent": Sent,
                "type": Type,
                "author": Author,
                "subject": Subject,
                "href": Detail_href,
                "deadline": Deadline,
                "webpage": WebPage_href
                }
 ```
* xxx.txt `xxx is the sequence number of message` saves the content of that message 

---
## Building Search Engine ##
We use Whoosh `pip install Whoosh` to construct out search engine.


from whoosh.index import create_in
from whoosh.fields import *
import sys
import os
import json

class DBworldIndexer:

    def __init__(self, msgdir):
        self.msgdir = msgdir
        self.docnum = len(os.listdir(msgdir))//2

    def create_index(self):
        schema = Schema(
            author=TEXT(stored=True),
            sent=DATETIME(stored=True, sortable=True),
            deadline=DATETIME(stored=True, sortable=True),
            subject=TEXT(stored=True),
            content=TEXT(stored=True),
            doctype=TEXT(stored=True),
            href=TEXT(stored=True),
            webpage=TEXT(stored=True)
        )

        if not os.path.exists("index"):
            os.mkdir("index")
        ix = create_in("index", schema)

        mon2num = {"Jan":'01',
                   "Feb":'02',
                   "Mar":'03',
                   "Apr":'04',
                   "May":'05',
                   "Jun":'06',
                   "Jul":'07',
                   "Aug":'08',
                   "Sep":'09',
                   "Oct":'10',
                   "Nov":'11',
                   "Dec":'12'}

        # load docs
        writer = ix.writer()

        for idx in range(self.docnum):
            jsonpath = "{}/{}.json".format(self.msgdir, idx)
            txtpath = "{}/{}.txt".format(self.msgdir, idx)

            in_json = open(jsonpath, "r")
            buf = in_json.read()
            dic_data = json.loads(buf)
            #print(dic_data)

            in_txt = open(txtpath, "r")
            txt_data = in_txt.read()
            #print(txt_data)

            sent_tmp = dic_data["sent"]
            if len(sent_tmp):
                sent_tmp = sent_tmp.split("-")
                sent_field = "{}-{}-{}".format(sent_tmp[2], mon2num[sent_tmp[1]], sent_tmp[0])


            deadline_tmp = dic_data["deadline"]
            if len(deadline_tmp):
                deadline_tmp = deadline_tmp.split("-")
                deadline_field = "{}-{}-{}".format(deadline_tmp[2], mon2num[deadline_tmp[1]], deadline_tmp[0])
            else:
                deadline_field = None

            #print(sent_field)
            #print(deadline_field)
            if deadline_field:
                writer.add_document(
                    author=dic_data["author"],
                    sent=sent_field,
                    deadline=deadline_field,
                    subject=dic_data["subject"],
                    content=txt_data,
                    doctype=dic_data["type"],
                    href=dic_data["href"],
                    webpage=dic_data["webpage"]
                )
            else:
                writer.add_document(
                    author=dic_data["author"],
                    sent=sent_field,
                    subject=dic_data["subject"],
                    content=txt_data,
                    doctype=dic_data["type"],
                    href=dic_data["href"],
                    webpage=dic_data["webpage"]
                )

            print("{} added".format(txtpath))

        # commit adding process
        writer.commit()


if __name__=='__main__':
    dbworldindexer = DBworldIndexer(msgdir=sys.argv[1])
    dbworldindexer.create_index()

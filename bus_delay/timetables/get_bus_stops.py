#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import sys
import json
import sqlite3
import re
import os.path

# pip install pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import pickle

class TimeTableStops(object):
    def __init__(self, line):
        self.line = line
        self.direction_1 = []
        self.direction_1_label = ""

        self.direction_2 = []
        self.direction_2_label = ""

    def doPostProcessing(self):
        self.direction_1_label = self.direction_1_label.strip()
        self.direction_2_label = self.direction_2_label.strip()
    def __str__(self):
        return "Line {line}\n" \
               "Direction 1 ({label_1}): {stops_d1}\n" \
               "Direction 2 ({label_2}): {stops_d2}\n"\
            .format(line=self.line,
                    label_1=self.direction_1_label,
                    stops_d1=self.direction_1,
                    label_2=self.direction_2_label,
                    stops_d2=self.direction_2)

class DBSingleton(object):
    def __init__(self, dbname="timetable.db", createfile="create_db.sql"):
        self.dbname = dbname
        self.createfile = createfile

        self.conn = sqlite3.connect(self.dbname)

        with open(self.createfile) as fd:
            script = "\n".join(fd.readlines())
            self.conn.executescript(script)

        self.cursor = self.conn.cursor()

    def getCursor(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

DBCon = DBSingleton()

# Code form http://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    # Get the last page of the PDF
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        pass
    interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def skip_blank_lines(it):
    """
    Iterate until a non empty line is found
    :param it: input iterator (modified)
    :return: the first non-empty line found
    """
    stopit = False
    ret = None
    while stopit == False:
        ret = it.next().strip() # TODO: do not assume that it.next() returns a non None obj
        if ret:
            stopit = True
    return ret

def read_text_block(it):
    """
    Read a block of text (set of non empty lines)
    :param it:
    :return: a list of string representing the block of text
    """
    ret = []
    stopit = False
    while stopit == False:
        tmp = it.next()
        if tmp and tmp.strip():
            ret.append(tmp.strip())
        else:
            stopit = True
    return ret

def get_group(regex, s, group=1):
    m = re.match(regex, s)
    ret = None
    found_match = False
    if m:
        found_match = True
        ret = m.group(group)
        if ret:
            ret = ret.strip()
    return [found_match, ret]

def read_stops_block(it):
    za_re = re.compile("zB|zA(.*)")

    #### Read direction
    bstop = skip_blank_lines(it)

    # TODO: check for Za here (in case of a single column)
    right_dir = [bstop] + read_text_block(it)
    marker = skip_blank_lines(it)
    matched, bstop = get_group(za_re, marker)


    if matched and not bstop:
        bstop = skip_blank_lines(it)
        bstop = [bstop]
    elif matched and bstop:
        tmp = skip_blank_lines(it)
        bstop = [bstop, tmp]

    left_dir = bstop + read_text_block(it)

    return left_dir+right_dir

def extract_stops(txt):
    print(txt)
    table = iter(txt.split('\n'))

    # define regex
    line_re = re.compile("Hållplatser linje (.*)")
    noter_re = re.compile("Noter")
    

    # direction 2
    line = table.next()
    m = re.match(line_re, line)
    if m:
        line = m.group(1)
        line = line.strip()
    time_table = TimeTableStops(line=line)
    time_table.direction_2_label = table.next()

    line = skip_blank_lines(table)


    if re.match(noter_re, line.strip()):
        print(read_text_block(table))
    # direction 1
    m = re.match(line_re, line)
    if m:
        line = m.group(1)
        line = line.strip()
    #if line != time_table.line:
        #raise Exception("Unexpected line: direction 1 and direction 2 line's label not matching. "
        #                "Read {line_d1} while expecting {line_d2}".format(line_d1=line,                                                                      line_d2=time_table.line))
    time_table.direction_1_label = table.next()

    #### Read direction
    #time_table.direction_2 = read_stops_block(table)
    time_table.direction_1 = read_stops_block(table)

    #print(len(time_table.direction_1))
    #print(len(time_table.direction_2))
    time_table.doPostProcessing()
    print("---------------------------------------")
    print(time_table)

    return time_table


def persist_timetable(tt):

    cur = DBCon.getCursor()
    # line_info_query = '''INSERT INTO line_info (lineid, direction, label) VALUES (?,?,?)'''
    # cur.execute(line_info_query, (tt.line, 1, tt.direction_1_label))
    # cur.execute(line_info_query, (tt.line, 2, tt.direction_2_label))

    line_query = '''INSERT INTO line (lineid, direction, id, name) VALUES '''

    gen_vals = lambda line, dir, stops: ",".join(["(\"{lineid}\", {direction}, {id}, \"{name}\")"
                                                      .format(lineid=line,
                                                              direction=dir,
                                                              id=i,
                                                              name=stops[i])
                                                  for i in range(len(stops))])

    #print(line_query + gen_vals(tt.line, 1, tt.direction_1))
    cur.execute(line_query + gen_vals(tt.line, 1, tt.direction_1))
    cur.execute(line_query + gen_vals(tt.line, 2, tt.direction_2))

    DBCon.commit()


root_url = "http://sl.se"
url_api = "http://sl.se/api/sv/TimeTableSearch/GetLineTimeTables/NULL/NULL/BUS/"
json_links = None


if sys.version_info[0] < 3:
    import urllib2
    urlopen = urllib2.urlopen
else:
    import urllib.request
    urlopen = urllib.request.urlopen

sl_json = 'sl_pdf_list.json'
if (not os.path.isfile(sl_json)):
    json_links = json.loads(urlopen(url_api).read())
else:
    with open(sl_json,'r') as f:
        json_links = json.loads(f.read())
#print(json_links)

ltracking = None
tracking_fn = "tracking.pkl"

try:
    ltracking = pickle.load(open(tracking_fn, "r"))
except Exception as e:
    print(e.message)
    ltracking = []

print(ltracking)
force_redo = []
force_ignore = ["35Ö"]

# for i in json_links["data"]:
#     if not i["IsCollectionTimeTable"]:
#         lineid = i["LineId"]
#         if lineid not in ltracking or lineid in force_redo and lineid not in force_ignore:
#             url = root_url+i["LineTableUrl"]
#             file_name ='pdfs/' + url.split('/')[-1]
#             print((os.path.isfile(file_name)))
#             if not os.path.isfile(file_name) or not os.path.isfile(file_name.replace(' ','')):
#                 print(lineid+": Downloading "+root_url+i["LineTableUrl"])
#                 response = urlopen(url)                
#                 f = open(file_name, 'w')
#                 f.write(response.read())
#                 f.close()
#             try:
#                 tt = extract_stops(convert_pdf_to_txt(file_name))
#                 persist_timetable(tt)
#                 ltracking.append(lineid)
#                 with open(tracking_fn, "w+") as fd:
#                     pickle.dump(ltracking, fd)
#                 print(i["LineId"]+" has been processed properly")
#             except Exception as e:
#                 print(e.message)
#                 #print(u"Error while processing "+lineid+u": "+e.message)
#                 pass

tt = extract_stops(convert_pdf_to_txt("pdfs/302.pdf"))
#persist_timetable(tt)
#print(convert_pdf_to_txt("V01.pdf"))

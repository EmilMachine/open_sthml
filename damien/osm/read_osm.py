#!/usr/bin/python

from imposm.parser import OSMParser
import json
import io
import os
import sqlite3
import re

class getConn(object):

    def __init__(self, db="osm.db"):
        self.db = db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)

        with open("create_db.sql") as fd:
            script = "\n".join(fd.readlines())
            self.conn.executescript(script)

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return True if exc_type is None else False

tmp = getConn()
conn = tmp.__enter__()

class CallBack(object):

    def __init__(self):
        self.possible_tags = {}
        self.tags_values = {}

    def node_callback(self, nodes):
        for osm_id, tags, coords in nodes:
            self.possible_tags = set(self.possible_tags) | {i for i in tags.keys()}
        #print '%s %.4f %.4f' % (osm_id, lon, lat)

    def node_tags_callback(self, node):
        for osm_id, tags, coords in node:
            for i in tags.keys():
                if i in self.tags_values:
                    self.tags_values[i] = self.tags_values[i] | {tags[i]}
                else:
                    self.tags_values[i] = {tags[i]}

    def node_tags_to_db_callback(self, node):
        filter = ["amenity", "railway", "leasure"]

        for osm_id, tags, coords in node:
            for i in tags.keys():
                t = None
                if i in filter:
                    t = tags[i]
                    #try:
                    #    conn.execute('''INSERT INTO category(name) VALUES(?)''', (tags[i],))
                    #except sqlite3.IntegrityError as e:
                    #    print e
                    #    pass
                    try:
                        conn.execute('''INSERT INTO entity(lat,lon,type,name) VALUES(?, ?, ?, ?)''', (coords[1], coords[0], t, tags["name"]))
                    except Exception as e:
                        pass


    def tags_values_to_json(self):
        d = self.tags_values
        return json.dumps(dict([(i, list(d[i])) for i in d.keys()]), indent=4, ensure_ascii=False).encode("utf8")


cb = CallBack()
#p = OSMParser(concurrency=4, nodes_callback=cb.node_tags_callback)
p = OSMParser(concurrency=5, nodes_callback=cb.node_tags_to_db_callback)
p.parse("stockholm.osm")

conn.commit()
conn.close()

#with io.open("all_tags_values.json", "w") as fd:
#    fd.write(unicode(cb.tags_values_to_json(), "utf8"))


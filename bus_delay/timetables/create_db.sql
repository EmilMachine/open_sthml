CREATE TABLE IF NOT EXISTS line (
lineid	    VARCHAR,
direction   INTEGER,
id	        INTEGER,
name	    VARCHAR,
UNIQUE(lineid, direction, id) ON CONFLICT IGNORE
);

CREATE TABLE IF NOT EXISTS line_info (
lineid      VARCHAR,
direction   INTEGER,
label       VARCHAR
);
import fileinput
import sqlite3
from itertools import izip
from collections import defaultdict

TABLE_SCHEMA = ('CREATE TABLE WordLemma('
                    "word TEXT COLLATE NOCASE, "
                    'lemma TEXT, '
                    'tag TEXT, '
                    'probability REAL, '
                    'PRIMARY KEY (word, lemma, tag)'
                    ');')

def parse_bnc_word_lemma():
    for line in fileinput.input('bnc.word.lemma.pos.txt'):
        lemma, word, tag, count, total, prob = line.split()
        # data parsing
        lemma, word, tag, count, total, prob = lemma[1:-1], word[1:-1], tag[1:-1], float(count), float(total), float(prob)
        # ignore foreign words (tag = F)
        if tag == 'F': continue
        yield (word, lemma, tag, prob)

def init_word_lemma_db(words):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS WordLemma;")
        # create table
        cur.execute(TABLE_SCHEMA)
        # insert data
        cur.executemany('INSERT INTO WordLemma VALUES (?, ?, ?, ?)', words)

def get_connection(db_path='bnc_word_lemma_pos.db'):
    conn = sqlite3.connect(db_path)
    # object type returned for TEXT data type
    conn.text_factory = str
    return conn

def search_lemma(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT lemma FROM WordLemma WHERE word=? and tag="v" ORDER BY probability DESC;'
        for res in cur.execute(cmd, (word,)):
            return res[0]

def search_tag(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT tag, probability FROM WordLemma WHERE word=? ORDER BY probability DESC;'
        res = list(cur.execute(cmd, (word,)))
        return res

def bncTag(words):
    tagged = [ str(search_tag(w.strip().lower())) for w in words ]
    return tagged

class BncTagger:
    def __init__(self, db_path='bnc_word_lemma_pos.db'):
        self.conn = get_connection(db_path)
    def __del__(self):
        self.conn.close()
    def __getitem__(self, key):
        return self.search_tag(key)
    def search_tag(self, word):
        cur = self.conn.cursor()
        cmd = 'SELECT tag, MAX(probability) FROM WordLemma WHERE word=? GROUP BY word;'
        cur.execute(cmd, (word,))
        return cur.fetchone()
    def parse(self, words):
        cur = self.conn.cursor()
        # search tags for all words
        cmd = 'SELECT word, tag, MAX(probability) FROM WordLemma WHERE word in ({0}) GROUP BY word;'.format(', '.join('?'*len(words)))
        pos_dict = defaultdict(lambda: 'None')
        pos_dict.update( (word.lower(), pos) for word, pos, prob in cur.execute(cmd, words) )
        tagged = tuple(pos_dict[word.lower()] for word in words)
        return tagged

if __name__ == '__main__':
    # insert data into sqlite3 db
    # init_word_lemma_db(parse_bnc_word_lemma())
    # tag example
    words = 'This concert hall was too small to enter all of the audience .'.split()
    tagger = BncTagger()
    tagged = tagger.parse(words)
    print ' '.join('%s/%s' % wordTag for wordTag in izip(words, tagged))

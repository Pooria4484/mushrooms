import btree
try:
    ff = open("btree", "r+b")
    db = btree.open(ff)
    db.flush()
    #print(db[b"update"])
    db.close()
except OSError:
    ff = open("btree", "w+b")
    db = btree.open(ff)
    db.flush()
ff.close()
def save(key,val):
    f = open("btree", "r+b")
    db = btree.open(f)
    db[key]=val
    db.flush()
    db.close()
    f.close()
def load(key):    
    f = open("btree", "r+b")
    db = btree.open(f)
    val=db[key]
    db.close()
    f.close()
    return val
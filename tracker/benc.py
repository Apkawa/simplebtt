from types import IntType, LongType, StringType, ListType, TupleType, DictType
from types import BooleanType
from types import UnicodeType
from cStringIO import StringIO

def decode_int(x, f):
    f += 1
    newf = x.index('e', f)
    n = int(x[f:newf])
    if x[f] == '-':
        if x[f + 1] == '0':
            raise ValueError
    elif x[f] == '0' and newf != f+1:
        raise ValueError
    return (n, newf+1)
  
def decode_string(x, f):
    colon = x.index(':', f)
    n = int(x[f:colon])
    if x[f] == '0' and colon != f+1:
        raise ValueError
    colon += 1
    return (x[colon:colon+n], colon+n)

def decode_list(x, f):
    r, f = [], f+1
    while x[f] != 'e':
        v, f = decode_func[x[f]](x, f)
        r.append(v)
    return (r, f + 1)

def decode_dict(x, f):
    r, f = {}, f+1
    lastkey = None
    while x[f] != 'e':
        k, f = decode_string(x, f)
        if lastkey >= k:
            raise ValueError
        lastkey = k
        r[k], f = decode_func[x[f]](x, f)
    return (r, f + 1)

decode_func = {}
decode_func['l'] = decode_list
decode_func['d'] = decode_dict
decode_func['i'] = decode_int
decode_func['0'] = decode_string
decode_func['1'] = decode_string
decode_func['2'] = decode_string
decode_func['3'] = decode_string
decode_func['4'] = decode_string
decode_func['5'] = decode_string
decode_func['6'] = decode_string
decode_func['7'] = decode_string
decode_func['8'] = decode_string
decode_func['9'] = decode_string

def bdecode(x, sloppy = 0):
    try:
        r, l = decode_func[x[0]](x, 0)
    except (IndexError, KeyError, ValueError):
        raise ValueError, "bad bencoded data"
    if not sloppy and l != len(x):
        raise ValueError, "bad bencoded data"
    return r

bencached_marker = []

class Bencached:
    def __init__(self, s):
        self.marker = bencached_marker
        self.bencoded = s

BencachedType = type(Bencached('')) # insufficient, but good as a filter

def encode_bencached(x,r):
    assert x.marker == bencached_marker
    r.append(x.bencoded)

def encode_int(x,r):
    r.extend(('i',str(x),'e'))

def encode_bool(x,r):
    encode_int(int(x),r)

def encode_string(x,r):    
    r.extend((str(len(x)),':',x))

def encode_unicode(x,r):
    encode_string(x.encode('UTF-8'),r)

def encode_list(x,r):
        r.append('l')
        for e in x:
            encode_func[type(e)](e, r)
        r.append('e')

def encode_dict(x,r):
    r.append('d')
    ilist = x.items()
    ilist.sort()
    for k,v in ilist:
        r.extend((str(len(k)),':',k))
        encode_func[type(v)](v, r)
    r.append('e')

encode_func = {}
encode_func[BencachedType] = encode_bencached
encode_func[IntType] = encode_int
encode_func[LongType] = encode_int
encode_func[StringType] = encode_string
encode_func[ListType] = encode_list
encode_func[TupleType] = encode_list
encode_func[DictType] = encode_dict
if BooleanType:
    encode_func[BooleanType] = encode_bool
if UnicodeType:
    encode_func[UnicodeType] = encode_unicode


class EncError(ValueError):
    def __str__(self):
	return "%s"%self.args

def bencode(x):
    r = []
    try:
        encode_func[type(x)](x, r)
    except:
	raise EncError("*** error *** could not encode type %s (value: %s)" % (type(x), x))
    return ''.join(r)


import sys

class bitarray(object):
    def __init__(self, n):
        if type(n)==int:
            self.n = n
            self.data = n*[True]
        elif type(n)==list:
            self.n = len(n)
            self.data = n
    
    def __and__(self, other):
        return bitarray([self.data[i] & other.data[i] for i in range(self.n)])
    
    def __or__(self, other):
        return bitarray([self.data[i] | other.data[i] for i in range(self.n)])
    
    def __lshift__(self, n):
        ret = self.data[n:]
        ret.extend(n*[0])
        return bitarray(ret)
    
    def __getitem__(self, i):
        return self.data[self.n-i-1]
    
    def __setitem__(self, i, obj):
        self.data[self.n-i-1] = obj
    
    def __str__(self):
        return "".join(map(lambda a:'1' if a else '0', self.data))


def char_mask(pat, ab):
    masks = {}
    m = len(pat)
    for a in ab:
        masks[a] = bitarray(m)
    stamp = bitarray(m)
    stamp[0] = 0
    for i in range(m):
        masks[pat[i]] = masks[pat[i]] & stamp
        stamp = stamp << 1
        stamp[0] = 1
    #for a in ab:
    #    print a, ":", masks[a]
    return masks


def shift_or(txt, pat, ab):
    n = len(txt)
    m = len(pat)
    S = bitarray(m)
    C = char_mask(pat, ab)
    occ = []
    for i in range(n):
        S = (S<<1) | C[txt[i]]
        if not S[m-1]:
            occ.append(i-m+1)
    return occ


def main1():
    txt = "abracadabra"
    pat = "abra"
    ab = "abcdrx"
    occ = shift_or(txt, pat, ab)
    print occ

def main():
    filename = sys.argv[1]
    ab = [chr(i) for i in range(256)]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    count = 0
    lcount = 0
    for txt in txtfile:
        #print "txt=",txt
        occ = shift_or(txt, pat, ab)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines" 

if __name__ == "__main__":
    main()

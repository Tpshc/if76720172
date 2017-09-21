import sys

class BaseNode (object):
    def __init__(self):
        pass

class Node (BaseNode):
    def __init__(self):
        BaseNode.__init__(self)
        self.chd=[None,None,None]

class Leaf (BaseNode):
    def __init__(self, idx):
        BaseNode.__init__(self)
        self.idx = idx

def Qinsert(root, s, idx):
    newnode = False
    m = len(s)-1
    cur = root
    i = 1
    while i <= m:
        if cur.chd[s[i]-s[i-1]]:
            cur = cur.chd[s[i]-s[i-1]]
            i += 1
        else:
            break
    while i < m:
        n = Node()
        cur.chd[s[i]-s[i-1]] = n
        cur = n
        i+=1        
    
    if i==m:
        l = Leaf(idx)
        cur.chd[s[i]-s[i-1]] = l
        cur = l
        newnode = True
        
    return cur, newnode
        
		
		
		
def nextcolumn_orig(col, pat, a):
    m = len(pat)
    ncol = (m+1)*[0]
    for i in range(1,m+1):
        phi = 0 if a==pat[i-1] else 1
        ncol[i] = min(col[i]+1, ncol[i-1]+1, col[i-1]+phi)
    return tuple(ncol)


def nextcolumn(col, pat, a, err):
    m = len(pat)
    ncol = (m+1)*[0]
    for i in range(1,m+1):
        phi = 0 if a==pat[i-1] else 1
        ncol[i] = min(col[i]+1, ncol[i-1]+1, col[i-1]+phi, err+1)
    return tuple(ncol)


def build_fsm(pat, ab, err):
    m = len(pat)
    s = tuple(range(m+1))
    idx = 0
    queue = [(s,idx)]
    Q = {s:idx}
    F = set()
    delta = {}
    if m<=err:
        F.add(idx)
    while queue:
        (s,i) = queue.pop(0)
        for a in ab:
            snxt = nextcolumn(s, pat, a, err)
            if snxt not in Q:
                idx += 1
                Q[snxt] = idx
                queue.append((snxt,idx))
                if snxt[m]<=err:
                    F.add(idx)
            inxt = Q[snxt]
            delta[(i,a)] = inxt
    return(delta, F)


def build_fsm2(pat, ab, err):
    m = len(pat)
    s = tuple(range(m+1))
    idx = 0
    queue = [(s,idx)]
    Q = Node()
    F = set()
    delta = {}
    if m<=err:
        F.add(idx)
    while queue:
        (s,i) = queue.pop(0)
        for a in ab:
            snxt = nextcolumn(s, pat, a, err)
            node, newnode = Qinsert(Q, snxt, idx+1)
	    if newnode:
                idx += 1
                queue.append((snxt,node.idx))
                if snxt[m]<=err:
                    F.add(idx)
            delta[(i,a)] = node.idx
    return(delta, F)



def scan(txt, fsm):
    (delta, F) = fsm
    n = len(txt)
    cur = 0
    occ = []
    for j in range(n):
        cur = delta[(cur, txt[j])]
        if cur in F:
            occ.append(j)
    return occ


def main2():
    txt = "abracadabra"
    pat = "abra"
    ab = "abcdrx"
    err = 1
    fsm = build_fsm(pat, ab, err)
    occ = scan(txt, fsm)
    print occ

def main():
    filename = sys.argv[1]
    txtfile = open(filename, "r")
    pat = sys.argv[2]
    err = int(sys.argv[3])
    count = 0
    lcount = 0
    ab = [chr(x) for x in range(256)]
    fsm = build_fsm(pat, ab, err)
    for txt in txtfile:
        #print "txt=",txt
        occ = scan(txt, fsm)
        count += len(occ)
        lcount += min(1,len(occ))
        if len(occ):
            print txt
    print "found",count,"occurrences in",lcount,"lines" 
    print "FSM has ", len(fsm[0])/len(ab), "states"

if __name__ == "__main__":
    main()


def build_fsm_1(pat,ab):
    fsm = {}
    m = len(pat)
    for a in ab:
        fsm[(0,a)] = 0
    fsm[(0,pat[0])] = 1
    brd = 0
    for j in range(1,m+1):
        #print "brd", brd
        #print fsm
        for a in ab:
            fsm[(j,a)] = fsm[(brd,a)]
        if j!=m:
            fsm[(j,pat[j])] = j+1
        brd = fsm[(brd,pat[j-1])]
    return fsm

def scan_1(txt, fsm, m):
    state = 0
    n = len(txt)
    occ = []
    for i in range(n):
        state = fsm[(state, txt[i])]
        if state == m: #bip
            occ.append (i-m+1)
    return occ



def build_goto(P,ab):
    g = {}
    occ = [[]]
    nxt = 0
    for k in range(len(P)):
        pat = P[k]
        m = len(pat)
        cur, j = 0,0
        while j<m and (cur, pat[j]) in g:
            cur = g[(cur, pat[j])]
            j += 1
        while j<m:
            nxt += 1
            g[(cur, pat[j])] = nxt
            cur = nxt
            occ.append([])
            j += 1
        occ[cur].append(k)
    for a in ab:
        if (0,a) not in g:
            g[(0,a)] = 0
    return g,occ


def build_fsm(P, ab):
    g,o= build_goto(P,ab)
    f = None
    return g,o,f



def print_goto(g):
    for s in sorted(g.keys()):
        print "g[%d, %c]=%d"%(s[0], s[1], g[s])

def print_occ(o, P):
    for s in range(len(o)):
        print "%d: "%s, [P[k] for k in o[s]]

def main():
    P = ["he", "she", "his", "hers"]
    ab = [chr(i) for i in range(256)]
    ab = "eihrsa"
    g,o,f = build_fsm(P, ab) 
    print_goto(g)
    print_occ(o, P)
    

def main1():
    ab = [chr(i) for i in range(256)]
    pat = "church"
    fsm = build_fsm(pat, ab)
    txt = "diogo went to the churchurch to study the church-turing thesis"
    #txt = "church"
    occ = scan(txt, fsm, len(pat))
    print occ


if __name__ == "__main__":
    main()

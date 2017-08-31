import sys

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

def build_fail(P, g, o, ab):
	Q = []
	f = len(o)*[0]
	for a in ab:
		if g[(0,a)] != 0:
			Q.append(g[(0,a)])
			f[g[(0,a)]] = 0
	while Q:
		cur = Q.pop(0)
		for a in ab:
			if (cur,a) in g:
				nxt = g[(cur,a)]
				Q.append(nxt)
				brd = f[cur]
				while (brd, a) not in g:
					brd = f[brd]
				f[nxt] = g[(brd,a)]
				o[nxt].extend(o[f[nxt]])
	return f,o	
	

def build_fsm(P, ab):
    g,o= build_goto(P,ab)
    f,o= build_fail(P,g,o,ab)
    return g,o,f


def print_goto(g):
    for s in sorted(g.keys()):
        print "g[%d, %c]=%d"%(s[0], s[1], g[s])

def print_occ(o, P):
    for s in range(len(o)):
        print "%d: "%s, [P[k] for k in o[s]]

def print_fail(f):
    for s in range(len(f)):
        print "%d --> %d"%(s,f[s])

def scan(txt, pat, g, o, f):
    	npat = len(pat)
    	n = len(txt)
    	occ = [ [] for i in range(npat) ]
	cur = 0
	for i in range(n):
		while (cur, txt[i]) not in g:
			cur = f[cur]
		cur = g[(cur, txt[i])]
		for k in o[cur]:
			occ[k].append(i-len(pat[k])+1)
	return occ

def main2():
    P = ["he", "she", "his", "hers"]
    ab = [chr(i) for i in range(256)]
    ab = "eihrsa"
    g,o,f = build_fsm(P, ab) 
    print_goto(g)
    print_occ(o, P)
    print_fail(f)

    

def main1():
    ab = [chr(i) for i in range(256)]
    pat = "church"
    fsm = build_fsm(pat, ab)
    txt = "diogo went to the churchurch to study the church-turing thesis"
    #txt = "church"
    occ = scan(txt, fsm, len(pat))
    print occ

def main():
    ab = [chr(i) for i in range(256)]
    filename = sys.argv[1]
    patfilename = sys.argv[2]
    txtfile = open(filename, "r")
    patfile = open(patfilename, "r")
    pat = []
    for line in patfile:
        pat.append(line.strip())
    patfile.close()
    print "patterns", pat
    g,o,f = build_fsm(pat, ab)
    #print_goto(g)
    print_occ(o, pat)
    print_fail(f) 
    count = len(pat)*[0]
    lcount = len(pat)*[0]
    for txt in txtfile:
        occ = scan(txt, pat, g, o, f)
	count = map(sum, zip(count, map(len, occ)))
        lcount = map(sum, zip(lcount, map(lambda x:1 if len(x) else 0, occ)))
        if sum(map(len,occ)):
            print "txt=",txt
            print "occ=", occ
    for i in range(len(pat)):
        print "found",count[i],"occurrences of", pat[i], "in",lcount[i],"lines" 

if __name__ == "__main__":
    main()

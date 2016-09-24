class dnaRollingHash(object):

    def __init__(self,s):
        self.seqlen = len(s)
        ind = len(s) - 1
        h = 0
        self.p = 7368787
        self.base = 1
        self.baseDict = {'A': 1, 'T': 2, 'G': 3, 'C': 4, 'a': 1, 't': 2, 'g': 3, 'c': 4}
        for i in range(len(s)-1,-1,-1):
##            h += (self.baseDict.get(s[i],0)) * self.base
            h = (h+(self.baseDict.get(s[i],0)) * self.base)#%self.p
            if i != 0:
##                self.base = self.base * 5
                self.base = (self.base * 5)#%self.p
        self.currentHash = (h)
            
    def getHash(self):
        return self.currentHash

    def nextHash(self, prevItem, nextItem):
##        self.currentHash = (self.currentHash - (self.baseDict.get(prevItem,0))*(self.base))
##        self.currentHash = (self.currentHash*5 + (self.baseDict.get(nextItem,0)))
        self.currentHash = (5*(self.currentHash - (self.baseDict.get(prevItem,0))*(self.base))+ (self.baseDict.get(nextItem,0)))#%self.p
        return (self.currentHash)


def subsequenceHashes(seq, k):
    rollingHash = dnaRollingHash(seq[0:k])
    firstInd = 0
    nextInd = k
    yield [rollingHash.getHash(), firstInd]
    while nextInd < len(seq):
        yield [rollingHash.nextHash(seq[firstInd], seq[nextInd]), (firstInd+1)]
        firstInd += 1
        nextInd += 1

def dna_match(navi_dna, human_dna):
    """Get nucleotide sequence that exists in both the `navi_dna` and the
    `human_dna` with maxiumum length.

    Finds the nucleotide sequence, s, with maximum length, such that s exists in
    both the Na'vi and human DNA.

    Args:
        navi_dna (str): DNA sequence from a Na'vi.
        human_dna (str): DNA sequence of a human.

    Returns:
        The nucleotide sequence that exists in both the `navi_dna` and
        the `human_dna` that has maxiumum length.
    """
    navi_dna = list(navi_dna)
    human_dna = list(human_dna)
    
    # Lower and upper bounds for the maximum length of the common subsequence s
    lower, upper = 0, len(human_dna)
    commonSubseq = ""
    naviSubseqs = dict()


    while lower < upper - 1:
        found = False
        mid  = (upper + lower)/2
        
        for x in subsequenceHashes(navi_dna, mid):
            # X takes the form where x[0] is the hash key
            # and x[1] is the first index of the substring associated with this hash key
            naviSubseqs[x[0]] = (x[1], mid)
            
        for x in subsequenceHashes(human_dna, mid):
            # x[0] is a hash key of a human_dna substring with a length of 'mid'
            # x[1] is the beginning index of the associated substring
            if x[0] in naviSubseqs:
                commonSubseq = (x[1], mid)
                lower = mid
                found = True
                break
            
        if found == False:
            upper = mid

        naviSubseqs.clear()

    for x in subsequenceHashes(navi_dna, upper):
        naviSubseqs[x[0]] = (x[1], upper)

    for x in subsequenceHashes(human_dna, upper):
        if x[0] in naviSubseqs:
            commonSubseq = (x[1], upper)

    try:
        answer = human_dna[commonSubseq[0]:commonSubseq[0]+commonSubseq[1]]
    except:
        answer = []

    return "".join(answer)

##navi_dna = "BBATGCabc"
##human_dna = "ATGC"
##
##print dna_match(navi_dna, human_dna)


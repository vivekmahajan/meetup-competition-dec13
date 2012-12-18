from heap import Heap 
import sys
from math import log, fabs
import copy

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]



class phrase_table:
    def __init__(self, filename, out_source):
        self.phrase_table_file = open(filename, "r")
        self.phrase_table = self.generate_phrases(out_source=out_source)
        
        count = 0
        for i in self.phrase_table:
            count += len(i)
        print count

    def similarity_measure(self, string1, string2):
        return levenshtein(string1, string2)
    
    def generate_phrases(self, out_source):
        line = self.phrase_table_file.readline()
        words = line[:-1].split(' ||| ')
        source = list(words[0])
        target = list(words[1])
        out_source = list(out_source)
        #print source, target, out_source
        phrase_table = {}
        n = 3 #for n-gram
        alpha = 0.5 
        all_words = self.generate_all_words()
        for i in range(0, len(source)):
            if i-n < 0:
                k = 0
            else:
                k = i-n
            #generating n-grams for source
            for p in range(k, i+1):
                n_gram_s = " ".join(source[p:i+1]) 
                #print " ".join(n_gram)
                
                for j in range(0, len(target)):
                    if j-n < 0:
                        u = 0
                    else:
                        u = j-n
                    #generating n-grams for target
                    for v in range(u, j+1):
                        n_gram_t = " ".join(target[v:j+1]) 
                        sim_measure = self.similarity_measure(string1=n_gram_t.replace(" ",""), string2=n_gram_s.replace(" ",""))
                        #print n_gram_t," * ", n_gram_s, sim_measure
                        
                        out_src_ngram = " ".join(out_source[p:i+1]) #change if lengths are not equal
                        for word in all_words:
                            if sim_measure == self.similarity_measure(string1=word.replace(" ",""), string2=out_src_ngram.replace(" ","")):
                                if phrase_table.has_key(out_src_ngram):
                                    phrase_table[out_src_ngram].append((word, pow(alpha, sim_measure + fabs(p-u))))
                                else:
                                    phrase_table[out_src_ngram] = []
                                    phrase_table[out_src_ngram].append((word, pow(alpha, sim_measure + fabs(p-u))))

                
        return phrase_table
    def generate_all_words(self):
        alphabets = list('abcdefghijklmnopqrstuvwxyz')
        all_words = []
        for i in range(0, len(alphabets)):
            for j in range(0, len(alphabets)):
                for k in range(0, len(alphabets)):
                    all_words.append(alphabets[i]+" "+alphabets[j]+" "+alphabets[k])
        
        return all_words   
        

class Hypothesis:
    def __init__(self, trans_source, dest, p_Lm, p_pt, dis, stack_id, end_d):
        self.p_Lm = pow( 10,float(p_Lm))
        self.p_pt = float(p_pt)
        self.dis = float(dis)
        self.dest = copy.deepcopy(dest)
        self.trans_source = copy.deepcopy(trans_source)
        self.stack_id = stack_id
        self.end_d = end_d
        #print "creating hypothesis ",self.trans_source, self.stack_id
    def get_priority(self):
        return (self.p_Lm * self.p_pt * self.dis)
    def get_mld(self):
        return (self.p_Lm * self.p_pt * self.dis)
        #return (self.p_pt * self.dis)

def generate_gaps(trans_source, end_d):
    #calculating the gaps
    string_gaps = []
    gap = []
    start_index = -1
    for i in range(0, len(trans_source)):
        if trans_source[i][1] == 1 :
            if len(gap) is not 0:
                if abs(start_index - end_d) < dis_limit:
                    string_gaps.append((gap, start_index))
            gap = []
            start_index = -1
        else:
            gap.append(trans_source[i][0])
            if start_index == -1:
                start_index = i
    if len(gap) is not 0:
        if abs(start_index - end_d) < dis_limit:
            string_gaps.append((gap, start_index))
    return string_gaps

def lang_model(destination):
    return 1.0

def generate_all_hypothesis(hp):
    #This will contains all the possible hypothesis
    hypothesis = []

    string_gaps = generate_gaps(hp.trans_source, hp.end_d)        
    #generating unigrams, bigrams and trigrams
    for gap in string_gaps:
        #length 1
        for i in range(0, len(gap[0])):
            #unigram 
            uni = gap[0][i]
            if pt.phrase_table.has_key(uni):
                for trans in pt.phrase_table[uni]: 
                    uni_trans_source = copy.deepcopy(hp.trans_source)
                    uni_trans_source[gap[1]+i] = (gap[0][i], 1)
                    uni_dest = hp.dest + trans[0] + " "
                    uni_p_Lm = lang_model(uni_dest.rstrip())
                    uni_p_pt = hp.get_mld() * float(trans[1])
                    uni_dis = pow(alpha, abs(hp.end_d-i-gap[1])) 
                    uni_stack_id = hp.stack_id + 1
                    uni_end_d = i + gap[1]
                    hpu = Hypothesis(trans_source = uni_trans_source, dest=uni_dest, p_Lm=uni_p_Lm, p_pt=uni_p_pt, dis=uni_dis, stack_id=uni_stack_id, end_d=uni_end_d)
                    hypothesis.append(hpu)
            #bigram
            if i > 0 :
                bi = gap[0][i-1]+" "+gap[0][i]
                if pt.phrase_table.has_key(bi):
                    for trans in pt.phrase_table[bi]: 
                        bi_trans_source = copy.deepcopy(hp.trans_source)
                        bi_trans_source[gap[1]+i] = (gap[0][i], 1)
                        bi_trans_source[gap[1]+i-1] = (gap[0][i-1], 1)
                        bi_dest = hp.dest + trans[0] + " "
                        bi_p_Lm = lang_model(bi_dest.rstrip())
                        bi_p_pt = hp.get_mld() * float(trans[1])
                        bi_dis = pow(alpha, abs(hp.end_d-i-1-gap[1])) 
                        bi_stack_id = hp.stack_id + 2
                        bi_end_d = i + gap[1]
                        hpb = Hypothesis(trans_source = bi_trans_source, dest=bi_dest, p_Lm=bi_p_Lm, p_pt=bi_p_pt, dis=bi_dis, stack_id=bi_stack_id, end_d=bi_end_d)
                        hypothesis.append(hpb)

            #trigram
            if i > 1 :     
                tri = gap[0][i-2]+" "+gap[0][i-1]+" "+gap[0][i]
                if pt.phrase_table.has_key(tri):
                    for trans in pt.phrase_table[tri]: 
                        tri_trans_source = copy.deepcopy(hp.trans_source)
                        tri_trans_source[gap[1]+i] = (gap[0][i], 1)
                        tri_trans_source[gap[1]+i-1] = (gap[0][i-1], 1)
                        tri_trans_source[gap[1]+i-2] = (gap[0][i-2], 1)
                        tri_dest = hp.dest + trans[0] + " "
                        tri_p_Lm = lang_model(tri_dest.rstrip())
                        tri_p_pt = hp.get_mld() * float(trans[1])
                        tri_dis = pow(alpha, abs(hp.end_d-i-2-gap[1])) 
                        tri_stack_id = hp.stack_id + 3
                        tri_end_d = i + gap[1]
                        hpt = Hypothesis(trans_source = tri_trans_source, dest=tri_dest, p_Lm=tri_p_Lm, p_pt=tri_p_pt, dis=tri_dis, stack_id=tri_stack_id, end_d=tri_end_d)
                        hypothesis.append(hpt)

    return hypothesis

class Decoder:
    def __init__(self, phrase_table):
        self.phrase_table = phrase_table
        self.source = ""
        self.stacks = {}

    def decode(self, source):
        #self.source = source.split(" ")
        self.source = list(source)
        self.clear_stacks()
        self.init_stacks()
        #initialing the first stack
        trans_source = []
        for i in range(0, len(self.source)):
             trans_source.append((self.source[i], 0))
        hp = Hypothesis(trans_source=trans_source, dest="", p_Lm=1, p_pt=1, dis=1, stack_id=0, end_d=0)
        self.stacks[0].push(1, hp)
        for i in range(0, len(self.source)):
            #popping all the elements from the ith stack
            #print "size of the %s stack =  " % i , self.stacks[i].__len__() 
	    while self.stacks[i].__len__() > 0:
                hp = self.stacks[i].pop()
                for hypothesis in generate_all_hypothesis(hp):
                    stack_no = hypothesis.stack_id
                    if self.stacks[stack_no].__len__() >= beam:
                        #get the root
                        root_prob = self.stacks[stack_no]._heap[0][0]
                        if root_prob < hypothesis.get_priority():
                            self.stacks[stack_no].pop()
                            self.stacks[stack_no].push(hypothesis.get_priority(), hypothesis)
                    else:
                        self.stacks[stack_no].push(hypothesis.get_priority(), hypothesis)
        return self.stacks[len(self.source)]

             
    def clear_stacks(self):
        del self.stacks
        self.stacks = {}
        
    def init_stacks(self):
        for i in range(0, len(self.source)+1):
            self.stacks[i] = Heap() 

    

if __name__ == '__main__':
    global beam, dis_limit, pt, alpha
    if len(sys.argv) == 7:
        train_filename = sys.argv[1]
        decoder_input_filename = sys.argv[2]
        beam = int(sys.argv[3])
    	alpha = float(sys.argv[4])
	dis_limit = int(sys.argv[5])
	n_best = int(sys.argv[6])
    else:
        print >> sys.stderr, "usage:python %s phrase_table_file decoder_input beam alpha dis_limit n_best" % sys.argv[0]
        sys.exit(-1)
   

    input_source = open(decoder_input_filename, "r")
    out_source = input_source.readline()[:-1].rstrip() 
    pt = phrase_table(out_source=out_source, filename=train_filename)
    decoder = Decoder(pt)
    output = decoder.decode(out_source)
    stack = []
    print ">>>>>>>> ", out_source, " <<<<<<<<<"
    #print "length ",output.__len__()
    if output.__len__() == 0:
        print "Could not translate"
    while output.__len__() > 0:
        obj = output.pop()
        stack.append(obj)
    
    for i in range(0, n_best):
        if len(stack) == 0:
            break
        obj = stack.pop()
        print obj.dest, obj.get_priority()
            

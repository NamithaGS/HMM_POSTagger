import codecs
import re, os, sys
import string,math
import json

import time
start_time = time.time()

#input model
#fpipmodelfilename = codecs.open('C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hmmmodel.txt',"r", encoding='utf-8')
fpipmodelfilename = codecs.open('hmmmodel.txt',"r", encoding='utf-8')
fpmodel  = json.load(fpipmodelfilename)

#testfile = 'C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hw6-dev-train\mytest\dev.txt'
#testfile = 'C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hw6-dev-train\catalan_corpus_dev_raw.txt'
testfile = sys.argv[1]

#outputfile = codecs.open('C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hmmoutput.txt',"wb", encoding='utf-8')
outputfile = codecs.open('hmmoutput.txt',"wb", encoding='utf-8')

if __name__ == "__main__":
    sys.stdout.write("\n--- %s seconds1---" % (time.time() - start_time))
    statesperword = fpmodel['States per word']
    #starttransprob = fpmodel['Start transition probabilities']
    transprob = fpmodel['Transition probabilities']
    emissionprob = fpmodel['Emission probabilities']
    allstates = fpmodel['All states'].split()
    #allstates = ['AO', 'AQ', 'CC', 'CS', 'DA', 'DD', 'DI', 'DP', 'DR', 'DT', 'FF', 'II', 'NC', 'NP', 'P0', 'PD', 'PI', 'PP', 'PR', 'PT', 'PX', 'RG', 'RN', 'SP',  'VA', 'VM', 'VS', 'WW', 'ZZ']
    #allstates = ['VB', 'IN', 'NN', 'DT']
    allstates.remove('START')

    mostprobablepostag  = fpmodel['Most probable pos tag']
    mostprobposprob = fpmodel['Most probable pos tag probability']

    sys.stdout.write("\n--- %s seconds2---" % (time.time() - start_time))
    with codecs.open(testfile, encoding='utf-8') as fptestfile:
        index=0
        for eachline in fptestfile:
            index+=1
            #sys.stdout.write("\n %s line : " % eachline )
            firsttime = True
            words = eachline.split()
            probability = {}
            backpointer= []
            for eachword in words:
                eachword = eachword
                unseen = False
                statesQ = []
                if statesperword.has_key(eachword) :
                    statesQ = (statesperword[eachword]).split(" ")
                if len(statesQ)== 0:
                    statesQ = allstates
                    unseen = True

                probability1 = {}
                max1 = -sys.maxint - 1
                maxstate = "NULL"

                if firsttime == True:
                    for eachstate in statesQ:
                        #if transprob.has_key("START - " +eachstate): #and ( (unseen == True) or emissionprob.has_key(eachstate+" - "+ eachword)):
                        if ((eachstate+" - "+ eachword) not in emissionprob):
                            probability[eachstate] = transprob["START - "+eachstate]
                        else:
                            probability[eachstate] = transprob["START - "+eachstate] * emissionprob[eachstate+" - "+ eachword]
                    backpointer.append((eachword ,"START"))
                    firsttime = False
                else:
                    for eachstate in statesQ:
                        max1 = -sys.maxint - 1
                        maxstate = "NULL"
                        for eachpos,value in probability.items():
                            myval = 0
                            #if transprob.has_key(eachpos+" - "+eachstate):# and ( (unseen == True) or emissionprob.has_key(eachstate+" - "+ eachword)):
                            if  ((eachstate+" - "+ eachword) not in emissionprob):
                                myval = value * transprob[eachpos+" - "+eachstate]
                            else:
                                myval = value * transprob[eachpos+" - "+eachstate] * emissionprob[eachstate+" - "+ eachword]
                            if (myval)>max1:
                                max1 = myval
                                maxstate = eachpos

                        if(maxstate!="NULL"):
                            probability1[eachstate] = max1
                            backpointer.append( (eachword,  eachstate + " - "+maxstate))
                    if(len(probability1)==0):     # no transition prob seen, then get the  max of pos in prob tags to whatever possible
                        mystates = statesperword[eachword].split()
                        maxstatefortheword = max(mystates)   #get the max possible tag for the word
                        probability1[maxstatefortheword] = max(probability.values())
                        backpointer.append( (eachword,  maxstatefortheword + " - "+max(probability,key=probability.get)))

                    probability = probability1
                    probability1 = {}
            #sys.stdout.write( backpointer)

            #get the backpointers
            correcttag = {}
            lastword = eachline.split()[-1]
            lasttag = max(probability,key=probability.get)

            for myeachword in reversed(eachline.split()):
                correcttag[myeachword] = lasttag
                for key,value in backpointer:
                    if key == myeachword:
                        if value.split(" - ")[0] == lasttag:
                            lasttag = value.split(" - ")[1]
                            break

            for myeachword in (eachline.split()):
                outputfile.write(myeachword+"/"+correcttag[myeachword]+" ")
            outputfile.write("\n")
        sys.stdout.write("\n--- %s seconds3 ---" % (time.time() - start_time))


    ##compare code




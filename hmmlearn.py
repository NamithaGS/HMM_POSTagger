
__author__ = 'namithags'
import json
import time
start_time = time.time()
import codecs
import sys, math
#Input training tagged data
#fpipfile = 'C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hw6-dev-train\mytest\htrain.txt'
#fpipfile = 'C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hw6-dev-train\hfull.txt'
fpipfile = sys.argv[1]

#Model to write to
#fpmodel = open('C:\Users\Namithaa\Desktop\NLP\Assignments\Assignment6\hmmmodel.txt', "wb")
fpmodel = codecs.open('hmmmodel.txt', "wb", encoding='utf-8')

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

#get the starting states
def getstatesperword(emissionprobmatrix):
    statesperword1 = {}
    for key ,value in emissionprobmatrix.items():
        if key.split(" - ")[1] in statesperword1:
            statesperword1[key.split(" - ")[1]] += " " + (key.split(" - ")[0])
        else:
            statesperword1[key.split(" - ")[1]] = key.split(" - ")[0]
    return statesperword1

#Get the transistion probability matrix
def gettransrob(statesQ , allstates):
    allstates1 = allstates.split(" ")
    n = len(allstates1)    #including start state
    transprob={}
    totalperpos ={}

    for i in range(0,len(statesQ)-1):
        bb0 = statesQ[i]
        bb1 = statesQ[i+1]
        if(bb1 != "START"):
            mykey = bb0+" - "+bb1
            if transprob.has_key(mykey):
                transprob[mykey] = transprob.get(mykey)+1
            else:
                transprob[mykey] = 1

            if totalperpos.has_key(bb0):
                totalperpos[bb0] = totalperpos.get(bb0)+1
            else:
                totalperpos[bb0] = 1
        i=i+1

    transprob.update((key,(float(value+1)/ float(n + totalperpos[(key.split(" - "))[0]])) ) for key, value in transprob.items())
    for eachstatefirst in allstates1:
        for eachstatenext in allstates1:
            tag = eachstatefirst + " - " + eachstatenext
            if tag not in transprob:
                transprob[tag] = ( 1/float(n + totalperpos[eachstatefirst]))

    #transprob.update((key,round((math.log(value/totalperpos[(key.split(" - "))[0]])),4)) for key, value in transprob.items())

    return transprob


#Get the emission probability matrix
def getemissionprob( statesobs ):
    emissionprob1 = {}
    totalperpos={}
    for key,value in statesobs:
        aa = key + " - " + value
        if emissionprob1.has_key(aa):
            emissionprob1[aa] = emissionprob1[aa]+1
        else:
            emissionprob1[aa] = 1
        if totalperpos.has_key(key):
            totalperpos[key] = totalperpos.get(key)+1
        else:
            totalperpos[key] = 1
    #emissionprob1.update((key,round(math.log(value/totalperpos[key.split(" - ")[0]]),4)) for key, value in emissionprob1.items())
    emissionprob1.update((key,(float(value)/float(totalperpos[key.split(" - ")[0]]))) for key, value in emissionprob1.items())

    return emissionprob1

#################start
if __name__ == "__main__":
    sys.stdout.write("\n--- %s seconds1---" % (time.time() - start_time))
    countnumberoflines = 0
    statesQ = []
    obsvQ=[]
    #startstates = []
    startprobmatrix={}
    transprobmatrix={}
    statesperword1={}
    emissionprobmatrix={}
    statesobs=[]
    with open(fpipfile) as fpiptagged:
        for traintext in fpiptagged:
            countnumberoflines+=1
            statesQ.append("START")
            #traintext = fpiptagged.readline()
            traintextdict = traintext.split()
            obsvQ.append("START")
            for eachword in traintextdict:
                p = eachword.rfind("/") + 1
                word = eachword[:(p-1)]
                postag = eachword[p:]
                statesQ.append(postag)
                obsvQ.append(word)
                statesobs.append((postag,word))

    allstates =  " ".join(list((set(statesQ))))
    sys.stdout.write("\n--- %s seconds2 ---" % (time.time() - start_time))
    transprobmatrix = gettransrob (statesQ , allstates )   ### transition probability matrix
    sys.stdout.write("\n--- %s seconds3 ---" % (time.time() - start_time))
    emissionprobmatrix =  getemissionprob ( statesobs )    ###Emission probability
    sys.stdout.write("\n--- %s seconds4 ---" % (time.time() - start_time))
    statesperword1 = getstatesperword(emissionprobmatrix)

    sys.stdout.write("\n--- %s seconds5 ---" % (time.time() - start_time))
    fpmodel.write('{ "States per word" : \n')
    fpmodel.write(json.dumps(statesperword1))
    #fpmodel.write(",")

    sys.stdout.write("\n--- %s seconds7 ---" % (time.time() - start_time))
    fpmodel.write(",")
    fpmodel.write('\n "Transition probabilities" : \n')
    fpmodel.write(json.dumps(transprobmatrix))
    sys.stdout.write("\n--- %s seconds8 ---" % (time.time() - start_time))
    fpmodel.write(",")
    fpmodel.write('\n"Emission probabilities" : \n')
    fpmodel.write(json.dumps(emissionprobmatrix))

    fpmodel.write(",")
    fpmodel.write('\n"Most probable pos tag" : \n')

    statesQ = remove_values_from_list(statesQ,"START")
    mostprobablepostag = max(statesQ)
    #mostprobablepostagprob = round(math.log(statesQ.count(mostprobablepostag)/len(statesQ)),4)
    mostprobablepostagprob = statesQ.count(mostprobablepostag)/len(statesQ)

    fpmodel.write(json.dumps(mostprobablepostag))

    fpmodel.write(",\n")
    fpmodel.write('\n"Most probable pos tag probability" : \n')
    fpmodel.write(json.dumps(mostprobablepostagprob))


    fpmodel.write(",\n")
    fpmodel.write('\n"All states" : \n')


    fpmodel.write(json.dumps(allstates))

    fpmodel.write("\n}")

    sys.stdout.write("\n--- %s seconds9 ---" % (time.time() - start_time))






from successordict import SuccessorDict as sdict
import re
import math
import sys
import gzip
import json

sys.stdout.write("Reading in words...");sys.stdout.flush()
with gzip.open('engmodel5.json.gz', 'rb') as f:
    dictionary = json.loads(f.read(),object_pairs_hook=sdict)
print "done!"
# We need to build a complete model, including capitals, because the stats don't have that.
# (Should I include ALL CAPS versions of some words? All words?)
#this is a list of over 300 words that are disproportionately likely to be uppercased
cumsum = 0
toplist = ['the','an','some','who','whose','what','which','where','when','why','how','do','did','have','had',
           "will","was","is","may","might","could","should","would","were",
           "are","am","shall","can","my","you","your","he","his","she","her",
           "it","its","we","our","they","their","this","that",
           "these","those","any","all","no","every","each","everyone","one","none","and","or","but","yet","so","for","neither","either","both",
           "if","because","unless","as","until","since","before","after","while","although","even","whereas","whenever","whether","which","now",
           "then","there","here","in","on","by","around","to","from","at","though","as","while","henceforth","thenceforth","above","below","among",
           "beneath","beside","besides","between","beyond","considering","despite","during","except","following","inside","outside","into","like",
           "near","onto","into","opposite","under","over","save","through","underneath","unlike","until","upon","anything","something","everything",
           "everybody","somebody","nobody","nothing","no-one","someone","anyone","anybody","however","sometimes","soon","recently","usually","rather",
           "indeed","tonight","today","tomorrow","next","clearly","rather","basically","obviously","well","only","also","later","earlier","actually",
           "once","perhaps","thus","does","doesn't","has","hasn't","can't","must","you've","she'll","we've","they've","whoever","whatever","whichever",
           "wherever","many","few","lots","several","more","less","most","given","facing","down","up","about","concerning","far","apart","according",
           "therefore","nevertheless","also","often","never","occasionally","immediately","maybe","possibly","probably","certainly","people","things",
           "hopefully","seriously","honestly","hours","days","weeks","months","years","times","places","stuff","oh","uh","hi","hello","goodbye","bye",
           "um","ah","ow","ugh","argh","eek","aha","ahem","hey","eh","right","please","thank","okay","alright","thanks","aw","two","three","four","five",
           "six","seven","eight","nine","ten","eleven","twelve","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety","damn","shit","hell",
           "fuck","cool","nice","neat","awesome","go","get","ask","avoid","be","bring","come","meet","send","make","take","put","keep","stay","remember",
           "listen","look","pardon","work","hold","move","let","allow","permit","excuse","forgive","show","prove","believe","tell"]
sys.stdout.write("Adding new entries...");sys.stdout.flush()
noncapcount = 0
for word,freq in dictionary.items():
    # relative frequencies of lowercase and uppercase versions are pure speculation. this model could surely benefit from more data analysis but that takes effort
    if word[0].isalpha():
        if word=="i": # roughly 19% of i should  be capitalized (much more than any other letter)
	    width1 = int(0.18*freq)
            width2 = int(0.72*freq)
        elif len(word)==1 or word in toplist:
            width1 = int(math.floor(14./15*freq))
            width2 = int(math.ceil(freq/15.))
        else:
            width1 = int(math.floor(999./1000*freq))
            width2 = 0
            noncapcount += freq
        dictionary[word] = width1
        if width2:
            dictionary[word.capitalize()] = width2
        cumsum+=width1+width2
    else:
	cumsum += freq
	dictionary[word]=freq

dictionary[u"CAPITALIZED"] = noncapcount/900 #capitalized words (not most common)
cumsum += noncapcount/900
dictionary[u"ALLCAPS"] = noncapcount/10000 #all caps words
cumsum += noncapcount/10000
dictionary[u"WHOLESTRINGCAPS"] = noncapcount/100000
cumsum += noncapcount/100000

i = dictionary["I"]
you = dictionary["you"]
he = dictionary["he"]
she = dictionary["she"]
it = dictionary["it"]
we = dictionary["we"]
they = dictionary["they"]

ve = int(.0244*(i+they+you+we))
ere = int(.06995*(you+they+we))
d = int(.051335*(i+you+they+we+he+she+it))
ll = int(.029696*(i+you+they+we+he+she+it))

cumsum+=ll+ve+d+ere
dictionary[u"'ll"] = ll
dictionary[u"'ve"] = ve
dictionary[u"'d"] = d
dictionary[u"'re"] = ere

do = dictionary["do"]
does = dictionary["does"]
did = dictionary["did"]
had = dictionary["had"]
have = dictionary["have"]
could = dictionary["could"]
iz = dictionary["is"]
was = dictionary["was"]
would = dictionary["would"]
were = dictionary["were"]
should = dictionary["should"]
are = dictionary["are"]

nt = do+does+did+had/20+have/30+were/15+are/20+was/15+iz/100+would/5+should/7+could/4
dictionary[u"n't"] = nt
cumsum+=nt

dictionary[u"can't"] = dictionary["can"]/3
cumsum += dictionary["can't"]
dictionary[u"won't"] = dictionary["will"]/3
cumsum += dictionary["won't"]

#these coefficients take into account the target cumsum in each case, so we can update cumsum immediately
s = int(.0075513*cumsum)
dictionary[u"'s"] = s
cumsum += s
imm = int(.00118478 * cumsum)
dictionary[u"I'm"] = imm
print "done!"

sys.stdout.write("Sorting keys and accumulating values...");sys.stdout.flush()
intermodel = sdict()
cumsum=0
for key,val in sorted(dictionary.items()):
    cumsum+=val
    intermodel[key] = cumsum
print "done!"
sys.stdout.write("Saving new model...");sys.stdout.flush()
with gzip.open('engmodel6.json.gz', 'wb') as f:
    f.write(json.dumps(intermodel, f, separators=(',',':')))
print "done!"
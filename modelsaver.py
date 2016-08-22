from collections import OrderedDict as odict
import re
import math
import sys
import gzip
import json

sys.stdout.write("Reading in words...");sys.stdout.flush()
with gzip.open('engmodel1.json.gz', 'rb') as f:
    dictionary = odict(json.loads(f.read()))
# We need to build a complete model, including capitals, because the stats don't have that.
# (Should I include ALL CAPS versions of some words? All words?)
#this is a list of over 300 words that are disproportionately likely to be uppercased
toplist = ['the','an','some','who','whose','what','which','where','when','why','how','do','did',"didn't","don't",'have','had',"hadn't","haven't",
           "will","was","is","won't","wasn't","isn't","may","might","could","should","would","couldn't","wouldn't","shouldn't","were","weren't",
           "are","aren't","am","shall","can","my","you","you're","your","you'll","you'd","he","his","he's","he'll","he'd","she","her","she's",
           "she'd","it","its","it's","it'll","it'd","we","we're","we'll","we'd","our","they","they're","they'll","they'd","their","this","that",
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

for word,freq in dictionary.items():
    # relative frequencies of lowercase and uppercase versions are pure speculation. this model could surely benefit from more data analysis but that takes effort
    if re.search('[a-zA-Z]', word):
        if word=="i": # roughly 19% of i should  be capitalized
            width1 = int(math.ceil(freq/10000.))
            width2 = freq
        elif word in toplist:
            width1 = freq
            width2 = int(math.ceil(freq/15.))
        else:
            width1 = freq
            width2 = int(math.ceil(freq/1000.))
        dictionary[word.capitalize()] = width2
        dictionary[word+" "] = width1
        dictionary[word.capitalize()+" "] = width2
    else:
        words.append(word)
        breakpoints.append(cumsum)
        cumsum+=freq
breakpoints.append(cumsum)
words.append(-1) #stop symbol
model[-1] = (cumsum,cumsum+int(cumsum/10.))
breakpoints.append(cumsum+int(cumsum/10.)) # the stop symbol is guaranteed to occur, so it takes up an eleventh of the probability space


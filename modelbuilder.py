def buildModel(self,dictionary):
    """
    dictionary maps symbols to frequencies
    """
    # We need to build a complete model, including capitals, because the stats don't have that.
    # (Should I include ALL CAPS versions of some words? All words?)
    cumsum = 0
    toplist = ['the','an','some','who','whose','what','which','where','when','why','how','do','did',"didn't","don't",'have','had',"hadn't","haven't",
               "will","was","is","won't","wasn't","isn't","may","might","could","should","would","couldn't","wouldn't","shouldn't","were","weren't",
               "are","aren't","am","shall","can","me","my","you","you're","your","you'll","you'd","he","his","he's","he'll","he'd","she","her","she's",
               "she'd","it","its","it's","it'll","it'd","we","we're","we'll","we'd","our","they","they're","they'll","they'd","their","this","that",
               "these","those","any","all","no","every","each","everyone","one","none","and","or","but","yet","so","for","neither","either","both",
               "if","because","unless","as","until","since","before","after","while","although","even","whereas","whenever","whether","which","now",
               "then","there","here","in","on","by","around","to","from","at","though","as","while","henceforth","thenceforth","above","below","among",
               "beneath","beside","besides","between","beyond","considering","despite","during","except","following","inside","outside","into","like",
               "near","onto","into","opposite","under","over","save","through","underneath","unlike","until","upon","anything","something","everything",
               "everybody","somebody","nobody","nothing","no-one","someone","anyone","anybody","however","sometimes","soon","recently","usually","rather",
               "indeed","tonight","today","tomorrow","next","clearly","rather","basically","obviously","well","only","also","later","earlier","actually",
               "once","perhaps","thus"]
Indefinite pronouns, common adverbs, a few other categories
    model = ddict(int)
    for word,freq in dictionary.items():
        # that lowercase is 100 times more common for most words is pure speculation.
        if re.search('[a-zA-Z]', word):
            if word.startswith("i'"):
                model[word] = (cumsum,cumsum+math.ceil(freq/10000.))
                cumsum += math.ceil(freq/10000.)
                model[word.capitalize()] = (cumsum,cumsum+freq)
                cumsum += freq
                model[word+" "] = (cumsum,cumsum+math.ceil(freq/10000.))
                cumsum += math.ceil(freq/10000.)
                model[word.capitalize()+" "] = (cumsum,cumsum+freq)
                cumsum += freq
            elif word in toplist:
                model[word] = (cumsum,cumsum+freq)
                cumsum+=freq
                model[word.capitalize()] = (cumsum,cumsum+math.ceil(freq/15.))
                cumsum+=freq
                model[word+" "] = (cumsum,cumsum+freq)
                cumsum+=freq
                model[word.capitalize()+" "] = (cumsum,cumsum+math.ceil(freq/15.))
                cumsum+=freq
            else:
                model[word] = (cumsum,cumsum+freq)
                cumsum+=freq
                model[word.capitalize()] = (cumsum,cumsum+math.ceil(freq/1000.))
                cumsum+=freq
                model[word+" "] = (cumsum,cumsum+freq)
                cumsum+=freq
                model[word.capitalize()+" "] = (cumsum,cumsum+math.ceil(freq/1000.))
                cumsum+=freq
        else:
            model[word] = (sumsum,cumsum+freq)
            cumsum+=freq
    
    return model,cumsum
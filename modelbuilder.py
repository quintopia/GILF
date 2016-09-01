import string

def build_model(dictionary,symbols):
    """
    dictionary (succesordict) maps words to cumulative frequencies
    symbols maps base64 encoded symbols to relative frequencies
    """
    # All this is supposed to do is make sure all printable ascii chars get into the english model, just in case.
    # So we need to add the (decoded) symbols from symbols to dictionary with frequencies given by their relative frequencies and the total size of the model
    # we need to do this every time since some symbols are bytes and may not appear directly in json files, so we keep these base64 encoded in a separate file. we don't want them in the regular word file because then we either have to base64 encode the whole thing (huge file) or have to parse
    # it all to find the encoded ones (slow)
    # why not just pickle instead of json? I want people to be able to host an interpreter and trust that it's not malicious without having to pick apart the pickled file.
    # TODO: eventually maybe all "reasonable" bytes can be put in this file

    
    #what's the minimum relfreq?
    minrelfreq = min(symbols.values())
    symbols = {k.decode('base64'):v for k,v in symbols.items()}
    cumsum = dictionary[dictionary.last_key()]
    for symbol in string.printable:
        try:
            dictionary[symbol]
        except KeyError:
            try:
                symbols[symbol]
            except KeyError:
                symbols[symbol] = minrelfreq
                
    ocumsum = cumsum
    for symbol,relfreq in symbols.items():
        cumsum += int(relfreq/(1-relfreq)*ocumsum)
        dictionary[symbol]=cumsum
    #now that the model is complete, we must add a stop symbol
    
    dictionary[-1] = cumsum+int(cumsum/10.)
    
    return dictionary
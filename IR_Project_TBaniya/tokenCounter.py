
def countTokens(file):
    f = open(file,'r')
    words = f.read().split()
    return len(words)
    

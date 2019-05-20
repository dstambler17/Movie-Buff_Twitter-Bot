import requests
import io

#DEVELOPER Note: used to Fix combined quotes
def breakUneven(QuoteList):
    res = []
    for quote in QuoteList:
        if '\\n\\t\\n\\t' in quote:
            TwoQuotes = quote.split("\\n\\t\\n\\t")
            res.append(TwoQuotes[0])
            res.append(TwoQuotes[1])
        else:
            res.append(quote)
    return res

#DEVELOPER Note: used to clean up list from site format
def cleanQuoteList(QuoteList):
    QuoteList = breakUneven(QuoteList)
    QuoteList[99] = (QuoteList[99].split('\\n\\t​'))[0]
    Result = []
    for quote in QuoteList:
        if '\\n\\t' in quote:
            quote = quote.split('\\n\\t')[0]
        quote = quote.replace("\\u0027", "'")
        Result.append(quote)
    return Result

def writeToFile(QuoteList):
    with io.open('movie_List.txt', 'w', encoding="utf-8") as wfile:
        count = 1
        for quote in QuoteList:
            line = str(count) + '___' + str(quote) + '\n'
            #line = line.replace(':', '')
            print(line)
            wfile.write(line)
            count = count + 1
    wfile.close()


def main():
    r = requests.get('https://www.infoplease.com/arts-entertainment/movies-and-videos/top-100-movie-quotes')
    info = str((r.text)).split('\\n\\n\\n\\n\\n\\n\\n\\t')[1].split('\\nSource:')[0]
    #break into quotes
    UnCleanList = info.split('\\n\\t\\n\\t\\n\\t')
    #Now clean up quotes to get our list
    QuoteList = cleanQuoteList(UnCleanList)
    writeToFile(QuoteList)
    #for quote in QuoteList:
    #    print(quote)

if __name__ == "__main__":
    main()

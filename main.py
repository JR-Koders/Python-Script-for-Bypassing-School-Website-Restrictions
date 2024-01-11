
try:
    # base of this script, the search function gets up to 100 google results
    from googlesearch import search
    # requests is very import, it allows us to request websites
    import requests
    # beautifulsoup parses the html from a website, detecting if a wesbite is blocked or not
    from bs4 import BeautifulSoup
    # to get the terminal size
    import os
    # to be able to print things in color
    from colorama import init
    init()
    from termcolor import colored
except ImportError:
    # if a library couldn't be imported, then tell the user how to install it
    print("""Some modules aren't importing! You are probably missing some!
          \nTo install them, run \"pip install --upgrade requests bs4 Beautifulsoup4 google colorama termcolor\"""")
    exit(1)


# this function checks if a given url is blocked by mccsc or not
def checkIfUrlBlocked(url: str) -> str:
    # by default, a url is not blocked
    blocked = "unblocked"

    # try to request the website, if not responding or something else then it's broken
    try:
        # print("requesting the website", end='\r')
        webPage = requests.get(url=url, timeout=5)
    except:
        # print("ohoh, this url doesn't work")
        blocked = "broken"
        return blocked
    
    # initialize beautifulsoup
    soup = BeautifulSoup(webPage.text, 'lxml')

    # NOTE: here, I detect wether it's blocked or not by using the number of specific elements that in my case
    # corresponded to a blocked website, if this is not working for you, then output the html to an html file
    # like so
    # with open('output.html', 'wb') as f:
    #     f.write(webPage.text)
    # and try to find by yourself the elements that distinguish a blocked webpage from a valid webpage

    try:
        if len(soup.find_all('input', {'type': 'Hidden'})) > 10:
            blocked = "blocked"
    except:
        pass
    
    # this can return "unblocked", "broken" or "blocked"
    return blocked



# this function extracts the domain name from url
def getDomain(url):
    try:
        from urllib.parse import urlparse
    except ImportError:
        print("Error, you need the urllibe library.\nTo install it, type: \"pip install --upgrade urllib\"")
    
    t = urlparse(url).netloc
    domain = '.'.join(t.split('.')[-2:])

    return domain

def printOnlyOneLine(toBePrinted: str, color: str):
    toPrint = toBePrinted
    terminalSize = os.get_terminal_size()[0]
    if len(toPrint) > terminalSize:
        # then let's cut it to the right size and add three dots at the end
        toPrint = toPrint[terminalSize-3:]
        toPrint += '...'
    else:
        toPrint += ' '*(terminalSize-len(toPrint))
    
    print(colored(toPrint, color))
        


def analyseUrlResult(urlToTest: str, urlResult: str) -> None:
    if urlResult == "unblocked":
        # print("Good news, this website is available: {}".format(urlToTest))
        printOnlyOneLine(urlToTest, 'green')
        Results.append(urlToTest)
    elif urlResult == "blocked":
        # print("Uh-oh, I think this website is blocked: {}".format(urlToTest))
        printOnlyOneLine(urlToTest, 'red')
        listOfBlockedDomains.append(getDomain(urlToTest))
    elif urlResult == "broken":
        # print("Ohhoh, this website is broken: {}".format(urlToTest))
        printOnlyOneLine(urlToTest, 'red')
        listOfBrokenUrls.append(urlToTest)


def main(searchquery: str, numResults: int) -> None:
    # NOTE: searchquery is the string of text that is going to be looked for on google!

    ResultsGen = search(searchquery, tld="co.in", stop=numResults)
    # This list will contain all the not blocked url ex: "https://balal.com"
    global Results
    Results = []
    # This list will contain blocked domains ex: 'abc.com'
    global listOfBlockedDomains
    listOfBlockedDomains = []
    # this list will contain all the urls that the script failed making contact with
    global listOfBrokenUrls
    listOfBrokenUrls = []


    # loop through the results given by the googlesearch library
    for currentResult in ResultsGen:
        # requests doesn't work by default with https, so replace with http
        urlToTest = currentResult.replace('https', 'http')

        # if the domain name has already been tested as blocked, then there's no need to test the url
        if getDomain(urlToTest) in listOfBlockedDomains:
            continue

        print("Testing this url:", urlToTest, end='\r')
        analyseUrlResult(urlToTest=urlToTest, urlResult=checkIfUrlBlocked(urlToTest))

    print(colored("\nnumber of broken urls = {}".format(len(listOfBrokenUrls)), 'red'))
    print(colored(listOfBrokenUrls, 'red'))

    print(colored("\nnumber of blocked urls = {}".format(len(listOfBlockedDomains)), 'red'))
    print(colored(listOfBlockedDomains, 'red'))

    print(colored("\n\nnumber of unblocked urls = {}".format(len(Results)), 'green'))
    print(colored(Results, 'green'))

def getFullWordTermSize(m: str, sep: str) -> str:
    size = os.get_terminal_size()[0]
    titleBorders = (size-len(m))/2
    return str("\n" + sep*int(titleBorders) + m + sep*int(titleBorders) + "\n")


if __name__ == '__main__':

    query = input(getFullWordTermSize('What do you want to look for on google?', '-'))
    # NOTE: you can't really go above 150-200 results (the googlesearch library doesn't work above)
    numOfResults = int(input(getFullWordTermSize('How many results do you want? (more than 200 won\'t probably work)', '-')))
    main(query, numOfResults)

    print(getFullWordTermSize('Finished', '-'))










### Vivian Thach (vlthach, 33939402) and Alicia Xu (aliciax, 86486004)
### CS 121 Project 3: Search Engine (Complete)
###
import codecs
from bs4 import BeautifulSoup
from collections import defaultdict
import math
#global inverted_index - our index
inverted_index = defaultdict(lambda : defaultdict(list))
# key = term, value = defaultdict is "df": document frequency number, "tf-idf":
# tf-idf score, and webpages where
# key = url and value = tf (int)
# can change if we want
## defaultdict(word, defaultdict(webpage, list(tf, special, tf-idf)))

number_of_documents = 0
webpages_not_found = 0
special_characters = "\'`~!@#$%^&*()_=+[]{}|;:<>,./?\"\n\t\r\\" #add hyphen or no?
indexes_off_by_one = ['0/50', '0/83', '0/205', '0/233', '0/260', '0/272',
                     '0/334', '0/453', '0/467', '1/5', '1/20', '1/51',
                     '1/113', '1/131', '1/274', '1/292', '1/307', '1/390',
                     '1/494', '1/498', '2/20']
index_file = codecs.open("index.txt", 'w', encoding = 'utf-8')


file_name = "bookkeeping.tsv"
    
# Reads a line in from the book keeping file
# Returns a list where the first element is the booking index
# and the second element is the webpage
def read_book_keeping_line(file):
    line = next(f)
    l = list()
    for word in line.split():
        word = word.replace("\"", "")
        word = word.replace(",", "")
        l.append(word.strip())
    return l

# Given the book keeping index, find the content of the webpage
# Extract all text and return a tuple of word_list (list of all terms)
# and a special set a list of words that are in one of: h1, h2, h3, bolded,
# strong
# This is where we parse and extract the HTML content using BeautifulSoup
# and lxml.
def find_URL_content(bk_index):
    global number_of_documents
    global webpages_not_found
    #print(bk_index)
    word_list = []
    special_set = set()

    try:
        if(bk_index in indexes_off_by_one):
            l = bk_index.split("/")
            bk_index = l[0] + "/" + str(int(l[1])-1)
        content = codecs.open(bk_index, 'r', encoding = 'utf-8')
        soup = BeautifulSoup(content, 'lxml')
        t = soup.find_all('h1')
        t.extend(soup.find_all('h2'))
        t.extend(soup.find_all('h3'))
        t.extend(soup.find_all('b'))
        t.extend(soup.find_all('strong'))
        
        for i in t:
            for j in i.text.split():
                if(len(j) != 0):
                    new_word = j.translate({ord(character): " " for character in special_characters}).strip()
                    if (len(new_word) != 0):
                        if (len(new_word.split()) > 1):
                            for word2 in new_word.split():
                                special_set.add(word2.strip().lower())
                        else:
                            special_set.add(new_word.strip().lower())   
        for word in soup.get_text().split():
            strip_word(word, word_list)
            
    except:
        number_of_documents -= 1
        print("FILE NOT FOUND")
        pass
       
    return (word_list, special_set)

# Helper method to strip a term of special characters (if any) and separate
# the term further (if able to)
def strip_word(word,l):
    if(len(word) != 0):
        new_word = word.translate({ord(character): " " for character in special_characters}).strip()
        if (len(new_word) != 0):
            if (len(new_word.split()) > 1):
                for word2 in new_word.split():
                    l.append(word2.strip().lower())
            else:
                l.append(new_word.strip().lower())    

# Puts all the terms and documents into our inverted index:
# defaultdict(word, defaultdict(webpage, list(tf, special, tf-idf)))
# Also counts the term frequency
def process_content_into_index(word_list,special_set, webpage):
    for word in word_list:
        if(word not in inverted_index.keys()or webpage not in inverted_index[word].keys()):
            inverted_index[word][webpage].append(1)
            if(word in special_set):
                inverted_index[word][webpage].append(True)
            else:
                inverted_index[word][webpage].append(False)
        else:
            inverted_index[word][webpage][0] += 1 # term frequency

# Once the inverted index is created, we call this to set each term-document
# pair's TF-IDF and add it to the term-document pair in the inverted index
def set_tfidf():
    for key in inverted_index.keys():
        for webpage in inverted_index[key].keys():
            inverted_index[key][webpage].append(get_tfidf(inverted_index[key][webpage][0],len(inverted_index[key]),inverted_index[key][webpage][1]))

# Helper method to calculate TF-IDF given a term frequency, document
# frequency and if the term is special or not (h1, h2, h3, bold, strong)
def get_tfidf(tf,df,special):
    #log(1 + tf) x log(N/df)
    if(special):
        return math.log10((1+tf)) * math.log10(number_of_documents/df);
    else:
        return math.log10((1+tf)) * math.log10(number_of_documents/df);

# Method to print and/or write the inverted index into a text file (index_file)
def print_inverted_index():
    for key in sorted(inverted_index.keys()):
        #s = ""
        s2 = ""
        s = "{} ".format(key)
        for key2 in inverted_index[key].keys():
            s2+= "({}, {}), ".format(key2, inverted_index[key][key2])
        #print ("%-20s"%(s) + "(" + s2[:-2] + ")\n") #adjust -20s spacing when needed
        index_file.write("%-20s"%(s) + "(" + s2[:-2] + ")\n")

# Given a query, strip and split it into a list of terms (if more than one)
# Go through the inverted index to find the term(s); if they aren't found
# prints that it wasn't found, else it will return a dictionary of retrieved
# webpages along with its value: TF-IDF
def retrieve_query(query):
    qlist = query.split()
    rdict = {}
    wlist = []
    for q in qlist:
        strip_word(q, wlist)

    for term in wlist:
        if term in inverted_index.keys():
            for site,val in inverted_index[term].items():
                if(site not in rdict):
                    rdict[site] = [val[2],1]
                else:
                   rdict[site][0] = rdict[site][0] + val[2]
                   rdict[site][1] += 1
        else:
            print("Term " + term + " was not found!")

    # If the site contains both terms (instead of just one) add
    # a special weight (3)
    for site,l in rdict.items():
        if l[1] == len(wlist):
            l[0] += 3
    return rdict

# Sorts the dictionary into a list of webpages based on TF-IDF
# and prints the top 5
def print_results(rdict):
    rankedList = sorted(rdict, key=rdict.get, reverse=True)
    topn = 5

    if(len(rankedList) < 5):
        topn = len(rankedList)
        
    for x in range(0,topn): #prints top 5 urls
        print(str(x+1) + " : " + rankedList[x] + " :tf-idf: " + str(rdict[rankedList[x]]))


# Main function of our program that starts it.
if __name__ == "__main__":
    
    f = codecs.open(file_name, 'r', encoding = 'utf-8')
    f2 = codecs.open(file_name, 'r', encoding = 'utf-8')
    
    count = 1;
    number_of_documents = len(f2.readlines())
    book_keeping = ""
    print("Creating Index...")
    while(count <= number_of_documents):
        book_keeping = read_book_keeping_line(f)
        count = count + 1
        content = find_URL_content(book_keeping[0])
        process_content_into_index(content[0], content[1], book_keeping[1])
    set_tfidf()
    print("Finished Creating Index!")
    
    print("Printing/writing inverted index...")    
    print_inverted_index()
    print("Number of documents: {}".format(number_of_documents))
    print("Number of unique words: {}".format(len(inverted_index.keys())))
    print("Done with printing/writing inverted index!")
    index_file.close()
    query = input("Please enter a query: ")
    while(query != 'quit'):
        ranked_list = retrieve_query(query)
        print_results(ranked_list)
        query = input("Please enter a query: ")
    print("Ending Search Program.")
        
        

        

    
        
    


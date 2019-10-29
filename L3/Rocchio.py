"""
.. module:: SearchIndexWeight
SearchIndex
*************
:Description: SearchIndexWeight
    Performs a AND query for a list of words (--query) in the documents of an index (--index)
    You can use word^number to change the importance of a word in the match
    --nhits changes the number of documents to retrieve
:Authors: bejar
:Version:
:Created on: 20/10/2019 18:40
"""
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse
import math

from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

__author__ = 'Pol i Ruben'


"""
FUNCIONS LABS ANTERIORS
"""
def doc_count(client, index):
    """
    Returns the number of documents in an index
    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

def search_file_by_path(client, index, path):
    """
    Search for a file using its path
    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError('File [%s] not found'%path)
    else:
        return lfiles[0].meta.id


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term
    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, doc_type='document', id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    sum = 0
    for _,x in tw.items():
        sum += math.pow(x,2)
    norm =math.sqrt(sum)
    result = {}
    for t,w in tw.items():
        result[t] = w/norm

    return result

def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document
    :param file:
    :return:
    """
    # Get document terms frequency and overall terms document frequency
    file_tv, file_df = document_term_vector(client, index, file_id)
    max_freq = max([f for _, f in file_tv])
    dcount = doc_count(client, index)

    tfidfw = {}
    for (t, w),(_, df) in zip(file_tv, file_df):
        # 1. Calculo tfid: nombre freq del doc entre freq total
        tfid = w / max_freq
        # 2. Calculo idfi (inversa freq del doc sobre el term i)
        idfi = math.log(dcount / df,2)
        weight = tfid * idfi
        tfidfw[t] = weight
        pass
    return normalize(tfidfw)

def RocchioRule(alpha,beta,dupla_query,tfidfwquery,nhits):
    """
    NOU CODI
    Aplica la regla de Rocchio aplicant els parametres d'entrada
    """
    newquery= {}
    for word, weight in dupla_query.items():

        meank = tfidfwquery[word]/nhits
        w = int(alpha)*int(weight)
        w += int(beta)*int(meank)
        newquery[word] = w

    return newquery

def query2list(query):
    """
    Return the same input of the query in list format
    :param: String of a query
    :return: List of [word,weight]
    """
    l = {}
    for word in query:
        if "^" not in word:
            l[word] = 1
        else:
            s = word.split("^")
            l[s[0]] = s[1]
    return l

def list2query(dupla_query):
    """
    Return a query in string format
    :param: List of [word,weight]
    :return: String of a query
    """
    sq=""
    for t,w in dupla_query.items():

        strw =  str(int(w))
        sq += t+"^"+strw+" "

    return sq

def calculateTFIDFofList(dupla_query,docsit,client,index):
    """
    Return a list of each word of the query. List is: [query, totalD]
    totalD is the sum of the TFIFD of the k relevants documents
    :param: words of query, k relevant docs, client and index
    :return: list of [query, totalD]
    """

    tfidfwquery = {}
    #Inicialitzem a 0 totes les paraules
    for word,_ in dupla_query.items():
        tfidfwquery[word] = 0

    for dk in docsit:
        iddoc = search_file_by_path(client, index, dk.path)
        result = toTFIDF(client, index, iddoc)
        for word , _ in dupla_query.items():
            tfidfwquery[word] += result[word]

    return tfidfwquery
#Each word have the total weight (not the mean o k docs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    # NOUS PARAMETRES AFEGITS (alpha, beta, R, nrounds)
    parser.add_argument('--nrounds', default=1, type=int, help='Number of iterations for applicate Rocchio formula')
    parser.add_argument('-R', default=None, type=int, help='Maximum number of new terms to be kept in the new query')
    parser.add_argument('--alpha', default=None, type=int, help='Alpha parameter for Rocchio rule')
    parser.add_argument('--beta', default=None, type=int, help='Beta parameter for Rocchio rule')

    args = parser.parse_args()

    index = args.index
    query = args.query
    nhits = args.nhits

    #VARIABLES PELS NOUS PARAMETRES
    nrounds = args.nrounds
    r = args.R
    alpha = args.alpha
    beta = args.beta

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            q = Q('query_string',query=query[0])
            for i in range(1, len(query)):
                q &= Q('query_string',query=query[i])

            s = s.query(q)
            response = s[0:nhits].execute()

            #Reutilitzem la funció query2list per obtemir la dupla (paraula, pes)
            dupla_query = query2list(query)
            print('Iteracio: %s Query Actual =%s' % ('1',  query))
            #Obtenim TFIDF i reutilitzem la funció calculateTFIDFofList
            tfidfwquery = calculateTFIDFofList(dupla_query,response,client,index)

            #Aplicarem la Rocchio's Rule amb nrounds de iteracions
            for i in range(3,nrounds):
                #Apliquem Rocchio's Rule
                dupla_query = RocchioRule(alpha,beta,dupla_query,tfidfwquery,nhits)

                #Nova query a partir dels resultats del Rocchio's Rule
                newquery = list2query(dupla_query)

                print('Iteracio: %s Query Actual =%s' % (str(i-1),  newquery))

                q = Q('query_string',query=newquery[0])
                for i in range(1, len(query)):
                    q &= Q('query_string',query=newquery[i])

                s = s.query(q)
                response = s[0:nhits].execute()

                #Obtenim TFIDF i reutilitzem la funció calculateTFIDFofList
                tfidfwquery = calculateTFIDFofList(dupla_query,response,client,index)

            #Iteracio nround de Rocchio
            dupla_query = RocchioRule(alpha,beta,dupla_query,tfidfwquery,nhits)  #Retornem query final

            #Nova query a partir dels resultats de la ultima itreacio de Rocchio's Rule
            newquery = list2query(dupla_query)


            print('Iteracío FINAL: %s Query =%s' % (str(nrounds),  newquery))
            q = Q('query_string',query=newquery[0])
            for i in range(1, len(query)):
                q &= Q('query_string',query=newquery[i])
            s = s.query(q)
            response = s[0:nhits].execute()
            for r in response:  # only returns a specific number of results
                print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
                print('PATH= %s' % r.path)
                print('TEXT: %s' % r.text[:50])
                print('-----------------------------------------------------------------')
                print ('%d Hits Totals'% response.hits.total.value)
        else:
            print('No query parameters passed')



    except NotFoundError:
        print('Index %s does not exists' % index)

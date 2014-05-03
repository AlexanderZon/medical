import urllib
import re
from pymongo import *
import os

URL = 'http://diagnosticodesintomas.com'
htmlfile = urllib.urlopen(URL)
htmltext = htmlfile.read()

conexion = Connection()

db = conexion['medical']

colenfermedades = db['enfermedades']
colcaracteristicas = db['caracteristicas']
colsintomas = db['sintomas']

def getSintomasURLs():
    htmlfile = urllib.urlopen(URL)
    htmltext = htmlfile.read()
    regex = "<a rel='external' href='/tengo/(.+?)'>"
    pattern = re.compile(regex)
    urls = re.findall(pattern, htmltext)
    return urls

def getSintomasByURLs(urls):
    sintomas = {}
    for n in range(len(urls)):
        regex = "<a rel='external' href='/tengo/"+ urls[n] +"'>(.+?)</a>"
        pattern = re.compile(regex)
        temp = (re.findall(pattern, htmltext))
        try:
            temp = temp[0].decode('utf-8')
            collection = { 'id': n, 'content': temp}
            print temp
            sintomas[n] = temp
            colsintomas.insert(collection)
        except Exception as e:
            print "ERROR: "
            print e

        #raw_input()
        
    print sintomas
    return sintomas

def insertCaracteristicasInCollection(caracteristicas, i):
    collections = {}
    for j in range(len(caracteristicas[i])):
        try:
            print "    CARACTERISTICAS: " + caracteristicas[i][j].decode('utf-8')
            collection = { 'description': caracteristicas[i][j].decode('utf-8') }
            #print collection
            collection = colcaracteristicas.insert(collection)
            #collections[str(j)] = { 'id': collection._id }
        except Exception as e:
            print "ERROR: ", j
            print e
    print "COLECCION: ",collections
    return collections

def updateSintomas(collections, i):
    #print ''
    #print 'COLLECTIONs: ' 
    #print collections
    try:
        colsintomas.update( { 'id': i }, { '$set' : { 'caracteristicas': collections } } )
    except Exception as e:
        print "ERROR: " 
        print e

def parseCaracteristicasHRef(href):
    caracteristicasURLs = {}
    for i in range(len(href)):
        pass
    


def getCaracteristicasURLs(urls):
    caracteristicasURLs = {}
    #for i in range(len(urls)):
    for i in range(10):
        html = urllib.urlopen(URL + '/tengo/' + urls[i] ).read()
        regex = "<li class='liadd'>(.+?)</li>"
        pattern = re.compile(regex)
        caracteristicasURLs[i] = re.findall(pattern, html)
        print caracteristicasURLs[i]
    return True



def getCaracteristicasBySintomas(urls):
    caracteristicas = {}
    #for i in range(len(urls)):
    for i in range(10):
        html = urllib.urlopen(URL + '/tengo/' + urls[i] ).read()
        regex = "<li class='liadd'>(.+?)</li>"
        pattern = re.compile(regex)
        caracteristicas[i] = re.findall(pattern, html)
        raw_input()
        os.system('cls')
        print caracteristicas[i]       
        try:
            print sintomas[i]
            collections = insertCaracteristicasInCollection(caracteristicas, i)
            updateSintomas(collections, i)
        except Exception as e:
            print "ERROR: ", i
            print e
        print ""
        print "FALTAN ", (len(urls) - i ) ," iteraciones"
        print ""
        print ""
    return caracteristicas

SintomasURLs = getSintomasURLs()
Sintomas = getSintomasByURLs(SintomasURLs)
CaracteristicasURLs = getCaracteristicasURLs(SintomasURLs)

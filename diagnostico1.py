import urllib
import re
from pymongo import *
import sys


URL = 'http://diagnosticodesintomas.com'
htmlfile = urllib.urlopen(URL)
htmltext = htmlfile.read()

conexion = Connection()

db = conexion['medical']

colenfermedades = db['enfermedades']
colcaracteristicas = db['caracteristicas']
colsintomas = db['sintomas']

def idCalculate( i , j):
    return '{0}{1}'. format(i,j)

def getEnfermedadesURL():
    regex = "<a rel='external' href='/enfermedad/(.+?)'>"
    pattern = re.compile(regex)
    urls = re.findall(pattern, htmltext)
    return urls

def getEnfermedadesByURLs(urls):
    enfermedades = {}
    for n in range(len(urls)):
        regex = "<a rel='external' href='/enfermedad/"+ urls[n] +"'>(.+?)</a>"
        pattern = re.compile(regex)
        temp = (re.findall(pattern, htmltext))
        try:
            temp = temp[0].decode('utf-8')
            collection = { 'id': n, 'content': temp}
            print temp
            enfermedades[n] = temp
            colenfermedades.insert(collection)
         
        #except AttributeError, IndexError:
        #    print "ERROR de Atributos"
        #    break
        #except IndexError:
        #    print "ERROR de Indice"
        #    break
        except:
            pass
    print enfermedades
    return enfermedades

def insertCaracteristicasInCollection(caracteristicas, i):
    collections = {}
    for j in range(len(caracteristicas[i])):
        try:
            print "    SINTOMA: " + caracteristicas[i][j].decode('utf-8')
            collection = { 'id': idCalculate(i,j),  'description': caracteristicas[i][j].decode('utf-8') , 'enfermedadId': i}
            print collection
            colcaracteristicas.insert(collection)
            collections['caracteristica_'+str(j)] = { 'id': idCalculate(i,j),  'description': caracteristicas[i][j].decode('utf-8') , 'enfermedadId': i}
        except Exception as e:
            print "ERROR: ", j
            print e
    return collections

def updateEnfermedades(collections, i):
    print ''
    print 'COLLECTIONs: ' 
    print collections
    try:
        colenfermedades.update( { 'id': i }, { '$set' : { 'caracteristicas': collections } } )
    except Exception as e:
        print "ERROR: " 
        print e


def getCaracteristicasByEnfermedades(urls):
    caracteristicas = {}
    #for i in range(len(urls)):
    for i in range(10):
        html = urllib.urlopen(URL + '/enfermedad/' + urls[i] ).read()
        regex = '<li [^.]*>(.+?)</li>'
        pattern = re.compile(regex)
        caracteristicas[i] = re.findall(pattern, html)
        
        try:
            print enfermedades[i]
            collections = insertCaracteristicasInCollection(caracteristicas, i)
            updateEnfermedades(collections, i)
        except:
            pass
        print ""
        print "FALTAN ", (len(urls) - i ) ," iteraciones"
        print ""
        print ""

    return caracteristicas

def getSintomasURLs():
    URL = 'http://diagnosticodesintomas.com'
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
    print sintomas
    return sintomas


'''
colenfermedades.insert(enfermedades)
colcaracteristicas.insert(sintomas)
'''
urls = getEnfermedadesURL()
enfermedades = getEnfermedadesByURLs(urls)
caracteristicas = getCaracteristicasByEnfermedades(urls)

urls = getSintomasURLs()
sintomas = getSintomasByURLs(urls)
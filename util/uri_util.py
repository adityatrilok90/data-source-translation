import os
import rdflib
from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal, RDF, OWL, BNode
from datetime import datetime
import pandas as pds


def make_uri_map(filename):
    # build graph
    g = rdflib.Graph()
    g.parse(filename)

    # add mapping: lowercase short uri / label -> uri
    uri_map = {}
    for subj in g.subjects(RDF.type, OWL.Class):
        if type(subj) != rdflib.term.BNode:
            # use encode('ascii', 'ignore') to ignore unicode characters
            short_uri = str(subj.encode('ascii', 'ignore')).lower().split('/')[-1]
            uri_map[short_uri] = str(subj.encode('ascii', 'ignore'))

    # g.parse(filename)
    # print  g.triples( (None, None, None) )
    # for subj, obj in g.subject_objects(RDFS.label):
    for subj, pred, obj in g.triples((None, None, None)):
            # g.query("select ?subj ?pred ?obj where {?subj <http://www.w3.org/2000/01/rdf-schema#label> ?obj .}"):
            # g.triples((None, None, None)):
            # g.query("select ?subj ?pred ?obj where { ?subj rdfs:label ?obj .} limit 100"):

        print (subj, pred, obj)
        labelx = str(obj.encode('ascii', 'ignore')).lower()
        print labelx
        uri_map[labelx] = str(subj.encode('ascii', 'ignore'))

    return uri_map

def write_uri_map(uri_map, filename='uri_map.txt'):
    # save label2uri to file
    with open(filename, 'w') as f:
        f.write(str(uri_map)) # note: uri_map is converted to string


def load_uri_map(force=False, filepath=__file__, filename='uri_map.txt'):
    # create and the lable2uri under the following two coditions:
    # the file does NOT exist OR force is True
    # uri_map_full_name = os.path.join(filepath, filename)
    uri_map_full_name = os.path.join(os.path.abspath('.'), filename)
    if force == True or os.path.exists(uri_map_full_name) == False:
        # print "creating map"
        # make the uri_map map
        uri_map = make_uri_map()

        # write uri_map to file
        write_uri_map(uri_map, uri_map_full_name)

    # otherwise read uri_map from file
    else:
        # print "load from file"
        uri_map = eval(open(uri_map_full_name).read())

    # return uri_map
    return uri_map

uri_map = make_uri_map('simple-dental-ontology.owl')
# print uri_map
# print uri_map.items()
# print pds.DataFrame(uri_map.items(), columns=['label', 'uri'])
# write_uri_map(uri_map)
# print uri_map['restored tooth']
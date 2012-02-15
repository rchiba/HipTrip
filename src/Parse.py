#!/usr/bin/python
# -*- coding: utf-8 -*-
import rdflib

from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef
from rdflib import RDF
from rdflib import RDFS

graph = Graph()

graph.bind("dc", "http://http://purl.org/dc/elements/1.1/")
graph.bind("foaf", "http://xmlns.com/foaf/0.1/")
graph.bind("fb", "http://rdf.freebase.com/ns/")

graph.parse("http://rdf.freebase.com/rdf/en.nikola_tesla", format="xml")
graph.parse("http://rdf.freebase.com/rdf/en.johann_wolfgang_goethe", format="xml")

test = Namespace('http://example.com/test/')
graph.add((test['user/1'], test['name'], Literal('Fernando')))

print len(graph)

print graph.serialize(format="xml")
print graph.serialize(format="nt")

for triple in graph:
    print triple

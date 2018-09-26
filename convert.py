import os
from os import path
import rdflib


def export_classes_as_yaml(g, filename, ont_yaml_dir):
    yaml = None
    # get ont details for file header
    q = '''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?label 
    WHERE {
        ?ont a owl:Ontology ;
             rdfs:label ?label .
        FILTER(lang(?label) = "" || langMatches(lang(?label), "EN"))
    }
    '''
    for r in g.query(q):
        yaml = '# classes in the ontology: ' + r['label'] + '\n\n'

    if yaml is None:
        yaml = '# classes in the ontology ' + filename + '\n\n'

    q = '''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?c ?label ?comment
    WHERE {
        {?c a rdfs:Class .}
        UNION
        {?c a owl:Class .}
        ?c rdfs:label ?label ;
           rdfs:comment ?comment .
        FILTER(lang(?label) = "" || langMatches(lang(?label), "EN"))
        FILTER(lang(?comment) = "" || langMatches(lang(?comment), "EN"))
    } ORDER BY ?c
    '''

    for c in g.query(q):
        yaml += str(c['c']) + ': ' + '\n'
        yaml += '  label: ' + yaml_str(c['label'])
        yaml += '  description: ' + yaml_str(c['comment']) + '\n'

    with open(os.path.join(ont_yaml_dir, name.split('.')[0] + '_classes.yml'), 'w', encoding='utf-8') as f:
        f.write(yaml)


def export_properties_as_yaml(g, filename, ont_yaml_dir):
    yaml = None
    # get ont details for file header
    q = '''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?label 
    WHERE {
        ?ont a owl:Ontology ;
             rdfs:label ?label .
        FILTER(lang(?label) = "" || langMatches(lang(?label), "EN"))
    }
    '''
    for r in g.query(q):
        yaml = '# properties in the ontology: ' + r['label'] + '\n\n'

    if yaml is None:
        yaml = '# properties in the ontology ' + filename + '\n\n'

    q = '''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?c ?label ?comment
    WHERE {
        {?c a rdf:Property .}
        UNION    
        {?c a rdfs:Property .}
        UNION
        {?c a owl:AnnotationProperty .}
        UNION
        {?c a owl:DatatypeProperty .}
        UNION
        {?c a owl:ObjectProperty .}
        ?c rdfs:label ?label ;
           rdfs:comment ?comment .
        FILTER(lang(?label) = "" || langMatches(lang(?label), "EN"))
        FILTER(lang(?comment) = "" || langMatches(lang(?comment), "EN"))
    } ORDER BY ?c
    '''

    for c in g.query(q):
        yaml += str(c['c']) + ': ' + '\n'
        yaml += '  label: ' + yaml_str(c['label'])
        yaml += '  description: ' + yaml_str(c['comment']) + '\n'

    with open(os.path.join(ont_yaml_dir, name.split('.')[0] + '_properties.yml'), 'w', encoding='utf-8') as f:
        f.write(yaml)


def yaml_str(i):
    return '"' + str(i).replace('\n', ' ').replace('\r', '').replace('  ', '').replace('"', '\\"') + '"\n'


if __name__ == '__main__':
    APP_DIR = path.dirname(path.realpath(__file__))
    ONTS_TO_PROCESS_DIR = path.join(APP_DIR, 'onts_to_process')
    ONTS_PROCESSED_DIR = path.join(APP_DIR, 'onts_processed')
    ONTS_YAML_DIR = path.join(APP_DIR, 'onts_yaml')

    # read all onts in onts_to_process
    for root, dirs, files in os.walk(ONTS_TO_PROCESS_DIR):
        for name in files:
            print('processing ' + name)
            g = rdflib.Graph()
            file_path = os.path.join(root, name)
            g.parse(file_path, format=rdflib.util.guess_format(file_path))
            export_classes_as_yaml(g, name, ONTS_YAML_DIR)
            export_properties_as_yaml(g, name, ONTS_YAML_DIR)
            print(len(g))

    # for each ont
        # extract ont metadata
        # extract class info
        # write YAML file into onts_yaml

        # extract properties info
        # write YAML file into onts_yaml

        # move ont to onts_processed dir
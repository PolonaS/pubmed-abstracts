import xml.etree.ElementTree
import shutil
import os

from lib.db import create_table, insert
from lib.schwartz import extract_pairs


FILE = "pubmed_results.xml"
RESULTS = None  # if you want limit just put integer here


root = xml.etree.ElementTree.parse(FILE).getroot()


def parse_abstracts(el, results=None):
    if results is None:
        results = []
    for child in el:
        if child.tag == 'AbstractText':
            results.append(child.text)
        parse_abstracts(child, results)
    return results


def create_results_folder():
    try:
        os.mkdir("results")
    except OSError:
        pass


def create_file(abstracts, file_name):
    f = open("results/" + file_name, "w")
    f.write("\n".join(abstracts))
    f.close()


def create_orig_file(id, abstracts):
    create_results_folder()
    create_file(abstracts, file_name=id + ".txt")


def create_without_acronym_file(id, abstracts):
    create_results_folder()
    create_file(abstracts, file_name=id + "_without_acronym.txt")


def create_without_definition_file(id, abstracts):
    create_results_folder()
    create_file(abstracts, file_name=id + "_without_definition.txt")


def parse():
    for article in root:
        id = article.find("MedlineCitation").find("PMID").text
        abstracts = parse_abstracts(article)
        create_orig_file(id, abstracts)
        abstracts_without_acronym = []
        abstracts_without_definition = []
        for abstract in abstracts:
            sentences = abstract.split(". ")
            for sentence in sentences:
                pairs = extract_pairs(sentence)
                abstract_without_acronym = abstract
                abstract_without_definition = abstract
                for pair in pairs:
                    insert(id, pair["acronym"], pair["definition"])
                    abstract_without_acronym = abstract_without_acronym.replace(pair["acronym"], "")
                    abstract_without_definition = abstract_without_definition.replace(pair["definition"], "")
                abstracts_without_acronym.append(abstract_without_acronym)
                abstracts_without_definition.append(abstract_without_definition)
        create_without_acronym_file(id, abstracts_without_acronym)
        create_without_definition_file(id, abstracts_without_definition)


def main():
    shutil.rmtree("results", True)
    create_table()
    parse()


if __name__ == "__main__":
    main()

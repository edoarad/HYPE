import xml.etree.ElementTree as et
import unicodecsv as csv
from pathlib import Path


def make_csv_from_ART(ART_corpus_dir_path, csv_file_path):
    directories = [Path(ART_corpus_dir_path + '\\ann' + str(i)) for i in range(1,10)]
    with open(csv_file_path, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, dialect="excel", encoding='UTF-8')
        csv_writer.writerow(["Paper", "Annotation", "Content"])
        for d in directories:
            for xfile in d.iterdir():
                name = (str(xfile.name))[:-4]
                tree = et.parse(xfile)
                root = tree.getroot()
                for annot in root.iter('annotationART'):
                    typ = annot.attrib['type']
                    sen = "".join(annot.itertext()) # Captures all sub-tags
                    csv_writer.writerow([name, typ, sen])
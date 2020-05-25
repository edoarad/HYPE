import xml.etree.ElementTree as et
from tokenize import String
import subprocess
import unicodecsv as csv
from pathlib import Path
import requests
import pandas as pd


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


def get_tsv_url_from_spike_query(query: String = '\\\"boolean\\\": \\\"coronavirus\\\"'):
    """
    :param query: of the form
        '\\\"token\\\": \\\"virus\\\", \\\"boolean\\\": \\\"coronavirus\\\"'
    """

    request = f'curl -v -X POST "http://35.246.128.202:5000/api/3/search/query" ' \
              f'-H "accept: application/json" -H "Content-Type: application/json" ' \
              f'-d "{{ \\\"queries\\\": {{ {query} }},' \
              f' \\\"data_set_name\\\": \\\"covid19\\\"}}"'
    stream = subprocess.Popen(request, shell=True, stderr=subprocess.PIPE)
    out = stream.stderr
    tsv_path = str(out.readlines()[20])
    assert tsv_path[4:16] == 'TSV-Location'
    tsv_path = 'http://35.246.128.202:5000' + tsv_path[18:-7]
    return tsv_path


def get_csv_from_tsv_url(url, file_path = './downloaded_query.csv'):
    r = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(r.content)
    csv_table = pd.read_table(file_path, sep='\t')
    csv_table.to_csv(file_path, index=False)


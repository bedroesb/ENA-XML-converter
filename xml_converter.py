from lxml import etree
from io import StringIO, BytesIO
from jinja2 import Environment, FileSystemLoader
import requests

checklists = ["ERC000012", "ERC000013", "ERC000014", "ERC000015", "ERC000016", "ERC000017", "ERC000018", "ERC000019", "ERC000020", "ERC000021", "ERC000022", "ERC000023", "ERC000024", "ERC000025", "ERC000027", "ERC000028", "ERC000029", "ERC000030", "ERC000031", "ERC000032", "ERC000033", "ERC000034", "ERC000035", "ERC000036", "ERC000037", "ERC000038", "ERC000039", "ERC000040", "ERC000041", "ERC000043", "ERC000044", "ERC000045", "ERC000047", "ERC000048", "ERC000049", "ERC000050", "ERC000051", "ERC000052", "ERC000053", "ERC000011"]

for checklist in checklists:
    print(f"Parsing {checklist}")
    url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{checklist}?download=true"
    r = requests.get(url, allow_redirects=True)

    xml_tree = {}

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    root = etree.fromstring(r.content)

    for attribute in root.iter('FIELD'):
        name = ''
        cardinality = ''
        for sub_attr in attribute:
            if sub_attr.tag == 'NAME':
                name = sub_attr.text
            elif sub_attr.tag == 'MANDATORY':
                cardinality = sub_attr.text
        xml_tree[name] = cardinality

    t = env.get_template('ENA_sample_template.xml')
    output_from_parsed_template = t.render(attributes=xml_tree)
    with open(f"ENA_template_samples_{checklist}.xml", "w") as fh:
        fh.write(output_from_parsed_template)


import os
import subprocess

from lxml import etree

rcc_path = '../.venv/Scripts/pyside6-rcc.exe'
exclude_files = ['resources.qrc, resources.py']

script_path = os.getcwd()
resources_folder = os.path.join(os.path.dirname(script_path), 'app/resources')

resources_paths = []
resources_files = []

for root, dirs, files in os.walk(resources_folder):
    for file in files:
        if file in exclude_files:
            continue
        resources_paths.append(os.path.join(root, file))

for path in resources_paths:
    resources_files.append(path.replace(resources_folder + '\\', ''))

root = etree.Element('RCC')
root.set('version', '1.0')
qresource = etree.SubElement(root, 'qresource')
for file in resources_files:
    child = etree.SubElement(qresource, 'file')
    child.text = file

with open(os.path.join(resources_folder, 'resources.qrc'), 'wb') as xml:
    head = '<!DOCTYPE RCC>\n'
    xml.write(head.encode('utf-8'))
    xml.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=False))

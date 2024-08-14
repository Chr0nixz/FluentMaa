import os
import subprocess

from lxml import etree

import dictionary

language = 'zh_CN'

lup_path = '../.venv/Scripts/pylupdate5.exe'

scan_path = ['view']
exclude = ['__init__.py', '__pycache__']

ts_path = 'app/resources/i18n/maa.' + language + '.ts'
temp_path = 'app/resources/i18n/temp.ts'

root = etree.Element('TS')
root.set('version', '2.1')
root.set('language', language)
root.set('sourcelanguage', "en_US")

path = os.getcwd()
parent = os.path.dirname(path)
ts_path = os.path.join(parent, ts_path)
temp_path = os.path.join(parent, temp_path)

translation = dict()
if language == 'zh_CN':
    translation = dictionary.zh_CN

for scan_file in scan_path:

    path = os.path.join(parent, 'app', scan_file)

    for file in os.listdir(path):
        if file in exclude:
            continue

        file = os.path.join(path, file)
        command = lup_path + ' ' + file + ' -ts ' + temp_path
        print(command)
        subprocess.call(command)

        temp_root = etree.parse(temp_path)
        context = temp_root.find('context')

        for message in context.findall('message'):
            source = message.find('source').text
            if source in translation:
                text = translation.get(source)
                if text:
                    child = message.find('translation')
                    child.attrib.pop('type', None)
                    child.text = text
                else:
                    print('翻译为空:' + source)
            else:
                print('无翻译:' + source)

        root.append(context)
        os.remove(temp_path)

os.remove(ts_path)

with open(ts_path, 'wb') as xml:
    head = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n'
    xml.write(head.encode('utf-8'))
    xml.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=False))

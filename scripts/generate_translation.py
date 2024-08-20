import os
import subprocess

from lxml import etree

import dictionary

language = 'zh_CN'

lup_path = '../.venv/Scripts/pyside6-lupdate.exe'
lre_path = '../.venv/Scripts/pyside6-lrelease.exe'

scan_path = [
    'view',
    'components',
    'components/setting_cards',
    'components/task_setting_views'
]
exclude = ['__init__.py', '__pycache__']

check_translation = True

ts_path = 'app/resources/i18n/maa.' + language + '.ts'
qm_path = 'app/resources/i18n/maa.' + language + '.qm'
temp_path = 'app/resources/i18n/temp.ts'


root = etree.Element('TS')
root.set('version', '2.1')
root.set('language', language)
root.set('sourcelanguage', "en_US")

path = os.getcwd()
parent = os.path.dirname(path)
ts_path = os.path.join(parent, ts_path)
qm_path = os.path.join(parent, qm_path)
temp_path = os.path.join(parent, temp_path)

translation = dict()
if language == 'zh_CN':
    translation = dictionary.zh_CN

for scan_file in scan_path:

    path = os.path.join(parent, 'app', scan_file)

    for file in os.listdir(path):
        if file in exclude or os.path.isdir(file):
            continue

        file = os.path.join(path, file)
        command = lup_path + ' ' + file + ' -ts ' + temp_path
        print(command)
        subprocess.call(command)

        temp_root = etree.parse(temp_path)
        contexts = temp_root.findall('context')

        for context in contexts:
            for message in context.findall('message'):
                source = message.find('source').text
                if source in translation:
                    text = translation.get(source)
                    if text:
                        child = message.find('translation')
                        child.attrib.pop('type', None)
                        child.text = text
                    else:
                        print('\033[91m翻译为空:\033[0m' + source)
                        check_translation = False
                else:
                    print('\033[91m无翻译:\033[0m' + source)
                    check_translation = False
            root.append(context)
        os.remove(temp_path)

os.remove(ts_path)

with open(ts_path, 'wb') as xml:
    head = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n'
    xml.write(head.encode('utf-8'))
    xml.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=False))

if check_translation:
    command = lre_path + ' ' + ts_path + ' -qm ' + qm_path
    subprocess.call(command)
else:
    print('Please use linguist to release.')

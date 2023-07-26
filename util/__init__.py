# -*- coding: utf-8 -*-
import codecs
from jinja2 import Environment, FileSystemLoader, Template
import os
import json
import re

class CaseConverter:
    def __init__(self, word):
        self.word_list = list()
        word = re.sub('([A-Z])', '_\\1', word)
        if word[0] == '_':
            word = word[1:]
        if '_' in word:
            self.word_list = word.split('_')
        else:
            self.word_list.append(word.lower())
        pass
    def to_upper_snake_case(self):
        snake_case = '_'.join(self.word_list).upper()
        return snake_case
    def to_lower_snake_case(self):
        snake_case = '_'.join(self.word_list).lower()
        return snake_case
    def to_upper_camel_case(self):
        upper_camel_case_word = ''.join([i[0].upper() + i[1:] for i in self.word_list])
        return upper_camel_case_word
    def to_lower_camel_case(self):
        tmp = self.to_upper_camel_case()
        lower_camel_case_word = tmp[0].lower() + tmp[1:]
        return lower_camel_case_word
    def to_kebab_case(self):
        return self.to_lower_snake_case().replace('_', '-')

def to_lower_snake_case(param):
    return CaseConverter(param).to_lower_snake_case()
def to_upper_snake_case(param):
    return CaseConverter(param).to_upper_snake_case()
def to_lower_camel_case(param):
    return CaseConverter(param).to_lower_camel_case()
def to_upper_camel_case(param):
    return CaseConverter(param).to_upper_camel_case()

def get_template_file_path(language: str, template_type: str):
    template_file_path: str = ''
    template_file_path = f'./ore/{language}/{template_type}.{language}.j2'
    try:
        if os.path.isfile(template_file_path):
            return template_file_path
        else:
            print('テンプレートファイルが見つかりません')
            exit(0)
    except:
        print('テンプレートファイルが見つかりません')
        exit(0)

def create_concrete_from_params(template_file_name: str, params: dict, output_file_name: str):

    # テンプレートファイル読み込み
    if not os.path.isfile(template_file_name):
        print('テンプレートファイル[' + template_file_name + ']が見つかりませんでした')
        return
    template_file = codecs.open(template_file_name, 'r', 'utf8')


    env = Environment(loader=FileSystemLoader('.'), trim_blocks=False)
    env.filters['to_lower_snake_case'] = to_lower_snake_case
    env.filters['to_upper_snake_case'] = to_upper_snake_case
    env.filters['to_lower_camel_case'] = to_lower_camel_case
    env.filters['to_upper_camel_case'] = to_upper_camel_case
    template = env.get_template(template_file_name)
    #template = Template(template_file.read())
    #template_file.close()

    # 出力ファイル書き込み
    try:
        output_file = codecs.open(output_file_name, 'w', 'utf8')
        output_file.write(template.render(params))
        output_file.close()
        print('[' + output_file_name + ']を作成しました')
    except:
        print('ファイル[' + output_file_name + ']を作成できませんでした')
        pass
    return

def create_concrete_from_files(template_file_name: str, params_file_name: str, output_file_name: str):

    # テンプレートファイル読み込み
    if not os.path.isfile(template_file_name):
        print('テンプレートファイル[' + template_file_name + ']が見つかりませんでした')
        return
    # template_file = codecs.open(template_file_name, 'r', 'utf8')
    # template = Template(template_file.read())
    # template_file.close()

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=False)
    env.filters['to_lower_snake_case'] = to_lower_snake_case
    env.filters['to_upper_snake_case'] = to_upper_snake_case
    env.filters['to_lower_camel_case'] = to_lower_camel_case
    env.filters['to_upper_camel_case'] = to_upper_camel_case
    template = env.get_template(template_file_name)

    # パラメータファイル読み込み
    if not os.path.isfile(params_file_name):
        print('パラメータファイル[' + params_file_name + ']が見つかりませんでした')
        return
    params_file = codecs.open(params_file_name, 'r', 'utf8')
    params = json.load(params_file)
    params_file.close()

    # 出力ファイル書き込み
    try:
        output_file = codecs.open(output_file_name, 'w', 'utf8')
        output_file.write(template.render(params))
        output_file.close()
        print('ファイル[' + output_file_name + ']を作成しました')
    except:
        print('ファイル[' + output_file_name + ']を作成できませんでした')
        pass
    return



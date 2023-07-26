# -*- coding: utf-8 -*-

import json
import codecs
import util
import os
import re

import config
output_root = config.OUTPUT_ROOT

def mkdir(dir: str):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return

def dao(extension: str):
    # 出力ディレクトリ設定
    dao_root = f'{output_root}/dao'
    mkdir(dao_root)
    action_root = f'{output_root}/action'
    mkdir(action_root)
    template_root = f'{output_root}/template'
    mkdir(template_root)

    # 入力ファイル
    input_file_name = 'db/db.json'
    input_file = codecs.open(input_file_name, 'r', 'utf8')
    domain_dict = json.load(input_file)
    for table in domain_dict.get('tableList'):
        table_name = table['name']
        columnList = table['columnList']
        mkdir(dao_root + '/' + table_name)
        class_name = util.CaseConverter(table_name).to_upper_camel_case()
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{dao_root}/{table_name}/{class_name}.{extension}')
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{dao_root}/{table_name}/{class_name}Dao.{extension}')
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{dao_root}/{table_name}/{class_name}FindList.{extension}')

        # 画面とペアになっているコントローラはここで生成
        mkdir(action_root + '/' + table_name)
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{action_root}/{table_name}/{class_name}DetailAction.{extension}')
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{action_root}/{table_name}/{class_name}ListAction.{extension}')
        mkdir(template_root + '/' + table_name)
        page_name = util.CaseConverter(table_name).to_lower_camel_case()
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{template_root}/{table_name}/{page_name}Detail.html')
        util.create_concrete_from_params(f'db/{extension}/db.{extension}.j2', table, f'{template_root}/{table_name}/{page_name}List.html')
    return
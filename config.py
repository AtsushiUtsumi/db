# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
import os
load_dotenv()

# デフォルトは親ディレクトリ
default_output_root = '..'

# 環境変数を参照
import os
OUTPUT_ROOT = default_output_root
candidate_output_root = os.getenv('OUTPUT_ROOT')

if os.path.exists(candidate_output_root):
    OUTPUT_ROOT = candidate_output_root
else:
    print('異常な出力ディレクトリ:[' + candidate_output_root + ']')
    exit(0)
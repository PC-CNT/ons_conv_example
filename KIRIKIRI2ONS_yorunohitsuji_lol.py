from pathlib import Path
import re

def title_info():
    return {
        'brand': '夜のひつじ',
        'date': 20141230,
        'title': '相思相愛ロリータ',
        'cli_arg': 'yorunohitsuji_lol',
        'requiredsoft': [],
        'is_4:3': bool(not r'<ONS_RESOLUTION_CHECK_DISABLED>' in default_txt()),
        'exe_name': ['lol'],
        'input_resolution': (1024, 768),#スクリプトで処理する解像度と実際の画像の解像度が合致しない場合後者をここに記入

        'version': [
            '相思相愛ロリータ DMM GAMES DL版(yoruno_0001)',
        ],

        'notes': [
            'ここに説明を記載',
        ]
    }


def extract_resource(values: dict, values_ex: dict, pre_converted_dir: Path):
    from utils import extract_archive_garbro # type: ignore
    # ここにマルチコンバータ利用時の自動展開処理を記載(最悪Prince-of-seaがやるので放置で可)

    return


def default_txt():
    return '''\
'''


# メイン関数
def main(values: dict = {}, values_ex: dict = {}, pre_converted_dir: Path = Path.cwd()):

    _txt = default_txt()
    
    ks_list = [
        "A000.ks",
        "A001.ks",
        "A002.ks",
        "B000.ks",
        "B001.ks",
        "B002.ks",
        "B003.ks",
        "C000.ks",
        "ending.ks"
    ]
    
    _raw = ""
    
    for ks in ks_list:
        with open(pre_converted_dir / "data" / "scenario" / ks, encoding="cp932", errors="ignore") as f:
            _raw += f.read()
    
    _txt += _raw
    
    with open(pre_converted_dir / "0.txt", "x", encoding="cp932") as f:
        f.write(_txt)
    
    return


#事前に展開済みなら単体でも動作するようにしておく
if __name__ == "__main__":
    main()

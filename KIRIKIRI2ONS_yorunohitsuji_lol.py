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


# effect生成時に使う関数
def effect_edit(t,f, effect_startnum, effect_list):
    # 「何ミリ秒間」、「どの画像効果で」フェードするかを引数で受け取りeffect_listに記録、
    # エフェクト番号を(effect_startnumからの)連番で発行
    # また、過去に同一の秒数/画像の組み合わせを利用した場合は再度同じエフェクト番号になる
    list_num = 0
    if re.fullmatch(r'[0-9]+', t):#timeが数字のみ＝本処理

        for i, e in enumerate(effect_list,effect_startnum + 1):#1からだと番号が競合する可能性あり
            if (e[0] == t) and (e[1] == f):
                list_num = i

        if not list_num:
            effect_list.append([t, f])
            list_num = len(effect_list) + effect_startnum
    
    else:
        print('ERROR: effect指定ミス')

    return str(list_num), effect_startnum, effect_list


#吉里吉里の命令文及び変数指定をざっくりpythonの辞書に変換するやつ
def krcmd2krdict(c):
    kr_dict = {}

    for p in re.findall(r'([A-z0-9-_]+?)=("(.*?)"|([^\t\s]+))', c):
        kr_dict[p[0]] = p[2] if p[2] else p[3]

    return kr_dict


# ディレクトリの存在チェック関数
def dir_check(path_list):

    CHK = True
    for p in path_list:
        if not p.exists():
            print('ERROR: "' + str(p) + '" is not found!')
            CHK = False
            
    return CHK


# 文字列置換
def message_replace(txt):
    if (r'[' in txt):
        print('message error:' + txt)

    cnvl = [
        ['1', '１'], ['2', '２'], ['3', '３'], ['4', '４'], ['5', '５'], ['6', '６'], ['7', '７'], ['8', '８'], ['9', '９'], ['0', '０'],

        ['a', 'ａ'], ['b', 'ｂ'], ['c', 'ｃ'], ['d', 'ｄ'], ['e', 'ｅ'], ['f', 'ｆ'], ['g', 'ｇ'], ['h', 'ｈ'], ['i', 'ｉ'], ['j', 'ｊ'],
        ['k', 'ｋ'], ['l', 'ｌ'], ['m', 'ｍ'], ['n', 'ｎ'], ['o', 'ｏ'], ['p', 'ｐ'], ['q', 'ｑ'], ['r', 'ｒ'], ['s', 'ｓ'], ['t', 'ｔ'], 
        ['u', 'ｕ'], ['v', 'ｖ'], ['w', 'ｗ'], ['x', 'ｘ'], ['y', 'ｙ'], ['z', 'ｚ'], 

        ['A', 'Ａ'], ['B', 'Ｂ'], ['C', 'Ｃ'], ['D', 'Ｄ'], ['E', 'Ｅ'], ['F', 'Ｆ'], ['G', 'Ｇ'], ['H', 'Ｈ'], ['I', 'Ｉ'], ['J', 'Ｊ'], 
        ['K', 'Ｋ'], ['L', 'Ｌ'], ['M', 'Ｍ'], ['N', 'Ｎ'], ['O', 'Ｏ'], ['P', 'Ｐ'], ['Q', 'Ｑ'], ['R', 'Ｒ'], ['S', 'Ｓ'], ['T', 'Ｔ'], 
        ['U', '∪'], ['V', '∨'], ['W', 'Ｗ'], ['X', 'Ｘ'], ['Y', 'Ｙ'], ['Z', 'Ｚ'], 

        ['%', '％'], ['!', '！'], ['?', '？'], [' ', '　'], [':', '：'], [';', '；'], 
    ]

    for v in cnvl:
        txt = txt.replace(v[0], v[1])

    return txt


# txt置換→0.txt出力関数
def text_cnv(debug, zero_txt, scenario):

    # effect管理用変数
    effect_startnum = 10
    effect_list = []

    #default.txtを読み込み
    txt = default_txt()
    
    _l = [
        (scenario / 'A000.ks'),
        (scenario / 'A001.ks'),
        (scenario / 'A002.ks'),
        (scenario / 'B000.ks'),
        (scenario / 'B001.ks'),
        (scenario / 'B002.ks'),
        (scenario / 'B003.ks'),
        (scenario / 'C000.ks'),
        (scenario / 'ending.ks'),
    ]

    #シナリオファイルを読み込み
    for p in _l:
        with open(p, encoding='cp932', errors='ignore') as f:
            fr = f.read()
            fr = re.sub(r'\[ruby\stext\s?=\s?"(.+?)"\](.+?)', r'(\2/\1)', fr)#ルビをons仕様に
            fr = re.sub(r'\@(.+?)\n', r'[\1]\n', fr)# @からの命令も[]同様に処理したいので
            fr = fr.replace(r'[l]', '@')# 文章停止
            fr = fr.replace(r'[ll]', '@\n')# 文章停止+改行
            fr = fr.replace(r'[cm]', '\ntextclear_d\n')# メッセージ表示を一旦消す?
            fr = fr.replace(r'[pcm]', '\ntextclear_d\n')# とりあえずcmと同様の実装で
            fr = fr.replace(r'[r]', '　\n')# 一行完全な空白
            fr = re.sub(r'\[(.+?)\]', r'\n[\1]\n', fr)#ここまで来てまだ文中に挟まってる命令は強制改行
            fr = re.sub(r'\@\n*\\', r'\\', fr)#＠￥両方になってるのを消す
    
            #デコード済みtxt一つごとに開始時改行&サブルーチン化
            if debug:
                txt += '\n;--------------- '+ str(p.name) +' ---------------'
            txt += '\n*SCR_'+ str(p.name).replace('.', '_') +'\n\n'

            for line in fr.splitlines():
                kakko_line = re.search(r'\[(.+?)\]', line)

                #改行は無視
                if re.match('\n', line):
                    pass
                
                #元々コメントアウトのやつ目立たせる
                elif re.match(r';', line):
                    line = (r';;;;' + line) if debug else ''
                
                #gotoと間違えそうなやつ
                elif re.match(r'\*', line): 
                    line = (';' + line) if debug else ''

                #textclear
                elif re.match(r'textclear_d', line):
                    pass

                #多分セリフとか
                elif not re.match(r'\[', line):
                    #半角置換
                    mrline = message_replace(line)

                    if mrline:
                        #行末@削除
                        if mrline[-1] == '@': mrline = mrline[0:-1]
                    
                    if mrline:
                        #無の行はクリック@飛ばす
                        if mrline == '　': line = 'ab "' + mrline + '",1'
                        else: line = 'ab "' + mrline + '",0'
                    
                    else:
                        line = ''

                #命令文 - []内
                elif kakko_line:
                    d = krcmd2krdict('kr_cmd=' + kakko_line[1])
                    kr_cmd = d['kr_cmd']

                    if kr_cmd == 'msgc':
                        line = 'textclear_d'

                    elif kr_cmd == 'wait':
                        line = ('wait ' + d['time'])

                    elif kr_cmd == 'quake':
                        line = ('quake 4,' + d['time'])

                    elif kr_cmd == 'jump':
                        storage = d['storage']
                        
                        if (storage == 'logo.ks'):
                            line = ('mov %500,1:reset')

                        else:
                            line = ('goto *SCR_'+ str(storage).replace('.', '_'))

                    elif kr_cmd == 'background' or kr_cmd == 'ecgbg':
                        storage = d['storage']
                        time = d['time']
                        method = d['method']
                        rule = d.get('rule')
                        msgc = d.get('msgc')

                        effect_num, effect_startnum, effect_list = effect_edit(time, 'fade', effect_startnum, effect_list) if (method == 'crossfade') else effect_edit(time, rule, effect_startnum, effect_list)

                        line = ('bg "data\\bgimage\\' + storage + '.png",' + effect_num)

                        if (msgc == 'true'):
                            line += '\ntextclear_d'

                    elif kr_cmd == 'fgitrans':
                        #methodはcrossfade固定
                        #pageはfore固定
                        storage = d['storage']
                        time = d['time']
                        layer = d['layer']# 0 or 1 →20/21で運用しようかと
                        pos = d['pos']
                        msgc = d.get('msgc')

                        effect_num, effect_startnum, effect_list = effect_edit(time, 'fade', effect_startnum, effect_list)

                        line = ('tati "data\\fgimage\\' + storage + '.png",' + effect_num + ',2' + layer + ',"' + pos + '"')

                        if (msgc == 'true'):
                            line += '\ntextclear_d'

                    elif kr_cmd == 'fgic':
                        layer = d['layer']
                        effect_num, effect_startnum, effect_list = effect_edit('500', 'fade', effect_startnum, effect_list)
                        line = ('csp 2' + layer + ':print ' + effect_num)

                    elif kr_cmd == 'freeimage':
                        layer = d['layer']
                        effect_num, effect_startnum, effect_list = effect_edit('200', 'fade', effect_startnum, effect_list)
                        line = ('csp 2' + layer + ':print ' + effect_num)

                    elif kr_cmd == 'image':
                        #本作だとラストの白背景表示のみ
                        effect_num, effect_startnum, effect_list = effect_edit('1800', 'fade', effect_startnum, effect_list)
                        line = ('bg white,' + effect_num)

                    elif kr_cmd == 'clickskip':
                        enabled = d['enabled']

                        if (enabled == 'true'):
                            line = ''
                        else:
                            line = 'skipoff'

                    elif kr_cmd == 'playse':
                        storage = d['storage']
                        line = 'dwave 1,"data\\sound\\' + storage + '.ogg"'

                    elif kr_cmd == 'playbgm':
                        storage = d['storage']
                        line = 'bgm "data\\bgm\\' + storage + '.ogg"'

                    elif kr_cmd == 'stopbgm':
                        line = 'bgmstop'

                    elif kr_cmd == 'fadeinbgm':
                        storage = d['storage']
                        time = d['time']

                        line = 'bgmfadein ' + time
                        line += ':bgm "data\\bgm\\' + storage + '.ogg"'
                        line += ':bgmfadein 0'

                    elif kr_cmd == 'fadeoutbgm':
                        time = d['time']

                        line = 'bgmfadeout ' + time
                        line += ':stop'
                        line += ':bgmfadeout 0'

                    #他
                    else:
                        if debug:
                            #pass
                            print(kr_cmd)

                        line = (';' + line) if debug else ''

                #その他 - エラー防止の為コメントアウト(多分ない)
                else:
                    line = (';' + line) if debug else ''
            
                #変換した命令行が空ではない場合
                if line:
                    txt += (line + '\n')#入力

    # エフェクト定義用の配列を命令文に&置換
    add0txt_effect = ''
    for i,e in enumerate(effect_list,effect_startnum+1):

        if e[1] == 'fade':
            add0txt_effect +='effect ' + str(i) + ',10,'+e[0]+'\n'

        else:
            add0txt_effect +='effect ' + str(i) + ',18,'+e[0]+',"data\\rule\\'+str(e[1]).replace('"','')+'.png"\n'
    
    #ガ バ ガ バ 修 正
    txt = txt.replace('wait 7000\n@', 'wait 7000\n')
    #txt = txt.replace(r'', '')

    txt = txt.replace(r';<<-EFFECT->>', add0txt_effect)

    #出力結果を書き込み
    open(zero_txt, 'w', encoding='cp932', errors='ignore').write(txt)

    return


def junk_del(delete_list):

    #リスト内のディレクトリパスでfor
    for d in delete_list:

        #ディレクトリパス内のファイル一覧でfor
        for p in d.glob('*'):

            #削除
            p.unlink()
        
        #ディレクトリも削除
        d.rmdir()

    return


# メイン関数
def main(values: dict = {}, values_ex: dict = {}, pre_converted_dir: Path = Path.cwd()):

    #(マルチコンバータ利用時)自動展開
    if values: extract_resource(values, values_ex, pre_converted_dir)

    debug = 0

    #同一階層のパスを変数へ代入
    same_hierarchy = pre_converted_dir#Path.cwd()

    #debug時にtestフォルダに入れないやつ(default.txt等)はこっちを利用
    same_hierarchy_const = same_hierarchy

    if debug:
        #デバッグ時はtestディレクトリ直下
        same_hierarchy = (same_hierarchy / '_test')

    #利用するパスを辞書に入れ一括代入
    PATH_DICT = {
        #先に準備しておくべきファイル一覧
        'bgimage' :(same_hierarchy / 'data' / 'bgimage'),
        'bgm' :(same_hierarchy / 'data' / 'bgm'),
        'fgimage' :(same_hierarchy / 'data' / 'fgimage'),
        'image' :(same_hierarchy / 'data' / 'image'),
        'others' :(same_hierarchy / 'data' / 'others'),
        'rule' :(same_hierarchy / 'data' / 'rule'),
        'scenario' :(same_hierarchy / 'data' / 'scenario'),
        'sound' :(same_hierarchy / 'data' / 'sound'),
        'system' :(same_hierarchy / 'data' / 'system'),
        'video' :(same_hierarchy / 'data' / 'video'),

        'startup_tjs' :(same_hierarchy / 'data' / 'startup.tjs'),
    }

    PATH_DICT2 = {
        #変換後に出力されるファイル一覧
        '0_txt'  :(same_hierarchy / '0.txt'),
    }

    #ディレクトリの存在チェック
    dir_check_result = dir_check(PATH_DICT.values())

    #存在しない場合終了
    if not dir_check_result:
        return

    #txt置換→0.txt出力
    text_cnv(debug, PATH_DICT2['0_txt'], PATH_DICT['scenario'])

    #不要データ削除
    if not debug:
        junk_del([
            PATH_DICT['others'],
            PATH_DICT['scenario'],
            PATH_DICT['video'],
        ])


#事前に展開済みなら単体でも動作するようにしておく
if __name__ == "__main__":
    main()

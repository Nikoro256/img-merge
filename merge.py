from PIL import Image
import os.path, json, mimetypes, glob, logging

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warning message')
# logger.error('error message')
# logger.critical('critical message')

# フォーマットを定義
formatter = '%(levelname)s : %(asctime)s : %(message)s'

# ログレベルを DEBUG に変更
logging.basicConfig(
    filename='logfile/logger.log',
    level=logging.DEBUG,
    format=formatter
)

# 現在のロギングの情報を取得(引数はファイル名)
logger = logging.getLogger(__name__)

logger.info('merge.py起動')

def check_setting_file(file_name):
    """
    設定ファイルを確認＆値取得  
    ---
    Parameter:
        string: 設定用jsonファイル名 *.json
    return:
        boolean: flag, json
    """
    logger.info('設定ファイル確認開始')

    # エラー判定用
    flag = False

    try:
        logger.info('設定ファイル名: ' + file_name)
        json_open = open(file_name, 'r')
    except FileNotFoundError as e:
        logger.error('setting.jsonがありません')
        return flag, 'setting.jsonがありません'
    else:
        json_load = json.load(json_open)
        logger.info('jsonファイル内: ' + str(json_load))
        flag = True

        return flag, json_load


def list_dir_file(dir_name):
    """
    画像ディレクトリ内ファイル取得
    ---
    Parameter:
        string: 画像保存ディレクトリ名
    return:
        list: ファイル名
    """
    logger.info('ディレクトリ内のファイル取得開始')

    # directory名内の全ファイルを取得
    files = glob.glob(dir_name + '/*')
    logger.info('画像ディレクトリ内: ' + str(files))

    return files


def check_type(file_list, type_list):
    """
    ディレクトリ内ファイルのMIMEタイプを比較 
    --- 
    Parameter:
        file_list:
            list: ディレクトリ内ファイルリスト
        type_list:
            list: setting.jsonのimgTypeリスト
    return
        list: ファイルタイプが一致したファイル名
    """
    logger.info('ディレクトリ内のファイルタイプ比較開始')

    img_file_list = []

    for file in file_list:
        # ファイルタイプ取得
        file_type, encode = mimetypes.guess_type(file)

        # ファイル対応がリストにあるか判定
        if file_type in type_list:
            img_file_list.append(file)

    return img_file_list


def img_save(file, file_name, extention):
    """
    画像保存
    ---
    Parameter:
        file: 
            image: 画像ファイル
        file_name: 
            string: 保存ファイル名
    保存先はカレントカレントディレクトリ
    """
    logger.info('画像保存開始')

    file_path = './{}{}'.format(file_name, extention)
    try:
        file.save(file_path, quality=100)
    except ZeroDivisionError as e:
        logger.error('ZeroDivisionError:' +  str(e))
        # return 'ZeroDivisionError:' +  str(e)
    except NameError as e:
        logger.error('NameError:' + str(e))
        # return 'NameError:' + str(e)
    except Exception as e:
        logger.error('Exception:' + str(e))
        # return 'Exception:' + str(e)

    return True


def merge_img(file_list, file_name):
    """
    画像結合 
    --- 
    Parameter:
        list: ファイル名のリスト
    return:
        string: 完了メッセージ
    error:
        string: 画像が4枚以上の場合エラー
    """
    logger.info('画像結合開始')

    # 画像ファイル数
    num = len(file_list)

    if num != 4:
        response = False
        logger.error('画像が４枚ではありません')
    else:
        for i, file in enumerate(file_list):
            # ファイルを画像として開く
            img = Image.open(file)

            # 画像サイズ取得
            img_width, img_height = img.size

            re_width = int(img_width / 2)
            re_height = int(img_height / 2)

            if i == 0:
                #　画像背景の作成
                new_file = Image.new('RGB', (img_width, img_height))

            # 画像縮小
            re_img = img.resize((re_width, re_height))

            if i == 0:
                new_file.paste(re_img, (0, 0))
            elif i == 1:
                new_file.paste(re_img, (re_width, 0))
            elif i == 2:
                new_file.paste(re_img, (0, re_height))
            elif i == 3:
                new_file.paste(re_img, (re_width, re_height))

        # 保存処理
        response = img_save(new_file, file_name, '.jpeg')

    return response


if __name__ == "__main__":

    setting = 'setting.json'

    print('-----------------------')
    
    print('結合開始')

    flag, json = check_setting_file(setting)

    file_list = list_dir_file(json['directory'])
    type_list = json['imgType'].split(',')
    merge_list = check_type(file_list, type_list)

    if merge_img(merge_list, json['fileName']):
        logger.info('merge.py終了')
        print('結合終了')
    else:
        logger.error('merge.py異常終了')
        print('異常終了')
        
    print('-----------------------')


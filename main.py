from tello import TelloController
import sys
from datetime import datetime
import time


def process_command_line(command, tello_controller):
    """コマンド1行分の処理"""
    if command != '' and command != '\n':
        # コマンドの後の空白や空行を削除
        command = command.rstrip()

        if command.find('delay') != -1:
            # 待機コマンドの場合
            delay_time_sec = command.partition('delay')[2]
            sec = float(delay_time_sec)
            print(f"{sec}[秒]待機")
            time.sleep(sec)
            pass
        else:
            # 待機以外のコマンドの場合、TELLOにコマンドを送信する
            tello_controller.send_command(command)


def logging(tello_controller):
    """ログ記録＆表示処理"""
    # 記録されたログを取得
    log = tello_controller.get_log()

    # ログ出力ファイル名を生成（log/<時刻>.txt）
    log_file = 'log/' + str(datetime.now()) + '.txt'

    # ログファイルを書き込みモードでオープン
    try:
        with open(log_file, 'w') as out_file:
            for stat in log:
                # statからログ情報を1つ抜き出して表示する
                stat.print_stats()
                # ログファイルに書き出す
                out_file.write(stat.return_stats())
    except IOError:
        # エラー表示
        print(f"予期せぬエラーが発生しました")


def send_tello_commands(file_name):
    """TELLOにファイルから読み出したコマンドを1つずつ送信する"""
    # TELLOを制御するためのクラスの生成
    tello_controller = TelloController()

    # コマンドの実行
    try:
        # コマンドファイルを開く
        with open(file_name, 'r') as in_file:
            # 全ての行数分取り出す
            commands = in_file.readlines()
            for command in commands:
                # 1行分を取り出してコマンド解析し送信する
                process_command_line(command, tello_controller)
    except FileNotFoundError:
        # エラー表示
        print(f"コマンドファイルが見つかりませんでした {file_name}")
    except IOError:
        # エラー表示
        print(f"予期せぬエラーが発生しました {file_name}")

    # ログ記録＆表示
    logging(tello_controller)


# メイン処理
if len(sys.argv) == 2:
    # 引数からコマンドが書かれたファイル名を取得する
    send_tello_commands(sys.argv[1])
else:
    # エラー表示
    print(f"引数が間違っています")

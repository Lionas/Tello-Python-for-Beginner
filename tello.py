import socket
import threading
import time
from stats import Stats


class TelloController:
    """TELLO制御クラス"""

    def __init__(self):
        """初期化処理"""
        # 通信ソケットの生成
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))

        # コマンド受信用スレッド
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # TELLOのIPアドレスとポートの設定
        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)

        # コマンド送信履歴用のリスト
        self.log = []

        # コマンドの最大待ち時間までの時間[秒]
        self.MAX_TIME_OUT = 15.0

    def send_socket(self, command):
        """ソケット通信でコマンドを送信する"""
        # 指定されたIPアドレス/ポートを有する相手（TELLO）にコマンドを送信する
        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        # 送信したコマンドを表示
        print(f"コマンド {command} を {self.tello_ip} に送信しました")

    def is_timeout(self, start_time):
        """コマンドの最大待ち時間を経過したかどうか"""
        # 現在の時間を記憶
        now = time.time()
        # コマンド送信時刻からの経過時間を計算
        diff = now - start_time
        # 経過時間がコマンドの最大待ち時間を超えていた場合、コマンドの完了を待たずに終了する
        if diff > self.MAX_TIME_OUT:
            # 最大待ち時間を経過した
            return True
        else:
            # 最大待ち時間を経過していない
            return False

    def send_command(self, command):
        """
        指定されたIPアドレス/ポートを有する相手（TELLO）にコマンドを送信します。
        最後のコマンドが「OK」を受け取るまでブロックされます。
        コマンドが失敗した場合（タイムアウトまたはエラーのいずれか）、コマンドを再送しようとします。
        ：param command：送信するコマンド（文字列型）
        ：param ip：TelloのIP（文字列型）
        ：return：最新のコマンド応答
        """
        # 新しくコマンド履歴を生成する
        log = Stats(command, len(self.log))

        # ログの最後尾に、新しく作ったコマンド履歴を追加する
        self.log.append(log)

        # 指定されたIPアドレス/ポートを有する相手（TELLO）にコマンドを送信する
        self.send_socket(command)

        # コマンド送信時刻を記憶
        start_time = time.time()

        # TELLOから応答を受け取るまで繰り返す
        while not self.log[-1].got_response():
            if self.is_timeout(start_time):
                print(f"{command} を送信しましたが応答がありませんでした")
                return

        print(f"{command} を {self.tello_ip} に送信しました！")

    def _receive_thread(self):
        """
        Telloからの応答を受けるための処理。
        スレッドとして実行され、Telloが最後に返したものにself.responseを設定します。
        """
        # 無限ループで受信する
        while True:
            try:
                # ソケットからの受信
                self.response, ip = self.socket.recvfrom(1024)
                # ログ履歴の最後にレスポンスを追加
                self.log[-1].add_response(self.response)
                # レスポンスの内容を表示
                print(f"{ip}'からの応答：{self.response}")
            except socket.error as exc:
                # ソケット通信エラーが発生
                print(f"ソケット通信エラーが発生しました。エラー内容：{exc}")

    # def on_close(self):
    #     pass

    def get_log(self):
        """記録したログを取得"""
        return self.log

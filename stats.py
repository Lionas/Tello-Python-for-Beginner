from datetime import datetime


class Stats:
    """コマンド履歴管理クラス"""
    def __init__(self, command, log_id):
        """初期化"""
        self.command = command
        self.log_id = log_id
        self.response = None
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None

    def add_response(self, response):
        """TELLOからの応答メッセージを追加する"""
        self.response = response
        self.end_time = datetime.now()
        self.duration = self.get_duration_time()

    def got_response(self):
        """取得済み応答メッセージを返す"""
        if self.response is None:
            return False
        else:
            return True

    def get_duration_time(self):
        """所要時間を算出する"""
        diff = self.end_time - self.start_time
        return diff.total_seconds()

    def get_id_str(self):
        """IDの出力メッセージ"""
        return f"id: {self.log_id}"

    def get_command_str(self):
        """コマンドの出力メッセージ"""
        return f"コマンド: {self.command}"

    def get_response_str(self):
        """応答メッセージの出力メッセージ"""
        return f"応答メッセージ: {self.response}"

    def get_start_time_str(self):
        """開始時刻の出力メッセージ"""
        return f"開始時刻: {self.start_time}"

    def get_end_time_str(self):
        """終了時刻の出力メッセージ"""
        return f"終了時刻: {self.end_time}"

    def get_duration_time_str(self):
        """所要時間の出力メッセージ"""
        return f"所要時間: {self.duration}"

    def print_stats(self):
        """コマンド履歴をコンソールに表示する"""
        print("\n")
        print(self.get_id_str())
        print(self.get_command_str())
        print(self.get_response_str())
        print(self.get_start_time_str())
        print(self.get_end_time_str())
        print(self.get_duration_time_str())

    def return_stats(self):
        """コマンド履歴をつなげた文字列を返す"""
        return_str = "\n"
        return_str += self.get_id_str() + "\n"
        return_str += self.get_command_str() + "\n"
        return_str += self.get_response_str() + "\n"
        return_str += self.get_start_time_str() + "\n"
        return_str += self.get_end_time_str() + "\n"
        return_str += self.get_duration_time_str() + "\n"
        return return_str

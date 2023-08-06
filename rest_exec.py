import urllib.request
import json
import csv
import ssl

# CSVを読み込んで辞書のリストに変換
def convert_csv_to_json(csv_data):
    with open(csv_data, 'r') as csv_file:
        # CSVリーダーオブジェクトを作成
        csv_reader = csv.DictReader(csv_file)
        # 各行を辞書に変換し、その辞書をリストに追加
        data_list = [row for row in csv_reader]
    return data_list


# 設定ファイルを読み込む
with open("config.json", "r") as f:
    config = json.load(f)

# 設定ファイルからデータを取得する
url = config["url"]
cert_file = config["cert_file"]
data_file = config["data_file"]

# CSVファイルを読み込み、JSON形式に変換する
with open(data_file, "r") as f:
    csv_data = csv.reader(f)
    json_data_list = convert_csv_to_json(data_file)

for json_data in json_data_list:
    # JSONデータを文字列に変換する
    json_data_string = json.dumps(json_data)

    # クライアント証明書を読み込む
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile=cert_file)

    # POSTリクエストを送信する
    req = urllib.request.Request(url, data=json_data_string.encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=context) as res:
    ## クライアント証明書を使わない場合
    #with urllib.request.urlopen(req) as res:
        response = res.read()
        print(response)

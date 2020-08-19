import os
from pprint import pprint
from estat_api import EstatRestAPI_URLParser
from io_utils import get_json, download_all_csv, download_csv

appId = "65a9e884e72959615c2c7c293ebfaeaebffb6030"  # Application ID
estatapi_url_parser = EstatRestAPI_URLParser()  # URL Parser


def search_tables():
    """
    Prams (dictionary) to search eStat tables.
    For more details, see also 
    https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0#api_3_2

        - appId: Application ID (*required)
        - lang: 言語(J:日本語, E:英語)
        - surveyYears: 調査年月 (YYYYY or YYYYMM or YYYYMM-YYYYMM)
        - openYears: 調査年月と同様
        - statsField: 統計分野 (2桁:統計大分類, 4桁:統計小分類)
        - statsCode: 政府統計コード (8桁)
        - searchWord: 検索キーワード
        - searchKind: データの種別 (1:統計情報, 2:小地域・地域メッシュ)
        - collectArea: 集計地域区分 (1:全国, 2:都道府県, 3:市区町村)
        - explanationGetFlg: 解説情報有無(Y or N)
        - ...
    """
    appId = "65a9e884e72959615c2c7c293ebfaeaebffb6030"  # Application ID
    params_dict = {
        "appId": appId,
        "lang": "J",
        "statsCode": "00200502",
        "searchWord": "社会・人口統計体系",  # "統計でみる市区町村のすがた",
        "searchKind": 1,
        "collectArea": 3,
        "explanationGetFlg": "N"
    }

    url = estatapi_url_parser.getStatsListURL(params_dict, format="json")
    json_dict = get_json(url)
    # pprint(json_dict)

    if json_dict['GET_STATS_LIST']['DATALIST_INF']['NUMBER'] != 0:
        tables = json_dict["GET_STATS_LIST"]["DATALIST_INF"]["TABLE_INF"]
    else:
        tables = []
    return tables


def parse_table_id(table):
    return table["@id"]


def parse_table_raw_size(table):
    return table["OVERALL_TOTAL_NUMBER"]


def parse_table_urls(table_id, table_raw_size, csv_raw_size=100000):
    urls = []
    for j in range(0, int(table_raw_size / csv_raw_size) + 1):
        start_pos = j * csv_raw_size + 1
        params_dict = {
            "appId": appId,  # Application ID
            "lang": "J",  # 言語 (J: 日本語, E: 英語)
            "statsDataId": str(table_id),  # 統計表ID
            "startPosition": start_pos,  # 開始行
            "limit": csv_raw_size,  # データ取得件数
            "explanationGetFlg": "N",  # 解説情報有無(Y or N)
            "annotationGetFlg": "N",  # 注釈情報有無(Y or N)
            "metaGetFlg": "N",  # メタ情報有無(Y or N)
            "sectionHeaderFlg": "2",  # CSVのヘッダフラグ(1:取得, 2:取得無)
        }
        url = estatapi_url_parser.getStatsDataURL(params_dict, format="csv")
        urls.append(url)
    return urls


if __name__ == '__main__':
    CSV_RAW_SIZE = 100000

    # list of tables
    tables = search_tables()

    # extract all table ids
    if len(tables) == 0:
        print("No tables were found.")
    elif len(tables) == 1:
        table_ids = [parse_table_id(tables[0])]
    else:
        table_ids = list(map(parse_table_id, tables))

    # list of urls
    table_urls = []
    table_raw_size = list(map(parse_table_raw_size, tables))
    for i, table_id in enumerate(table_ids):
        table_urls = table_urls + parse_table_urls(table_id, table_raw_size[i])

    # list of filepathes
    filepathes = []
    for i, table_id in enumerate(table_ids):
        table_name = tables[i]["TITLE_SPEC"]["TABLE_NAME"]
        table_dir = f"./downloads/tmp/{table_name}_{table_id}"
        os.makedirs(table_dir, exist_ok=True)
        for j in range(0, int(table_raw_size[i] / CSV_RAW_SIZE) + 1):
            filepath = f"{table_dir}/{table_name}_{table_id}_{j}.csv"
            filepathes.append(filepath)

    download_all_csv(table_urls, filepathes, max_workers=30)

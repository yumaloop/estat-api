import csv
from tqdm import tqdm
from estat_api import EstatRestApiClient

"""
国勢調査(2015)にある統計表のリストをCSVファイルで取得
"""
estat_api_client = EstatRestApiClient(app_id= "65a9e884e72959615c2c7c293ebfaeaebffb6030")
json_dict = estat_api_client.getStatsList(lang="J", surveyYears="2015", statsCode="00200521", format="json")

filepath = "./example2.csv"
with open(filepath, 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["政府統計コード", "政府統計名", "集計名", "統計表ID(StatsDataId)", "統計表名", "表章地域"])

    table_list = json_dict["GET_STATS_LIST"]["DATALIST_INF"]["TABLE_INF"]
    for table in tqdm(table_list):
        tokei_code = table["STAT_NAME"]["@code"]

        if "TABULATION_CATEGORY" in table["STATISTICS_NAME_SPEC"]:
            tokei_name = table["STATISTICS_NAME_SPEC"]["TABULATION_CATEGORY"]
        else:
            tokei_name = ""

        if "TABULATION_SUB_CATEGORY1" in table["STATISTICS_NAME_SPEC"]:
            shukei_name = table["STATISTICS_NAME_SPEC"]["TABULATION_SUB_CATEGORY1"]
        else:
            shukei_name = ""

        if "TABLE_NAME" in table["TITLE_SPEC"]:
            table_name = table["TITLE_SPEC"]["TABLE_NAME"]
        else:
            table_name = ""

        if "TABLE_SUB_CATEGORY1" in table["TITLE_SPEC"]:
            table_areaunit = table["TITLE_SPEC"]["TABLE_SUB_CATEGORY1"]
        else:
            table_areaunit = ""

        table_id = table["@id"]

        row = [tokei_code, tokei_name, shukei_name, table_id, table_name, table_areaunit]
        writer.writerow(row)


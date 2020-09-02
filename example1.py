import json
from pprint import pprint
from estat_api import EstatRestApiClient

"""
国勢調査(2015) > 人口等基本集計にある統計表のリストをJSONファイルで取得
"""

estat_api_client = EstatRestApiClient(app_id= "65a9e884e72959615c2c7c293ebfaeaebffb6030")
json_dict = estat_api_client.getStatsList(lang="J", surveyYears="2015", statsCode="00200521", searchWord="人口等基本集計", limit=10, format="json")

pprint(json_dict)

filepath = "./example1.json"
json_str = json.dumps(json_dict, indent=2, ensure_ascii=False)
with open(filepath, "w") as f:
    f.write(json_str)

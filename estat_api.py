import sys
import urllib
import requests
import common


class EstatRestApiClient:
    """
    This is a simple python module class for e-Stat API (ver.3.0).
    See more details at https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0
    """

    def __init__(self, api_version=None, app_id=None):
        self.base_url = "https://api.e-stat.go.jp/rest"
        self.api_version = "3.0" if api_version is None else api_version
        self.app_id = "65a9e884e72959615c2c7c293ebfaeaebffb6030" if app_id is None else app_id

    def _request_get(self, endpoint, logging=True, stream=True, **params):
        try:
            res = requests.get(endpoint, params=params, stream=stream)
            res.encoding = res.apparent_encoding
            if logging:
                print(res, "HTTP GET:", res.url)
        except requests.exceptions.RequestException as error:
            print(error)
            sys.exit(1)
        return res

    def getStatsList(self, format="csv", **kwargs):
        """
        2.1 統計表情報取得 (HTTP GET)

        Keyword Args:
        =============
        appId: str
            Application ID. *REQUIRED
        lang: str
            language ("J" or "E").
        surveyYears: str
            YYYY or YYYYMM or YYYYMM-YYYYMM
        statsField: str
            数値2桁：統計大分類で検索 or
            数値4桁：統計小分類で検索
        statsCode: str
            数値5桁：作成機関で検索 or
            数値8桁：政府統計コードで検索
        searchWord: str
            検索キーワード
        searchKind: 1,2,3
            1：統計情報(省略値)
            2：小地域・地域メッシュ
            3：社会・人口統計体系
        statsNameList: str
            Y：統計調査名一覧
        startPosition: int (default: 1)
            データの取得開始位置（1から始まる行番号）
            統計データを複数回に分けて取得する場合等、
            前回受信したデータの<NEXT_KEY>タグの値を指定する
        limit: int (default: 100000)
            データの取得行数
        updatedDate: str
            YYYY or YYYYMM or YYYYMMDD or YYYYMMDD-YYYYMMDD
        callback: 
            コールバック関数
            only needed for `jsonp` format requests
        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/getStatsList"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/getStatsList"
            res = self._request_get(endpoint, **params)
            return res.json()
        elif format == "jsonp":
            endpoint = f"{self.base_url}/{self.api_version}/app/jsonp/getStatsList"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "csv":
            endpoint = f"{self.base_url}/{self.api_version}/app/getSimpleStatsList"
            res = self._request_get(endpoint, **params)
            return res.content.decode("utf-8")

    def getMetaInfoURL(self, params_dict, format="csv", **kwargs):
        """
        2.2 メタ情報取得 (HTTP GET)
        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/getMetaInfo"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/getMetaInfo"
            res = self._request_get(endpoint, **params)
            return res.json()
        elif format == "jsonp":
            endpoint = f"{self.base_url}/{self.api_version}/app/jsonp/getMetaInfo"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "csv":
            endpoint = f"{self.base_url}/{self.api_version}/app/getSimpleMetaInfo"
            res = self._request_get(endpoint, **params)
            return res.content.decode("utf-8")

    def getStatsData(self, params_dict, format="csv", **kwargs):
        """
        2.3 統計データ取得 (HTTP GET)

        Keyword Args:
        appId: str
            Application ID. *REQUIRED
        lang: str
            language ("J" or "E").
        dataSetId: str
            「データセット登録」で登録したデータセットID
        statsDataId: str
            統計表ID
        lvTab: 
            絞り込み条件 > 表章事項 > 階層レベル
            "X" or "X-X" or "-X" or "X-"
        cdTab: 
            絞り込み条件 > 表章事項 > 単一コード
            各メタ情報の項目コード
            "X1, X2, X3, ... XN"
        cdTabFrom
            絞り込み条件 > 表章事項 > コードFrom
            絞り込む範囲にある開始位置の項目コード
            "X"
        cdTabTo
            絞り込み条件 > 表章事項 > コードTo
            絞り込む範囲にある終了位置の項目コード
            "X"
        lvTime
            絞り込み条件 > 時間軸事項 > 階層レベル
            "X" or "X-X" or "-X" or "X-"
        cdTime
            絞り込み条件 > 時間軸事項 > 単一コード
        cdTimeFrom
            絞り込み条件 > 時間軸事項 > コードFrom
        cdTimeTo
            絞り込み条件 > 時間軸事項 > コードTo
        lvArea
            絞り込み条件 > 地域事項 > 階層レベル
        cdArea
            絞り込み条件 > 地域事項 > 単一コード
        cdAreaFrom
            絞り込み条件 > 地域事項 > コードFrom
        cdAreaTo
            絞り込み条件 > 地域事項 > コードTo
        lvCat01
            絞り込み条件 > 分類事項 > 階層レベル
        cdCat01
            絞り込み条件 > 分類事項 > 単一コード
        cdCat01From
            絞り込み条件 > 分類事項 > コードFrom
        cdCat01To
            絞り込み条件 > 分類事項 > コードTo
        startPosition: int (default: 1)
            データの取得開始位置（1から始まる行番号）
            統計データを複数回に分けて取得する場合等、
            前回受信したデータの<NEXT_KEY>タグの値を指定する
        limit: int (default: 100000)
            データの取得行数
        metaGetFlg: True or False
            メタ情報有無
        cntGetFlg: True or False
            件数取得フラグ
        sectionHeaderFlg : 1 or 2
            せくチョンヘッダフラグ
            - 1 : セクションヘッダを出力する (省略値)
            - 2 : セクションヘッダを取得しない
        callback: 
            コールバック関数
            only needed for `jsonp` format requests
            

        =============

        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/getStatsData"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/getStatsData"
            res = self._request_get(endpoint, **params)
            return res.json()
        elif format == "jsonp":
            endpoint = f"{self.base_url}/{self.api_version}/app/jsonp/getStatsData"
            res = self._request_get(endpoint, **params)
            # TODO: Refine & Test followings
            return res.text
        elif format == "csv":
            endpoint = f"{self.base_url}/{self.api_version}/app/getSimpleStatsData"
            res = self._request_get(endpoint, **params)
            return res.content.decode("utf-8")

    def postDataset(self):
        """
        2.4 データセット登録 (HTTP POST)
        """
        endpoint = f"{self.base_url}/{self.api_version}/app/postDataset"
        pass

    def refDataset(self, format="xml", **kwargs):
        """
        2.5 データセット参照 (HTTP GET)
        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/refDataset"
            pass
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/refDataset"
            pass
        elif format == "jsonp":
            endpoint = f"{self.base_url}/{self.api_version}/app/jsonp/refDataset"
            pass

    def getDataCatalog(self, format="xml", **kwargs):
        """
        2.6 データカタログ情報取得 (HTTP GET)
        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/getDataCatalog"
            pass
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/getDataCatalog"
            pass
        elif format == "jsonp":
            endpoint = f"{self.base_url}/{self.api_version}/app/jsonp/getDataCatalog"
            pass

    def getStatsDatas(self, format="xml", **kwargs):
        """
        2.7 統計データ一括取得 (HTTP GET)
        """
        params = kwargs
        params["appId"] = self.app_id if not "appId" in params else kwargs["appId"]

        if format == "xml":
            endpoint = f"{self.base_url}/{self.api_version}/app/getStatsDatas"
            pass
        elif format == "json":
            endpoint = f"{self.base_url}/{self.api_version}/app/json/getStatsDatas"
            pass
        elif format == "csv":
            endpoint = f"{self.base_url}/{self.api_version}/app/getSimpleStatsDatas"
            pass

import urllib
import requests


class EstatRestAPI_URLParser:
    """
    This is a simple python module class for e-Stat API (ver.3.0).
    See more details at https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0
    """

    def __init__(self, api_version=None, app_id=None):
        # base url
        self.base_url = "https://api.e-stat.go.jp/rest"

        # e-Stat REST API Version
        if api_version is None:
            self.api_version = "3.0"
        else:
            self.api_version = api_version

        # Application ID
        if app_id is None:
            self.app_id = "65a9e884e72959615c2c7c293ebfaeaebffb6030"
        else:
            self.app_id = app_id

    def getStatsListURL(self, params_dict, format="csv"):
        """
        2.1 統計表情報取得 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getStatsList?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/getStatsList?{params_str}"
            )
        elif format == "jsonp":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/jsonp/getStatsList?{params_str}"
            )
        elif format == "csv":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getSimpleStatsList?{params_str}"
            )
        return url

    def getMetaInfoURL(self, params_dict, format="csv"):
        """
        2.2 メタ情報取得 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getMetaInfo?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/getMetaInfo?{params_str}"
            )
        elif format == "jsonp":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/jsonp/getMetaInfo?{params_str}"
            )
        elif format == "csv":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getSimpleMetaInfo?{params_str}"
            )
        return url

    def getStatsDataURL(self, params_dict, format="csv"):
        """
        2.3 統計データ取得 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getStatsData?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/getStatsData?{params_str}"
            )
        elif format == "jsonp":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/jsonp/getStatsData?{params_str}"
            )
        elif format == "csv":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getSimpleStatsData?{params_str}"
            )
        return url

    def postDatasetURL(self):
        """
        2.4 データセット登録 (HTTP POST)
        """
        url = (
            f"{self.base_url}/{self.api_version}"
            "/app/postDataset"
        )
        return url

    def refDataset(self, params_dict, format="xml"):
        """
        2.5 データセット参照 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                + f"/app/refDataset?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/refDataset?{params_str}"
            )
        elif format == "jsonp":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/jsonp/refDataset?{params_str}"
            )
        return url

    def getDataCatalogURL(self, params_dict, format="xml"):
        """
        2.6 データカタログ情報取得 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getDataCatalog?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/getDataCatalog?{params_str}"
            )
        elif format == "jsonp":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/jsonp/getDataCatalog?{params_str}"
            )
        return url

    def getStatsDatasURL(self, params_dict, format="xml"):
        """
        2.7 統計データ一括取得 (HTTP GET)
        """
        params_str = urllib.parse.urlencode(params_dict)
        if format == "xml":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getStatsDatas?{params_str}"
            )
        elif format == "json":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/json/getStatsDatas?{params_str}"
            )
        elif format == "csv":
            url = (
                f"{self.base_url}/{self.api_version}"
                f"/app/getSimpleStatsDatas?{params_str}"
            )
        return url

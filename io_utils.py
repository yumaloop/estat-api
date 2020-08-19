import csv
import json
import xlrd
import zipfile
import requests
import functools
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def get_json(url):
    """
    Request a HTTP GET method to the given url (for REST API)
    and return its response as the dict object.

    Args:
    ====
    url: string
        valid url for REST API
    """
    try:
        print("HTTP GET", url)
        r = requests.get(url)
        json_dict = r.json()
        return json_dict
    except requests.exceptions.RequestException as error:
        print(error)


def download_json(url, filepath):
    """
    Request a HTTP GET method to the given url (for REST API)
    and save its response as the json file.

    Args:
    url: string
        valid url for REST API
    filepath: string
        valid path to the destination file
    """
    try:
        print("HTTP GET", url)
        r = requests.get(url)
        json_dict = r.json()
        json_str = json.dumps(json_dict, indent=2, ensure_ascii=False)
        with open(filepath, "w") as f:
            f.write(json_str)
    except requests.exceptions.RequestException as error:
        print(error)


def download_str(url, filepath, enc="utf-8", dec="utf-8", logging=False):
    """
    Request a HTTP GET method to the given url (for REST API)
    and save its response as the local text file.

    Args:
    =====
    url: string
        valid url for REST API
    filepathe: string
        valid path to the destination file
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: bool
        flag to display HTTP request status
    """
    try:
        r = requests.get(url, stream=True)
        if logging:
            print("HTTP GET",  f"[{r.status_code}]", url)
        with open(filepath, 'w', encoding=enc) as f:
            f.write(r.content.decode(dec))
    except requests.exceptions.RequestException as error:
        print(error)


def download_all_str(
        urls,
        filepathes,
        max_workers=10,
        enc="utf-8",
        dec="utf-8"):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the local text file.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    Args:
    =====
    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination file
    max_workers: int
        max number of working threads of CPUs within executing this method.
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: True/False
    """
    func = functools.partial(download_str, enc=enc, dec=dec)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(func, urls, filepathes), total=len(urls))
        )
        del results
        return


def download_bin(url, filepath, logging=False):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the xls file.

    Args:
    =====
    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination file
    logging: bool
        flag to display HTTP request status
    """
    try:
        r = requests.get(url, stream=True)
        if logging:
            print("HTTP GET",  f"[{r.status_code}]", url)
        with open(filepath, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.RequestException as error:
        print(error)


def download_all_bin(urls, filepathes, max_workers=5):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the local file.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    Args:
    =====
    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination file
    max_workers: int
        max number of working threads of CPUs within executing this method.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(download_bin, urls, filepathes), total=len(urls))
        )
        del results
        return


def csv_from_xls(xls_filepath, csv_filepath, sheet="Sheet1", enc="utf-8"):
    data_xls = pd.read_excel(xls_filepath, sheet, index_col=None)
    data_xls.to_csv(csv_filepath, encoding=enc)


def download_csv(url, filepath, enc="utf-8", dec="utf-8", logging=False):
    """
    Request a HTTP GET method to the given url (for REST API)
    and save its response as the csv file.

    Args:
    =====
    url: string
        valid url for REST API
    filepathe: string
        valid path to the destination file
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: True/False
        flag whether putting process log
    """
    try:
        if logging:
            print("HTTP GET", url)
        r = requests.get(url, stream=True)
        with open(filepath, 'w', encoding=enc) as f:
            f.write(r.content.decode(dec))
    except requests.exceptions.RequestException as error:
        print(error)


def download_all_csv(
        urls,
        filepathes,
        max_workers=10,
        enc="utf-8",
        dec="utf-8"):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the csv file.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    Args:
    =====
    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination file
    max_workers: int
        max number of working threads of CPUs within executing this method.
    enc: string
        encoding type for a content in a given url
    dec: string
        decoding type for a content in a downloaded file
            dec = 'utf-8' for general env
            dec = 'sjis'  for Excel on Win
            dec = 'cp932' for Excel with extended JP str on Win
    logging: True/False
    """
    func = functools.partial(download_csv, enc=enc, dec=dec)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(func, urls, filepathes), total=len(urls))
        )
        del results


def download_zip(url, filepath):
    try:
        r = requests.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except requests.exceptions.RequestException as error:
        print(error)
        return False


def download_all_zip(urls, filepathes, max_workers=5):
    """
    Request some HTTP GET methods to the given urls (for REST API)
    and save each response as the local file.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    Args:
    =====
    urls: list of strings
        valid urls for REST API
    filepathes: list of strings
        valid pathes to the destination files
    max_workers: int
        max number of working threads of CPUs within executing this method.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(download_zip, urls, filepathes), total=len(urls))
        )
        del results
        return


def extract_zip(filepath, target_dir):
    """
    Extract zip-file in the target directory.

    Args:
    =====
    filepath: string
        valid path to the target .zip file
    target_dir: path string
        valid dir path to the target directory where extracted files are saved
    """
    with zipfile.ZipFile(filepath) as f_zip:
        f_zip.extractall(target_dir)


def extract_all_zip(filepathes, target_dirs, max_workers=5):
    """
    Extract zip-file in the target directory.
    (!! This method uses multi threading when calling HTTP GET requests
    and downloading files in order to improve the processing speed.)

    Args:
    =====
    filepathes: list of strings
        valid pathes to the target .zip files
    target_dirs: list of path strings
        valid dir pathes to the target directories where extracted files are saved
    max_worker: int
        max number of working threads of CPUs within executing this method
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(executor.map(extract_zip, filepathes,
                              target_dirs), total=len(filepathes))
        )
        del results
        return

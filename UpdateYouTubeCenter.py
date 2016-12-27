"""
Updates the YouTubeCenter extension of Chrome.
"""
from __future__ import (division, absolute_import, print_function, unicode_literals)

import contextlib
import os
import urllib2
import urlparse
import webbrowser
import zipfile

URL = "https://github.com/YePpHa/YouTubeCenter/raw/master/dist/YouTubeCenter.crx"
DOWNLOAD_PATH = "E:\\tmp"
EXTRACT_PATH = "C:\\Users\\Daniel\\OneDrive\\AppData\\Chrome\\Extensions\\YouTubeCenter"
EXTENSION_URL = "chrome://extensions/?id=lpoacecbcfkbamdkgamplfgmmkdhhkbb"
CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"


def downloadFile(url, downloadDir):
    """
    Downloads the file specified in a URL and saves it inside the download directory. Filename is taken from the URL.
    Overwrites the file.
    Returns the full path to the downloaded file.
    :param url: The URL to load the file from.
    :type url: String
    :param downloadDir: The path of the download directory.
    :type downloadDir: String
    """
    path = urlparse.urlsplit(url)[2]
    fileName = os.path.join(downloadDir, os.path.basename(path))
    with contextlib.closing(urllib2.urlopen(url)) as socket, open(fileName, 'wb') as f:
        meta = socket.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        print("Downloading: {0}; Bytes: {1}".format(url, fileSize))

        fileSizeDL = 0
        blockSz = 8192  # should match the standard currBuffer size of most OS's
        while True:
            currBuffer = socket.read(blockSz)
            if not currBuffer:
                break

            fileSizeDL += len(currBuffer)
            f.write(currBuffer)
            status = "{0:16}".format(fileSizeDL)
            if fileSize:
                status += "   [{0:6.2f}%]".format(fileSizeDL * 100 / fileSize)
            status += os.linesep
            print(status, end="")
    return fileName


def unzipAll(sourceFilename, destDir):
    """
    Unzips the whole content of a zip-file to the destination directory.
    Overwrites files.
    :param sourceFilename: The path and file name of the zip file.
    :type sourceFilename: String
    :param destDir: The path to the destination directory.
    :type destDir: String
    """
    with zipfile.ZipFile(sourceFilename) as zf:
        zf.extractall(destDir)


unzipAll(downloadFile(URL, DOWNLOAD_PATH), EXTRACT_PATH)
print(webbrowser.get(CHROME_PATH + " %s").open_new_tab(EXTENSION_URL))

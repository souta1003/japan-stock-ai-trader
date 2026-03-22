import os
import certifi
import yfinance as yf
import pandas as pd
# import ssl
import requests

# SSL検証を無効化（開発環境のみ推奨）
# ssl._create_default_https_context = ssl._create_unverified_context

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def get_data(symbol="7203.T", period="6mo"):
    """
    株価データを取得する関数

    Parameters:
        symbol (str): 銘柄コード（例: 7203.T）
        period (str): 取得期間

    Returns:
        DataFrame: 株価データ（OHLCV）
    """

    try:
        df = yf.download(symbol, period=period, interval="1d", progress=False)
        if df.empty:
            print(f"Warning: No data for {symbol}")
            return pd.DataFrame()  # 空のDataFrameを返す
        return df

        # 欠損値を削除
        df.dropna(inplace=True)

        return df

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()  # エラー時は空のDataFrameを返す


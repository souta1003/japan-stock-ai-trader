import os
import certifi
import yfinance as yf
import pandas as pd
# import ssl
# import requests

# SSL検証を無効化
# ssl._create_default_https_context = ssl._create_unverified_context

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def get_market_trend():
    """
    地合い（市場全体のトレンド）を判定

    日経平均を使用
    """

    try:
        df = yf.download("^N225", period="3mo", interval="1d", progress=False)
        if df.empty or len(df) < 2:
            print("Warning: No data for ^N225")
            return "neutral"  # データがない場合は中立とする

    # トレンド判定ロジック（例: 最新価格 vs 過去平均）
        recent_avg = df["Close"].rolling(20).mean().iloc[-1]
        latest = df["Close"].iloc[-1]
        if latest > recent_avg * 1.02:
            return "bull"
        elif latest < recent_avg * 0.98:
            return "bear"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return "neutral"  # エラー時はデフォルト

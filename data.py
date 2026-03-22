import yfinance as yf

def get_data(symbol="7203.T", period="6mo"):
    """
    株価データを取得する関数

    Parameters:
        symbol (str): 銘柄コード（例: 7203.T）
        period (str): 取得期間

    Returns:
        DataFrame: 株価データ（OHLCV）
    """
    df = yf.download(symbol, period=period, interval="1d")

    # 欠損値を削除
    df.dropna(inplace=True)

    return df

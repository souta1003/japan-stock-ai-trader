import pandas as pd

def add_indicators(df):
    """
    テクニカル指標を追加
    """

    # 移動平均線
    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()

    # RSI計算
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # 出来高の移動平均
    df["vol_ma"] = df["Volume"].rolling(20).mean()

    return df


def add_ftd(df):
    """
    フォロースルーデー（簡易版）を検出

    条件：
    - 前日比+2%以上の上昇
    - 出来高が平均以上
    """

    df["ftd"] = 0

    for i in range(5, len(df)):
        prev_close = df.iloc[i-1]["Close"]
        curr_close = df.iloc[i]["Close"]

        change = (curr_close - prev_close) / prev_close

        volume = df.iloc[i]["Volume"]
        vol_ma = df.iloc[i]["Volume"]  # ※本来は移動平均にするのが望ましい

        if change > 0.02 and volume > vol_ma:
            df.at[df.index[i], "ftd"] = 1

    return df

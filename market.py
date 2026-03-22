import yfinance as yf

def get_market_trend():
    """
    地合い（市場全体のトレンド）を判定

    日経平均を使用
    """

    df = yf.download("^N225", period="3mo", interval="1d")

    # 25日移動平均
    df["ma25"] = df["Close"].rolling(25).mean()

    latest = df.iloc[-1]

    # 上昇トレンドか下降トレンドか
    if latest["Close"] > latest["ma25"]:
        return "bull"
    else:
        return "bear"

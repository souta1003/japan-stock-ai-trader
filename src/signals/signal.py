def calc_score_detail(row, weights):
    """
    各手法ごとのスコアを計算し、
    内訳（どの手法がどれだけ効いたか）も返す
    """

    detail = {}

    # トレンド判定
    if row["Close"] > row["ma20"] > row["ma50"]:
        detail["trend"] = weights["trend"]
    elif row["Close"] < row["ma20"] < row["ma50"]:
        detail["trend"] = -weights["trend"]
    else:
        detail["trend"] = 0

    # 出来高
    if row["Volume"] > row["vol_ma"] * 1.5:
        detail["volume"] = weights["volume"]
    else:
        detail["volume"] = 0

    # RSI
    if row["rsi"] < 30:
        detail["rsi"] = weights["rsi"]
    elif row["rsi"] > 70:
        detail["rsi"] = -weights["rsi"]
    else:
        detail["rsi"] = 0

    # FTD
    if row.get("ftd", 0) == 1:
        detail["ftd"] = weights["ftd"]
    else:
        detail["ftd"] = 0

    # 合計スコア
    score = sum(detail.values())

    return score, detail

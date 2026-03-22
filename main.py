import yaml

from data import get_data
from indicators import add_indicators, add_ftd
from signal import calc_score_detail
from backtest import backtest
from learn import update_weights
from notify import send_line
from market import get_market_trend
from screener import screen_symbols

# 対象銘柄（例）
symbols = ["7203.T", "6758.T", "9984.T"]

def main():
    # スクリーニング（有望銘柄抽出）
    targets = screen_symbols(symbols)

    # 地合い取得
    market = get_market_trend()

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    for sym in targets:
        df = get_data(sym)

        # 指標追加
        df = add_indicators(df)
        df = add_ftd(df)

        scores = []
        details = []

        # スコア計算
        for _, row in df.iterrows():
            score, detail = calc_score_detail(row, config["weights"])
            scores.append(score)
            details.append(detail)

        df["score"] = scores
        df["detail"] = details

        # 地合いフィルター（弱気なら取引しない）
        if config["market_filter"]["use"] and market == "bear":
            df["signal"] = 0
        else:
            df["signal"] = df["score"].apply(
                lambda x: 1 if x >= config["thresholds"]["buy"]
                else -1 if x <= config["thresholds"]["sell"]
                else 0
            )

        # バックテスト
        logs = backtest(df)

        # 学習（重み更新）
        update_weights(logs)

        # 最新シグナル
        latest = df.iloc[-1]

        if latest["signal"] == 1:
            send_line(f"{sym} 買いシグナル")
        elif latest["signal"] == -1:
            send_line(f"{sym} 売りシグナル")


if __name__ == "__main__":
    main()

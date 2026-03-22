import yaml

def update_weights(logs):
    """
    トレード結果を元に重みを調整

    利益が出た手法 → 強化
    損失になった手法 → 弱化
    """

    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    weights = config["weights"]

    for log in logs:
        profit = log["profit"]
        detail = log["detail"]

        for k, v in detail.items():
            if v == 0:
                continue

            # 勝ちトレード → 重み増加
            if profit > 0:
                weights[k] *= 1.02
            else:
                weights[k] *= 0.98

    config["weights"] = weights

    # ファイルに保存
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)

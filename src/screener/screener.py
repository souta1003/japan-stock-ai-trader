from src.data.data import get_data

def screen_symbols(symbols):
    """
    出来高急増銘柄を抽出

    Parameters:
        symbols (list): 銘柄リスト

    Returns:
        list: 条件を満たす銘柄
    """

    selected = []

    for sym in symbols:
        df = get_data(sym, period="1mo")

        if len(df) < 20:
            continue

        vol_ma = df["Volume"].rolling(20).mean().iloc[-1]
        latest_vol = df["Volume"].iloc[-1]

        # 出来高が1.5倍以上なら採用
        if latest_vol > vol_ma * 1.5:
            selected.append(sym)

    return selected

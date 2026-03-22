import pandas as pd

def backtest(df):
    """
    バックテストを実行し、取引ログを返す。
    df: DataFrame with columns including 'Close', 'signal', 'score', 'detail'
    Returns: list of dicts, each representing a trade log
    """
    logs = []
    position = 0  # 0: no position, 1: long, -1: short
    entry_price = 0
    entry_date = None
    
    for index, row in df.iterrows():
        signal = row['signal']
        price = row['Close']
        date = index
        
        if position == 0:
            # エントリー
            if signal == 1:  # 買いシグナル
                position = 1
                entry_price = price
                entry_date = date
            elif signal == -1:  # 売りシグナル
                position = -1
                entry_price = price
                entry_date = date
        elif position == 1:
            # ロングポジション中
            if signal == -1:  # 売りシグナルでクローズ
                profit = price - entry_price
                logs.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': entry_price,
                    'exit_price': price,
                    'profit': profit,
                    'position': 'long',
                    'score': row['score'],
                    'detail': row['detail']
                })
                position = 0
        elif position == -1:
            # ショートポジション中
            if signal == 1:  # 買いシグナルでクローズ
                profit = entry_price - price
                logs.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': entry_price,
                    'exit_price': price,
                    'profit': profit,
                    'position': 'short',
                    'score': row['score'],
                    'detail': row['detail']
                })
                position = 0
    
    # 最後のポジションがクローズされていない場合、強制クローズ（簡易版）
    if position != 0:
        profit = (price - entry_price) if position == 1 else (entry_price - price)
        logs.append({
            'entry_date': entry_date,
            'exit_date': date,
            'entry_price': entry_price,
            'exit_price': price,
            'profit': profit,
            'position': 'long' if position == 1 else 'short',
            'score': row['score'],
            'detail': row['detail']
        })
    
    return logs
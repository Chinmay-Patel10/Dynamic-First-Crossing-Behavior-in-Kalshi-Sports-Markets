# bias_summary.py — run on current 788
import pandas as pd
import ast
from pathlib import Path

summary = []
for f in Path("candles").glob("*.csv"):
    df = pd.read_csv(f)
    if df.empty: continue
    
    df['bid_close'] = df['yes_bid'].apply(
        lambda x: float(ast.literal_eval(x)['close']) if pd.notna(x) else float('nan')
    )
    
    min_price = df['bid_close'].min()
    cross_time = df[df['bid_close'] < 0.05].index.min()
    summary.append({
        'ticker': f.stem,
        'min_price': min_price,
        'cross_time': cross_time,
        'total_volume': df['volume'].sum()
    })

df_summary = pd.DataFrame(summary)
print("Bias Stats:")
print(df_summary['min_price'].describe())
print(f"Cross <5%: {len(df_summary[df_summary['cross_time'].notna()])}/{len(df_summary)}")
df_summary.to_csv("bias_summary_788.csv", index=False)
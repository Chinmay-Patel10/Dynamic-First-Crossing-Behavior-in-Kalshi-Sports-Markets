# monitor.py
import pandas as pd
import ast
from pathlib import Path
results = []

for f in Path("candles").glob("*.csv"):
    try:
        df = pd.read_csv(f)
        if df.empty: continue
        
        # Extract closes
        df['bid_close'] = df['yes_bid'].apply(
            lambda x: float(ast.literal_eval(x)['close']) if pd.notna(x) else float('nan')
        )
        
        hit_5pct = (df['bid_close'] < 0.05).any()
        results.append({
            'ticker': f.stem,
            'rows': len(df),
            'min_bid': df['bid_close'].min(),
            'hit_5pct': hit_5pct,
            'volume_sum': df['volume'].sum()
        })
    except:
        continue

summary = pd.DataFrame(results)
print(f"files: {summary['hit_5pct'].sum()} hit <5% ({100*summary['hit_5pct'].mean():.1f}%)")
print(summary[summary['hit_5pct']].head())
summary.to_csv("candle_summary.csv", index=False)
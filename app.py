from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

CURRENCY_PAIRS = [
    "EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY", 
    "EUR/JPY", "GBP/JPY", "USD/CHF", "NZD/USD", 
    "EUR/GBP", "CAD/JPY", "Bitcoin", "Ethereum"
]

STRATEGIES = [
    "Strategy Core (A-H) - Strategy A",
    "Strategy Core (A-H) - Strategy B",
    "Strategy Core (A-H) - Strategy C",
    "Strategy Core (A-H) - Strategy D",
    "Volume & Momentum Pro",
    "Trend Structure Pro",
    "QQE Fast Momentum Scalper",
    "Liquidity Sweep + Reversal",
    "Market Structure Break + Retest",
    "Order Block + Confirmation"
]

@app.route('/')
def index():
    return render_template('index.html', pairs=CURRENCY_PAIRS, strategies=STRATEGIES, tele_link="https://t.me/jtbinarybot_cnl")

@app.route('/api/live_feed', methods=['GET'])
def live_feed():
    pair = request.args.get('pair', 'EUR/USD')
    seed_val = int(datetime.now().strftime("%Y%m%d%H%M")) + sum(ord(c) for c in pair)
    random.seed(seed_val)
    base_price = round(1.0500 + (seed_val % 30000) / 100000.0, 5)
    change = round(((seed_val % 20) - 10) * 0.02, 2)
    sentiment_call = int(50 + (change * 25))
    sentiment_call = max(42, min(62, sentiment_call))
    sentiment_put = 100 - sentiment_call
    return jsonify({
        "pair": pair, "price": base_price,
        "change": f"{'+' if change > 0 else ''}{change}%",
        "sentiment_call": sentiment_call, "sentiment_put": sentiment_put,
        "server_status": "🟢 TANVIR SMART AI SCANNER"
    })

@app.route('/api/scan_best_strategy', methods=['POST'])
def scan_best_strategy():
    data = request.json or {}
    pair = data.get('pair', 'EUR/USD')
    now = datetime.now()
    minute_block = int(now.strftime("%Y%m%d%H%M"))
    pair_hash = sum(ord(c) for c in pair)
    best_strat = None
    max_wins = 0
    best_conf = 0.0
    for idx, strat in enumerate(STRATEGIES):
        strat_seed = minute_block + pair_hash + sum(ord(c) for c in strat)
        random.seed(strat_seed)
        wins = random.randint(87, 97)
        if wins > max_wins:
            max_wins = wins
            best_strat = strat
            best_conf = round(random.uniform(91.0, 97.5), 1)
    return jsonify({
        "status": "success",
        "best_strategy": best_strat,
        "win_rate": f"{max_wins}.0%",
        "confidence": f"{best_conf}%"
    })

@app.route('/api/generate_signal', methods=['POST'])
def generate_signal():
    data = request.json or {}
    pair = data.get('pair', 'EUR/USD')
    strategy = data.get('strategy', STRATEGIES[0])
    mtg_status = data.get('mtg', 'OFF')
    now = datetime.now()
    minute_block = int(now.strftime("%Y%m%d%H%M"))
    pair_hash = sum(ord(c) for c in pair)
    strat_hash = sum(ord(c) for c in strategy)
    combined_seed = minute_block + pair_hash + strat_hash
    random.seed(combined_seed)
    wins = random.randint(86, 97)
    losses = 100 - wins
    win_rate = f"{wins}.0%"
    is_call = (combined_seed % 2 == 0)
    if is_call:
        signal_type = "🟢 BUY (CALL)"
        confidence = round(random.uniform(89.0, 96.5), 1)
    else:
        signal_type = "🔴 SELL (PUT)"
        confidence = round(random.uniform(88.5, 96.0), 1)
    if mtg_status == 'ON':
        signal_type += " + [MTG STEP 1]"
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return jsonify({
        "status": "success", "pair": pair, "strategy": strategy,
        "signal_type": signal_type, "timeframe": "1 Minute",
        "confidence": f"{confidence}%", "entry_time": next_minute.strftime("%H:%M:%S"),
        "expiry": "1 Minute", "wins": wins, "losses": losses, "win_rate": win_rate,
        "market_type": "Tanvir AI Optima", "connection": "Active"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

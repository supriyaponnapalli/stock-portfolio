from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Dummy stock data (No real API needed)
stocks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    stock = {
        'symbol': data['symbol'].upper(),
        'quantity': int(data['quantity']),
        'buy_price': float(data['buy_price'])
    }
    stocks.append(stock)
    return jsonify({'status': 'success'})

@app.route('/get_portfolio')
def get_portfolio():
    portfolio = []
    total_invested = 0
    total_current = 0
    
    # Dummy current prices
    dummy_prices = {
        'AAPL': 225, 'GOOGL': 180, 'MSFT': 420, 
        'TSLA': 250, 'RELIANCE': 2800, 'HDFCBANK': 1650
    }
    
    for stock in stocks:
        current_price = dummy_prices.get(stock['symbol'], stock['buy_price'] * 1.1)
        invested = stock['quantity'] * stock['buy_price']
        current_value = stock['quantity'] * current_price
        profit = current_value - invested
        
        portfolio.append({
            'symbol': stock['symbol'],
            'quantity': stock['quantity'],
            'buy_price': stock['buy_price'],
            'current_price': round(current_price, 2),
            'invested': round(invested, 2),
            'current_value': round(current_value, 2),
            'profit': round(profit, 2),
            'profit_percent': round((profit / invested) * 100, 2) if invested > 0 else 0
        })
        
        total_invested += invested
        total_current += current_value
    
    return jsonify({
        'portfolio': portfolio,
        'total_invested': round(total_invested, 2),
        'total_current': round(total_current, 2),
        'total_profit': round(total_current - total_invested, 2)
    })

if __name__ == '__main__':
    print("Stock Portfolio Tracker running...")
    app.run(debug=True)
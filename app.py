from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import math

app = Flask(__name__)

def marketCountdown():
    now = datetime.now()
    marketOpen = now.replace(hour=9, minute=30, second=0, microsecond=0)
    marketClose = now.replace(hour=16, minute=0, second=0, microsecond=0)

    if now.weekday() < 5:
        if now < marketOpen:
            countdown = marketOpen - now
            status = "Market CLOSED - Opens in: "
        elif now >= marketOpen and now < marketClose:
            countdown = marketClose - now
            status = "Market OPEN - Closes in: "
        else:
            nextOpen = marketOpen + timedelta(days=1)
            while nextOpen.weekday() >= 5:
                nextOpen += timedelta(days=1)
            countdown = nextOpen - now
            status = "Market CLOSED - Opens in: "
    else:
        daysUntilMonday = (7 - now.weekday()) % 7
        if daysUntilMonday == 0:
            daysUntilMonday = 1
        nextOpen = marketOpen + timedelta(days=daysUntilMonday)
        countdown = nextOpen - now
        status = "Market CLOSED - Opens in: "
    return status + str(countdown).split('.')[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_market_status')
def get_market_status():
    status = marketCountdown()
    return jsonify({'status': status})

@app.route('/get_time')
def get_time():
    now = datetime.now()
    return jsonify({
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second
    })

if __name__ == '__main__':
    app.run(debug=True)
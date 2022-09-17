from flask import Flask
app = Flask(__name__)

import routes.TickerStream
import routes.CryptoCollapz
import routes.CalendarDays

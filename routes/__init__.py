from flask import Flask
app = Flask(__name__)

import routes.TickerStream

import routes.Rubiks
import routes.CryptoCollapz
import routes.CalendarDays
import routes.MagicCauldrons
import routes.TravellingSuisseRobot
import routes.QuordleKeyboard

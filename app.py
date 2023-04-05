from flask import Flask, request
from helpers.response_handlers import get_converted_time_http

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Hello, User! Go to <em>/convert-time</em> to get your time converted to a new time zone.'


@app.route('/convert-time')
def get_converted_time():
    args = request.args
    source_tz = args.get('source_timezone', 'Asia/Kolkata')
    time = args.get('time', '00:00')
    dest_tz = args.get('destination_timezone', 'UTC')
    return get_converted_time_http(time, source_tz, dest_tz)


app.run(port=5001)

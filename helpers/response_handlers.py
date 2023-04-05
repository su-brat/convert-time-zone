import requests
from constants import NUM_TIME_TO_WORD_ENDPOINT, TIMEZONE_CONVERTER_ENDPOINT
from helpers.time_handler import convert_to_12_hour_format


def form_request_body_from_args(time, source_tz, dest_tz):
    return {
        "fromTimeZone": source_tz,
        "dateTime": f"2021-03-14 {time}:00",
        "toTimeZone": dest_tz,
        "dstAmbiguity": ""
    }


def get_useful_params_form_response_body(json_body):
    required_body = json_body.get('conversionResult', {})
    return {
        "time": required_body.get('time'),
        "timeZone": required_body.get('timeZone')
    }


def get_converted_time_http(time, source_tz, dest_tz):
    request_body = form_request_body_from_args(
        time, source_tz, dest_tz)
    response = requests.post(TIMEZONE_CONVERTER_ENDPOINT,
                             json=request_body, timeout=10)
    if response.ok:
        response_body = response.json()
        cooked_response = get_useful_params_form_response_body(response_body)
        hour, minutes = map(int, cooked_response.get('time', ':').split(':'))
        hour = convert_to_12_hour_format(hour)
        augment_response = requests.get(NUM_TIME_TO_WORD_ENDPOINT, params={
            "h": hour,
            "m": minutes
        }, timeout=10)
        cooked_response['timeInWords'] = ''
        if augment_response.ok:
            cooked_response['timeInWords'] = augment_response.text
        return cooked_response, 200
    return 'Invalid input parameters', 400

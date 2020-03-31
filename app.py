import flask
from flask import request, jsonify
import requests
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

API_ENDPOINT = "https://api-crt.cert.havail.sabre.com/v1/offers/shop"

API_KEY = "T1RLAQKledIevdAVWMw9mzfq6pw5LDHyaRBzDFYeCW9e/FiWq+jriV3wAACwjT8vPq1ydjjF+7Zb0fhKi96s5gthT26me19/GXkihKbOa0NHEC5o6JRA1lbK2CLjPKDgZXk6cHr9bTfQ/Jf0lGsfC/cfjfA0GZGG+EaQlvttsR8boKwHdh1cfQXPZe9o+Oz4+tSf0gIeT/1M50U7cP3zAQPlqiNys+Kz8C2g5tYmOFRCivK0pgEPIe3fWr1llAvkfCVllH0NKOjCQo3p8g9BHdy3qL1+BA7GeCatHv0*"
hed = {'Authorization': 'Bearer ' + API_KEY, 'Content-Type': 'application/json'}
data = {
    "OTA_AirLowFareSearchRQ": {
        "OriginDestinationInformation": [
            {
                "DepartureDateTime": "2020-06-21T00:00:00",
                "DestinationLocation": {
                    "LocationCode": "SFO"
                },
                "OriginLocation": {
                    "LocationCode": "NYC"
                },
                "RPH": "0"
            },
            {
                "DepartureDateTime": "2020-06-22T00:00:00",
                "DestinationLocation": {
                    "LocationCode": "NYC"
                },
                "OriginLocation": {
                    "LocationCode": "SFO"
                },
                "RPH": "1"
            }
        ],
        "POS": {
            "Source": [
                {
                    "PseudoCityCode": "F9CE",
                    "RequestorID": {
                        "CompanyName": {
                            "Code": "TN"
                        },
                        "ID": "1",
                        "Type": "1"
                    }
                }
            ]
        },
        "TPA_Extensions": {
            "IntelliSellTransaction": {
                "RequestType": {
                    "Name": "200ITINS"
                }
            }
        },
        "TravelPreferences": {
            "TPA_Extensions": {
                "DataSources": {
                    "ATPCO": "Enable",
                    "LCC": "Disable",
                    "NDC": "Disable"
                },
                "NumTrips": {}
            }
        },
        "TravelerInfoSummary": {
            "AirTravelerAvail": [
                {
                    "PassengerTypeQuantity": [
                        {
                            "Code": "ADT",
                            "Quantity": 1
                        }
                    ]
                }
            ],
            "SeatsRequested": [
                1
            ]
        },
        "Version": "1"
    }
}


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/resources/bargainer/all', methods=['GET'])
def api_all():
    r = requests.post(url=API_ENDPOINT, json=data, headers=hed)
    # print(json.dumps(json.loads(r.content), indent=4, sort_keys=True))
    return json.dumps(json.loads(r.content), indent=4, sort_keys=True)


if __name__ == "__main__":
    app.run()

from flask import Flask
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

API_ENDPOINT = "https://api-crt.cert.havail.sabre.com/v1/offers/shop"

API_KEY = "T1RLAQKdwHQFmCgiuM/R7mCaG+6DXV9TYBBHHar0enUCDHVn6zBrxvn6AADAM7CWdWstzKO0VXPYRxhOAtGKWudnKSmGO0GwbWbc5wA/yg0lkHu6daO9cV6Af5Zhjk4jjH+7Som1Ycsukkr3gIF41qQEfnfE8eV+ee2O4KzXz1nvdOwZrcb6NXmWuH37f6c1G915GfVqVL1hj2ATIU4lXIi8QLkqkRO7nFcjZQbPFL2p0r7OitP+CsoQcqCJIHZC8sj350N8wmGxr60r0kX+epEWvJ97VkXVX+8Fu0n6FS9KbnRSN4/pmVJq9+2/"
hed = {'Authorization': 'Bearer ' + API_KEY}
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


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/v1/resources/bargainer/all', methods=['GET'])
def api_all():
    r = requests.post(url=API_ENDPOINT, json=data, headers=hed)
    return str(r.content)

if __name__ == '__main__':
    app.run()

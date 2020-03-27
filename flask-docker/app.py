from flask import Flask
from flask_restful import Resource, reqparse, Api
import requests

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

from base import Movies, db
db.init_app(app)
app.app_context().push()
db.create_all()

API_ENDPOINT = "https://api-crt.cert.havail.sabre.com/v1/offers/shop"
API_KEY = "T1RLAQKdwHQFmCgiuM/R7mCaG+6DXV9TYBBHHar0enUCDHVn6zBrxvn6AADAM7CWdWstzKO0VXPYRxhOAtGKWudnKSmGO0GwbWbc5wA/yg0lkHu6daO9cV6Af5Zhjk4jjH+7Som1Ycsukkr3gIF41qQEfnfE8eV+ee2O4KzXz1nvdOwZrcb6NXmWuH37f6c1G915GfVqVL1hj2ATIU4lXIi8QLkqkRO7nFcjZQbPFL2p0r7OitP+CsoQcqCJIHZC8sj350N8wmGxr60r0kX+epEWvJ97VkXVX+8Fu0n6FS9KbnRSN4/pmVJq9+2/"
hed = {'Authorization': 'Bearer ' + API_KEY}
data = {
    "OTA_AirLowFareSearchRQ": {
        "OriginDestinationInformation": [
            {
                "DepartureDateTime": "2020-06-21T00:00:00",
                "DestinationLocation": {
                    "LocationCode": "LAX"
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
                    "LocationCode": "LAX"
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

class Movies_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('director', type=str, required=False, help='Director of the movie')
    parser.add_argument('genre', type=str, required=False, help='Genre of the movie')
    parser.add_argument('collection', type=int, required=True, help='Gross collection of the movie')
    
    def get(self, movie):
        r = requests.post(url=API_ENDPOINT, json=data, headers=hed)
        return str(r.content)
        
    
    def post(self, movie):
        if Movies.find_by_title(movie):
            return {' Message': 'Movie with the  title {} already exists'.format(movie)}
        args = Movies_List.parser.parse_args()
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()
        
    def put(self, movie):
        args = Movies_List.parser.parse_args()
        item = Movies.find_by_title(movie)
        if item:
            item.collection = args['collection']
            item.save_to()
            return {'Movie': item.json()}
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()
            
    def delete(self, movie):
        item  = Movies.find_by_title(movie)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from records'.format(movie)}
        return {'Message': '{} is already not on the list'.format()}
    
class All_Movies(Resource):
    def get(self):
         r = requests.post(url=API_ENDPOINT, json=data, headers=hed)
        return str(r.content)
    
api.add_resource(All_Movies, '/')
api.add_resource(Movies_List, '/<string:movie>')

@app.route('/api/v1/resources/bargainer/all', methods=['GET'])
def api_all():
r = requests.post(url=API_ENDPOINT, json=data, headers=hed)
return str(r.content)

if __name__=='__main__':
    
app.run(debug=True)

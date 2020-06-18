import psycopg2
from flask import render_template
import json
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
import jwt
import datetime

t_host = "ec2-52-72-221-20.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "dcaj0g5nskdqq0"
t_user = "fjdftktouujcmb"
t_pw = "c9130e90451aca35b2dcbb6df700f6691a0256dc548e427c425c8feafc15518f"


class PostgressController:
    def get_airports(self, searchTerm: str):
        s = 'SELECT "AirportCode", "AirportName","City","Country" FROM "TravelDesk"."AirportDetails" WHERE LOWER("AirportCode") LIKE \'%' + searchTerm + '%\' OR LOWER("AirportName") LIKE \'%' + searchTerm + '%\' OR LOWER("City") LIKE \'%' + searchTerm + '%\' ORDER BY "AirportCode" ASC'
        try:
            db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
            db_cursor = db_conn.cursor()
            # Execute the SQL
            db_cursor.execute(s)
            # Retrieve records from Postgres into a Python List
            airportList = db_cursor.fetchall()
        except psycopg2.Error as e:
            # t_message = "Database error: " + e + "/n SQL: " + s
            return render_template("error.html", t_message=e)

            # Loop through the resulting list and print each user name, along with a line break:
        lstAirports = []
        for i in range(len(airportList)):
            lstAirports.append(
                formatDataKeyValuePair(airportList[i][0].strip(), airportList[i][1].strip(), airportList[i][2],
                                       airportList[i][3]))
        results = [obj.to_dict() for obj in lstAirports]
        jsdata = json.dumps(results)
        print(jsdata)
        db_cursor.close()
        db_conn.close()
        return jsdata

    def clientAuthentication(self, username: str, password: str):
        print(username)
        print(password)
        query = 'SELECT "Id", "ClientId", "ClientPassword" FROM "TravelDesk"."TravelDeskClients" WHERE "ClientId" = \'' + username + '\' AND "ClientPassword" = \''+ password + '\''
        #'SELECT "AirportCode", "AirportName","City","Country" FROM "TravelDesk"."AirportDetails" WHERE LOWER("AirportCode") LIKE \'%' + searchTerm + '%\' OR LOWER("AirportName") LIKE \'%' + searchTerm + '%\' OR LOWER("City") LIKE \'%' + searchTerm + '%\' ORDER BY "AirportCode" ASC'
        try:
            db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
            db_cursor = db_conn.cursor()
            db_cursor.execute(query)
            queryResponse = db_cursor.fetchone()
        except psycopg2.Error as e:
            return render_template("error.html", t_message=e)
        print(queryResponse)

        if queryResponse is None:
            return "0"
        else:
            try:
                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                    'iat': datetime.datetime.utcnow(),
                    'sub': username
                }
                return jwt.encode(
                    payload,
                    '0v&0&sBH*aUX@q&&',
                    algorithm='HS256'
                )
            except Exception as e:
                return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, '0v&0&sBH*aUX@q&&')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class formatDataKeyValuePair:
    AirportCode: str
    AirportName: str
    City: str
    Country: str

    def __init__(self, AirportCode: str, AirportName: str, City: str, Country: str) -> None:
        self.AirportCode = AirportCode
        self.AirportName = AirportName
        self.City = City
        self.Country = Country

    @staticmethod
    def from_dict(obj: Any) -> 'formatDataKeyValuePair':
        assert isinstance(obj, dict)
        AirportCode = obj.get("AirportCode")
        AirportName = obj.get("AirportName")
        City = obj.get("City")
        Country = obj.get("Country")
        return formatDataKeyValuePair(AirportCode, AirportName, City, Country)

    def to_dict(self) -> dict:
        result: dict = {}
        result["AirportCode"] = self.AirportCode
        result["AirportName"] = self.AirportName
        result["City"] = self.City
        result["Country"] = self.Country
        return result

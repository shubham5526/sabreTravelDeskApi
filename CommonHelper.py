import psycopg2
from flask import render_template
import json
from typing import Optional, Any, List, TypeVar, Type, cast, Callable

t_host = "ec2-34-225-82-212.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "d4d3v5kbvtoml5"
t_user = "ipywomgffvnkju"
t_pw = "b45f0c644d283cdcc737b6401b8d63a4bd6ebea93e9806db0c5e4c0fe26d1cf7"


class PostgressController:
    def get_airports(self, searchTerm: str):
        print(searchTerm)
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

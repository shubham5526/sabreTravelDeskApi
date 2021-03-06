# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


class HaltOnStatus:
    Code: Optional[str]

    def __init__(self, Code: Optional[str]) -> None:
        self.Code = Code

    @staticmethod
    def from_dict(obj: Any) -> 'HaltOnStatus':
        assert isinstance(obj, dict)
        Code = from_union([from_str, from_none], obj.get("Code"))
        return HaltOnStatus(Code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Code"] = from_union([from_str, from_none], self.Code)
        return result


class NLocation:
    LocationCode: Optional[str]

    def __init__(self, LocationCode: Optional[str]) -> None:
        self.LocationCode = LocationCode

    @staticmethod
    def from_dict(obj: Any) -> 'NLocation':
        assert isinstance(obj, dict)
        LocationCode = from_union([from_str, from_none], obj.get("LocationCode"))
        return NLocation(LocationCode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["LocationCode"] = from_union([from_str, from_none], self.LocationCode)
        return result


class MarketingAirline:
    Code: Optional[str]
    FlightNumber: Optional[str]

    def __init__(self, Code: Optional[str], FlightNumber: Optional[int]) -> None:
        self.Code = Code
        self.FlightNumber = FlightNumber

    @staticmethod
    def from_dict(obj: Any) -> 'MarketingAirline':
        assert isinstance(obj, dict)
        Code = from_union([from_str, from_none], obj.get("Code"))
        FlightNumber = from_union([from_none, lambda x: int(from_str(x))], obj.get("FlightNumber"))
        return MarketingAirline(Code, FlightNumber)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Code"] = from_union([from_str, from_none], self.Code)
        result["FlightNumber"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                             lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                            self.FlightNumber)
        return result


class FlightSegment:
    ArrivalDateTime: Optional[str]
    DepartureDateTime: Optional[str]
    FlightNumber: Optional[str]
    NumberInParty: Optional[str]
    ResBookDesigCode: Optional[str]
    Status: Optional[str]
    DestinationLocation: Optional[NLocation]
    MarketingAirline: Optional[MarketingAirline]
    OriginLocation: Optional[NLocation]
    InstantPurchase: Optional[bool]

    def __init__(self, ArrivalDateTime: Optional[datetime], DepartureDateTime: Optional[datetime],
                 FlightNumber: Optional[int], NumberInParty: Optional[int], ResBookDesigCode: Optional[str],
                 Status: Optional[str], DestinationLocation: Optional[NLocation],
                 MarketingAirline: Optional[MarketingAirline], OriginLocation: Optional[NLocation],
                 InstantPurchase: Optional[bool]) -> None:
        self.ArrivalDateTime = ArrivalDateTime
        self.DepartureDateTime = DepartureDateTime
        self.FlightNumber = FlightNumber
        self.NumberInParty = NumberInParty
        self.ResBookDesigCode = ResBookDesigCode
        self.Status = Status
        self.DestinationLocation = DestinationLocation
        self.MarketingAirline = MarketingAirline
        self.OriginLocation = OriginLocation
        self.InstantPurchase = InstantPurchase

    @staticmethod
    def from_dict(obj: Any) -> 'FlightSegment':
        assert isinstance(obj, dict)
        ArrivalDateTime = from_union([from_datetime, from_none], obj.get("ArrivalDateTime"))
        DepartureDateTime = from_union([from_datetime, from_none], obj.get("DepartureDateTime"))
        FlightNumber = from_union([from_none, lambda x: int(from_str(x))], obj.get("FlightNumber"))
        NumberInParty = from_union([from_none, lambda x: int(from_str(x))], obj.get("NumberInParty"))
        ResBookDesigCode = from_union([from_str, from_none], obj.get("ResBookDesigCode"))
        Status = from_union([from_str, from_none], obj.get("Status"))
        DestinationLocation = from_union([NLocation.from_dict, from_none], obj.get("DestinationLocation"))
        MarketingAirline = from_union([MarketingAirline.from_dict, from_none], obj.get("MarketingAirline"))
        OriginLocation = from_union([NLocation.from_dict, from_none], obj.get("OriginLocation"))
        InstantPurchase = from_union([from_bool, from_none], obj.get("InstantPurchase"))
        return FlightSegment(ArrivalDateTime, DepartureDateTime, FlightNumber, NumberInParty, ResBookDesigCode, Status,
                             DestinationLocation, MarketingAirline, OriginLocation, InstantPurchase)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ArrivalDateTime"] = from_union([lambda x: x.isoformat(), from_none], self.ArrivalDateTime)
        result["DepartureDateTime"] = from_union([lambda x: x.isoformat(), from_none], self.DepartureDateTime)
        result["FlightNumber"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                             lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                            self.FlightNumber)
        result["NumberInParty"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                              lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                             self.NumberInParty)
        result["ResBookDesigCode"] = from_union([from_str, from_none], self.ResBookDesigCode)
        result["Status"] = from_union([from_str, from_none], self.Status)
        result["DestinationLocation"] = from_union([lambda x: to_class(NLocation, x), from_none],
                                                   self.DestinationLocation)
        result["MarketingAirline"] = from_union([lambda x: to_class(MarketingAirline, x), from_none],
                                                self.MarketingAirline)
        result["OriginLocation"] = from_union([lambda x: to_class(NLocation, x), from_none], self.OriginLocation)
        result["InstantPurchase"] = from_union([from_bool, from_none], self.InstantPurchase)
        return result


class OriginDestinationInformation:
    FlightSegment: Optional[List[FlightSegment]]

    def __init__(self, FlightSegment: Optional[List[FlightSegment]]) -> None:
        self.FlightSegment = FlightSegment

    @staticmethod
    def from_dict(obj: Any) -> 'OriginDestinationInformation':
        assert isinstance(obj, dict)
        FlightSegment = from_union([lambda x: from_list(FlightSegment.from_dict, x), from_none],
                                   obj.get("FlightSegment"))
        return OriginDestinationInformation(FlightSegment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["FlightSegment"] = from_union([lambda x: from_list(lambda x: to_class(FlightSegment, x), x), from_none],
                                             self.FlightSegment)
        return result


class RetryRebook:
    Option: Optional[bool]

    def __init__(self, Option: Optional[bool]) -> None:
        self.Option = Option

    @staticmethod
    def from_dict(obj: Any) -> 'RetryRebook':
        assert isinstance(obj, dict)
        Option = from_union([from_bool, from_none], obj.get("Option"))
        return RetryRebook(Option)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Option"] = from_union([from_bool, from_none], self.Option)
        return result


class AirBook:
    RetryRebook: Optional[RetryRebook]
    HaltOnStatus: Optional[List[HaltOnStatus]]
    OriginDestinationInformation: OriginDestinationInformation

    def __init__(self, RetryRebook: Optional[RetryRebook], HaltOnStatus: Optional[List[HaltOnStatus]],
                 OriginDestinationInformation: Optional[OriginDestinationInformation]) -> None:
        self.RetryRebook = RetryRebook
        self.HaltOnStatus = HaltOnStatus
        self.OriginDestinationInformation = OriginDestinationInformation

    @staticmethod
    def from_dict(obj: Any) -> 'AirBook':
        assert isinstance(obj, dict)
        RetryRebook = from_union([RetryRebook.from_dict, from_none], obj.get("RetryRebook"))
        HaltOnStatus = from_union([lambda x: from_list(HaltOnStatus.from_dict, x), from_none], obj.get("HaltOnStatus"))
        OriginDestinationInformation = from_union([OriginDestinationInformation.from_dict, from_none],
                                                  obj.get("OriginDestinationInformation"))
        return AirBook(RetryRebook, HaltOnStatus, OriginDestinationInformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["RetryRebook"] = from_union([lambda x: to_class(RetryRebook, x), from_none], self.RetryRebook)
        result["HaltOnStatus"] = from_union([lambda x: from_list(lambda x: to_class(HaltOnStatus, x), x), from_none],
                                            self.HaltOnStatus)
        result["OriginDestinationInformation"] = from_union(
            [lambda x: to_class(OriginDestinationInformation, x), from_none], self.OriginDestinationInformation)
        return result


class Source:
    ReceivedFrom: Optional[str]

    def __init__(self, ReceivedFrom: Optional[str]) -> None:
        self.ReceivedFrom = ReceivedFrom

    @staticmethod
    def from_dict(obj: Any) -> 'Source':
        assert isinstance(obj, dict)
        ReceivedFrom = from_union([from_str, from_none], obj.get("ReceivedFrom"))
        return Source(ReceivedFrom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ReceivedFrom"] = from_union([from_str, from_none], self.ReceivedFrom)
        return result


class EmailEndTransaction:
    Ind: Optional[bool]

    def __init__(self, Ind: Optional[str]) -> None:
        self.Ind = Ind

    @staticmethod
    def from_dict(obj: Any) -> 'EmailEndTransaction':
        assert isinstance(obj, dict)
        Ind = from_union([from_bool, from_none], obj.get("Ind"))
        return EmailEndTransaction(Ind)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Ind"] = from_union([from_bool, from_none], self.get("Ind"))
        return result


class EndTransaction:
    Source: Optional[Source]
    Email: Optional[EmailEndTransaction]

    def __init__(self, Source: Optional[Source], Email: Optional[EmailEndTransaction]) -> None:
        self.Source = Source
        self.Email = Email

    @staticmethod
    def from_dict(obj: Any) -> 'EndTransaction':
        assert isinstance(obj, dict)
        Source = from_union([Source.from_dict, from_none], obj.get("Source"))
        Email = from_union([EmailEndTransaction.from_dict, from_none], obj.get("Email"))
        return EndTransaction(Source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Source"] = from_union([lambda x: to_class(Source, x), from_none], self.Source)
        result["Email"] = from_union([lambda x: to_class(EmailEndTransaction, x), from_none], self.Email)
        return result


class RedisplayReservation:
    waitInterval: Optional[int]

    def __init__(self, waitInterval: Optional[int]) -> None:
        self.waitInterval = waitInterval

    @staticmethod
    def from_dict(obj: Any) -> 'RedisplayReservation':
        assert isinstance(obj, dict)
        waitInterval = from_union([from_int, from_none], obj.get("waitInterval"))
        return RedisplayReservation(waitInterval)

    def to_dict(self) -> dict:
        result: dict = {}
        result["waitInterval"] = from_union([from_int, from_none], self.waitInterval)
        return result


class PostProcessing:
    EndTransaction: Optional[EndTransaction]
    RedisplayReservation: Optional[RedisplayReservation]

    def __init__(self, EndTransaction: Optional[EndTransaction],
                 RedisplayReservation: Optional[RedisplayReservation]) -> None:
        self.EndTransaction = EndTransaction
        self.RedisplayReservation = RedisplayReservation

    @staticmethod
    def from_dict(obj: Any) -> 'PostProcessing':
        assert isinstance(obj, dict)
        EndTransaction = from_union([EndTransaction.from_dict, from_none], obj.get("EndTransaction"))
        RedisplayReservation = from_union([RedisplayReservation.from_dict, from_none], obj.get("RedisplayReservation"))
        return PostProcessing(EndTransaction, RedisplayReservation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["EndTransaction"] = from_union([lambda x: to_class(EndTransaction, x), from_none], self.EndTransaction)
        result["RedisplayReservation"] = from_union([lambda x: to_class(RedisplayReservation, x), from_none],
                                                    self.RedisplayReservation)
        return result


class StateCountyProv:
    StateCode: Optional[str]

    def __init__(self, StateCode: Optional[str]) -> None:
        self.StateCode = StateCode

    @staticmethod
    def from_dict(obj: Any) -> 'StateCountyProv':
        assert isinstance(obj, dict)
        StateCode = from_union([from_str, from_none], obj.get("StateCode"))
        return StateCountyProv(StateCode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StateCode"] = from_union([from_str, from_none], self.StateCode)
        return result


class Address:
    AddressLine: Optional[str]
    CityName: Optional[str]
    CountryCode: Optional[str]
    PostalCode: Optional[int]
    StateCountyProv: Optional[StateCountyProv]
    StreetNmbr: Optional[str]

    def __init__(self, AddressLine: Optional[str], CityName: Optional[str], CountryCode: Optional[str],
                 PostalCode: Optional[int], StateCountyProv: Optional[StateCountyProv],
                 StreetNmbr: Optional[str]) -> None:
        self.AddressLine = AddressLine
        self.CityName = CityName
        self.CountryCode = CountryCode
        self.PostalCode = PostalCode
        self.StateCountyProv = StateCountyProv
        self.StreetNmbr = StreetNmbr

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        AddressLine = from_union([from_str, from_none], obj.get("AddressLine"))
        CityName = from_union([from_str, from_none], obj.get("CityName"))
        CountryCode = from_union([from_str, from_none], obj.get("CountryCode"))
        PostalCode = from_union([from_none, lambda x: int(from_str(x))], obj.get("PostalCode"))
        StateCountyProv = from_union([StateCountyProv.from_dict, from_none], obj.get("StateCountyProv"))
        StreetNmbr = from_union([from_str, from_none], obj.get("StreetNmbr"))
        return Address(AddressLine, CityName, CountryCode, PostalCode, StateCountyProv, StreetNmbr)

    def to_dict(self) -> dict:
        result: dict = {}
        result["AddressLine"] = from_union([from_str, from_none], self.AddressLine)
        result["CityName"] = from_union([from_str, from_none], self.CityName)
        result["CountryCode"] = from_union([from_str, from_none], self.CountryCode)
        result["PostalCode"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                           lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                          self.PostalCode)
        result["StateCountyProv"] = from_union([lambda x: to_class(StateCountyProv, x), from_none],
                                               self.StateCountyProv)
        result["StreetNmbr"] = from_union([from_str, from_none], self.StreetNmbr)
        return result


class Ticketing:
    TicketType: Optional[str]

    def __init__(self, TicketType: Optional[str]) -> None:
        self.TicketType = TicketType

    @staticmethod
    def from_dict(obj: Any) -> 'Ticketing':
        assert isinstance(obj, dict)
        TicketType = from_union([from_str, from_none], obj.get("TicketType"))
        return Ticketing(TicketType)

    def to_dict(self) -> dict:
        result: dict = {}
        result["TicketType"] = from_union([from_str, from_none], self.TicketType)
        return result


class AgencyInfo:
    Address: Optional[Address]
    Ticketing: Optional[Ticketing]

    def __init__(self, Address: Optional[Address], Ticketing: Optional[Ticketing]) -> None:
        self.Address = Address
        self.Ticketing = Ticketing

    @staticmethod
    def from_dict(obj: Any) -> 'AgencyInfo':
        assert isinstance(obj, dict)
        Address = from_union([Address.from_dict, from_none], obj.get("Address"))
        Ticketing = from_union([Ticketing.from_dict, from_none], obj.get("Ticketing"))
        return AgencyInfo(Address, Ticketing)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Address"] = from_union([lambda x: to_class(Address, x), from_none], self.Address)
        result["Ticketing"] = from_union([lambda x: to_class(Ticketing, x), from_none], self.Ticketing)
        return result


class ContactNumber:
    NameNumber: Optional[str]
    Phone: Optional[str]
    PhoneUseType: Optional[str]

    def __init__(self, NameNumber: Optional[str], Phone: Optional[str], PhoneUseType: Optional[str]) -> None:
        self.NameNumber = NameNumber
        self.Phone = Phone
        self.PhoneUseType = PhoneUseType

    @staticmethod
    def from_dict(obj: Any) -> 'ContactNumber':
        assert isinstance(obj, dict)
        NameNumber = from_union([from_str, from_none], obj.get("NameNumber"))
        Phone = from_union([from_str, from_none], obj.get("Phone"))
        PhoneUseType = from_union([from_str, from_none], obj.get("PhoneUseType"))
        return ContactNumber(NameNumber, Phone, PhoneUseType)

    def to_dict(self) -> dict:
        result: dict = {}
        result["NameNumber"] = from_union([from_str, from_none], self.NameNumber)
        result["Phone"] = from_union([from_str, from_none], self.Phone)
        result["PhoneUseType"] = from_union([from_str, from_none], self.PhoneUseType)
        return result


class ContactNumbers:
    ContactNumber: Optional[List[ContactNumber]]

    def __init__(self, ContactNumber: Optional[List[ContactNumber]]) -> None:
        self.ContactNumber = ContactNumber

    @staticmethod
    def from_dict(obj: Any) -> 'ContactNumbers':
        assert isinstance(obj, dict)
        ContactNumber = from_union([lambda x: from_list(ContactNumber.from_dict, x), from_none],
                                   obj.get("ContactNumber"))
        return ContactNumbers(ContactNumber)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ContactNumber"] = from_union([lambda x: from_list(lambda x: to_class(ContactNumber, x), x), from_none],
                                             self.ContactNumber)
        return result


class PersonName:
    NameNumber: Optional[str]
    PassengerType: Optional[str]
    GivenName: Optional[str]
    Surname: Optional[str]

    def __init__(self, NameNumber: Optional[str], PassengerType: Optional[str], GivenName: Optional[str],
                 Surname: Optional[str]) -> None:
        self.NameNumber = NameNumber
        self.PassengerType = PassengerType
        self.GivenName = GivenName
        self.Surname = Surname

    @staticmethod
    def from_dict(obj: Any) -> 'PersonName':
        assert isinstance(obj, dict)
        NameNumber = from_union([from_str, from_none], obj.get("NameNumber"))
        PassengerType = from_union([from_str, from_none], obj.get("PassengerType"))
        GivenName = from_union([from_str, from_none], obj.get("GivenName"))
        Surname = from_union([from_str, from_none], obj.get("Surname"))
        return PersonName(NameNumber, PassengerType, GivenName, Surname)

    def to_dict(self) -> dict:
        result: dict = {}
        result["NameNumber"] = from_union([from_str, from_none], self.NameNumber)
        result["PassengerType"] = from_union([from_str, from_none], self.PassengerType)
        result["GivenName"] = from_union([from_str, from_none], self.GivenName)
        result["Surname"] = from_union([from_str, from_none], self.Surname)
        return result


class Email:
    NameNumber: Optional[str]
    Address: Optional[str]

    def __init__(self, NameNumber: Optional[str], Address: Optional[str]) -> None:
        self.NameNumber = NameNumber
        self.Address = Address

    @staticmethod
    def from_dict(obj: Any) -> 'Email':
        assert isinstance(obj, dict)
        NameNumber = from_union([from_str, from_none], obj.get("NameNumber"))
        Address = from_union([from_str, from_none], obj.get("Address"))
        return Email(NameNumber, Address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["NameNumber"] = from_union([from_str, from_none], self.NameNumber)
        result["Address"] = from_union([from_str, from_none], self.Address)
        return result


class CustomerInfo:
    ContactNumbers: Optional[ContactNumbers]
    PersonName: Optional[List[PersonName]]
    Email: Optional[List[Email]]

    def __init__(self, ContactNumbers: Optional[ContactNumbers], PersonName: Optional[List[PersonName]],
                 Email: Optional[List[Email]]) -> None:
        self.ContactNumbers = ContactNumbers
        self.PersonName = PersonName
        self.Email = Email

    @staticmethod
    def from_dict(obj: Any) -> 'CustomerInfo':
        assert isinstance(obj, dict)
        ContactNumbers = from_union([ContactNumbers.from_dict, from_none], obj.get("ContactNumbers"))
        PersonName = from_union([lambda x: from_list(PersonName.from_dict, x), from_none], obj.get("PersonName"))
        Email = from_union([lambda x: from_list(Email.from_dict, x), from_none], obj.get("Email"))
        return CustomerInfo(ContactNumbers, PersonName, Email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ContactNumbers"] = from_union([lambda x: to_class(ContactNumbers, x), from_none], self.ContactNumbers)
        result["PersonName"] = from_union([lambda x: from_list(lambda x: to_class(PersonName, x), x), from_none],
                                          self.PersonName)
        result["Email"] = from_union([lambda x: from_list(lambda x: to_class(Email, x), x), from_none], self.Email)
        return result


class TravelItineraryAddInfo:
    AgencyInfo: Optional[AgencyInfo]
    CustomerInfo: Optional[CustomerInfo]

    def __init__(self, AgencyInfo: Optional[AgencyInfo], CustomerInfo: Optional[CustomerInfo]) -> None:
        self.AgencyInfo = AgencyInfo
        self.CustomerInfo = CustomerInfo

    @staticmethod
    def from_dict(obj: Any) -> 'TravelItineraryAddInfo':
        assert isinstance(obj, dict)
        AgencyInfo = from_union([AgencyInfo.from_dict, from_none], obj.get("AgencyInfo"))
        CustomerInfo = from_union([CustomerInfo.from_dict, from_none], obj.get("CustomerInfo"))
        return TravelItineraryAddInfo(AgencyInfo, CustomerInfo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["AgencyInfo"] = from_union([lambda x: to_class(AgencyInfo, x), from_none], self.AgencyInfo)
        result["CustomerInfo"] = from_union([lambda x: to_class(CustomerInfo, x), from_none], self.CustomerInfo)
        return result


class BookingInfo:
    BookingKey: Optional[str]
    RequestorID: Optional[str]

    def __init__(self, BookingKey: Optional[str], RequestorID: Optional[str]) -> None:
        self.BookingKey = BookingKey
        self.RequestorID = RequestorID

    @staticmethod
    def from_dict(obj: Any) -> 'BookingInfo':
        assert isinstance(obj, dict)
        BookingKey = obj.get("BookingKey")
        RequestorID = from_union([from_str, from_none], obj.get("RequestorID"))
        return BookingInfo(BookingKey, RequestorID)

    def to_dict(self) -> dict:
        result: dict = {}
        result["BookingKey"] = self.BookingKey
        result["RequestorID"] = from_union([from_str, from_none], self.RequestorID)
        return result


class FullCardHolderName:
    FirstName: Optional[str]
    LastName: Optional[str]

    def __init__(self, FirstName: Optional[str], LastName: Optional[str]) -> None:
        self.FirstName = FirstName
        self.LastName = LastName

    @staticmethod
    def from_dict(obj: Any) -> 'FullCardHolderName':
        assert isinstance(obj, dict)
        FirstName = from_union([from_str, from_none], obj.get("FirstName"))
        LastName = from_union([from_str, from_none], obj.get("LastName"))
        return FullCardHolderName(FirstName, LastName)

    def to_dict(self) -> dict:
        result: dict = {}
        result["FirstName"] = from_union([from_str, from_none], self.FirstName)
        result["LastName"] = from_union([from_str, from_none], self.LastName)
        return result


class PaymentCard:
    PaymentType: Optional[str]
    CardCode: Optional[str]
    CardNumber: Optional[str]
    ExpiryMonth: Optional[int]
    ExpiryYear: Optional[int]
    FullCardHolderName: Optional[FullCardHolderName]
    CSC: Optional[int]

    def __init__(self, PaymentType: Optional[str], CardCode: Optional[str], CardNumber: Optional[str],
                 ExpiryMonth: Optional[int], ExpiryYear: Optional[int],
                 FullCardHolderName: Optional[FullCardHolderName], CSC: Optional[int]) -> None:
        self.PaymentType = PaymentType
        self.CardCode = CardCode
        self.CardNumber = CardNumber
        self.ExpiryMonth = ExpiryMonth
        self.ExpiryYear = ExpiryYear
        self.FullCardHolderName = FullCardHolderName
        self.CSC = CSC

    @staticmethod
    def from_dict(obj: Any) -> 'PaymentCard':
        assert isinstance(obj, dict)
        PaymentType = from_union([from_str, from_none], obj.get("PaymentType"))
        CardCode = from_union([from_str, from_none], obj.get("CardCode"))
        CardNumber = from_union([from_str, from_none], obj.get("CardNumber"))
        ExpiryMonth = from_union([from_int, from_none], obj.get("ExpiryMonth"))
        ExpiryYear = from_union([from_none, lambda x: int(from_str(x))], obj.get("ExpiryYear"))
        FullCardHolderName = from_union([FullCardHolderName.from_dict, from_none], obj.get("FullCardHolderName"))
        CSC = from_union([from_none, lambda x: int(from_str(x))], obj.get("CSC"))
        return PaymentCard(PaymentType, CardCode, CardNumber, ExpiryMonth, ExpiryYear, FullCardHolderName, CSC)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PaymentType"] = from_union([from_str, from_none], self.PaymentType)
        result["CardCode"] = from_union([from_str, from_none], self.CardCode)
        result["CardNumber"] = from_union([from_str, from_none], self.CardNumber)
        result["ExpiryMonth"] = from_union([from_int, from_none], self.ExpiryMonth)
        result["ExpiryYear"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                           lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                          self.ExpiryYear)
        result["FullCardHolderName"] = from_union([lambda x: to_class(FullCardHolderName, x), from_none],
                                                  self.FullCardHolderName)
        result["CSC"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                    lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.CSC)
        return result


class FormOfPayment:
    PaymentCard: Optional[PaymentCard]

    def __init__(self, PaymentCard: Optional[PaymentCard]) -> None:
        self.PaymentCard = PaymentCard

    @staticmethod
    def from_dict(obj: Any) -> 'FormOfPayment':
        assert isinstance(obj, dict)
        PaymentCard = from_union([PaymentCard.from_dict, from_none], obj.get("PaymentCard"))
        return FormOfPayment(PaymentCard)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PaymentCard"] = from_union([lambda x: to_class(PaymentCard, x), from_none], self.PaymentCard)
        return result


class PaymentInformation:
    FormOfPayment: Optional[FormOfPayment]
    Type: Optional[str]

    def __init__(self, FormOfPayment: Optional[FormOfPayment], Type: Optional[str]) -> None:
        self.FormOfPayment = FormOfPayment
        self.Type = Type

    @staticmethod
    def from_dict(obj: Any) -> 'PaymentInformation':
        assert isinstance(obj, dict)
        FormOfPayment = from_union([FormOfPayment.from_dict, from_none], obj.get("FormOfPayment"))
        Type = from_union([from_str, from_none], obj.get("Type"))
        return PaymentInformation(FormOfPayment, Type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["FormOfPayment"] = from_union([lambda x: to_class(FormOfPayment, x), from_none], self.FormOfPayment)
        result["Type"] = from_union([from_str, from_none], self.Type)
        return result


class Contact:
    Phone: Optional[str]

    def __init__(self, Phone: Optional[str]) -> None:
        self.Phone = Phone

    @staticmethod
    def from_dict(obj: Any) -> 'Contact':
        assert isinstance(obj, dict)
        Phone = from_union([from_str, from_none], obj.get("Phone"))
        return Contact(Phone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Phone"] = from_union([from_str, from_none], self.Phone)
        return result


class Guest:
    Contact: Optional[Contact]
    FirstName: Optional[str]
    LastName: Optional[str]
    Index: Optional[int]
    LeadGuest: Optional[bool]
    Type: Optional[int]
    Email: Optional[str]

    def __init__(self, Contact: Optional[Contact], FirstName: Optional[str], LastName: Optional[str],
                 Index: Optional[int], LeadGuest: Optional[bool], Type: Optional[int], Email: Optional[str]) -> None:
        self.Contact = Contact
        self.FirstName = FirstName
        self.LastName = LastName
        self.Index = Index
        self.LeadGuest = LeadGuest
        self.Type = Type
        self.Email = Email

    @staticmethod
    def from_dict(obj: Any) -> 'Guest':
        assert isinstance(obj, dict)
        Contact = from_union([Contact.from_dict, from_none], obj.get("Contact"))
        FirstName = from_union([from_str, from_none], obj.get("FirstName"))
        LastName = from_union([from_str, from_none], obj.get("LastName"))
        Index = from_union([from_int, from_none], obj.get("Index"))
        LeadGuest = from_union([from_bool, from_none], obj.get("LeadGuest"))
        Type = from_union([from_int, from_none], obj.get("Type"))
        Email = from_union([from_str, from_none], obj.get("Email"))
        return Guest(Contact, FirstName, LastName, Index, LeadGuest, Type, Email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Contact"] = from_union([lambda x: to_class(Contact, x), from_none], self.Contact)
        result["FirstName"] = from_union([from_str, from_none], self.FirstName)
        result["LastName"] = from_union([from_str, from_none], self.LastName)
        result["Index"] = from_union([from_int, from_none], self.Index)
        result["LeadGuest"] = from_union([from_bool, from_none], self.LeadGuest)
        result["Type"] = from_union([from_int, from_none], self.Type)
        result["Email"] = from_union([from_str, from_none], self.Email)
        return result


class Guests:
    Guest: Optional[List[Guest]]

    def __init__(self, Guest: Optional[List[Guest]]) -> None:
        self.Guest = Guest

    @staticmethod
    def from_dict(obj: Any) -> 'Guests':
        assert isinstance(obj, dict)
        Guest = from_union([lambda x: from_list(Guest.from_dict, x), from_none], obj.get("Guest"))
        return Guests(Guest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Guest"] = from_union([lambda x: from_list(lambda x: to_class(Guest, x), x), from_none], self.Guest)
        return result


class Room:
    Guests: Optional[Guests]
    RoomIndex: Optional[int]

    def __init__(self, Guests: Optional[Guests], RoomIndex: Optional[int]) -> None:
        self.Guests = Guests
        self.RoomIndex = RoomIndex

    @staticmethod
    def from_dict(obj: Any) -> 'Room':
        assert isinstance(obj, dict)
        Guests = from_union([Guests.from_dict, from_none], obj.get("Guests"))
        RoomIndex = from_union([from_int, from_none], obj.get("RoomIndex"))
        return Room(Guests, RoomIndex)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Guests"] = from_union([lambda x: to_class(Guests, x), from_none], self.Guests)
        result["RoomIndex"] = from_union([from_int, from_none], self.RoomIndex)
        return result


class Rooms:
    Room: Optional[List[Room]]

    def __init__(self, Room: Optional[List[Room]]) -> None:
        self.Room = Room

    @staticmethod
    def from_dict(obj: Any) -> 'Rooms':
        assert isinstance(obj, dict)
        Room = from_union([lambda x: from_list(Room.from_dict, x), from_none], obj.get("Room"))
        return Rooms(Room)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Room"] = from_union([lambda x: from_list(lambda x: to_class(Room, x), x), from_none], self.Room)
        return result


class HotelBook:
    BookingInfo: Optional[BookingInfo]
    Rooms: Optional[Rooms]
    PaymentInformation: Optional[PaymentInformation]

    def __init__(self, BookingInfo: Optional[BookingInfo], Rooms: Optional[Rooms],
                 PaymentInformation: Optional[PaymentInformation]) -> None:
        self.BookingInfo = BookingInfo
        self.Rooms = Rooms
        self.PaymentInformation = PaymentInformation

    @staticmethod
    def from_dict(obj: Any) -> 'HotelBook':
        assert isinstance(obj, dict)
        BookingInfo = from_union([BookingInfo.from_dict, from_none], obj.get("BookingInfo"))
        Rooms = from_union([Rooms.from_dict, from_none], obj.get("Rooms"))
        PaymentInformation = from_union([PaymentInformation.from_dict, from_none], obj.get("PaymentInformation"))
        return HotelBook(BookingInfo, Rooms, PaymentInformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["BookingInfo"] = from_union([lambda x: to_class(BookingInfo, x), from_none], self.BookingInfo)
        result["Rooms"] = from_union([lambda x: to_class(Rooms, x), from_none], self.Rooms)
        result["PaymentInformation"] = from_union([lambda x: to_class(PaymentInformation, x), from_none],
                                                  self.PaymentInformation)
        return result


class CreatePassengerNameRecordRQ:
    version: Optional[str]
    targetCity: Optional[str]
    haltOnAirPriceError: Optional[bool]
    TravelItineraryAddInfo: Optional[TravelItineraryAddInfo]
    AirBook: Optional[AirBook]
    PostProcessing: Optional[PostProcessing]
    HotelBook: Optional[HotelBook]

    def __init__(self, version: Optional[str], targetCity: Optional[str], haltOnAirPriceError: Optional[bool],
                 TravelItineraryAddInfo: Optional[TravelItineraryAddInfo], AirBook: Optional[AirBook],
                 PostProcessing: Optional[PostProcessing], HotelBook: Optional[HotelBook]) -> None:
        self.version = version
        self.targetCity = targetCity
        self.haltOnAirPriceError = haltOnAirPriceError
        self.TravelItineraryAddInfo = TravelItineraryAddInfo
        self.AirBook = AirBook
        self.PostProcessing = PostProcessing
        self.HotelBook = HotelBook

    @staticmethod
    def from_dict(obj: Any) -> 'CreatePassengerNameRecordRQ':
        assert isinstance(obj, dict)
        version = from_union([from_str, from_none], obj.get("version"))
        targetCity = from_union([from_str, from_none], obj.get("targetCity"))
        haltOnAirPriceError = from_union([from_bool, from_none], obj.get("haltOnAirPriceError"))
        TravelItineraryAddInfo = from_union([TravelItineraryAddInfo.from_dict, from_none],
                                            obj.get("TravelItineraryAddInfo"))
        AirBook = from_union([AirBook.from_dict, from_none], obj.get("AirBook"))
        #HotelBook = from_union([HotelBook.from_dict, from_none], obj.get("HotelBook"))
        PostProcessing = from_union([PostProcessing.from_dict, from_none], obj.get("PostProcessing"))
        return CreatePassengerNameRecordRQ(version, targetCity, haltOnAirPriceError, TravelItineraryAddInfo, AirBook,
                                           PostProcessing, HotelBook)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = from_union([from_str, from_none], self.version)
        result["targetCity"] = from_union([from_str, from_none], self.targetCity)
        result["haltOnAirPriceError"] = from_union([from_bool, from_none], self.haltOnAirPriceError)
        result["TravelItineraryAddInfo"] = from_union([lambda x: to_class(TravelItineraryAddInfo, x), from_none],
                                                      self.TravelItineraryAddInfo)
        result["AirBook"] = from_union([lambda x: to_class(AirBook, x), from_none], self.AirBook)
        result["PostProcessing"] = from_union([lambda x: to_class(PostProcessing, x), from_none], self.PostProcessing)
        #result["HotelBook"] = from_union([lambda x: to_class(HotelBook, x), from_none], self.HotelBook)
        return result


class Welcome:
    CreatePassengerNameRecordRQ: Optional[CreatePassengerNameRecordRQ]

    def __init__(self, CreatePassengerNameRecordRQ: Optional[CreatePassengerNameRecordRQ]) -> None:
        self.CreatePassengerNameRecordRQ = CreatePassengerNameRecordRQ

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        CreatePassengerNameRecordRQ = from_union([CreatePassengerNameRecordRQ.from_dict, from_none],
                                                 obj.get("CreatePassengerNameRecordRQ"))
        return Welcome(CreatePassengerNameRecordRQ)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CreatePassengerNameRecordRQ"] = from_union(
            [lambda x: to_class(CreatePassengerNameRecordRQ, x), from_none], self.CreatePassengerNameRecordRQ)
        return result


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)


def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)

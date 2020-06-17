import flask
from flask import request, jsonify
import requests
import json
import time
from typing import Any, Optional, List, Union, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime, timedelta
import dateutil.parser
import base64

import CreatePNRModel as CreatePNRModel
import HotelRateModel as HotelRateModel
import HotelPriceCheckModel as HotelPriceCheckModel
import CommonHelper as CommonHelper

app = flask.Flask(__name__)
app.config["DEBUG"] = True

PCC_Code = 'C3RK'

Authenticate_Endpoint = "https://api-crt.cert.havail.sabre.com/v2/auth/token"
BFM_Endpoint = "https://api-crt.cert.havail.sabre.com/v1/offers/shop"
PNR_Endpoint = "https://api-crt.cert.havail.sabre.com/v2.3.0/passenger/records?mode=create"
HotelRateInfo_Endpoint = "https://api-crt.cert.havail.sabre.com/v3.0.0/get/hotelrateinfo"
HotelPriceCheck_Endpoint = "https://api-crt.cert.havail.sabre.com/v2.1.0/hotel/pricecheck"
HotelAvailability_Endpoint = "https://api-crt.cert.havail.sabre.com/v3.0.0/get/hotelavail"
HotelDetail_Endpoint = "https://api-crt.cert.havail.sabre.com/v2.0.0/get/hoteldetails"

API_KEY = ''
AuthorizationHeader = {}

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


class BaggageAllowanceDesc:
    id: int
    pieceCount: int

    def __init__(self, id: int, pieceCount: int) -> None:
        self.id = id
        self.pieceCount = pieceCount

    @staticmethod
    def from_dict(obj: Any) -> 'BaggageAllowanceDesc':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        pieceCount = from_int(obj.get("pieceCount"))
        return BaggageAllowanceDesc(id, pieceCount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["pieceCount"] = from_int(self.pieceCount)
        return result


# class Direction(Enum):
#    WH = "WH"


# class Directionality(Enum):
#    FROM = "FROM"


# class FareCurrency(Enum):
#    USD = "USD"


class PassengerType(Enum):
    ADT = "ADT"


# class FareType(Enum):
#    END = "END"
#    EOU = "EOU"
#    SIP = "SIP"


# class GoverningCarrier(Enum):
#    AA = "AA"
#    AS = "AS"
#    B6 = "B6"
#    DL = "DL"
#    UA = "UA"


class PurpleSegment:
    stopover: Optional[bool]

    def __init__(self, stopover: Optional[bool]) -> None:
        self.stopover = stopover

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleSegment':
        # assert isinstance(obj, dict)
        stopover = from_union([from_bool, from_none], obj.get("stopover"))
        return PurpleSegment(stopover)

    def to_dict(self) -> dict:
        result: dict = {}
        result["stopover"] = from_union([from_bool, from_none], self.stopover)
        return result


class FareComponentDescSegment:
    segment: PurpleSegment

    def __init__(self, segment: PurpleSegment) -> None:
        self.segment = segment

    @staticmethod
    def from_dict(obj: Any) -> 'FareComponentDescSegment':
        assert isinstance(obj, dict)
        segment = PurpleSegment.from_dict(obj.get("segment"))
        return FareComponentDescSegment(segment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["segment"] = to_class(PurpleSegment, self.segment)
        return result


class VendorCode(Enum):
    ATP = "ATP"


class FareComponentDesc:
    applicablePricingCategories: str
    direction: str
    directionality: str
    fareAmount: int
    fareBasisCode: str
    fareCurrency: str
    farePassengerType: PassengerType
    fareRule: str
    fareTariff: int
    fareType: str
    fareTypeBitmap: str
    governingCarrier: str
    id: int
    notValidAfter: datetime
    oneWayFare: bool
    publishedFareAmount: int
    segments: List[FareComponentDescSegment]
    vendorCode: VendorCode
    notValidBefore: Optional[datetime]

    def __init__(self, applicablePricingCategories: str, direction: str, directionality: str,
                 fareAmount: int, fareBasisCode: str, fareCurrency: str, farePassengerType: PassengerType,
                 fareRule: str, fareTariff: int, fareType: str, fareTypeBitmap: str,
                 governingCarrier: str, id: int, notValidAfter: datetime, oneWayFare: bool,
                 publishedFareAmount: int, segments: List[FareComponentDescSegment], vendorCode: VendorCode,
                 notValidBefore: Optional[datetime]) -> None:
        self.applicablePricingCategories = applicablePricingCategories
        self.direction = direction
        self.directionality = directionality
        self.fareAmount = fareAmount
        self.fareBasisCode = fareBasisCode
        self.fareCurrency = fareCurrency
        self.farePassengerType = farePassengerType
        self.fareRule = fareRule
        self.fareTariff = fareTariff
        self.fareType = fareType
        self.fareTypeBitmap = fareTypeBitmap
        self.governingCarrier = governingCarrier
        self.id = id
        self.notValidAfter = notValidAfter
        self.oneWayFare = oneWayFare
        self.publishedFareAmount = publishedFareAmount
        self.segments = segments
        self.vendorCode = vendorCode
        self.notValidBefore = notValidBefore

    @staticmethod
    def from_dict(obj: Any) -> 'FareComponentDesc':
        assert isinstance(obj, dict)
        applicablePricingCategories = from_str(obj.get("applicablePricingCategories"))
        direction = obj.get("direction")
        directionality = obj.get("directionality")
        fareAmount = obj.get("fareAmount")
        fareBasisCode = from_str(obj.get("fareBasisCode"))
        fareCurrency = (obj.get("fareCurrency"))
        farePassengerType = PassengerType(obj.get("farePassengerType"))
        fareRule = from_str(obj.get("fareRule"))
        fareTariff = int(from_str(obj.get("fareTariff")))
        fareType = obj.get("fareType")
        fareTypeBitmap = from_str(obj.get("fareTypeBitmap"))
        governingCarrier = obj.get("governingCarrier")
        id = from_int(obj.get("id"))
        notValidAfter = obj.get("notValidAfter")
        oneWayFare = obj.get("oneWayFare")
        publishedFareAmount = obj.get("publishedFareAmount")
        segments = obj.get("segments")
        vendorCode = VendorCode(obj.get("vendorCode"))
        notValidBefore = obj.get("notValidBefore")
        return FareComponentDesc(applicablePricingCategories, direction, directionality, fareAmount, fareBasisCode,
                                 fareCurrency, farePassengerType, fareRule, fareTariff, fareType, fareTypeBitmap,
                                 governingCarrier, id, notValidAfter, oneWayFare, publishedFareAmount, segments,
                                 vendorCode, notValidBefore)

    def to_dict(self) -> dict:
        result: dict = {}
        result["applicablePricingCategories"] = from_str(self.applicablePricingCategories)
        result["direction"] = self.direction
        result["directionality"] = self.directionality
        result["fareAmount"] = self.fareAmount
        result["fareBasisCode"] = from_str(self.fareBasisCode)
        result["fareCurrency"] = self.fareCurrency
        result["farePassengerType"] = to_enum(PassengerType, self.farePassengerType)
        result["fareRule"] = from_str(self.fareRule)
        result["fareTariff"] = from_str(str(self.fareTariff))
        result["fareType"] = self.fareType
        result["fareTypeBitmap"] = from_str(self.fareTypeBitmap)
        result["governingCarrier"] = self.governingCarrier
        result["id"] = from_int(self.id)
        result["notValidAfter"] = self.notValidAfter
        result["oneWayFare"] = self.oneWayFare
        result["publishedFareAmount"] = self.publishedFareAmount
        result["segments"] = self.segments
        result["vendorCode"] = to_enum(VendorCode, self.vendorCode)
        result["notValidBefore"] = self.notValidBefore
        return result


# class Station(Enum):
#   DTW = "DTW"
#  EWR = "EWR"
# JFK = "JFK"
# PHX = "PHX"
# SFO = "SFO"
# LGA = "LGA"


class LegDescription:
    arrivalLocation: str
    departureDate: datetime
    departureLocation: str

    def __init__(self, arrivalLocation: str, departureDate: datetime, departureLocation: str) -> None:
        self.arrivalLocation = arrivalLocation
        self.departureDate = departureDate
        self.departureLocation = departureLocation

    @staticmethod
    def from_dict(obj: Any) -> 'LegDescription':
        assert isinstance(obj, dict)
        arrivalLocation = obj.get("arrivalLocation")
        departureDate = obj.get("departureDate")
        departureLocation = obj.get("departureLocation")
        return LegDescription(arrivalLocation, departureDate, departureLocation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["arrivalLocation"] = self.arrivalLocation
        result["departureDate"] = self.departureDate
        result["departureLocation"] = self.departureLocation
        return result


class GroupDescription:
    legDescriptions: List[LegDescription]

    def __init__(self, legDescriptions: List[LegDescription]) -> None:
        self.legDescriptions = legDescriptions

    @staticmethod
    def from_dict(obj: Any) -> 'GroupDescription':
        assert isinstance(obj, dict)
        legDescriptions = from_list(LegDescription.from_dict, obj.get("legDescriptions"))
        return GroupDescription(legDescriptions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["legDescriptions"] = from_list(lambda x: to_class(LegDescription, x), self.legDescriptions)
        return result


class DiversitySwapper:
    weighedPrice: float

    def __init__(self, weighedPrice: float) -> None:
        self.weighedPrice = weighedPrice

    @staticmethod
    def from_dict(obj: Any) -> 'DiversitySwapper':
        assert isinstance(obj, dict)
        weighedPrice = from_float(obj.get("weighedPrice"))
        return DiversitySwapper(weighedPrice)

    def to_dict(self) -> dict:
        result: dict = {}
        result["weighedPrice"] = to_float(self.weighedPrice)
        return result


class Schedule:
    ref: int

    def __init__(self, ref: int) -> None:
        self.ref = ref

    @staticmethod
    def from_dict(obj: Any) -> 'Schedule':
        assert isinstance(obj, dict)
        ref = from_int(obj.get("ref"))
        return Schedule(ref)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ref"] = from_int(self.ref)
        return result


# class GoverningCarriers(Enum):
#    AA_AA = "AA AA"
#    AS_AS = "AS AS"
#    B6_B6 = "B6 B6"
#    DL_AS = "DL AS"
#    DL_DL = "DL DL"
#    UA_UA = "UA UA"


# class TerminalEnum(Enum):
#    A = "A"
#    B = "B"
#    C = "C"
#    EM = "EM"


class BaggageInformationSegment:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'BaggageInformationSegment':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        return BaggageInformationSegment(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        return result


class BaggageInformation:
    airlineCode: str
    allowance: Schedule
    provisionType: str
    segments: List[BaggageInformationSegment]

    def __init__(self, airlineCode: str, allowance: Schedule, provisionType: str,
                 segments: List[BaggageInformationSegment]) -> None:
        self.airlineCode = airlineCode
        self.allowance = allowance
        self.provisionType = provisionType
        self.segments = segments

    @staticmethod
    def from_dict(obj: Any) -> 'BaggageInformation':
        assert isinstance(obj, dict)
        airlineCode = obj.get("airlineCode")
        allowance = Schedule.from_dict(obj.get("allowance"))
        provisionType = obj.get("provisionType")
        segments = from_list(BaggageInformationSegment.from_dict, obj.get("segments"))
        return BaggageInformation(airlineCode, allowance, provisionType, segments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["airlineCode"] = self.airlineCode
        result["allowance"] = to_class(Schedule, self.allowance)
        result["provisionType"] = self.provisionType
        result["segments"] = from_list(lambda x: to_class(BaggageInformationSegment, x), self.segments)
        return result


class CurrencyConversion:
    exchangeRateUsed: int
    currencyConversion_from: str
    to: str

    def __init__(self, exchangeRateUsed: int, currencyConversion_from: str, to: str) -> None:
        self.exchangeRateUsed = exchangeRateUsed
        self.currencyConversion_from = currencyConversion_from
        self.to = to

    @staticmethod
    def from_dict(obj: Any) -> 'CurrencyConversion':
        assert isinstance(obj, dict)
        exchangeRateUsed = obj.get("exchangeRateUsed")
        currencyConversion_from = (obj.get("from"))
        to = (obj.get("to"))
        return CurrencyConversion(exchangeRateUsed, currencyConversion_from, to)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchangeRateUsed"] = self.exchangeRateUsed
        result["from"] = self.currencyConversion_from
        result["to"] = self.to
        return result


class DotRating(Enum):
    B = "B"
    K = "K"
    L = "L"
    N = "N"
    Q = "Q"
    R = "R"
    U = "U"
    X = "X"


# class CabinCode(Enum):
#    Y = "Y"


# class MealCode(Enum):
#    F = "F"
#    G = "G"
#    S = "S"


class FluffySegment:
    availabilityBreak: Optional[bool]
    bookingCode: DotRating
    cabinCode: str
    mealCode: Optional[str]
    seatsAvailable: int

    def __init__(self, availabilityBreak: Optional[bool], bookingCode: DotRating, cabinCode: str,
                 mealCode: Optional[str], seatsAvailable: int) -> None:
        self.availabilityBreak = availabilityBreak
        self.bookingCode = bookingCode
        self.cabinCode = cabinCode
        self.mealCode = mealCode
        self.seatsAvailable = seatsAvailable

    @staticmethod
    def from_dict(obj: Any) -> 'FluffySegment':
        assert isinstance(obj, dict)
        availabilityBreak = from_union([from_bool, from_none], obj.get("availabilityBreak"))
        bookingCode = obj.get("bookingCode")
        cabinCode = (obj.get("cabinCode"))
        mealCode = obj.get("mealCode")
        seatsAvailable = from_int(obj.get("seatsAvailable"))
        return FluffySegment(availabilityBreak, bookingCode, cabinCode, mealCode, seatsAvailable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["availabilityBreak"] = from_union([from_bool, from_none], self.availabilityBreak)
        result["bookingCode"] = self.bookingCode
        result["cabinCode"] = self.cabinCode
        result["mealCode"] = self.mealCode
        result["seatsAvailable"] = from_int(self.seatsAvailable)
        return result


class FareComponentSegment:
    segment: FluffySegment

    def __init__(self, segment: FluffySegment) -> None:
        self.segment = segment

    @staticmethod
    def from_dict(obj: Any) -> 'FareComponentSegment':
        assert isinstance(obj, dict)
        # segment = FluffySegment.from_dict(obj.get("segment"))
        segment = obj.get("segment")
        return FareComponentSegment(segment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["segment"] = self.segment
        return result


class FareComponent:
    ref: int
    segments: List[FareComponentSegment]

    def __init__(self, ref: int, segments: List[FareComponentSegment]) -> None:
        self.ref = ref
        self.segments = segments

    @staticmethod
    def from_dict(obj: Any) -> 'FareComponent':
        assert isinstance(obj, dict)
        ref = from_int(obj.get("ref"))
        segments = from_list(FareComponentSegment.from_dict, obj.get("segments"))
        return FareComponent(ref, segments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ref"] = from_int(self.ref)
        result["segments"] = from_list(lambda x: to_class(FareComponentSegment, x), self.segments)
        return result


class Info(Enum):
    ALTERNATE_VALIDATING_CARRIER_S_AS = "ALTERNATE VALIDATING CARRIER/S - AS"
    CAT_15_SALES_RESTRICTIONS_FREE_TEXT_FOUND_VERIFY_RULES = "CAT 15 SALES RESTRICTIONS FREE TEXT FOUND - VERIFY RULES"
    NONREF_NOCBBG_NOASR = "NONREF/NOCBBG/NOASR"
    NONREF_NOCHGS = "NONREF/NOCHGS"
    NONREF_NOCHGS_VALID_AS = "NONREF/NOCHGS/VALID AS/"
    NONREF_NOCHG_BESH_NOSEAT = "NONREF/NOCHG/BESH/NOSEAT"
    NONREF_PENALTY_APPLIES = "NONREF/PENALTY APPLIES"
    NONREF_SVCCHGPLUSFAREDIF_CXL_BY_FLT_TIME_OR_NOVALUE_VALID_AS = "NONREF/SVCCHGPLUSFAREDIF/CXL BY FLT TIME OR NOVALUE/VALID AS/"
    VALIDATING_CARRIER_AA = "VALIDATING CARRIER - AA"
    VALIDATING_CARRIER_AS = "VALIDATING CARRIER - AS"
    VALIDATING_CARRIER_B6 = "VALIDATING CARRIER - B6"
    VALIDATING_CARRIER_DL = "VALIDATING CARRIER - DL"
    VALIDATING_CARRIER_UA = "VALIDATING CARRIER - UA"


class TypeForFirstLegEnum(Enum):
    N = "N"
    W = "W"


class FareMessage:
    carrier: str
    code: int
    info: Info
    type: TypeForFirstLegEnum

    def __init__(self, carrier: str, code: int, info: Info, type: TypeForFirstLegEnum) -> None:
        self.carrier = carrier
        self.code = code
        self.info = info
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'FareMessage':
        assert isinstance(obj, dict)
        carrier = obj.get("carrier")
        code = int(from_str(obj.get("code")))
        info = obj.get("info")
        type = TypeForFirstLegEnum(obj.get("type"))
        return FareMessage(carrier, code, info, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["carrier"] = self.carrier
        result["code"] = from_str(str(self.code))
        result["info"] = self.info
        result["type"] = to_enum(TypeForFirstLegEnum, self.type)
        return result


class PassengerTotalFare:
    baseFareAmount: int
    baseFareCurrency: str
    commissionAmount: int
    commissionPercentage: int
    constructionAmount: int
    constructionCurrency: str
    currency: str
    equivalentAmount: int
    equivalentCurrency: str
    exchangeRateOne: int
    totalFare: float
    totalTaxAmount: float

    def __init__(self, baseFareAmount: int, baseFareCurrency: str, commissionAmount: int,
                 commissionPercentage: int, constructionAmount: int, constructionCurrency: str,
                 currency: str, equivalentAmount: int, equivalentCurrency: str, exchangeRateOne: int,
                 totalFare: float, totalTaxAmount: float) -> None:
        self.baseFareAmount = baseFareAmount
        self.baseFareCurrency = baseFareCurrency
        self.commissionAmount = commissionAmount
        self.commissionPercentage = commissionPercentage
        self.constructionAmount = constructionAmount
        self.constructionCurrency = constructionCurrency
        self.currency = currency
        self.equivalentAmount = equivalentAmount
        self.equivalentCurrency = equivalentCurrency
        self.exchangeRateOne = exchangeRateOne
        self.totalFare = totalFare
        self.totalTaxAmount = totalTaxAmount

    @staticmethod
    def from_dict(obj: Any) -> 'PassengerTotalFare':
        assert isinstance(obj, dict)
        baseFareAmount = obj.get("baseFareAmount")
        baseFareCurrency = obj.get("baseFareCurrency")
        commissionAmount = obj.get("commissionAmount")
        commissionPercentage = obj.get("commissionPercentage")
        constructionAmount = obj.get("constructionAmount")
        constructionCurrency = obj.get("constructionCurrency")
        currency = obj.get("currency")
        equivalentAmount = obj.get("equivalentAmount")
        equivalentCurrency = obj.get("equivalentCurrency")
        exchangeRateOne = obj.get("exchangeRateOne")
        totalFare = from_float(obj.get("totalFare"))
        totalTaxAmount = from_float(obj.get("totalTaxAmount"))
        return PassengerTotalFare(baseFareAmount, baseFareCurrency, commissionAmount, commissionPercentage,
                                  constructionAmount, constructionCurrency, currency, equivalentAmount,
                                  equivalentCurrency, exchangeRateOne, totalFare, totalTaxAmount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baseFareAmount"] = self.baseFareAmount
        result["baseFareCurrency"] = self.baseFareCurrency
        result["commissionAmount"] = from_int(self.commissionAmount)
        result["commissionPercentage"] = from_int(self.commissionPercentage)
        result["constructionAmount"] = from_int(self.constructionAmount)
        result["constructionCurrency"] = self.constructionCurrency
        result["currency"] = self.currency
        result["equivalentAmount"] = from_int(self.equivalentAmount)
        result["equivalentCurrency"] = self.equivalentCurrency
        result["exchangeRateOne"] = from_int(self.exchangeRateOne)
        result["totalFare"] = to_float(self.totalFare)
        result["totalTaxAmount"] = to_float(self.totalTaxAmount)
        return result


class PassengerInfo:
    baggageInformation: List[BaggageInformation]
    currencyConversion: CurrencyConversion
    fareComponents: List[FareComponent]
    fareMessages: List[FareMessage]
    nonRefundable: bool
    passengerNumber: int
    passengerTotalFare: PassengerTotalFare
    passengerType: PassengerType
    taxSummaries: List[Schedule]
    taxes: List[Schedule]

    def __init__(self, baggageInformation: List[BaggageInformation], currencyConversion: CurrencyConversion,
                 fareComponents: List[FareComponent], fareMessages: List[FareMessage], nonRefundable: bool,
                 passengerNumber: int, passengerTotalFare: PassengerTotalFare, passengerType: PassengerType,
                 taxSummaries: List[Schedule], taxes: List[Schedule]) -> None:
        self.baggageInformation = baggageInformation
        self.currencyConversion = currencyConversion
        self.fareComponents = fareComponents
        self.fareMessages = fareMessages
        self.nonRefundable = nonRefundable
        self.passengerNumber = passengerNumber
        self.passengerTotalFare = passengerTotalFare
        self.passengerType = passengerType
        self.taxSummaries = taxSummaries
        self.taxes = taxes

    @staticmethod
    def from_dict(obj: Any) -> 'PassengerInfo':
        assert isinstance(obj, dict)
        # if 'None' in obj.get("baggageInformation"):
        # baggageInformation = from_list(BaggageInformation.from_dict, obj.get("baggageInformation"))
        # else:
        baggageInformation = obj.get("baggageInformation")
        currencyConversion = CurrencyConversion.from_dict(obj.get("currencyConversion"))
        fareComponents = from_list(FareComponent.from_dict, obj.get("fareComponents"))
        fareMessages = from_list(FareMessage.from_dict, obj.get("fareMessages"))
        nonRefundable = from_bool(obj.get("nonRefundable"))
        passengerNumber = from_int(obj.get("passengerNumber"))
        passengerTotalFare = PassengerTotalFare.from_dict(obj.get("passengerTotalFare"))
        passengerType = PassengerType(obj.get("passengerType"))
        taxSummaries = from_list(Schedule.from_dict, obj.get("taxSummaries"))
        taxes = from_list(Schedule.from_dict, obj.get("taxes"))
        return PassengerInfo(baggageInformation, currencyConversion, fareComponents, fareMessages, nonRefundable,
                             passengerNumber, passengerTotalFare, passengerType, taxSummaries, taxes)

    def to_dict(self) -> dict:
        result: dict = {}
        # result["baggageInformation"] = from_list(lambda x: to_class(BaggageInformation, x), self.baggageInformation)
        result["baggageInformation"] = self.baggageInformation
        result["currencyConversion"] = to_class(CurrencyConversion, self.currencyConversion)
        result["fareComponents"] = from_list(lambda x: to_class(FareComponent, x), self.fareComponents)
        result["fareMessages"] = from_list(lambda x: to_class(FareMessage, x), self.fareMessages)
        result["nonRefundable"] = from_bool(self.nonRefundable)
        result["passengerNumber"] = from_int(self.passengerNumber)
        result["passengerTotalFare"] = to_class(PassengerTotalFare, self.passengerTotalFare)
        result["passengerType"] = to_enum(PassengerType, self.passengerType)
        result["taxSummaries"] = from_list(lambda x: to_class(Schedule, x), self.taxSummaries)
        result["taxes"] = from_list(lambda x: to_class(Schedule, x), self.taxes)
        return result


class PassengerInfoList:
    passengerInfo: PassengerInfo

    def __init__(self, passengerInfo: PassengerInfo) -> None:
        self.passengerInfo = passengerInfo

    @staticmethod
    def from_dict(obj: Any) -> 'PassengerInfoList':
        assert isinstance(obj, dict)
        passengerInfo = PassengerInfo.from_dict(obj.get("passengerInfo"))
        return PassengerInfoList(passengerInfo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["passengerInfo"] = to_class(PassengerInfo, self.passengerInfo)
        return result


class TotalFare:
    baseFareAmount: int
    baseFareCurrency: str
    constructionAmount: int
    constructionCurrency: str
    currency: str
    equivalentCurrency: str
    totalPrice: float
    totalTaxAmount: float

    def __init__(self, baseFareAmount: int, baseFareCurrency: str, constructionAmount: int,
                 constructionCurrency: str, currency: str, equivalentCurrency: str,
                 totalPrice: float, totalTaxAmount: float) -> None:
        self.baseFareAmount = baseFareAmount
        self.baseFareCurrency = baseFareCurrency
        self.constructionAmount = constructionAmount
        self.constructionCurrency = constructionCurrency
        self.currency = currency
        self.equivalentCurrency = equivalentCurrency
        self.totalPrice = totalPrice
        self.totalTaxAmount = totalTaxAmount

    @staticmethod
    def from_dict(obj: Any) -> 'TotalFare':
        assert isinstance(obj, dict)
        baseFareAmount = obj.get("baseFareAmount")
        baseFareCurrency = (obj.get("baseFareCurrency"))
        constructionAmount = obj.get("constructionAmount")
        constructionCurrency = (obj.get("constructionCurrency"))
        currency = (obj.get("currency"))
        equivalentCurrency = (obj.get("equivalentCurrency"))
        totalPrice = from_float(obj.get("totalPrice"))
        totalTaxAmount = from_float(obj.get("totalTaxAmount"))
        return TotalFare(baseFareAmount, baseFareCurrency, constructionAmount, constructionCurrency, currency,
                         equivalentCurrency, totalPrice, totalTaxAmount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baseFareAmount"] = from_int(self.baseFareAmount)
        result["baseFareCurrency"] = self.baseFareCurrency
        result["constructionAmount"] = from_int(self.constructionAmount)
        result["constructionCurrency"] = self.constructionCurrency
        result["currency"] = self.currency
        result["equivalentCurrency"] = self.equivalentCurrency
        result["totalPrice"] = to_float(self.totalPrice)
        result["totalTaxAmount"] = to_float(self.totalTaxAmount)
        return result


class Fare:
    eTicketable: bool
    governingCarriers: str
    lastTicketDate: datetime
    passengerInfoList: List[PassengerInfoList]
    totalFare: TotalFare
    validatingCarrierCode: str
    validatingCarriers: List[Schedule]
    vita: bool

    def __init__(self, eTicketable: bool, governingCarriers: str, lastTicketDate: datetime,
                 passengerInfoList: List[PassengerInfoList], totalFare: TotalFare,
                 validatingCarrierCode: str, validatingCarriers: List[Schedule], vita: bool) -> None:
        self.eTicketable = eTicketable
        self.governingCarriers = governingCarriers
        self.lastTicketDate = lastTicketDate
        self.passengerInfoList = passengerInfoList
        self.totalFare = totalFare
        self.validatingCarrierCode = validatingCarrierCode
        self.validatingCarriers = validatingCarriers
        self.vita = vita

    @staticmethod
    def from_dict(obj: Any) -> 'Fare':
        assert isinstance(obj, dict)
        eTicketable = from_bool(obj.get("eTicketable"))
        governingCarriers = obj.get("governingCarriers")
        lastTicketDate = obj.get("lastTicketDate")
        passengerInfoList = from_list(PassengerInfoList.from_dict, obj.get("passengerInfoList"))
        totalFare = TotalFare.from_dict(obj.get("totalFare"))
        validatingCarrierCode = obj.get("validatingCarrierCode")
        validatingCarriers = from_list(Schedule.from_dict, obj.get("validatingCarriers"))
        vita = from_bool(obj.get("vita"))
        return Fare(eTicketable, governingCarriers, lastTicketDate, passengerInfoList, totalFare, validatingCarrierCode,
                    validatingCarriers, vita)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eTicketable"] = from_bool(self.eTicketable)
        result["governingCarriers"] = self.governingCarriers
        result["lastTicketDate"] = self.lastTicketDate
        result["passengerInfoList"] = from_list(lambda x: to_class(PassengerInfoList, x), self.passengerInfoList)
        result["totalFare"] = to_class(TotalFare, self.totalFare)
        result["validatingCarrierCode"] = self.validatingCarrierCode
        result["validatingCarriers"] = from_list(lambda x: to_class(Schedule, x), self.validatingCarriers)
        result["vita"] = from_bool(self.vita)
        return result


class PricingSubsource(Enum):
    MIP = "MIP"


class PricingInformation:
    fare: Fare
    pricingSubsource: PricingSubsource

    def __init__(self, fare: Fare, pricingSubsource: PricingSubsource) -> None:
        self.fare = fare
        self.pricingSubsource = pricingSubsource

    @staticmethod
    def from_dict(obj: Any) -> 'PricingInformation':
        assert isinstance(obj, dict)
        fare = Fare.from_dict(obj.get("fare"))
        pricingSubsource = PricingSubsource(obj.get("pricingSubsource"))
        return PricingInformation(fare, pricingSubsource)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fare"] = to_class(Fare, self.fare)
        result["pricingSubsource"] = to_enum(PricingSubsource, self.pricingSubsource)
        return result


class PricingSource(Enum):
    ADVJR1 = "ADVJR1"


class Itinerary:
    diversitySwapper: DiversitySwapper
    id: int
    legs: List[Schedule]
    pricingInformation: List[PricingInformation]
    pricingSource: PricingSource

    def __init__(self, diversitySwapper: DiversitySwapper, id: int, legs: List[Schedule],
                 pricingInformation: List[PricingInformation], pricingSource: PricingSource) -> None:
        self.diversitySwapper = diversitySwapper
        self.id = id
        self.legs = legs
        self.pricingInformation = pricingInformation
        self.pricingSource = pricingSource

    @staticmethod
    def from_dict(obj: Any) -> 'Itinerary':
        assert isinstance(obj, dict)
        diversitySwapper = DiversitySwapper.from_dict(obj.get("diversitySwapper"))
        id = from_int(obj.get("id"))
        legs = from_list(Schedule.from_dict, obj.get("legs"))
        pricingInformation = from_list(PricingInformation.from_dict, obj.get("pricingInformation"))
        pricingSource = PricingSource(obj.get("pricingSource"))
        return Itinerary(diversitySwapper, id, legs, pricingInformation, pricingSource)

    def to_dict(self) -> dict:
        result: dict = {}
        result["diversitySwapper"] = to_class(DiversitySwapper, self.diversitySwapper)
        result["id"] = from_int(self.id)
        result["legs"] = from_list(lambda x: to_class(Schedule, x), self.legs)
        result["pricingInformation"] = from_list(lambda x: to_class(PricingInformation, x), self.pricingInformation)
        result["pricingSource"] = to_enum(PricingSource, self.pricingSource)
        return result


class ItineraryGroup:
    groupDescription: GroupDescription
    itineraries: List[Itinerary]

    def __init__(self, groupDescription: GroupDescription, itineraries: List[Itinerary]) -> None:
        self.groupDescription = groupDescription
        self.itineraries = itineraries

    @staticmethod
    def from_dict(obj: Any) -> 'ItineraryGroup':
        assert isinstance(obj, dict)
        groupDescription = GroupDescription.from_dict(obj.get("groupDescription"))
        itineraries = from_list(Itinerary.from_dict, obj.get("itineraries"))
        return ItineraryGroup(groupDescription, itineraries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupDescription"] = to_class(GroupDescription, self.groupDescription)
        result["itineraries"] = from_list(lambda x: to_class(Itinerary, x), self.itineraries)
        return result


class LegDesc:
    id: int
    schedules: List[Schedule]

    def __init__(self, id: int, schedules: List[Schedule]) -> None:
        self.id = id
        self.schedules = schedules

    @staticmethod
    def from_dict(obj: Any) -> 'LegDesc':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        schedules = from_list(Schedule.from_dict, obj.get("schedules"))
        return LegDesc(id, schedules)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["schedules"] = from_list(lambda x: to_class(Schedule, x), self.schedules)
        return result


class Message:
    code: str
    severity: str
    text: str
    type: str

    def __init__(self, code: str, severity: str, text: str, type: str) -> None:
        self.code = code
        self.severity = severity
        self.text = text
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        severity = from_str(obj.get("severity"))
        text = from_str(obj.get("text"))
        type = from_str(obj.get("type"))
        return Message(code, severity, text, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["severity"] = from_str(self.severity)
        result["text"] = from_str(self.text)
        result["type"] = from_str(self.type)
        return result


# class City(Enum):
#    DTT = "DTT"
#    PHX = "PHX"
#    QYC = "QYC"
#    SFO = "SFO"


# class Country(Enum):
#    US = "US"


# class State(Enum):
#    AZ = "AZ"
#    CA = "CA"
#    MI = "MI"
#    NJ = "NJ"
#    NY = "NY"


class Arrival:
    airport: str
    city: str
    country: str
    dateAdjustment: Optional[int]
    state: str
    terminal: str
    time: datetime

    def __init__(self, airport: str, city: str, country: str, dateAdjustment: Optional[int], state: str
                 ,
                 terminal: str, time: datetime) -> None:
        self.airport = airport
        self.city = city
        self.country = country
        self.dateAdjustment = dateAdjustment
        self.state = state
        self.terminal = terminal
        self.time = time

    def convert12(self, strTime):

        # Get Hours
        h1 = ord(strTime[0]) - ord('0');
        h2 = ord(strTime[1]) - ord('0');
        convertedtime: str = '';
        hh = h1 * 10 + h2;

        # Finding out the Meridien of time
        # ie. AM or PM
        Meridien = "";
        if (hh < 12):
            Meridien = "AM";
        else:
            Meridien = "PM";

        hh %= 12;

        # Handle 00 and 12 case separately
        if (hh == 0):
            print("12", end="");
            convertedtime = convertedtime + "12";

            # Printing minutes and seconds
            for i in range(2, 8):
                convertedtime = convertedtime + strTime[i];
                print(strTime[i], end="");

        else:
            print(hh, end="");
            convertedtime = convertedtime + str(hh);

            # Printing minutes and seconds
            for i in range(2, 8):
                convertedtime = convertedtime + strTime[i];
                print(strTime[i], end="");
        print(" " + Meridien);
        convertedtime = convertedtime + " " + Meridien;
        print("convertedtime" + convertedtime);
        return convertedtime;

    @staticmethod
    def from_dict(obj: Any) -> 'Arrival':
        assert isinstance(obj, dict)
        airport = obj.get("airport")
        city = obj.get("city")
        country = obj.get("country")
        dateAdjustment = from_union([from_int, from_none], obj.get("dateAdjustment"))
        state = obj.get("state")
        terminal = obj.get("terminal")
        time = obj.get("time")
        return Arrival(airport, city, country, dateAdjustment, state, terminal, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["airport"] = self.airport
        result["city"] = self.city
        result["country"] = self.country
        result["dateAdjustment"] = from_union([from_int, from_none], self.dateAdjustment)
        result["state"] = self.state
        result["terminal"] = self.terminal
        if '-' in self.time:
            print(int("-" + self.time.split("-")[1].split(":")[0]));
            timeValue = datetime.strptime(self.time.split("-")[0], '%H:%M:%S') + timedelta(
                hours=int("-" + self.time.split("-")[1].split(":")[0]),
                minutes=int("-" + self.time.split("-")[1].split(":")[1]))
            print(self.convert12(str(timeValue.time())));
            result["strtime"] = self.convert12(str(timeValue.time()))
            result["strtime24hrLocal"] = str(timeValue.time())
        else:
            timeValue = datetime.strptime(self.time.split("+")[0], '%H:%M:%S') + timedelta(
                hours=int(self.time.split("+")[1].split(":")[0]), minutes=int(self.time.split("+")[1].split(":")[1]))
            print(self.convert12(str(timeValue.time())));
            # str(self.time.split("+")[0])
            result["strtime"] = self.convert12(str(timeValue.time()))
            result["strtime24hrLocal"] = str(timeValue.time())
        if '-' in self.time:
            result["strtime24hr"] = self.time.split("-")[0]
        else:
            result["strtime24hr"] = self.time.split("+")[0]

        return result


class Equipment:
    code: str
    typeForFirstLeg: TypeForFirstLegEnum
    typeForLastLeg: TypeForFirstLegEnum

    def __init__(self, code: str, typeForFirstLeg: TypeForFirstLegEnum, typeForLastLeg: TypeForFirstLegEnum) -> None:
        self.code = code
        self.typeForFirstLeg = typeForFirstLeg
        self.typeForLastLeg = typeForLastLeg

    @staticmethod
    def from_dict(obj: Any) -> 'Equipment':
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        typeForFirstLeg = TypeForFirstLegEnum(obj.get("typeForFirstLeg"))
        typeForLastLeg = TypeForFirstLegEnum(obj.get("typeForLastLeg"))
        return Equipment(code, typeForFirstLeg, typeForLastLeg)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["typeForFirstLeg"] = to_enum(TypeForFirstLegEnum, self.typeForFirstLeg)
        result["typeForLastLeg"] = to_enum(TypeForFirstLegEnum, self.typeForLastLeg)
        return result


class Carrier:
    equipment: Equipment
    marketing: str
    marketingFlightNumber: int
    operating: str
    operatingFlightNumber: int
    alliances: Optional[str]

    def __init__(self, equipment: Equipment, marketing: str, marketingFlightNumber: int,
                 operating: str, operatingFlightNumber: int, alliances: Optional[str]) -> None:
        self.equipment = equipment
        self.marketing = marketing
        self.marketingFlightNumber = marketingFlightNumber
        self.operating = operating
        self.operatingFlightNumber = operatingFlightNumber
        self.alliances = alliances

    @staticmethod
    def from_dict(obj: Any) -> 'Carrier':
        assert isinstance(obj, dict)
        equipment = Equipment.from_dict(obj.get("equipment"))
        marketing = obj.get("marketing")
        marketingFlightNumber = from_int(obj.get("marketingFlightNumber"))
        operating = obj.get("operating")
        operatingFlightNumber = from_int(obj.get("operatingFlightNumber"))
        alliances = from_union([from_str, from_none], obj.get("alliances"))
        return Carrier(equipment, marketing, marketingFlightNumber, operating, operatingFlightNumber, alliances)

    def to_dict(self) -> dict:
        result: dict = {}
        result["equipment"] = to_class(Equipment, self.equipment)
        result["marketing"] = self.marketing
        result["marketingFlightNumber"] = from_int(self.marketingFlightNumber)
        result["operating"] = self.operating
        result["operatingFlightNumber"] = from_int(self.operatingFlightNumber)
        result["alliances"] = from_union([from_str, from_none], self.alliances)
        return result


class ScheduleDesc:
    arrival: Arrival
    carrier: Carrier
    departure: Arrival
    dotRating: Union[DotRating, int, None]
    eTicketable: bool
    frequency: str
    id: int
    stopCount: int
    totalMilesFlown: int
    onTimePerformance: Optional[int]

    def __init__(self, arrival: Arrival, carrier: Carrier, departure: Arrival, dotRating: Union[DotRating, int, None],
                 eTicketable: bool, frequency: str, id: int, stopCount: int, totalMilesFlown: int,
                 onTimePerformance: Optional[int]) -> None:
        self.arrival = arrival
        self.carrier = carrier
        self.departure = departure
        self.dotRating = dotRating
        self.eTicketable = eTicketable
        self.frequency = frequency
        self.id = id
        self.stopCount = stopCount
        self.totalMilesFlown = totalMilesFlown
        self.onTimePerformance = onTimePerformance

    @staticmethod
    def from_dict(obj: Any) -> 'ScheduleDesc':
        assert isinstance(obj, dict)
        arrival = Arrival.from_dict(obj.get("arrival"))
        carrier = Carrier.from_dict(obj.get("carrier"))
        departure = Arrival.from_dict(obj.get("departure"))
        dotRating = from_union([from_none, lambda x: from_union([DotRating, lambda x: int(x)], from_str(x))],
                               obj.get("dotRating"))
        eTicketable = from_bool(obj.get("eTicketable"))
        frequency = from_str(obj.get("frequency"))
        id = from_int(obj.get("id"))
        stopCount = from_int(obj.get("stopCount"))
        totalMilesFlown = from_int(obj.get("totalMilesFlown"))
        onTimePerformance = from_union([from_int, from_none], obj.get("onTimePerformance"))
        return ScheduleDesc(arrival, carrier, departure, dotRating, eTicketable, frequency, id, stopCount,
                            totalMilesFlown, onTimePerformance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["arrival"] = to_class(Arrival, self.arrival)
        result["carrier"] = to_class(Carrier, self.carrier)
        result["departure"] = to_class(Arrival, self.departure)
        result["dotRating"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                                          lambda x: from_str(
                                              (lambda x: to_enum(DotRating, (lambda x: is_type(DotRating, x))(x)))(x)),
                                          lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))],
                                         self.dotRating)
        result["eTicketable"] = from_bool(self.eTicketable)
        result["frequency"] = from_str(self.frequency)
        result["id"] = from_int(self.id)
        result["stopCount"] = from_int(self.stopCount)
        result["totalMilesFlown"] = from_int(self.totalMilesFlown)
        result["onTimePerformance"] = from_union([from_int, from_none], self.onTimePerformance)
        return result


class Statistics:
    itineraryCount: int

    def __init__(self, itineraryCount: int) -> None:
        self.itineraryCount = itineraryCount

    @staticmethod
    def from_dict(obj: Any) -> 'Statistics':
        assert isinstance(obj, dict)
        itineraryCount = from_int(obj.get("itineraryCount"))
        return Statistics(itineraryCount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["itineraryCount"] = from_int(self.itineraryCount)
        return result


# class Code(Enum):
#    AY = "AY"
#    XF = "XF"


# class Description(Enum):
#    PASSENGER_CIVIL_AVIATION_SECURITY_SERVICE_FEE = "PASSENGER CIVIL AVIATION SECURITY SERVICE FEE"
#    PASSENGER_FACILITY_CHARGE = "PASSENGER FACILITY CHARGE"
#    PASSENGER_FACILITY_CHARGES = "PASSENGER FACILITY CHARGES"


class TaxDesc:
    amount: float
    code: str
    country: str
    currency: str
    description: str
    id: int
    publishedAmount: float
    publishedCurrency: str
    station: str

    def __init__(self, amount: float, code: str, country: str, currency: str, description: str,
                 id: int, publishedAmount: float, publishedCurrency: str, station: str) -> None:
        self.amount = amount
        self.code = code
        self.country = country
        self.currency = currency
        self.description = description
        self.id = id
        self.publishedAmount = publishedAmount
        self.publishedCurrency = publishedCurrency
        self.station = station

    @staticmethod
    def from_dict(obj: Any) -> 'TaxDesc':
        assert isinstance(obj, dict)
        amount = from_float(obj.get("amount"))
        code = (obj.get("code"))
        country = (obj.get("country"))
        currency = (obj.get("currency"))
        description = (obj.get("description"))
        id = from_int(obj.get("id"))
        publishedAmount = from_float(obj.get("publishedAmount"))
        publishedCurrency = (obj.get("publishedCurrency"))
        station = obj.get("station")
        return TaxDesc(amount, code, country, currency, description, id, publishedAmount, publishedCurrency, station)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = to_float(self.amount)
        result["code"] = self.code
        result["country"] = self.country
        result["currency"] = self.currency
        result["description"] = self.description
        result["id"] = from_int(self.id)
        result["publishedAmount"] = to_float(self.publishedAmount)
        result["publishedCurrency"] = self.publishedCurrency
        result["station"] = self.station
        return result


class Default:
    code: str

    def __init__(self, code: str) -> None:
        self.code = code

    @staticmethod
    def from_dict(obj: Any) -> 'Default':
        assert isinstance(obj, dict)
        code = obj.get("code")
        return Default(code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = self.code
        return result


class ValidatingCarrierDesc:
    default: Default
    id: int
    newVcxProcess: bool
    settlementMethod: str
    alternates: Optional[List[Default]]

    def __init__(self, default: Default, id: int, newVcxProcess: bool, settlementMethod: str,
                 alternates: Optional[List[Default]]) -> None:
        self.default = default
        self.id = id
        self.newVcxProcess = newVcxProcess
        self.settlementMethod = settlementMethod
        self.alternates = alternates

    @staticmethod
    def from_dict(obj: Any) -> 'ValidatingCarrierDesc':
        assert isinstance(obj, dict)
        default = Default.from_dict(obj.get("default"))
        id = from_int(obj.get("id"))
        newVcxProcess = from_bool(obj.get("newVcxProcess"))
        settlementMethod = from_str(obj.get("settlementMethod"))
        alternates = from_union([lambda x: from_list(Default.from_dict, x), from_none], obj.get("alternates"))
        return ValidatingCarrierDesc(default, id, newVcxProcess, settlementMethod, alternates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["default"] = to_class(Default, self.default)
        result["id"] = from_int(self.id)
        result["newVcxProcess"] = from_bool(self.newVcxProcess)
        result["settlementMethod"] = from_str(self.settlementMethod)
        result["alternates"] = from_union([lambda x: from_list(lambda x: to_class(Default, x), x), from_none],
                                          self.alternates)
        return result


class GroupedItineraryResponse:
    # baggageAllowanceDescs: List[BaggageAllowanceDesc]
    fareComponentDescs: List[FareComponentDesc]
    itineraryGroups: List[ItineraryGroup]
    # legDescs: List[LegDesc]
    messages: List[Message]
    scheduleDescs: List[ScheduleDesc]
    # statistics: Statistics
    # taxDescs: List[TaxDesc]
    # taxSummaryDescs: List[TaxDesc]
    # validatingCarrierDescs: List[ValidatingCarrierDesc]
    version: str

    def __init__(self, baggageAllowanceDescs: List[BaggageAllowanceDesc], fareComponentDescs: List[FareComponentDesc],
                 itineraryGroups: List[ItineraryGroup], legDescs: List[LegDesc], messages: List[Message],
                 scheduleDescs: List[ScheduleDesc], statistics: Statistics, taxDescs: List[TaxDesc],
                 taxSummaryDescs: List[TaxDesc], validatingCarrierDescs: List[ValidatingCarrierDesc],
                 version: str) -> None:
        self.baggageAllowanceDescs = baggageAllowanceDescs
        self.fareComponentDescs = fareComponentDescs
        self.itineraryGroups = itineraryGroups
        self.legDescs = legDescs
        self.messages = messages
        self.scheduleDescs = scheduleDescs
        self.statistics = statistics
        self.taxDescs = taxDescs
        self.taxSummaryDescs = taxSummaryDescs
        self.validatingCarrierDescs = validatingCarrierDescs
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'GroupedItineraryResponse':
        assert isinstance(obj, dict)
        baggageAllowanceDescs = from_list(BaggageAllowanceDesc.from_dict, obj.get("baggageAllowanceDescs"))
        fareComponentDescs = from_list(FareComponentDesc.from_dict, obj.get("fareComponentDescs"))
        itineraryGroups = from_list(ItineraryGroup.from_dict, obj.get("itineraryGroups"))
        legDescs = from_list(LegDesc.from_dict, obj.get("legDescs"))
        messages = from_list(Message.from_dict, obj.get("messages"))
        scheduleDescs = from_list(ScheduleDesc.from_dict, obj.get("scheduleDescs"))
        statistics = Statistics.from_dict(obj.get("statistics"))
        taxDescs = from_list(TaxDesc.from_dict, obj.get("taxDescs"))
        taxSummaryDescs = from_list(TaxDesc.from_dict, obj.get("taxSummaryDescs"))
        validatingCarrierDescs = from_list(ValidatingCarrierDesc.from_dict, obj.get("validatingCarrierDescs"))
        version = from_str(obj.get("version"))
        return GroupedItineraryResponse(baggageAllowanceDescs, fareComponentDescs, itineraryGroups, legDescs, messages,
                                        scheduleDescs, statistics, taxDescs, taxSummaryDescs, validatingCarrierDescs,
                                        version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baggageAllowanceDescs"] = from_list(lambda x: to_class(BaggageAllowanceDesc, x),
                                                    self.baggageAllowanceDescs)
        result["fareComponentDescs"] = from_list(lambda x: to_class(FareComponentDesc, x), self.fareComponentDescs)
        result["itineraryGroups"] = from_list(lambda x: to_class(ItineraryGroup, x), self.itineraryGroups)
        result["legDescs"] = from_list(lambda x: to_class(LegDesc, x), self.legDescs)
        result["messages"] = from_list(lambda x: to_class(Message, x), self.messages)
        result["scheduleDescs"] = from_list(lambda x: to_class(ScheduleDesc, x), self.scheduleDescs)
        result["statistics"] = to_class(Statistics, self.statistics)
        result["taxDescs"] = from_list(lambda x: to_class(TaxDesc, x), self.taxDescs)
        result["taxSummaryDescs"] = from_list(lambda x: to_class(TaxDesc, x), self.taxSummaryDescs)
        result["validatingCarrierDescs"] = from_list(lambda x: to_class(ValidatingCarrierDesc, x),
                                                     self.validatingCarrierDescs)
        result["version"] = from_str(self.version)
        return result


class Welcome:
    groupedItineraryResponse: GroupedItineraryResponse

    def __init__(self, groupedItineraryResponse: GroupedItineraryResponse) -> None:
        self.groupedItineraryResponse = groupedItineraryResponse

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        groupedItineraryResponse = GroupedItineraryResponse.from_dict(obj.get("groupedItineraryResponse"))
        return Welcome(groupedItineraryResponse)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupedItineraryResponse"] = to_class(GroupedItineraryResponse, self.groupedItineraryResponse)
        return result

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)


def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)


def authenticate():
    AuthenticationHeader = {'Authorization': 'Basic VmpFNk9UTTFNVEEzT2tNelVrczZRVUU9OlZFUnBaMms1TURFPQ==',
                            'Content-Type': 'application/x-www-form-urlencoded', 'grant_type': 'client_credentials'}
    authResponse = requests.post(url=Authenticate_Endpoint, headers=AuthenticationHeader)
    API_KEY = json.loads(authResponse.content)['access_token']
    AuthorizationHeader['Authorization'] = 'Bearer ' + API_KEY
    AuthorizationHeader['Content-Type'] = 'application/json'
    AuthorizationHeader['accept'] = 'application/json'
    print(json.loads(authResponse.content)['access_token'])


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/resources/authenticate', methods=['POST'])
def clientauthentication():
    print(base64.standard_b64decode(request.headers['Authorization'].split(' ')[1]))
    objCommonHelper = CommonHelper.PostgressController()
    return objCommonHelper.clientAuthentication('', '')


@app.route('/api/v1/resources/getairports', methods=['GET'])
def getAirports():
    searchTerm = request.args['searchTerm']
    objCommonHelper = CommonHelper.PostgressController()
    return objCommonHelper.get_airports(searchTerm.lower())


@app.route('/api/v1/resources/bargainer/all', methods=['POST'])
def api_all():
    authenticate()
    print(request.json)
    r = requests.post(url=BFM_Endpoint, json=request.json, headers=AuthorizationHeader)
    print(r.content)
    result = welcome_from_dict(json.loads(r.content))
    sabreAPIResponse = result.to_dict()
    return sabreAPIResponse


@app.route('/api/v1/resources/searchhotel', methods=['POST'])
def searchhotel():
    authenticate()
    print(request.json)
    hotelSearchResponse = requests.post(url=HotelAvailability_Endpoint, json=request.json, headers=AuthorizationHeader)
    return hotelSearchResponse.content


@app.route('/api/v1/resources/hoteldetails', methods=['POST'])
def hoteldetails():
    authenticate()
    print(request.json)
    hotelDetailResponse = requests.post(url=HotelDetail_Endpoint, json=request.json, headers=AuthorizationHeader)
    return hotelDetailResponse.content


@app.route('/api/v1/resources/createflightpnr', methods=['POST'])
def createflightpnr():
    authenticate()
    print(request.headers['Pnrfor'])
    StateCountyProv = CreatePNRModel.StateCountyProv('TX')
    Address = CreatePNRModel.Address('SABRE TRAVEL', 'SOUTHLAKE', 'US', '76092', StateCountyProv, '3150 SABRE DRIVE')
    Ticketing = CreatePNRModel.Ticketing('7TAW')
    AgencyInfo = CreatePNRModel.AgencyInfo(Address, Ticketing)
    # ContactNumber = CreatePNRModel.ContactNumber('1.1', '817-555-1212', 'H') commented code
    ContactNumbers = \
        request.json['CreatePassengerNameRecordRQ']['TravelItineraryAddInfo']['CustomerInfo']['ContactNumbers'][
            'ContactNumber']
    ContactNumbers = CreatePNRModel.ContactNumbers(ContactNumbers)
    # PersonName = CreatePNRModel.PersonName('1.1', 'ADT', 'Shubbham', 'Gupta') commented code
    PersonNames = request.json['CreatePassengerNameRecordRQ']['TravelItineraryAddInfo']['CustomerInfo']['PersonName']
    Emails = request.json['CreatePassengerNameRecordRQ']['TravelItineraryAddInfo']['CustomerInfo']['Email']
    CustomerInfo = CreatePNRModel.CustomerInfo(ContactNumbers, PersonNames, Emails)
    TravelItineraryAddInfo = CreatePNRModel.TravelItineraryAddInfo(AgencyInfo, CustomerInfo)
    Source = CreatePNRModel.Source('SP TEST')
    EmailEndTransaction = CreatePNRModel.EmailEndTransaction(bool(1))
    EndTransaction = CreatePNRModel.EndTransaction(Source, EmailEndTransaction)
    RedisplayReservation = CreatePNRModel.RedisplayReservation(100)
    PostProcessing = CreatePNRModel.PostProcessing(EndTransaction, RedisplayReservation)

    if request.headers['Pnrfor'] == "Flight":
        RetryRebook = CreatePNRModel.RetryRebook(bool(1))
        HaltOnStatuses = [CreatePNRModel.HaltOnStatus('HL'), CreatePNRModel.HaltOnStatus('KK'),
                          CreatePNRModel.HaltOnStatus('LL'), CreatePNRModel.HaltOnStatus('NN'),
                          CreatePNRModel.HaltOnStatus('NO')]
        FlightSegment = request.json['CreatePassengerNameRecordRQ']['AirBook']['OriginDestinationInformation'][
            'FlightSegment']
        OriginDestinationInformations = FlightSegment
        AirBook = CreatePNRModel.AirBook(RetryRebook, HaltOnStatuses,
                                         CreatePNRModel.OriginDestinationInformation(OriginDestinationInformations))
        CreatePassengerNameRecordRQ = CreatePNRModel.CreatePassengerNameRecordRQ('2.3.0', PCC_Code, bool(0),
                                                                                 TravelItineraryAddInfo, AirBook,
                                                                                 PostProcessing, '')
        del CreatePassengerNameRecordRQ.HotelBook
    else:
        # Source = HotelRateModel.Source(PCC_Code)
        # POS = HotelRateModel.Pos(Source)
        # HotelRef = HotelRateModel.HotelRef('100015408', 'GLOBAL')
        # HotelRefs = HotelRateModel.HotelRefs(HotelRef)
        # StayDateRange = HotelRateModel.StayDateRange('2020-05-15', '2020-05-20')
        # RateRange = HotelRateModel.RateRange(1, 5000)
        # Rooms = HotelRateModel.Rooms([HotelRateModel.Room('1', 1, 2, 1)])
        # RateInfoRef = HotelRateModel.RateInfoRef(StayDateRange, RateRange, Rooms, '100,112,113', 'USD',
        #                                         'IncludePrepaid')
        # GetHotelRateInfoRQ = HotelRateModel.GetHotelRateInfoRQ(POS, HotelRefs, RateInfoRef, '3.0.0')
        # HoteRateJSON = json.dumps(HotelRateModel.Welcome(GetHotelRateInfoRQ), default=lambda o: o.__dict__)
        # hotelRateInfoResponse = requests.post(url=HotelRateInfo_Endpoint, json=json.loads(HoteRateJSON),
        #                                      headers=AuthorizationHeader)
        # RateKey = json.loads(hotelRateInfoResponse.content)['GetHotelRateInfoRS']['HotelRateInfos']['HotelRateInfo'][0][
        #    'RateInfos']['RateInfo'][0]['RateKey']
        RateKey = request.json['CreatePassengerNameRecordRQ']['HotelRate']['RateKey']
        RateInfoRef = HotelPriceCheckModel.RateInfoRef(RateKey)
        HotelPriceCheckRQ = HotelPriceCheckModel.HotelPriceCheckRQ(RateInfoRef)
        print('RateKey: ' + HotelPriceCheckRQ.RateInfoRef.RateKey)
        HotelPriceCheckJSON = json.dumps(HotelPriceCheckModel.Welcome(HotelPriceCheckRQ), default=lambda o: o.__dict__)
        hotelPriceCheckResponse = requests.post(url=HotelPriceCheck_Endpoint,
                                                json=json.loads(HotelPriceCheckJSON),
                                                headers=AuthorizationHeader)
        print(hotelPriceCheckResponse.content)
        BookingKey = json.loads(hotelPriceCheckResponse.content)['HotelPriceCheckRS']['PriceCheckInfo']['BookingKey']
        BookingInfo = request.json['CreatePassengerNameRecordRQ']['HotelBook']['BookingInfo']
        Rooms = request.json['CreatePassengerNameRecordRQ']['HotelBook']['Rooms']
        PaymentInformation = request.json['CreatePassengerNameRecordRQ']['HotelBook']['PaymentInformation']
        BookingInfo['BookingKey'] = BookingKey
        HotelBook = CreatePNRModel.HotelBook(BookingInfo, Rooms, PaymentInformation)
        CreatePassengerNameRecordRQ = CreatePNRModel.CreatePassengerNameRecordRQ('2.3.0', PCC_Code, bool(0),
                                                                                 TravelItineraryAddInfo, '',
                                                                                 PostProcessing, HotelBook)
        del CreatePassengerNameRecordRQ.AirBook
        print('Hotel')

    createPNRJson = json.dumps(CreatePNRModel.Welcome(CreatePassengerNameRecordRQ), default=lambda o: o.__dict__)
    print(json.loads(createPNRJson))

    r = requests.post(url=PNR_Endpoint, json=json.loads(createPNRJson), headers=AuthorizationHeader)
    print(r.content)
    return r.content


if __name__ == "__main__":
    app.run()

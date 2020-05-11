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


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


class HotelRef:
    HotelCode: Optional[int]
    CodeContext: Optional[str]

    def __init__(self, HotelCode: Optional[int], CodeContext: Optional[str]) -> None:
        self.HotelCode = HotelCode
        self.CodeContext = CodeContext

    @staticmethod
    def from_dict(obj: Any) -> 'HotelRef':
        assert isinstance(obj, dict)
        HotelCode = from_union([from_none, lambda x: int(from_str(x))], obj.get("HotelCode"))
        CodeContext = from_union([from_str, from_none], obj.get("CodeContext"))
        return HotelRef(HotelCode, CodeContext)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HotelCode"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.HotelCode)
        result["CodeContext"] = from_union([from_str, from_none], self.CodeContext)
        return result


class HotelRefs:
    HotelRef: Optional[HotelRef]

    def __init__(self, HotelRef: Optional[HotelRef]) -> None:
        self.HotelRef = HotelRef

    @staticmethod
    def from_dict(obj: Any) -> 'HotelRefs':
        assert isinstance(obj, dict)
        HotelRef = from_union([HotelRef.from_dict, from_none], obj.get("HotelRef"))
        return HotelRefs(HotelRef)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HotelRef"] = from_union([lambda x: to_class(HotelRef, x), from_none], self.HotelRef)
        return result


class Source:
    PseudoCityCode: Optional[str]

    def __init__(self, PseudoCityCode: Optional[str]) -> None:
        self.PseudoCityCode = PseudoCityCode

    @staticmethod
    def from_dict(obj: Any) -> 'Source':
        assert isinstance(obj, dict)
        PseudoCityCode = from_union([from_str, from_none], obj.get("PseudoCityCode"))
        return Source(PseudoCityCode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["PseudoCityCode"] = from_union([from_str, from_none], self.PseudoCityCode)
        return result


class Pos:
    Source: Optional[Source]

    def __init__(self, Source: Optional[Source]) -> None:
        self.Source = Source

    @staticmethod
    def from_dict(obj: Any) -> 'Pos':
        assert isinstance(obj, dict)
        Source = from_union([Source.from_dict, from_none], obj.get("Source"))
        return Pos(Source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Source"] = from_union([lambda x: to_class(Source, x), from_none], self.Source)
        return result


class RateRange:
    Min: Optional[int]
    Max: Optional[int]

    def __init__(self, Min: Optional[int], Max: Optional[int]) -> None:
        self.Min = Min
        self.Max = Max

    @staticmethod
    def from_dict(obj: Any) -> 'RateRange':
        assert isinstance(obj, dict)
        Min = from_union([from_int, from_none], obj.get("Min"))
        Max = from_union([from_int, from_none], obj.get("Max"))
        return RateRange(Min, Max)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Min"] = from_union([from_int, from_none], self.Min)
        result["Max"] = from_union([from_int, from_none], self.Max)
        return result


class Room:
    ChildAges: Optional[int]
    Index: Optional[int]
    Adults: Optional[int]
    Children: Optional[int]

    def __init__(self, ChildAges: Optional[int], Index: Optional[int], Adults: Optional[int], Children: Optional[int]) -> None:
        self.ChildAges = ChildAges
        self.Index = Index
        self.Adults = Adults
        self.Children = Children

    @staticmethod
    def from_dict(obj: Any) -> 'Room':
        assert isinstance(obj, dict)
        ChildAges = from_union([from_none, lambda x: int(from_str(x))], obj.get("ChildAges"))
        Index = from_union([from_int, from_none], obj.get("Index"))
        Adults = from_union([from_int, from_none], obj.get("Adults"))
        Children = from_union([from_int, from_none], obj.get("Children"))
        return Room(ChildAges, Index, Adults, Children)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ChildAges"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ChildAges)
        result["Index"] = from_union([from_int, from_none], self.Index)
        result["Adults"] = from_union([from_int, from_none], self.Adults)
        result["Children"] = from_union([from_int, from_none], self.Children)
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


class StayDateRange:
    StartDate: Optional[datetime]
    EndDate: Optional[datetime]

    def __init__(self, StartDate: Optional[datetime], EndDate: Optional[datetime]) -> None:
        self.StartDate = StartDate
        self.EndDate = EndDate

    @staticmethod
    def from_dict(obj: Any) -> 'StayDateRange':
        assert isinstance(obj, dict)
        StartDate = from_union([from_datetime, from_none], obj.get("StartDate"))
        EndDate = from_union([from_datetime, from_none], obj.get("EndDate"))
        return StayDateRange(StartDate, EndDate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StartDate"] = from_union([lambda x: x.isoformat(), from_none], self.StartDate)
        result["EndDate"] = from_union([lambda x: x.isoformat(), from_none], self.EndDate)
        return result


class RateInfoRef:
    StayDateRange: Optional[StayDateRange]
    RateRange: Optional[RateRange]
    Rooms: Optional[Rooms]
    InfoSource: Optional[str]
    CurrencyCode: Optional[str]
    PrepaidQualifier: Optional[str]
    ConvertedRateInfoOnly: Optional[bool]

    def __init__(self, StayDateRange: Optional[StayDateRange], RateRange: Optional[RateRange], Rooms: Optional[Rooms], InfoSource: Optional[str], CurrencyCode: Optional[str], PrepaidQualifier: Optional[str], ConvertedRateInfoOnly: Optional[bool]) -> None:
        self.StayDateRange = StayDateRange
        self.RateRange = RateRange
        self.Rooms = Rooms
        self.InfoSource = InfoSource
        self.CurrencyCode = CurrencyCode
        self.PrepaidQualifier = PrepaidQualifier
        self.ConvertedRateInfoOnly = ConvertedRateInfoOnly

    @staticmethod
    def from_dict(obj: Any) -> 'RateInfoRef':
        assert isinstance(obj, dict)
        StayDateRange = from_union([StayDateRange.from_dict, from_none], obj.get("StayDateRange"))
        RateRange = from_union([RateRange.from_dict, from_none], obj.get("RateRange"))
        Rooms = from_union([Rooms.from_dict, from_none], obj.get("Rooms"))
        InfoSource = from_union([from_str, from_none], obj.get("InfoSource"))
        CurrencyCode = from_union([from_str, from_none], obj.get("CurrencyCode"))
        PrepaidQualifier = from_union([from_str, from_none], obj.get("PrepaidQualifier"))
        ConvertedRateInfoOnly = from_union([from_bool, from_none], obj.get("ConvertedRateInfoOnly"))
        return RateInfoRef(StayDateRange, RateRange, Rooms, InfoSource, CurrencyCode, PrepaidQualifier, ConvertedRateInfoOnly)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StayDateRange"] = from_union([lambda x: to_class(StayDateRange, x), from_none], self.StayDateRange)
        result["RateRange"] = from_union([lambda x: to_class(RateRange, x), from_none], self.RateRange)
        result["Rooms"] = from_union([lambda x: to_class(Rooms, x), from_none], self.Rooms)
        result["InfoSource"] = from_union([from_str, from_none], self.InfoSource)
        result["CurrencyCode"] = from_union([from_str, from_none], self.CurrencyCode)
        result["PrepaidQualifier"] = from_union([from_str, from_none], self.PrepaidQualifier)
        result["ConvertedRateInfoOnly"] = from_union([from_bool, from_none], self.ConvertedRateInfoOnly)
        return result


class GetHotelRateInfoRQ:
    POS: Optional[Pos]
    HotelRefs: Optional[HotelRefs]
    RateInfoRef: Optional[RateInfoRef]
    version: Optional[str]

    def __init__(self, POS: Optional[Pos], HotelRefs: Optional[HotelRefs], RateInfoRef: Optional[RateInfoRef], version: Optional[str]) -> None:
        self.POS = POS
        self.HotelRefs = HotelRefs
        self.RateInfoRef = RateInfoRef
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'GetHotelRateInfoRQ':
        assert isinstance(obj, dict)
        POS = from_union([Pos.from_dict, from_none], obj.get("POS"))
        HotelRefs = from_union([HotelRefs.from_dict, from_none], obj.get("HotelRefs"))
        RateInfoRef = from_union([RateInfoRef.from_dict, from_none], obj.get("RateInfoRef"))
        version = from_union([from_str, from_none], obj.get("version"))
        return GetHotelRateInfoRQ(POS, HotelRefs, RateInfoRef, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["POS"] = from_union([lambda x: to_class(Pos, x), from_none], self.POS)
        result["HotelRefs"] = from_union([lambda x: to_class(HotelRefs, x), from_none], self.HotelRefs)
        result["RateInfoRef"] = from_union([lambda x: to_class(RateInfoRef, x), from_none], self.RateInfoRef)
        result["version"] = from_union([from_str, from_none], self.version)
        return result


class Welcome:
    GetHotelRateInfoRQ: Optional[GetHotelRateInfoRQ]

    def __init__(self, GetHotelRateInfoRQ: Optional[GetHotelRateInfoRQ]) -> None:
        self.GetHotelRateInfoRQ = GetHotelRateInfoRQ

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        GetHotelRateInfoRQ = from_union([GetHotelRateInfoRQ.from_dict, from_none], obj.get("GetHotelRateInfoRQ"))
        return Welcome(GetHotelRateInfoRQ)

    def to_dict(self) -> dict:
        result: dict = {}
        result["GetHotelRateInfoRQ"] = from_union([lambda x: to_class(GetHotelRateInfoRQ, x), from_none], self.GetHotelRateInfoRQ)
        return result


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)


def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)

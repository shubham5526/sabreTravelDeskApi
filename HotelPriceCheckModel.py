# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from typing import Optional, Any, TypeVar, Type, cast


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class RateInfoRef:
    RateKey: Optional[str]

    def __init__(self, RateKey: Optional[str]) -> None:
        self.RateKey = RateKey

    @staticmethod
    def from_dict(obj: Any) -> 'RateInfoRef':
        assert isinstance(obj, dict)
        RateKey = from_union([from_str, from_none], obj.get("RateKey"))
        return RateInfoRef(RateKey)

    def to_dict(self) -> dict:
        result: dict = {}
        result["RateKey"] = from_union([from_str, from_none], self.RateKey)
        return result


class HotelPriceCheckRQ:
    RateInfoRef: Optional[RateInfoRef]

    def __init__(self, RateInfoRef: Optional[RateInfoRef]) -> None:
        self.RateInfoRef = RateInfoRef

    @staticmethod
    def from_dict(obj: Any) -> 'HotelPriceCheckRQ':
        assert isinstance(obj, dict)
        RateInfoRef = from_union([RateInfoRef.from_dict, from_none], obj.get("RateInfoRef"))
        return HotelPriceCheckRQ(RateInfoRef)

    def to_dict(self) -> dict:
        result: dict = {}
        result["RateInfoRef"] = from_union([lambda x: to_class(RateInfoRef, x), from_none], self.RateInfoRef)
        return result


class Welcome:
    HotelPriceCheckRQ: Optional[HotelPriceCheckRQ]

    def __init__(self, HotelPriceCheckRQ: Optional[HotelPriceCheckRQ]) -> None:
        self.HotelPriceCheckRQ = HotelPriceCheckRQ

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        HotelPriceCheckRQ = from_union([HotelPriceCheckRQ.from_dict, from_none], obj.get("HotelPriceCheckRQ"))
        return Welcome(HotelPriceCheckRQ)

    def to_dict(self) -> dict:
        result: dict = {}
        result["HotelPriceCheckRQ"] = from_union([lambda x: to_class(HotelPriceCheckRQ, x), from_none], self.HotelPriceCheckRQ)
        return result


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)

 
def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)

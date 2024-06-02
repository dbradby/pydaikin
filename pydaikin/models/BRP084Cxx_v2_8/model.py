from typing import List, Optional, Union

from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_DOWN

import re

class Md(BaseModel):
    pt: str
    st: Optional[int] = None
    mi: Optional[str] = None
    mx: Optional[str] = None


class ItemWithValue(BaseModel):
    pn: str
    pt: int
    pv: Optional[int | str] = None
    md: Md

    def getInt(self) -> int:
        return ItemWithValue._decode_pv_to_int(self.pv, self.md)
    
    # decode functions from https://github.com/lltcggie/py-dsapi
    # MIT Licence https://github.com/lltcggie/py-dsapi/blob/main/LICENSE
    @staticmethod
    def _decode_pv_to_int(pv, md) -> int:
        dec = ItemWithValue._decode_pv(pv, md)
        quantize = dec.quantize(Decimal('1.'),  rounding = ROUND_DOWN)
        return int(quantize)

    @staticmethod
    def _decode_pv(pv, md) -> Decimal:
        st = md.st
        str = ItemWithValue._convert_endian(pv)
        base = Decimal(int(str, 16))
        step = ItemWithValue._decode_step_value(st)
        if step == Decimal(0):
            return base
        mul = base * step
        return mul

    @staticmethod
    def _convert_endian(value) -> str:
        list = re.split('(..)', value)[1::2]
        list.reverse()
        return ''.join(list)

    @staticmethod
    def _decode_step_value(step) -> Decimal:
        if 0 > step or step > 255:
            raise ValueError(step)
        base = Decimal(step & 0x0F)
        step_value_coefficient = ItemWithValue._get_step_value_coefficient((step & 0xF0) >> 4)
        return base * step_value_coefficient

    @staticmethod
    def _get_step_value_coefficient(i) -> Decimal:
        if i == 0:
            return Decimal('1.0')
        elif i == 1:
            return Decimal('10.0')
        elif i == 2:
            return Decimal('100.0')
        elif i == 3:
            return Decimal('1000.0')
        elif i == 4:
            return Decimal('1.0E4')
        elif i == 5:
            return Decimal('1.0E5')
        elif i == 6:
            return Decimal('1.0E6')
        elif i == 7:
            return Decimal('1.0E7')
        elif i == 8:
            return Decimal('1.0E-8')
        elif i == 9:
            return Decimal('1.0E-7')
        elif i == 10:
            return Decimal('1.0E-6')
        elif i == 11:
            return Decimal('1.0E-5')
        elif i == 12:
            return Decimal('1.0E-4')
        elif i == 13:
            return Decimal('0.001')
        elif i == 14:
            return Decimal('0.01')
        elif i == 15:
            return Decimal('0.1')
        raise ValueError(i)

class Pc(BaseModel):
    pn: str
    pt: int
    pch: List[Union["Pc", ItemWithValue]] = Field()

    def getPc(self, str) -> "Pc":
        return list(filter(lambda pc: pc.pn == str, self.pch))[0]

    def getItem(self, str) -> ItemWithValue:
        return list(filter(lambda pc: pc.pn == str, self.pch))[0]

class Response(BaseModel):
    fr: str
    pc: Pc
    rsc: int

class BRP084cxxV28Response(BaseModel):
    responses: List[Response]

    def getAdr(self, str) -> Response:
        full_key = f'/dsiot/edge/{str}.dgc_status'
        return list(filter(lambda resp: resp.fr == full_key, self.responses))[0]

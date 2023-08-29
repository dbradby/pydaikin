import unittest

from pydaikin.models.base import CommonBasicInfo


class TestCommonBasicInfo(unittest.TestCase):
    fixtures = [
        {
            "msg": "brp069",
            "_response": "ret=OK,type=aircon,reg=eu,dst=1,ver=1_2_54,rev=203DE8C,pow=1,err=0,location=0,name=%4e%6f%74%74%65,icon=3,method=home only,port=30050,id=,pw=,lpw_flag=0,adp_kind=3,pv=3.20,cpv=3,cpv_minor=20,led=1,en_setzone=1,mac=409F38D107AC,adp_mode=run,en_hol=0,ssid1=Pinguino Curioso,radio1=-35,grp_name=,en_grp=0",
        }
    ]

    def test_base_parse(self):
        for data in self.fixtures:
            with self.subTest(**data):
                model = CommonBasicInfo(_response=data['_response'])
                self.assertEqual(model.ret, "OK")

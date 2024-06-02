import json
import os
import unittest

from pydaikin.models.BRP084Cxx_v2_8.model import BRP084cxxV28Response, ItemWithValue, Pc


class TestParser(unittest.IsolatedAsyncioTestCase):
    def test_parse(self):
        with open(os.path.dirname(__file__) + "/fixtures/first_discovery.json", "r") as infile:
            responsedata = json.load(infile)

        response = BRP084cxxV28Response.model_validate(responsedata)
        assert response

    def test_elements(self):
        with open(os.path.dirname(__file__) + "/fixtures/adr100-adr200.json", "r") as infile:
            responsedata = json.load(infile)
        
        response = BRP084cxxV28Response.model_validate(responsedata)

        # Power (off = 0, on = 1)
        self.assertEqual(response.getAdr("adr_0100")
              .pc.getPc("e_1002")
              .getPc("e_A002")
              .getItem("p_01").getInt(), 0)       

        # room temp
        self.assertEqual(response.getAdr("adr_0100")
              .pc.getPc("e_1002")
              .getPc("e_A00B")
              .getItem("p_01").getInt(), 17)

        # humidity
        self.assertEqual(response.getAdr("adr_0100")
              .pc.getPc("e_1002")
              .getPc("e_A00B")
              .getItem("p_02").getInt(), 55)
        
        # outdoor temp 
        self.assertEqual(response.getAdr("adr_0200")
              .pc.getPc("e_1003")
              .getPc("e_A00D")
              .getItem("p_01").getInt(), 11)
        
        # Operation Mode
        # fan = 0
        # heating = 1
        # cooling = 2
        # auto = 3
        # dehumidify = 5
        # humidify = 8
        self.assertEqual(response.getAdr("adr_0100")
                .pc.getPc("e_1002")
                .getPc("e_3001")
                .getItem("p_01").getInt(), 1)
         
        # cooling target temp
        self.assertEqual(response.getAdr("adr_0100")
                .pc.getPc("e_1002")
                .getPc("e_3001")
                .getItem("p_02").getInt(), 25)

        # heating target temp
        self.assertEqual(response.getAdr("adr_0100")
              .pc.getPc("e_1002")
              .getPc("e_3001")
              .getItem("p_03").getInt(), 20) 

    def test_small(self):
        responsedata = {
            "pn": "timz",
            "pt": 1,
            "pch": [
                {
                    "pn": "tmdf",
                    "pt": 2,
                    "pv": 600,
                    "md": {
                        "pt": "i"
                    }
                },
                {
                    "pn": "dst",
                    "pt": 2,
                    "pv": 1,
                    "md": {
                        "pt": "i"
                    }
                },
                {
                    "pn": "zone",
                    "pt": 2,
                    "pv": 234,
                    "md": {
                        "pt": "i"
                    }
                }
            ]
        }

        response = Pc.model_validate(responsedata)
        assert response

    def test_item_with_value(self):
        responsedata = {
            "pn": "tmdf",
            "pt": 2,
            "pv": 600,
            "md": {
                "pt": "i"
            }
        }

        response = ItemWithValue.model_validate(responsedata)
        assert response

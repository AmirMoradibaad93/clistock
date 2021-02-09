import unittest
import pandas as pd
import requests
import funcmodule

class TestFuncmodule(unittest.TestCase):	
	def test_get_anagraphic_data(self):
		data = funcmodule.get_anagraphic_data()
		self.assertEqual(data.iloc[0]['symbol'],'AAPL')
	
	def test_get_historical_data(self):
		anag = funcmodule.get_anagraphic_data()
		stock = funcmodule.get_historical_data(anag)
		for i in stock:
			self.assertEqual(i.iloc[0]['symbol'],'AAPL')
		
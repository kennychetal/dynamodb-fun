import unittest
import requests

class TestRetrieveMethods(unittest.TestCase):

  def test_not_found_id(self):
      response = requests.get(url="http://localhost:8080/retrieve?id=9999")
      self.assertEqual("{u'errors': {u'not_found': {u'status': 404, u'id': u'9999'}}}", str(response.json()))

  def test_not_found_name(self):
      response = requests.get(url="http://localhost:8080/retrieve?name=homer")
      self.assertEqual("{u'errors': {u'not_found': {u'status': 404, u'name': u'homer'}}}", str(response.json()))
  
  def test_both_id_and_name(self):
      response = requests.get(url="http://localhost:8080/retrieve?name=lullaby&id=9212")
      self.assertEqual("{u'errors': {u'not_supported': {u'status': 404, u'id': u'9212', u'name': u'lullaby'}}}", str(response.json()))
      
  #Found ID depends on whats in the db, so this test wont pass on systems with different data in dynamodb, by default testing with dummy
  def test_found_id(self):
      response = requests.get(url="http://localhost:8080/retrieve?id=3")
      self.assertEqual("{u'data': {u'activities': [u'activity one'], u'type': u'person', u'id': u'3', u'name': u'dummy'}}", str(response.json()))
  #Found Name depends on whats in the db, so this test wont pass on systems with different data in dynamodb, by default testing with dummy
  def test_found_name(self):
      response = requests.get(url="http://localhost:8080/retrieve?name=dummy")
      self.assertEqual("{u'data': {u'activities': [u'activity one'], u'type': u'person', u'id': u'3', u'name': u'dummy'}}", str(response.json()))


if __name__ == '__main__':
    unittest.main()
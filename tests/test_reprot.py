from facedetection.save_reprot import save_report
import re

def test_authorized_access_report():
    save_report('Mahmoud dinah')
    with open('./report.csv', 'r',encoding="utf-8") as file:
      new= file.read()
      search = re.findall('Mahmoud dinah,Drowsy', new)
      print(search)
    actual = search
    expected = 'Mahmoud dinah,Drowsy'
    assert expected == actual[-1]


def test_Unauthorized_access_report():
    save_report()
    with open('./report.csv', 'r',encoding="utf-8") as file:
      new= file.read()
      search = re.findall('unknown person,unuthorized access', new)
      print(search)
    actual = search
    expected = 'unknown person,unuthorized access'
    assert expected == actual[-1]






import requests, LoginInfo, json, time
from lxml import html

session = ""
cookiedict = ""
workingtoken = 'XgeJ9Ye9DYF6TUvrkShE9E1g9oKeaO9sypCUK1nDSJx8ME_wQ0So0fhE6VnHP_UsmJgy3E4JEceyAF-fy2aE8OXtEYo1'
workingtoken = 'hEMwm_NQi1KC14WVoC3UW21OoQbrSsAnmJSQFAj3pcun_BldP7YkmR_hdYZs5Q4pDFLHgApkDyO7koUA2BwfZ5oEI3s1'
workingtoken = 'u_ca2irAnBcxWx_1lh0sibYlUSWKEvRTGxpUoNh5BlavkPNex2Nw_Cqj4B2bXUmRIKoBulqTxx1FphmRhFt0pJq3whk1'
workingtoken = 'Na3Gs3KAdVx9S-522abYZlSws3esEEeGyptiGS7FeVKt3hVbtMAw29o8kX6ImS5jr4HVxyNdG6v_iZXhjqVVVmNruUk1'

def logIn():
  global session, cookiedict
  payload = { 
      "UserName": LoginInfo.email,
      "Password": LoginInfo.password,
      "RememberMe": "true",
      "btnsumit": "Sign in",
  }
  login_url = "https://www.plusportals.com/" + LoginInfo.school
  login_session = session.post(login_url, data=payload)
  cookiedict = session.cookies.get_dict()
def post():
  global session
  cookieformat = f'__RequestVerificationToken=3q2ARngt_LGisQdBB2EPNTxGnLvx-R6HSuIhfnzeFFAVP75t9Fvo3ISWeGM-TWOQunPoOAHp0bSNc11x1jte8CdUTCM1; _pps=-420; _ga=GA1.2.1678962814.1647487330; ppschoollink={LoginInfo.school}; _gid=GA1.2.1756563048.1650167720; emailoption={cookiedict["emailoption"]}; ASP.NET_SessionId={cookiedict["ASP.NET_SessionId"]}; UGUID={cookiedict["UGUID"]}; .ASPXAUTH={cookiedict[".ASPXAUTH"]}; UserSessionId={cookiedict["UserSessionId"]}; ppschoollink={LoginInfo.school}; ppusername={LoginInfo.email}' #
  payload2 = {
    "sort": "",
    "page": 1,
    "pageSize": 20,
    "group": "", 
    "filter": "", 
    "studentId": LoginInfo.student_id,
    "sectionId": 0,
    "courseworkRange": 1,
    "courseworkType": "All Types"
  }
  headers = {
    'authority': 'www.plusportals.com',
  '__requestverificationtoken': workingtoken,
  'accept': 'application/json, text/javascript, */*; q=0.01',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': cookieformat,
  'origin': 'https://www.plusportals.com',
  'referer': 'https://www.plusportals.com/ParentStudentDetails/ParentStudentDetails/17427',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
  'x-newrelic-id': 'XQEDUV5SGwUDXFhXBQc=',
  'x-requested-with': 'XMLHttpRequest'
  }
  coursework_url = "https://www.plusportals.com/ParentStudentDetails/GetCourseworkDetailsByStudent"
  response = session.post(coursework_url, data=payload2, headers=headers)
  return response
def workRequest():
  global session, cookiedict
  session = requests.Session()
  logIn()
  response = post()
  try:
    js = response.json() #response is not in .json format, so response failed 
    print("Success in requesting coursework details!")
    print("At " + time.strftime('%I:%M:%S %p %Z on %b %d, %Y'))
  except:
    print("Error in requesting coursework details!")
    print("At " + time.strftime('%I:%M:%S %p %Z on %b %d, %Y'))
  return response

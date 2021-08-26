import requests
from requests.exceptions import ConnectionError
import json
class Dingtalk_client():
    def __init__(self):
        self.app_key = 'dingn4n98leoon5ri0fm'
        self.app_secret = 'BxbJhDInNqKatP6jLHPaFPeMSBVnugszzU6PDFgQ_zSw1MdQqpaq5s_jNJj2B6W4'
        self.get_token_url = 'https://oapi.dingtalk.com/gettoken'
        self.calendar_url = 'https://oapi.dingtalk.com/topapi/calendar/v2/event/create?access_token={access_token}'
       # "attendees": [{"userid": "manager4270"}],
        self.event  = {
           "attendees":[],
           "calendar_id": "primary",
           "description": "This is a description",
           "end": {"timestamp": 1597737999, "timezone": "Asia/Shanghai"},
           "location": {
               "latitude": "30.285228",
               "longitude": "120.017022",
               "place": "futurepark"
           },
          # "notification_type": "notification",
            "notification_type": "NONE",
           "organizer": {"userid": "manager4270"},
           "reminder": {"method": "app", "minutes": 0},
           "start": {"timestamp": 1597653888, "timezone": "Asia/Shanghai"},
           "summary": "test summary"
        }
    def get_token(self):
        while True:
            try:
                response = requests.get(self.get_token_url, params={'appkey':self.app_key, 'appsecret':self.app_secret})
                response_json = json.loads(response.text)
                if response_json['errcode'] == 0:
                    print('get access_token:{access_token}'.format(access_token=response_json['access_token']))
                    return response_json['access_token']
                else:
                    print("Request Error, error code:{error_code}".format(error_code=response_json['errcode']))
                    return None
                break
            except ConnectionError as e:
                print('get token connection error')
                print(e)
    def set_calendar(self, addendees, summary, location, description, start_end_time):
        access_token = self.get_token()
        if  access_token  is not None:
            self.event['attendees']  = list([{ "userid":i } for i in addendees])
            self.event['description'] = description
            self.event['summary'] = summary
            self.event['location']['place'] = location
            self.event['end']['timestamp'] = start_end_time
            self.event['start']['timestamp'] = start_end_time
            form_data = {
                "event": str(self.event), 
            }

            while True:
                try:
                    response = requests.get(self.calendar_url.format(access_token=access_token), form_data) 
                    print(response.text)
                    break
                except ConnectionError as e:
                    print("set calendar connection error")
                    print(e)
        else:
            print("can't get  access token")


if __name__ == '__main__':
    dingtk = Dingtalk_client()
    addendees = ['manager4270', '2246335848-1500630749']
    summary = '80a43f8be6992e13\n  甲基安非他明/吗啡/氯胺酮\n  ABC-ZTF001 \n   阴性/阴性/阴性 '
    location = '陕西省榆林市靖边县南关东街靠近靖边县公务员'
    description = 'C值: 6877 T1值: 11680 T2值:9303 T3值:9690'
    img_url = 'http://58.87.111.39/img/19827.jpg'
    start_end_time = "1597898197"
    description =description+'\n'+img_url
    addendees = ['manager4270']
    dingtk.set_calendar(addendees, summary, location, description, start_end_time)

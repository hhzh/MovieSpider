import hashlib
import json


def md5(s):
    m = hashlib.md5(s.encode("utf8"))
    return m.hexdigest()


appkey = '597aaa8c45297d254a000147'
app_master_secret = 'sqkmkiib7evegs9qu63qyw6z17gvmqek'
method = 'POST'
url = 'http://msg.umeng.com/api/send'
# params = '{"appkey":"597aaa8c45297d254a000147","timestamp":"1523354746553","type":"broadcast","payload":{"display_type":"notification","body":{"ticker":"xddddd","title":"xxxdddd","text":"xxxddd","play_vibrate":true,"play_lights":true,"play_sound":true,"after_open":"go_app"}},"policy":{"start_time":"2018-04-10 18:40:00"},"production_mode":true,"description":"xxxxdd"}'
timestamp = '1523437501216'
method = 'POST'
url = 'http://msg.umeng.com/api/send'
params = {'appkey': appkey,
          'timestamp': timestamp,
          'type': 'broadcast',
          'production_mode': False,
          'payload': {'body': {'ticker': 'Hello World字符',
                               'title': '文章中文',
                               'text': 'ccccccc中文',
                               'after_open': 'go_app'},
                      'display_type': 'notification'
                      }
          }
post_body = json.dumps(params)
print(post_body)
sign = md5('%s%s%s%s' % (method, url, post_body, app_master_secret))
print(sign)
# print(md5("中文字幕到底到"))

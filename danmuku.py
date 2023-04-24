from utils import prohibition_check
from bilibili_api import live, sync

ROOM_ID = 21013446
MSG_INFO = {'timestamp' : 0, 'uid' : 0, 'nickname' : '', 'message' : ''}
PROHIBITION_LIST = []

try:
    with open('prohibitions.txt', 'r', encoding="UTF-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            PROHIBITION_LIST.append((line.strip('\n')))
except FileNotFoundError:
    print('Prohibitions File Not Exists Yet.')


room = live.LiveDanmaku(ROOM_ID)

@room.on('DANMU_MSG')
async def on_danmaku(event: dict, offenceCheck: bool = True):
    # 收到弹幕
    global MSG_INFO
    MSG_INFO['timestamp'] = event['data']['info'][9]['ts']
    MSG_INFO['uid'] = event['data']['info'][2][0]
    MSG_INFO['nickname'] = event['data']['info'][2][1]
    danmaku = event['data']['info'][1]

    message = '{0} : {1}'.format(MSG_INFO['nickname'], danmaku)

    if (offenceCheck) and (len(PROHIBITION_LIST) > 0):
        if prohibition_check(danmaku, PROHIBITION_LIST, **MSG_INFO):
            message = '▲' + message

    print(message)

@room.on('SUPER_CHAT_MESSAGE')
async def on_sc(event: dict, offenceCheck: bool = True):
    # 收到SC
    global MSG_INFO
    MSG_INFO['timestamp'] = event['data']['data']['ts']
    MSG_INFO['uid'] = event['data']['data']['uid']
    MSG_INFO['nickname'] = event['data']['data']['user_info']['uname']
    superchat = event['data']['data']['message']

    message = 'SC : {0} : {1}'.format(MSG_INFO['nickname'], superchat)

    if (offenceCheck) and (len(PROHIBITION_LIST) > 0):
        if prohibition_check(superchat, PROHIBITION_LIST, **MSG_INFO):
            message = '▲' + message
            
    print(message)

sync(room.connect())

import re
import time


def ts2str(timestamp: int, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    timeArray = time.localtime(timestamp)
    StyleTime = time.strftime(format, timeArray)
    return StyleTime

def prohibition_check(strToBeCheck: str, prohibitionList: list, **kwargs) -> bool:

    for prohibition in prohibitionList:
        if re.search(prohibition, strToBeCheck) :
            with open('probab_offenders.log', mode='a', encoding='UTF-8') as f:
                f.write('{0} : {1} : {2} : {3}\n'.format(ts2str(kwargs['timestamp']), str(kwargs['uid']), kwargs['nickname'], strToBeCheck))
            return True
    return False

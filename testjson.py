import json

LedCtrl1 = {'R':80, 'G':80, 'B':40}
print LedCtrl1['R']
LedCtrl2 = {'R':80, 'G':40, 'B':40}
LedCtrl3 = {'R':20, 'G':80, 'B':40}
LedCtrl4 = {'R':30, 'G':80, 'B':40}
LedCtrl = {"LedCtrl":[LedCtrl1,LedCtrl2, LedCtrl3, LedCtrl4]}
print LedCtrl
data_json = json.dumps(LedCtrl)
print data_json
data_str = json.loads(data_json)
print len(data_str["LedCtrl"])
print data_str["LedCtrl"][0]['R']
print data_str["LedCtrl"][1]['R']
print data_str["LedCtrl"][2]['R']
print data_str["LedCtrl"][3]['R']
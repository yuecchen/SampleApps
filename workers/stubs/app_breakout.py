#!/usr/bin/env python3
app_info='"limits":{"fds":16384,"mem":512,"disk":1024},"application_name":"WinkPatTry","application_uris":["winkpattry.stage1.mybluemix.net"],"name":"WinkPatTry","space_name":"dev","space_id":"21ee0aba-918c-408b-b7a2-5639c2b6f5dd","uris":["winkpattry.stage1.mybluemix.net"],"users":null,"version":"26da2ea9-f922-4993-b0a8-b53a86e3b23b","application_version":"26da2ea9-f922-4993-b0a8-b53a86e3b23b","application_id":"af164696-f8c5-457d-8f81-dd61f2645e13","instance_id":"c2bcb11fa49a4935a296c812aa27f8a3","instance_index":0,"host":"0.0.0.0","port":64602,"started_at":"2016-07-10 16:53:00 +0000","started_at_timestamp":1468169580,"start":"2016-07-10 16:53:00 +0000","state_timestamp":1468169580}'

start = '"mem":'
end = ','
print((app_info.split(start))[1].split(end)[0])

start = '"disk":'
end = '},'
print((app_info.split(start))[1].split(end)[0])

start = '"application_name":"'
end = '",'
print((app_info.split(start))[1].split(end)[0])

start = '"application_uris":["'
end = '"],'
print((app_info.split(start))[1].split(end)[0])

start = '"application_version":"'
end = '",'
print((app_info.split(start))[1].split(end)[0])

start = '"application_id":"'
end = '",'
print((app_info.split(start))[1].split(end)[0])

start = '"instance_id":"'
end = '",'
print((app_info.split(start))[1].split(end)[0])

start = '"instance_index":'
end = ','
print((app_info.split(start))[1].split(end)[0])

start = '"host":"'
end = '",'
print((app_info.split(start))[1].split(end)[0])

start = '"port":'
end = ','
print((app_info.split(start))[1].split(end)[0])

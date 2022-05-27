import requests

BASE = "http://127.0.0.1:5000/"

data = [
     {"name": "Wien Hbf", "address": "Am Hbf 1, 1100 Wien"},
     {"name": "St. Pölten Hbf", "address": "Bahnhofplatz 1, 3100 St. Pölten"},
     {"name": "Linz Hbf", "address": "Bahnhofplatz 3-6, 4020 Linz"}
]

section_data = [
    {"start": "Wien Hbf", "end": "Graz Hbf", "track": "normal", "fee": 10, "time": 100,
     "warnings": "Maintenance work on sections [St. Pölten Hbf - Linz Hbf] between March 2022 and June 2022"},
    {"start": "Wien Hbf", "end": "Linz Hbf", "track": "normal", "fee": 15, "time": 150},
    {"start": "Linz Hbf", "end": "Sbg Hbf", "track": "normal", "fee": 8, "time": 80},
    {"start": "Wien Hbf", "end": "St. Pölten Hbf", "track": "normal", "fee": 6, "time": 60},
    {"start": "St. Pölten Hbf", "end": "Linz Hbf", "track": "normal", "fee": 10, "time": 10}
]

route_data = [
    {"name": "Weststrecke", "start": "Wien Hbf", "end": "Sbg Hbf"}

]

warning_data = [
    {"warnings": "Maintenance work on sections [St. Pölten Hbf - Linz Hbf] between March 2022 and June 2022",
     "warnings": "Maintenance work on sections [...] between March 2022 and June 2022"}
]

# ------Trainstation_testing-----#
input()
for i in range(len(data)):
    response = requests.put(BASE + "trainstation/" + str(i), data[i])
    print(response.json())
input()
response = requests.patch(BASE + "trainstation/2", {"address": "213123back to old address"})
print(response.json())
input()
response = requests.get(BASE + "trainstation/2")
print(response.json())

input()
#response = requests.delete(BASE + "trainstation/2")
#print(response)
#input()

#response = requests.get(BASE + "trainstation/2")
#print(response.json())

# ------Section_testing-----#
for j in range(len(section_data)):
    response = requests.put(BASE + "section/" + str(j), section_data[j])
    print(response.json())
input()
response = requests.patch(BASE + "section/2", {"track": "new track for 2 id = special"})
print(response.json())
input()
response = requests.get(BASE + "section/2")
print(response.json())

# ------Route_testing-----#
#for k in range(len(route_data)):
#    response = requests.put(BASE + "route/" + str(k), route_data[k])
#    print(response.json())
#input()
#response = requests.patch(BASE + "route/0", {"warnings": "NEW Warnings to Route ID 0"})
#print(response.json())
#input()
#response = requests.get(BASE + "route/0")
#print(response.json())

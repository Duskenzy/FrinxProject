import psycopg2
import json

with open('configClear_v2.json', 'r') as json_file:
    user_data = json.load(json_file)

def sortData(e):
    return e['name']

gig_Lop_Port_Ten = user_data["frinx-uniconfig-topology:configuration"]["ietf-interfaces:interfaces"]["interface"]
bdi = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["BDI"]
gig_Lop_Port_Ten.sort(key=sortData)
bdi.sort(key=sortData)
allTogether = gig_Lop_Port_Ten + bdi


def createTable():
    conn=psycopg2.connect("dbname='FrinxProject' user='postgres' password='postgres123' host='localhost' port='5433'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS configuration (id SERIAL PRIMARY KEY, connection INTEGER, name VARCHAR(255) NOT NULL, "
                "description VARCHAR(255),config json, type VARCHAR(50), infra_type VARCHAR(50), port_channel_id INTEGER, max_frame_size INTEGER)")
    conn.commit()
    conn.close()

def insert(id, connection, name, description, config, type, infra_type, port_channel_id, max_frame_size):
    conn = psycopg2.connect("dbname='FrinxProject' user='postgres' password='postgres123' host='localhost' port='5433'")
    cur = conn.cursor()
    cur.execute("INSERT INTO configuration VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id, connection, name, description, config, type, infra_type, port_channel_id, max_frame_size))
    conn.commit()
    conn.close()

def modifyDataForInsertion():
    id = 0
    for i in allTogether:
        id += 1
        nam = i['name']
        confi = json.dumps(i)
        try:
            descr = i['description']
        except:
            descr = "[null]"

        try:
            typ = i['type']
        except:
            typ = "[null]"
        insert(id, 0, nam, descr, confi, typ, 0, 0, 0)

createTable()
modifyDataForInsertion()

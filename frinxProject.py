import psycopg2
import json

with open('configClear_v2.json', 'r') as json_file:
    user_data = json.load(json_file)

tenGigaEth = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["TenGigabitEthernet"]
tenGigaEth1 = user_data["frinx-uniconfig-topology:configuration"]["ietf-interfaces:interfaces"]["interface"]
gigaEth = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["GigabitEthernet"]
portChannel = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["Port-channel"]
loopback = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["Loopback"]
bdi = user_data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]["BDI"]

def create_table():
    conn=psycopg2.connect("dbname='testdb' user='postgres' password='postgres123' host='localhost' port='5433'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS configuration (id SERIAL PRIMARY KEY, connection INTEGER, name VARCHAR(255) NOT NULL, "
                "description VARCHAR(255),config json, type VARCHAR(50), infra_type VARCHAR(50), port_channel_id INTEGER, max_frame_size INTEGER)")
    conn.commit()
    conn.close()

def insert(connection, name, description, config, type, infra_type, port_channel_id, max_frame_size):
    conn = psycopg2.connect("dbname='testdb' user='postgres' password='postgres123' host='localhost' port='5433'")
    cur = conn.cursor()
    cur.execute("INSERT INTO configuration VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s)",
                (connection, name, description, config, type, infra_type, port_channel_id, max_frame_size))
    conn.commit()
    conn.close()

def myFunc(e):
    return e['name']

def mergeDict(second, first):
    return(first.update(second))

def modifyDataForInsertion():
    for i in allTogether:
        connect,typ,infra = None, None, None
        nam = i['name']
        try:
            descr = i['description']
        except:
            descr = None

        confi = json.dumps(i)
        try:
            port_id = i['id']
        except:
            port_id = None

        try:
            mtu = i['mtu']
        except:
            mtu = None

        insert(connect, nam, descr, confi, typ, infra, port_id, mtu)

a, b = tenGigaEth[0], tenGigaEth1[6]
c, d = tenGigaEth[1], tenGigaEth1[7]
e, f = tenGigaEth[2], tenGigaEth1[8]
g, h = tenGigaEth[3], tenGigaEth1[9]
i, j = tenGigaEth1[0], gigaEth[0]
k, l = tenGigaEth1[1], gigaEth[1]
m, n = tenGigaEth1[2], gigaEth[2]
q, r = tenGigaEth1[4], portChannel[0]
s, t = tenGigaEth1[5], portChannel[1]

mergeDict(b,a)
mergeDict(d,c)
mergeDict(f,e)
mergeDict(h,g)
mergeDict(i,j)
mergeDict(k,l)
mergeDict(m,n)
mergeDict(q,r)
mergeDict(s,t)

l = [a, c, e, g, j, k, m, tenGigaEth1[3], q, s]

allTogether = l + bdi
allTogether.sort(key=myFunc)

create_table()
modifyDataForInsertion()


from  pyhive import hive

conn = hive.Connection(host='localhost', port=8888,username='lmurdock',database='ss',auth_mechanism='PLAIN',
                        configuration={'mapred.job.queue.name':'adhoc}'})
cur = conn.cursor()
cur.execute("select * from ss.data")
for message in cur.fetch_logs() :
    print(message)

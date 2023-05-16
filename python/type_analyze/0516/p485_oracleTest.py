import cx_Oracle
import pandas as pd

# cx_Oracle.init_oracle_client(lib_dir="C:/oracleXE/instantclient_19_19")
cx_Oracle.init_oracle_client(lib_dir="/usr/local/OracleXE/instantclient_19_19")

import matplotlib.pyplot as plt
from pandas import Series

plt.rc('font', family='AppleGothic')

conn=None #접속객체
cur=None #커서 객체

try:
    loginfo ='hr/1234@192.168.1.137:1521/xe'
    conn=cx_Oracle.connect(loginfo)
    cur=conn.cursor()

    # sql = 'select power(2,10) from dual'
    sql='select * from three_country'
    cur.execute(sql)

    name =[]
    year =[]
    frequency=[]

    for result in cur:
        name.append(result[0])
        year.append(result[1])
        frequency.append(result[2])

    myseries = Series(frequency, index=[name, year])
    print(myseries)

    for idx in range(0,2):
        myframe = myseries.unstack(idx)
        print(myframe)
        myframe.plot(kind='barh', rot=0)
        plt.title('3개국 태러 발생 현황')

        filename = 'oracleChart02_2' + str(idx + 1) + '.png'
        plt.savefig(filename, dpi=400, bbox_inches='tight')
        print(filename + 'file saved...')

        plt.show()

except Exception as err:
    print(err)

finally:
    if cur !=None:
        cur.close()

    if conn != None:
        conn.close()

print('finished')
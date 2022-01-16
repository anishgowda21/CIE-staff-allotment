import pymysql.cursors
import ast
from random import choice
from datetime import datetime,timedelta
import traceback
import math
from collections import defaultdict
conn = pymysql.connect(host='localhost',user='root',password='mysql',database='DBS')


    # Create a dictionary to store the allotment list
allot_list = defaultdict(list)
assign_list = defaultdict(str)


def max_duties_for_faculty(sem_type):
    # calulate total duties required for a particular semester
    cur = conn.cursor()
    q1 = f"SELECT sum(total_duties) FROM {sem_type}_sem_info;"
    q2 = f"SELECT COUNT(*) FROM faculty;"
    cur.execute(q1)
    total_duties = cur.fetchall()[0][0]
    cur.execute(q2)
    total_fac = cur.fetchall()[0][0]
    max_duties = math.ceil(total_duties/total_fac)
    cur.close()
    return max_duties


def clear_tables_formate():
     # Clear the previous allotment list and set duties_assigned in faculty table to 0
    q1 = f"UPDATE faculty SET duties_assigned = 0"
    q2 =  f"DELETE FROM fin"
    with conn.cursor() as cur:
        cur.execute(q1)
        cur.execute(q2)
        conn.commit()
    

def allocation(room,sub_id,name,date,time,max_duties):
    # Get all the faculties from faculty table
    cur = conn.cursor()
    q1 = f"SELECT faculty_id FROM faculty"
    cur.execute(q1)
    fac_ids = cur.fetchall()
    cur.close()

    print("Inside allocation")
    print("max_duties",max_duties)

    while True:
        # Get a random faculty from the list who has less then 2 duties assigned on the same day
        rand_id = choice([i[0] for i in fac_ids if i[0] not in allot_list[date]])

        # Check if the faculty has less than max_duties duties assigned
        if assign_list[rand_id] < max_duties:
            with conn.cursor() as cur:
                q1 = f"SELECT * FROM fin where date='{date}' and fac_id='{rand_id}'"
                cur.execute(q1)
                rows = cur.fetchall()

                # If there is no duties allocated on the same day for the faculty
                if not rows:
                    q1 = f"INSERT INTO fin (sub_id,sub_name,time,date,room,fac_id) VALUES ('{sub_id}','{name}','{time}','{date}','{room}','{rand_id}')"
                    q2 = f"UPDATE faculty SET duties_assigned=duties_assigned+1 where faculty_id='{rand_id}'"
                    cur.execute(q1)
                    cur.execute(q2)
                    conn.commit()
                    assign_list[rand_id]+=1
                    print(f"inserted {rand_id} to {room} on {date} at {time}")
                    return
                
                # If there is one duty allocated on the same day for the faculty alltot anotther one based on time
                elif len(rows)==1:

                    if(time > rows[0][3]):
                        diff = time-rows[0][3]
                    else:
                        diff = rows[0][3]-time
                    
                    interval = timedelta(hours=2,minutes=0,seconds=0)
                    if(diff>=interval):
                        q1 = f"INSERT INTO fin (sub_id,sub_name,time,date,room,fac_id) VALUES ('{sub_id}','{name}','{time}','{date}','{room}','{rand_id}')"
                        q2 = f"UPDATE faculty SET duties_assigned=duties_assigned+1 where faculty_id='{rand_id}'"
                        cur.execute(q1)
                        cur.execute(q2)
                        conn.commit()
                        allot_list[date].append(rand_id)
                        assign_list[rand_id]+=1
                        print(f"inserted {rand_id} to {room} on {date} at {time}")
                        return

        

# Function to generate allotment list for a particular semester
def get_allot_list(sem_type):

    # calculate max duties for an individual faculty

    max_duties = max_duties_for_faculty(sem_type)
    # Clear the allotment list and formate some variables
    clear_tables_formate()
    print("Cleared tables")

    # Fill the assign_list dictionary with the faculty_id and the number of duties assigned
    q1 = f"select faculty_id from faculty;"
    cur = conn.cursor()
    cur.execute(q1)
    fac_ids = cur.fetchall()
    cur.close()
    for fac in fac_ids:
        assign_list[fac[0]]=0

        # Get the list of Semester in the semester type selected
    cur = conn.cursor()
    q1 = f"SELECT * FROM {sem_type}_sem_info"
    cur.execute(q1)
    sem_info = cur.fetchall()
    cur.close()

    # Get the list of subjects for the semester selected
    for sem in sem_info:
        semester = sem[0]
        cur = conn.cursor()
        q1 = f"SELECT * FROM {semester}"
        cur.execute(q1)
        sub_list = cur.fetchall()
        cur.close()

        # Iterate over the subjects and assign them to the faculty
        for sub in sub_list:
            alloted_fixed_fac = []
            ava_rooms = sem[3].split(',')
            for room in ava_rooms:
                try:
                    if sub[6]:
                        if not (len(sub[6].split(","))==len(alloted_fixed_fac)):
                            fac_id = sub[6].split(",")
                            rand_id = choice([i for i in fac_id if i not in alloted_fixed_fac])
                            q1 = f"insert into fin (sub_id,sub_name,time,date,room,fac_id) values('{sub[1]}','{sub[2]}','{sub[4]}','{sub[3]}','{room}','{rand_id}');"
                            q2 = f"update faculty set duties_assigned=duties_assigned+1 where faculty_id='{rand_id}';"
                            cur = conn.cursor()
                            cur.execute(q1)
                            cur.execute(q2)
                            conn.commit()
                            alloted_fixed_fac.append(rand_id)
                            allot_list[sub[3]].append(rand_id)
                            assign_list[rand_id]+=1
                            print(f"inserted {rand_id} to {room} on {sub[3]} at {sub[4]}")
                            continue
                    allocation(room,sub[1],sub[2],sub[3],sub[4],max_duties)
                except Exception:
                    print(traceback.format_exc())
                    return traceback.format_exc()
                

import pandas as pd
df=pd.read_csv('//192.168.6.24/Dept.Dir/CAAB - BAM/Data Analytics/Shirley/TaskScheduler/exportedtasks.csv')
df=df[['TaskName','Days','Start Date','Start Time','Author','Schedule Type','Status','Comment']]
print(df.columns)

new_df = df[df["Author"].str.contains(r'CASS\\wksio|CASS\\wqho|CASS\\ykho|CASS\\slmanalytics|CASS\\jlkor|CASS\\juanita|CASS\\lkkang|CASS\\yttan|CASS\\naomikoeh')==True]
new_df=new_df[new_df["Start Date"].notnull()]

import datetime
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead ==0:
        days_ahead=0
    elif days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

today=datetime.datetime.now()

def Convert(string):
    li = list(string.split(", "))
    return li

weekday_a=['MON','TUE',"WED","THU","FRI","SAT","SUN"]
with open('myfile.mw', 'w') as f:
    f.write('title:\n')
    f.write('key:\n -taks\n')
    for index, row in new_df.iterrows():
        f.write('group '+ row['TaskName']) 
        start_date=datetime.datetime.strptime(row['Start Date'], '%d/%m/%Y')
        today_date=today
        commands=[]
        days=str(row['Days'])
        days=Convert(days)
        start_time=(row['Start Time'][:-6] + row['Start Time'][-3:]).replace(" ","")
        if row['Schedule Type']=='Daily ':
            for i in range(1,31):
                try:
                    today_date=datetime.date(today_date.year, today_date.month,i)
                    command=today_date.strftime("%d %b %Y") +' '+start_time + ': ' + row['TaskName'] + ' #' + row['Author'][5:] + ' #' + row['Status'] + ' #'+row['Schedule Type']+ '\n'
                    f.write(command)
                    f.write(str(row['Days']) + '\n')
                    f.write(str(row['Comment']) + '\n')
                except:
                    pass
        elif row['Schedule Type']=='Weekly':
            for i in days:
                start_date=next_weekday(today_date,weekday_a.index(i))
                command= start_date.strftime("%d %b %Y") +' '+start_time +': ' + row['TaskName']+ ' #' + row['Author'][5:] + ' #' + row['Status'] + ' #'+row['Schedule Type']+ '\n'
                f.write(command)
                f.write(str(row['Days']) + '\n')
                f.write(str(row['Comment']) + '\n')
        elif row['Schedule Type']=='Monthly':
            for i in days:
                if i!= 'Second MON' and int(i) != 32:
                    try: 
                        start_date=datetime.date(today_date.year, today_date.month,int(i))
                    except:
                        pass  
                    command= start_date.strftime("%d %b %Y") +' '+start_time +': ' + row['TaskName']+ ' #' + row['Author'][5:] + ' #' + row['Status'] + ' #'+row['Schedule Type']+ '\n'
                    f.write(command)
                    f.write(str(row['Days']) + '\n')
                f.write(str(row['Comment']) + '\n')
        f.write('endGroup \n')

from git import Repo
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
PATH_OF_GIT_REPO =os.path.join(dir_path, '.git')  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'comment from python script'
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(A=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
    

git_push()

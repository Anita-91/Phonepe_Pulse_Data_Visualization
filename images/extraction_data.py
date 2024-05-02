import git
import os
import json
import pandas as pd
import pymysql


#-- 1. Data cloned from Github
repo_url = "https://github.com/PhonePe/pulse.git"
local_path = "C:/Users/phonepe_proj/phone_data"  # Specify the desired local directory path
git.Repo.clone_from(repo_url, local_path)
print("Phonepe data colned from github........")

#-- 2. Data -> CSV file:
path1 = "C:/Users/phonepe_proj/phone_data/data/aggregated/transaction/country/india/state/"
agg_trans_list = os.listdir(path1) # The os.listdir() function returns a list of all the items (directories and files) present in the specified directory.
#print(path1)

columns1 = {'State':[] , 'Year':[] , 'Quarter':[] , 'Transaction_type':[] , 'Transaction_count':[] , 'Transaction_amount':[]} #This dictionary, named columns1, will be used to collect the extracted data.
for state in agg_trans_list:
    cur_state = path1 + state + "/"        
    
    if not os.path.isdir(cur_state):
        continue
    agg_year_list = os.listdir(cur_state)
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
       
        if not os.path.isdir(cur_year):
            continue
       
        agg_file_list = os.listdir(cur_year)
        for file in agg_file_list:
            cur_file = cur_year + file 
            
            if not os.path.isfile(cur_file):
                continue
            data = open(cur_file,'r')
            A = json.load(data)
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(columns1)             
print(df_agg_trans.head(5))
df_agg_trans.shape

#-- 2. Data -> CSV file:
path1 = "C:/Users/phonepe_proj/phone_data/data/aggregated/transaction/country/india/state/"
agg_trans_list = os.listdir(path1)
columns1 = {'State':[] , 'Year':[] , 'Quarter':[] , 'Transaction_type':[] , 'Transaction_count':[] , 'Transaction_amount':[]} 
for state in agg_trans_list:
    cur_state = path1 + state + "/"        
    
    if not os.path.isdir(cur_state):
        continue
    agg_year_list = os.listdir(cur_state)
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
       
        if not os.path.isdir(cur_year):
            continue
       
        agg_file_list = os.listdir(cur_year)
        for file in agg_file_list:
            cur_file = cur_year + file 
            
            if not os.path.isfile(cur_file):
                continue
            data = open(cur_file,'r')
            A = json.load(data)
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(columns1)             
print(df_agg_trans.head(5))
df_agg_trans.shape


# - agg_user
path2 = "C:/Users/phonepe_proj/phone_data/data/aggregated/user/country/india/state/"
agg_user_list = os.listdir(path2)
columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
            'Percentage': []}
for state in agg_user_list:
    cur_state = path2 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            B = json.load(data)
            try:
                for i in B["data"]["usersByDevice"]:
                    brand_name = i["brand"]
                    counts = i["count"]
                    percents = i["percentage"]
                    columns2["Brands"].append(brand_name)
                    columns2["Count"].append(counts)
                    columns2["Percentage"].append(percents)
                    columns2["State"].append(state)
                    columns2["year"].append(year)
                    columns2["Quarter"].append(int(file.strip('.json')))
            except:
                pass
df_agg_user = pd.DataFrame(columns2)
print(df_agg_user.head(5))
df_agg_user.shape


#--- map_trans
path3 = "C:/Users/phonepe_proj/phone_data/data/map/transaction/hover/country/india/state/"
map_trans_list = os.listdir(path3)
columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
            'Amount': []}

for state in map_trans_list:
    cur_state = path3 + state + "/"
    map_year_list = os.listdir(cur_state)
    for year in map_year_list:
        cur_year = cur_state + year + "/"
        map_file_list = os.listdir(cur_year)
        for file in map_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            C = json.load(data)
            for i in C["data"]["hoverDataList"]:
                district = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                columns3["District"].append(district)
                columns3["Count"].append(count)
                columns3["Amount"].append(amount)
                columns3['State'].append(state)
                columns3['Year'].append(year)
                columns3['Quarter'].append(int(file.strip('.json')))
                
df_map_trans = pd.DataFrame(columns3)
print(df_map_trans.head(5))
df_map_trans.shape
#print(df_map_trans.isnull().sum()) 


#--map user
path4 = "C:/Users/phonepe_proj/phone_data/data/map/user/hover/country/india/state/"
map_user_list = os.listdir(path4)
columns4 = {"State": [], "Year": [], "Quarter": [], "District": [],
            "RegisteredUser": [], "AppOpens": []}

for state in map_user_list:
    cur_state = path4 + state + "/"
    map_year_list = os.listdir(cur_state)
    
    for year in map_year_list:
        cur_year = cur_state + year + "/"
        map_file_list = os.listdir(cur_year)
        
        for file in map_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            D = json.load(data)
            
            for i in D["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appOpens = i[1]['appOpens']
                columns4["District"].append(district)
                columns4["RegisteredUser"].append(registereduser)
                columns4["AppOpens"].append(appOpens)
                columns4['State'].append(state)
                columns4['Year'].append(year)
                columns4['Quarter'].append(int(file.strip('.json')))
                
df_map_user = pd.DataFrame(columns4)
print(df_map_user.head(5))
df_map_user.shape

#-- top trans
path5 = "C:/Users/phonepe_proj/phone_data/data/top/transaction/country/india/state/"
top_trans_list = os.listdir(path5)
columns5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
            'Transaction_amount': []}

for state in top_trans_list:
    cur_state = path5 + state + "/"
    top_year_list = os.listdir(cur_state)
    
    for year in top_year_list:
        cur_year = cur_state + year + "/"
        top_file_list = os.listdir(cur_year)
        
        for file in top_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            E = json.load(data)
            
            for i in E['data']['pincodes']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                columns5['Pincode'].append(name)
                columns5['Transaction_count'].append(count)
                columns5['Transaction_amount'].append(amount)
                columns5['State'].append(state)
                columns5['Year'].append(year)
                columns5['Quarter'].append(int(file.strip('.json')))
df_top_trans = pd.DataFrame(columns5)
df_top_trans.shape
print(df_top_trans.head(5))
#-- top users
path6 = "C:/Users/phonepe_proj/phone_data/data/top/user/country/india/state/"
top_user_list = os.listdir(path6)
columns6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
            'RegisteredUsers': []}
for state in top_user_list:
    cur_state = path6 + state + "/"
    top_year_list = os.listdir(cur_state)
    
    for year in top_year_list:
        cur_year = cur_state + year + "/"
        top_file_list = os.listdir(cur_year)
        
        for file in top_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            F = json.load(data)
            
            for i in F['data']['pincodes']:
                name = i['name']
                registeredUsers = i['registeredUsers']
                columns6['Pincode'].append(name)
                columns6['RegisteredUsers'].append(registeredUsers)
                columns6['State'].append(state)
                columns6['Year'].append(year)
                columns6['Quarter'].append(int(file.strip('.json')))
df_top_user = pd.DataFrame(columns6)
df_top_user.shape
print(df_top_user.head(5))
df_agg_trans.to_csv('C:/Users/phonepe_proj/csv_files/agg_trans.csv',index=False)
df_agg_user.to_csv('C:/Users//phonepe_proj/csv_files/agg_user.csv',index=False)
df_map_trans.to_csv('C:/Users//phonepe_proj/csv_files/map_trans.csv',index=False)
df_map_user.to_csv('C:/Users//phonepe_proj/csv_files/map_user.csv',index=False)
df_top_trans.to_csv('C:/Users/phonepe_proj/csv_files/top_trans.csv',index=False)
df_top_user.to_csv('C:/Users/phonepe_proj/csv_files/top_user.csv',index=False)
print("Phonepe Data --> CSV files done.......")


#-------- 3. INSERT DATA INTO MYSQL
def table_create_insert(): 
    try:
        db_conn = pymysql.connect(
            host='localhost',
            user='root',
            password='xxx')
    
        cursor_obj = db_conn.cursor()
    
        cursor_obj.execute("CREATE DATABASE IF NOT EXISTS phonepe_db")
        cursor_obj.execute("USE phonepe_db")
        
     
        cursor_obj.execute("create table agg_trans (State varchar(100), Year int, Quarter int, Transaction_type varchar(100), Transaction_count int, Transaction_amount double)")
        for i,row in df_agg_trans.iterrows():
            sql = "INSERT INTO agg_trans VALUES (%s,%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
        
            db_conn.commit()
        
        cursor_obj.execute("create table agg_user (State varchar(100), Year int, Quarter int, Brands varchar(100), Count int, Percentage double)")
        for i,row in df_agg_user.iterrows():
            sql = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
            db_conn.commit()
            
        cursor_obj.execute("create table map_trans (State varchar(100), Year int, Quarter int, District varchar(100), Count int, Amount double)")
        for i,row in df_map_trans.iterrows():
            sql = "INSERT INTO map_trans VALUES (%s,%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
            db_conn.commit()
    
        cursor_obj.execute("create table map_user (State varchar(100), Year int, Quarter int, District varchar(100), Registered_user int, App_opens int)")
        for i,row in df_map_user.iterrows():
            sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
            db_conn.commit()

        cursor_obj.execute("create table top_trans (State varchar(100), Year int, Quarter int, Pincode int, Transaction_count int, Transaction_amount double)")
        for i,row in df_top_trans.iterrows():
            sql = "INSERT INTO top_trans VALUES (%s,%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
            db_conn.commit()
            
        cursor_obj.execute("create table top_user (State varchar(100), Year int, Quarter int, Pincode int, Registered_users int)")
        for i,row in df_top_user.iterrows():
            sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
            cursor_obj.execute(sql, tuple(row))
            db_conn.commit()
                
        cursor_obj.execute("show tables")
        print(cursor_obj.fetchall())
        db_conn.close()
        
    except pymysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
    
table_create_insert()
print("INSERT DATA TO MYSQL DONE.......")


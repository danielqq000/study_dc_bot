import mysql.connector
import lib.config as config
from datetime import datetime, date

mydb = mysql.connector.connect(
    host = config.DB_HOST,
    port = config.DB_PORT,
    user = config.DB_USER,
    password = config.DB_PWD,
    database = config.DB_DATABASE
)

mycursor = mydb.cursor()

class DB_Process:
    def __init__(self):
        pass
        
    def Get_Data(show_data, table_name, others = ""):
        try:
            query = \
                f"SELECT {show_data}\n" \
                f"From {table_name}\n"\
                f"{others}"
                
            print(f"(Get_Data) query: {query}")
                
            mycursor.execute(query)
            myresult = mycursor.fetchall()
        except Exception as e:
            print(f"(Get_Data) - {repr(e)}")
        finally:
            if myresult:
                return myresult
            else:
                return False
    
    def Insert_Channel_Info(channel_id, channel_name, boost_percent = 1.0):
        try:
            insert_query = (
                f"INSERT INTO channel_boost"
                f"(channel_id, channel_name, boost_percent)"
                f"VALUES (%s, %s, %s)"
            )
            
            insert_data = (
                channel_id,
                channel_name,
                boost_percent
            )
        except Exception as e:
            print(f"(Insert_Channel_Info) {repr(e)}")
        finally:
            mycursor.execute(insert_query, insert_data)
            mydb.commit()
            print("(Insert_Channel_Info) Update User Info Successfully")
            
    def Create_Xp(self, user_id, amount, channel_id):
        try:
            flag = True
            # print(f"(Create_Xp) channel_id: {channel_id}")
            boost_percent = self.Get_Data("`boost_percent`", "`channel_boost`", f"WHERE `channel_id` = '{channel_id}'")
            # print(f"(Create_Xp) boost_percent: {boost_percent}")
            
            if boost_percent:
                insert_query = (
                    f"INSERT INTO xp_log"
                    f"(user_id, xp_add, channel_id, xp_record) "
                    f"VALUES (%(user_id)s, %(xp_add)s, %(channel_id)s, %(xp_record)s)"
                )
                
                # print(f"(Create_Xp) insert_query: {insert_query}")
                
                insert_data = {
                    'user_id': user_id,
                    'xp_add': int(amount * boost_percent[0][0]),
                    'channel_id': channel_id,
                    'xp_record': datetime.utcnow()
                }
                
                # print(f"(Create_Xp) insert_data: {insert_data}")
                
                mycursor.execute(insert_query, insert_data)
                mydb.commit()
                
            else:
                flag = False
            
        except Exception as e:
            print(f"(Create_Xp) {repr(e)}")
        finally:           
            print(f"(Create_Xp) The data has been inserted into DB")
            return flag
        
            
            
    def Create_NewMember(user_id):
        try:
            add_newuser = (
                f"INSERT INTO user_data"
                f"(user_id, user_xp, posts, reaction, joined_time, `leave`)"
                f"VALUES (%(user_id)s, %(user_xp)s, %(posts)s, %(reaction)s, %(joined_time)s, %(leave)s)"
            )
            
            data_newuser = {
                'user_id': user_id,
                'user_xp': 0,
                'posts': 0,
                'reaction': 0,
                'joined_time': datetime.utcnow(),
                'leave': False
            }
            
            mycursor.execute(add_newuser, data_newuser)
            mydb.commit()
        except Exception as e:
            print(f"(Create_NewMember) - {repr(e)}")
        # finally:
        #     mycursor.execute(add_newuser, data_newuser)
        #     mydb.commit()
            
    
    def Update_User_Info(user_id, key, value, table_name):
        try:
            update_query = \
                f"UPDATE {table_name}\n" \
                f"SET `{key}` = %s\n" \
                f"WHERE user_id = %s;"
                
            data_update = (
                value,
                user_id
            )
            
            print(f"(Update_User_Info) Query:\n{update_query}")
            print(f"(Update_User_Info) data_update: {data_update}")
            
            mycursor.execute(update_query, data_update)
            mydb.commit()
            print("(Update_User_Info) Update User Info Successfully")
            
        except Exception as e:
            print(f"(Update_User_Info) - {repr(e)}")
        # finally:
        #     mycursor.execute(update_query, data_update)
        #     mydb.commit()
        #     print("(Update_User_Info) Update User Info Successfully")
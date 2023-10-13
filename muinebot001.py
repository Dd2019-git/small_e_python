# current version: test 1
CurrentVersion = "01"
CurrentMode = "test"
# CurrentMode = "prod"
import logging
import os.path # и это для путей в файлах
# import xml.etree.ElementTree as ET # это для работы в читаемом человеком xml - не используется
import sys # для путей
import requests #это для работы http \ api \ telegram
import datetime #это для отметок времени в логах
import pickle #это для файлов https://java2blog.com/save-object-to-file-python/
import psycopg2 # это для postgre , не забываем pip install psycopg2  https://www.datacamp.com/tutorial/tutorial-postgresql-python

# Classless

# Functions
# Эта функция выпишет в бинарный файл нужный лист (массив) начиная с элемента номер F_PositionFrom
def write_2_file_if_not_exist(F_FileName, F_List, F_PositionFrom, F_comment): #функция для записи в файл
    print("Exec write_2_file_if_not_exist", F_comment)
    if os.path.isfile(F_FileName) == False:
        F_ArrOfMegaLinks = F_List[F_PositionFrom:]
        with open(F_FileName, 'wb') as f_file_handler_tmp:
            pickle.dump(F_ArrOfMegaLinks , f_file_handler_tmp)
            # f_file_handler_tmp.close
            print(f'Object successfully saved to "{F_FileName}"')
    return("write_2_file_if_not_exist done")

# Это чтение из бинарного файла - в набор имя \ ссылка \ комментарий. 
def load_from_file(F_LoadDataFromName,F_comment): 
    # то что получили - вывалиться в return
    with open (F_LoadDataFromName, "rb") as F_ArrayFormFile_handler:
    # F_ArrayFormFile_handler = open(F_LoadDataFromName, "rb")
        F_Data = pickle.load(F_ArrayFormFile_handler)
        print("load_from_file exec OK",len(F_Data), F_comment )
    return F_Data

def send_to_telegram_tests(f_chat, f_api, f_message):
    apiURL = f'https://api.telegram.org/bot{f_api}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': f_chat, 'text': f_message})
        print(response.text)
    except Exception as e:
        print(e)
        
#        https://www.freecodecamp.org/news/python-split-string-how-to-split-a-string-into-a-list-or-array-in-python/
# https://www.w3schools.com/python/ref_string_split.asp
def very_simple_parser_comma(f_inpitstr):
    f_parsed = f_inpitstr[0].split(",")
    return f_parsed

def main():
    print("Mark 0001")
    ct = datetime.datetime.now()
    print("current time:-", ct)

    # режим работы 
    ScriptDir2 = os.path.dirname(os.path.abspath(sys.argv[0]))
    MyLogPath = ScriptDir2 + "\\" + "Mbot_textlog.4bot"
    if CurrentMode == "test":
        TLGBotKeyFileName = ScriptDir2 + '\\' + 'Mbot_TlgBotKey_test.4bot'
    else:
        TLGBotKeyFileName = ScriptDir2 + '\\' + 'Mbot_TlgBotKey_prod.4bot'
    # если нет файла - создадим, если есть - считаем из него данные. 
   
    # сделаю файл логов  
    # _TODO вот это вынести в функцию "записать что-то в логи"
    ct = datetime.datetime.now() # ct stores current time
    ts = ct.timestamp()# ts store timestamp of current time
    if os.path.isfile(MyLogPath) == False:
        with open(MyLogPath, 'w') as file_handler_logs:
            file_handler_logs.write("first run V " + CurrentVersion + CurrentMode + "\n" + str(ct) + "\n" + str(ts) +"\n" + "---" )
    if os.path.isfile(MyLogPath) == True:
        with open(MyLogPath, 'a') as file_handler_logs:
            file_handler_logs.write("Regular run V " + CurrentVersion + CurrentMode + "\n" + str(ct) + "\n" + str(ts)+"\n" + "---")
            
# но отдельно написать генератор файла ключей-час с кофе.
# _TODO вот это вынести в функцию "сделать файл"
# пока что бот не умеет работать с несколькими ключами, 
# но отдельно написать генератор файла ключей-час с кофе.
    TGAPIIDxample = "APIT-a5678:b7890" #4 знака под индикатор что это, потом ID
    if os.path.isfile(TLGBotKeyFileName) == False:
        with open(TLGBotKeyFileName, 'w') as file_handler_tg:
            file_handler_tg.write(TGAPIIDxample + "\n" ) #"\r" автоматом идет в винде но это не точно
          

    if os.path.isfile(TLGBotKeyFileName) == True:
        with open(TLGBotKeyFileName, 'r') as file_handler_tg:
            TGData = []
            TGData = file_handler_tg.readlines()
            if TGData[0].strip('\n') == TGAPIIDxample:
                print("REWRITE TLG ID in format ")
    
    # _TODO тоже надо вынести в функцию - ip логин и пароль к базе постгре

    FirstRunID = "this is first run ID 0 CHANGE ME to any" #это для выноса в функцию
    PGsrvIP = "192.168.266.266"
    PGsrvLogin  = "PGUSER"
    PGsrvPassword = "PGPassword"
    PGDBName = "Exampledb"
    PGPort = "1234567890 def 5432" #def - 5432
    

    PGFile = ScriptDir2 + "\\" + "Mbot_pgdata.4bot" #хехе. его как раз бы в паблик не надо - вот этот файл
    if os.path.isfile(PGFile) == False:
        with open(PGFile, 'w') as file_handler_tg:
            file_handler_tg.write(FirstRunID + "\n" + PGsrvIP + "\n" + PGsrvLogin +  "\n" + PGsrvPassword + "\n" + PGDBName + "\n"+ PGPort) #"\r" автоматом идет в винде но это не точно
    if os.path.isfile(PGFile) == True:
        # print("Mode tmp PGFile ")
        with open(PGFile, 'r') as file_handler_t2:
            PGData = []
            PGData = file_handler_t2.readlines()
            # print(len(PGData)) #длина - length
            # print(PGData[0])
            # print(PGData[0].strip('\n') )
            # print(FirstRunID)
            PGsrvIP = PGData[1].strip('\n') 
            PGsrvLogin = PGData[2].strip('\n') 
            PGsrvPassword = PGData[3].strip('\n') 
            PGDBName = PGData[4].strip('\n')
            PGPort = PGData[5].strip('\n')

            if PGData[0].strip('\n') == FirstRunID:   #учитывать лишний перенос строки!
                print("REWRITE PG ID - IP - PWD - with your data ")

# Все что выше про три файла - надо вынести в функцию. Имя файла, передаваемый лист, считываемый лист, сообщение. 
    # print(PGsrvIP)
    DBconnID = psycopg2.connect(database = PGDBName, 
                        user = PGsrvLogin, 
                        host= PGsrvIP,
                        password = PGsrvPassword,
                        port = PGPort)

    DBconn = DBconnID.cursor()
    DBconn.execute('SELECT * FROM generalquestions;')  #тут надо переменную, а не хардкод
    FromDBgeneralquestions = DBconn.fetchall()
    DBconn.execute('SELECT * FROM temptests;') #тут надо переменную, а не хардкод и вообще все в функцию
    FromDBtemptests =  DBconn.fetchall()
    DBconn.execute("SELECT * FROM channelsforbot  WHERE textfield5_istest = 'test' ;")
    FromDBchannelsforbot = DBconn.fetchall()
    DBconnID.commit()
    DBconnID.close()


    # for row in rows:
    #    print(row)
    print("Mark 0002")  # примеры работы с массивами и типами данных. 
    # print(FromDBchannelsforbot)
 #   print(dir(FromDBchannelsforbot)) #атрибуты
    # print(type(FromDBchannelsforbot)) # <class 'list'>
    # print(len(FromDBchannelsforbot)) # длина массива
    # print(type(FromDBchannelsforbot[0])) #  class 'tuple' оказывается.
    # print(len(FromDBchannelsforbot[0]))
    # arr11test = very_simple_parser_comma(FromDBchannelsforbot)
    # print(arr11test)
    # print(rows[0])
    #print("Mark 0003")
    # dir(rows)
    # dir(rows[0])
    testchaid1234 = "-1234"
    testbotid1234 = "1234:abcd-efgh"
    
    testbotmessage1234 = "Я бот молодой, глупенький и знаниям не обученный"
    #send_to_telegram_tests(testchaid1234,testbotid1234,testbotmessage1234 )

if __name__ == '__main__':
    main()


    # man
    # https://www.postgresqltutorial.com/postgresql-python/connect/
    # https://www.datacamp.com/tutorial/tutorial-postgresql-python
    # потребуется pip install psycopg2
    # https://pganalyze.com/blog/pg-query-2-0-postgres-query-parser parser
    # parser man https://www.sqlalchemy.org/ 
    # parser https://www.datacamp.com/tutorial/how-to-use-sql-in-pandas-using-pandasql-queries
    # parser https://snyk.io/advisor/python/sqlparse/example
    # Как получить ID чата - https://api.telegram.org/bot<ваш_токен>/getUpdates 
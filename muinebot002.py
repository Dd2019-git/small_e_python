# current version: test 2
CurrentVersion = "02"
CurrentMode = "test"
# CurrentMode = "prod"


import logging # почему-то пока не прописал зачем это в логах
import os.path # и это для путей в файлах
# import xml.etree.ElementTree as ET # это для работы в читаемом человеком xml - не используется
import sys # для путей
import requests #это для работы http \ api \ telegram
import datetime #это для отметок времени в логах

import pickle #это для файлов https://java2blog.com/save-object-to-file-python/
import psycopg2 # это для postgre , не забываем pip install psycopg2  https://www.datacamp.com/tutorial/tutorial-postgresql-python
import json # Это для конвертации отметок 
from collections import namedtuple
from json import JSONEncoder #convert JSON to custom https://pynative.com/python-convert-json-data-into-custom-python-object/

# Classless
class CLChannelsforbot: # для таблицы channelsforbot 
    def __init__(self, textfield1_titleshort, textfield2_chatid, textfield3_username, textfield4_userid, textfield5_istest):
        self.textfield1_titleshort = textfield1_titleshort
        self.textfield2_chatid = textfield2_chatid
        self.textfield3_username = textfield3_username
        self.textfield4_userid = textfield4_userid
        self.textfield5_istest = textfield5_istest


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

# https://www.freecodecamp.org/news/python-split-string-how-to-split-a-string-into-a-list-or-array-in-python/
# https://www.w3schools.com/python/ref_string_split.asp
def very_simple_parser_comma(f_inpitstr):
    f_parsed = f_inpitstr[0].split(",")
    return f_parsed

def create_and_add_text(F_FullTextFileName, F_text, RWMark):
    F_CurrentTime = datetime.datetime.now()
    F_TimeStamp = F_CurrentTime.timestamp()
    if os.path.isfile(F_FullTextFileName) == False:
        with open(F_FullTextFileName, 'w') as f_file_handler:
            f_file_handler.write("first run V " + CurrentVersion + CurrentMode + "\n" + str(F_CurrentTime) + "\n" + str(F_TimeStamp) +"\n" + "---" )
    if os.path.isfile(F_FullTextFileName) == True and (RWMark == 'ADD'):
        with open(F_FullTextFileName, 'a') as f_file_handler:
            f_file_handler.write("Regular run Version: " + CurrentVersion + " Mode: " + CurrentMode + " timestamp " + str(F_CurrentTime) + " stamp " + str(F_TimeStamp)+"\n" + "---"+"\n")
            f_file_handler.write(F_text+"\n")
    if os.path.isfile(F_FullTextFileName) == True and (RWMark == 'REWR'):
        with open(F_FullTextFileName, 'w') as f_file_handler:
            f_file_handler.write("Regular RW Version: " + CurrentVersion + " Mode: " + CurrentMode + " timestamp " + str(F_CurrentTime) + " stamp " + str(F_TimeStamp)+"\n" + "---"+"\n")
            f_file_handler.write(F_text+"\n")
    

def do_time_test_example(F_chats_list, F_api, F_message):
    print("Mark 0003 do_time_test_example ")
    # print(len(F_chat_list))
    #print(F_chats_list)
    # print("F_chats_list type " + str(type(F_chats_list)))
    # print("F_chats_elements type " + str(type(F_chats_list[0])))
    for F_SingleRecFromChats in F_chats_list:
        # print("Mark 0004")
        # print(F_SingleRecFromChats)
        # print(type(F_SingleRecFromChats))
        # print(TG_APIID_Example)
        # print(len(F_SingleRecFromChats)) 
        F_TGCHATID = F_SingleRecFromChats[2]
        send_to_telegram_tests(F_TGCHATID,F_api,F_message )


def send_to_telegram_tests(f_chat, f_api, f_message):
    apiURL = f'https://api.telegram.org/bot{f_api}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': f_chat, 'text': f_message})
        print(response.text)
    except Exception as e:
        print(e)



def test123(F_test):
    return("123" + str(F_test))



def get_telegram_updates_all(F_ApiID, F_LogFile):
    F_IDapiFullURL = f'https://api.telegram.org/bot{F_ApiID}/getupdates'
    # print ("Run get_telegram_updates_all mark 1")
    create_and_add_text(F_LogFile,"call get_telegram_updates_all 1","ADD")
    # print(F_IDapiFullURL)
    try:
        # https://sky.pro/media/modul-requests-v-python/    
        F_AnswerBig = requests.get(F_IDapiFullURL)
        # print ("Run get_telegram_updates_all mark 2")
        create_and_add_text(F_LogFile,"call get_telegram_updates_all 3","ADD")
        # print(len(F_AnswerBig))
        # print(type(F_AnswerBig)) # <class 'requests.models.Response'>
        # print (dir(F_AnswerBig))
        # print(F_AnswerBig.ok) # True
        # print ("Run get_telegram_updates_all mark 4") 
        # print(F_AnswerBig.json) # <bound method Response.json of <Response [200]>> Чего ? 
        # print(dir(F_AnswerBig.json))
        # print(len(F_AnswerBig.json)) # object of type 'method' has no len()
        # print ("Run get_telegram_updates_all mark 5")
        # print(F_AnswerBig.text) #тут все хорошо, сюда валится длинный текст. не разобранный ! 
        # print(type(F_AnswerBig.text))  # ну круто, только это строка длинная. а не массив.
        # print(len(F_AnswerBig.text))
        #  схоронить в файл F_LogFile
        # так, а дальше то как разобрать https://stackoverflow.com/questions/61199555/telegram-bot-getupdates-and-parse-json-response
        #https://core.telegram.org/bots/api
        F_ReturnP1AsJSON =  json.loads(F_AnswerBig.text)
        F_Dict = F_ReturnP1AsJSON['result']
        print("Function get_telegram_updates_all exec") 
        print("Dictionary sise " + str(len(F_Dict))) ## ага вот так 6 объектов. Старые первые, [-1] - в конце - самые новые. 
        # print("Dictionary type " + str(type(F_Dict))) # Dictionary type <class 'list'>

        # но парсит все равно криииво. Прямо совсем.. 
        # записали что приехало в темп файл tmp1 но это не то что я хочу \ надо 
        create_and_add_text(F_LogFile+"tmp00",str(F_AnswerBig.text),"REWR")  # вот это вообще выглядит ОК, с переносами строк итд
        # create_and_add_text(F_LogFile+"tmp0",str(F_Dict[0]),"REWR")
        # create_and_add_text(F_LogFile+"tmp1",str(F_Dict[1]),"REWR")
        for S_update in F_Dict:
                # print(str(S_update))
                create_and_add_text(F_LogFile+"tmp00",str(S_update),"ADD")


        # print(F_Dict[-1])
        # create_and_add_text(F_LogFile,str(len(F_AnswerBig)))
        # create_and_add_text(F_LogFile,str(F_AnswerBig))

    except Exception as e:
        print(e)
    
    # return F_AnswerBig
    return F_Dict

def convert_listofD_inlistofOnj(F_InputListofD):
    print("convert_listofD_inlistofOnj exec")


def main():
    print("Mark 0001")
    CurrentTime = datetime.datetime.now()
    print("current time:-", CurrentTime)

    # режим работы 
    ScriptDir2 = os.path.dirname(os.path.abspath(sys.argv[0]))
    MyLogPath = ScriptDir2 + "\\" + "Mbot_textlog.4bot"
    MyGlobalReqLog = ScriptDir2 + "\\" + "Mbot_reqlog.txt" #сюда пойдут логи запросов до сброса

    if CurrentMode == "test":
        TLGBotKeyFileName = ScriptDir2 + '\\' + 'Mbot_TlgBotKey_test.4bot'
    else:
        TLGBotKeyFileName = ScriptDir2 + '\\' + 'Mbot_TlgBotKey_prod.4bot'
    # если нет файла - создадим, если есть - считаем из него данные. 
   
    # сделаю файл логов  
    # _TODO вот это вынести в функцию "записать что-то в логи"
    # ct = datetime.datetime.now() # ct stores current time
    TimeStamp = CurrentTime.timestamp()# ts store timestamp of current time
    if os.path.isfile(MyLogPath) == False:
        with open(MyLogPath, 'w') as file_handler_logs:
            file_handler_logs.write("first run V " + CurrentVersion + CurrentMode + "\n" + str(CurrentTime) + "\n" + str(TimeStamp) +"\n" + "---" )
    if os.path.isfile(MyLogPath) == True:
        with open(MyLogPath, 'a') as file_handler_logs:
            file_handler_logs.write("Regular run V " + CurrentVersion + CurrentMode + "\n" + str(CurrentTime) + "\n" + str(TimeStamp)+"\n" + "---")
            
# но отдельно написать генератор файла ключей-час с кофе.
# _TODO вот это вынести в функцию "сделать файл"
# пока что бот не умеет работать с несколькими ключами, 
# но отдельно написать генератор файла ключей-час с кофе.
    TG_APIID_Example = "APIT-a5678:b7890" #4 знака под индикатор что это, потом ID
    if os.path.isfile(TLGBotKeyFileName) == False:
        with open(TLGBotKeyFileName, 'w') as file_handler_tg:
            file_handler_tg.write(TG_APIID_Example + "\n" ) #"\r" автоматом идет в винде но это не точно
          

    if os.path.isfile(TLGBotKeyFileName) == True:
        with open(TLGBotKeyFileName, 'r') as file_handler_tg:
            TGData = []
            TGData = file_handler_tg.readlines()
            if TGData[0].strip('\n') == TG_APIID_Example:
                print("REWRITE TLG ID in format ")
            else:
                TG_APIID_Example = (TGData[0].replace("\n",""))[4:]
                # print(TG_APIID_Example)
    
    # _TODO тоже надо вынести в функцию - ip логин и пароль к базе постгре

    FirstRunID = "this is first run ID 0 CHANGE ME to any" #это для выноса в функцию - хм, а как выносить? В объект класса?
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
    # DBconn.execute("SELECT * FROM channelsforbot  WHERE textfield5_istest = 'test' ;")
    # https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/
    ExecStr = "SELECT * FROM channelsforbot  WHERE textfield5_istest = " + "'" + CurrentMode +"'" + ";" 
    # print(ExecStr)
    DBconn.execute(ExecStr)
    FromDBchannelsforbot = DBconn.fetchall()
    DBconnID.commit()
    DBconnID.close()


    # for row in rows:
    #    print(row)
    print("Mark 0002")  # примеры работы с массивами и типами данных. 
    # FromDBchannelsforbot - в этой переменной получили array of tuple И есть класс CLChannelsforbot
    # man https://pythonworld.ru/tipy-dannyx-v-python/kortezhi-tuple.html
    ArrayOfChatsInTg = [] #пустой список чатов для рассылки в телегу, но над ли его парсить ??
    # так, нужна функция получения ID бота из файла. А она есть выше в переменную TG_APIID_Example
    testbotmessage1 = "Муйневское время - " + str(CurrentTime) 
    testbotmessage1 = "Я бот молодой, глупенький и про это пока ничего не знаю, напишите большими буквами НОУКА и текст чему научить"
    # print(type(FromDBchannelsforbot[0]))
          
    # do_time_test_example(FromDBchannelsforbot, TG_APIID_Example, testbotmessage1)
    # получение обновлений тоже стоило бы в функцию
    # https://stackoverflow.com/questions/72524963/how-to-get-message-updates-from-the-user-after-the-bot-message-telegram-bot
    # https://docs.python-telegram-bot.org/en/v13.2/telegram.update.html
    # https://docs.python-telegram-bot.org/en/v20.6/telegram.update.html
    # https://stackoverflow.com/questions/72932853/get-updates-only-one-time-per-message

    create_and_add_text(MyGlobalReqLog,"modeREQ " + CurrentMode,"ADD")
    TgAllAnwerListPrimary = get_telegram_updates_all(TG_APIID_Example, MyGlobalReqLog) # отсюда получили массив ВСЕХ с ID ВСЕХ сообщений из ВСЕХ чатов. 
    # в виде массива с массой полей и внутри словарь, то есть JSON
    # теперь этот массив строк \ JSON надо как-то собрать в кучу и обработать. 
    # Важно! строки обрабатываются \ сбрасываются последовательно, поэтому лучше все же пересобрать. 
    # https://pynative.com/python-convert-json-data-into-custom-python-object/
    # # https://github.com/tg-bot-api/bot-api-base 
    # message_thread_id	Integer	Optional	\
    # Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    # https://stackoverflow.com/questions/60852011/how-to-make-telegram-bot-reply-to-a-specific-message
    print("Mark003 " + str(len(TgAllAnwerListPrimary)))
    # а мне бы его конвертировать в массив объектов. 

    # не актуальное и потом можно будет удалить ,а пока оставлено как пример и может для отладки
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
    #send_to_telegram_tests(testchaid1234,testbotid1234,testbotmessage1234   )

    

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
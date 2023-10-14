# current version: test 7
CurrentVersion = "07"
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
from types import SimpleNamespace # https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
import re


# Classless
class CLChannelsforbot: # для таблицы channelsforbot 
    def __init__(self, textfield1_titleshort, textfield2_chatid, textfield3_username, textfield4_userid, textfield5_istest):
        self.textfield1_titleshort = textfield1_titleshort
        self.textfield2_chatid = textfield2_chatid
        self.textfield3_username = textfield3_username
        self.textfield4_userid = textfield4_userid
        self.textfield5_istest = textfield5_istest

class PgConnect:
    def __init__(self, PGsrvIPorFQDN, PGsrvLogin, PGsrvPassword,PGDBName,PGPort):
        self.PGsrvIPorFQDN = PGsrvIPorFQDN
        self.PGsrvLogin = PGsrvLogin
        self.PGsrvPassword = PGsrvPassword
        self.PGDBName = PGDBName
        self.PGPort = PGPort


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
    

# def do_time_test_example(F_chats_list, F_ApiID_Token, F_message):
#    print("Mark 0003 do_time_test_example ")
#    # print(len(F_chat_list))#print(F_chats_list) # print("F_chats_list type " + str(type(F_chats_list)))     # print("F_chats_elements type " + str(type(F_chats_list[0])))
#    for F_SingleRecFromChats in F_chats_list:
#        # print("Mark 0004") # print(F_SingleRecFromChats)         # print(type(F_SingleRecFromChats))         # print(TG_APIID_Example# print(len(F_SingleRecFromChats)) 
#        F_TGCHATID = F_SingleRecFromChats[2]
#        send_to_telegram_tests(F_TGCHATID,F_ApiID_Token,F_message )

def do_send_TLG_example2(F_Chats_ID, F_ApiID_Token, F_message, F_ReplyTo, F_LogFile):
    print("Call do_send_TLG_example2")
    create_and_add_text(F_LogFile,"call do_send_TLG_example2","ADD")
    apiURL = f'https://api.telegram.org/bot{F_ApiID_Token}/sendMessage'
    if F_ReplyTo != "noreplay":
        try:
            response = requests.post(apiURL, json={'chat_id': F_Chats_ID, 'text': F_message, 'reply_to_message_id':F_ReplyTo})
            print(response.text) #а нафиг оно
        except Exception as e:
            print(e)
    if F_ReplyTo == "noreplay":      
        try:
            response = requests.post(apiURL, json={'chat_id': F_Chats_ID, 'text': F_message})
            print(response.text) #а нафиг оно
        except Exception as e:
            print(e)





def test123(F_test):
    return("123" + str(F_test))



def get_telegram_updates_all(F_ApiID_Token, F_LogFile):
    F_IDapiFullURL = f'https://api.telegram.org/bot{F_ApiID_Token}/getupdates'
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
        print("Call get_telegram_updates_all ") 
        # print("Dictionary sise " + str(len(F_Dict))) ## ага вот так 6 объектов. Старые первые, [-1] - в конце - самые новые. 
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

# def convert_listofD_inlistofOnj(F_InputListofD):
#    print("F_convert_listofD_inlistofOnj exec")
# https://pynative.com/python-convert-json-data-into-custom-python-object/
#    return namedtuple('X', F_InputListofD.keys())(*F_InputListofD.values())

def do_clear_TLG(F_Update_ID4reset,F_ApiID_Token, F_LogFile):
    F_IDapiFullURL = f'https://api.telegram.org/bot{F_ApiID_Token}/getUpdates?offset={F_Update_ID4reset}'
    create_and_add_text(F_LogFile,"call do_clear_TLG with " + str(F_ApiID_Token),"ADD")
    # print("call do_clear_TLG with " + F_IDapiFullURL )
    try:
        requests.get(F_IDapiFullURL)
    except Exception as e:
        print(e)

def get_AllPermitedChatFromSQLForKillSW(F_Connectors,F_CurrentMode, F_LogFile):
    print("call get_AllPermitedChatFromSQLForKillSW")
    F_CurrentMode4KS = "test"
    F_ReturnSQLIDlist = []
    create_and_add_text(F_LogFile,"call get_AllPermitedChatFromSQL " ,"ADD")
    # print(F_Connectors)
    # print("call get_AllPermitedChatFromSQL")
    F_DBconnID = psycopg2.connect(database = F_Connectors.PGDBName, 
                        user = F_Connectors.PGsrvLogin, 
                        host= F_Connectors.PGsrvIPorFQDN,
                        password = F_Connectors.PGsrvPassword,
                        port = F_Connectors.PGPort)
    F_DBconn = F_DBconnID.cursor()
    F_ExecStr = "SELECT * FROM channelsforbot  WHERE textfield5_istest = " + "'" + F_CurrentMode4KS +"'" + ";" 
    # F_ExecStr = "SELECT * FROM channelsforbot;"
    F_DBconn.execute(F_ExecStr)
    F_ReturnSQL = F_DBconn.fetchall()
    F_DBconnID.commit()
    F_DBconnID.close()
    for F_ID in F_ReturnSQL:
        F_ReturnSQLIDlist.append(F_ID[2]) 
    # print(type(F_ReturnSQLIDlist))
    return F_ReturnSQLIDlist

def get_AllPermitedChatFromSQL(F_Connectors,F_CurrentMode, F_LogFile):
    print("call get_AllPermitedChatFromSQL")
    F_ReturnSQLIDlist = []
    create_and_add_text(F_LogFile,"call get_AllPermitedChatFromSQL " ,"ADD")
    # print(F_Connectors)
    # print("call get_AllPermitedChatFromSQL")
    F_DBconnID = psycopg2.connect(database = F_Connectors.PGDBName, 
                        user = F_Connectors.PGsrvLogin, 
                        host= F_Connectors.PGsrvIPorFQDN,
                        password = F_Connectors.PGsrvPassword,
                        port = F_Connectors.PGPort)
    F_DBconn = F_DBconnID.cursor()
    # F_ExecStr = "SELECT * FROM channelsforbot  WHERE textfield5_istest = " + "'" + F_CurrentMode +"'" + ";" 
    F_ExecStr = "SELECT * FROM channelsforbot;"
    F_DBconn.execute(F_ExecStr)
    F_ReturnSQL = F_DBconn.fetchall()
    F_DBconnID.commit()
    F_DBconnID.close()
    for F_ID in F_ReturnSQL:
        F_ReturnSQLIDlist.append(F_ID[2]) 
    # print(type(F_ReturnSQLIDlist))
    return F_ReturnSQLIDlist

def get_SingleArticleFromSQLbyID(F_Connectors,F_CurrentMode, F_ArticleTable, F_ArticleID, F_LogFile):
    print("call get_SingleArticleFromSQLbyID")
    create_and_add_text(F_LogFile,"call send_single_article " + F_CurrentMode  + " 1 " +  F_ArticleTable +" 2 " + F_ArticleID,"ADD")
    F_DBconnID = psycopg2.connect(database = F_Connectors.PGDBName, 
                        user = F_Connectors.PGsrvLogin, 
                        host= F_Connectors.PGsrvIPorFQDN,
                        password = F_Connectors.PGsrvPassword,
                        port = F_Connectors.PGPort)
    F_DBconn = F_DBconnID.cursor()
    F_ExecStr =  "SELECT * FROM " + F_ArticleTable + " WHERE id = " + "'" + str(F_ArticleID) +"'" + ";" 
    F_DBconn.execute(F_ExecStr)
    F_ReturnSQL = F_DBconn.fetchall()
    F_DBconnID.commit()
    F_DBconnID.close()
    for F_ID in F_ReturnSQL:
        print(F_ID)
    print("call get_SingleArticleFromSQLbyID done return F_ReturnSQL len " + str(len(F_ReturnSQL)))
    return F_ReturnSQL

def get_articlesFromSQLbySingleTAG(F_Connectors,F_CurrentMode, F_ArticleTable, F_ArticleTAG, F_LogFile):
    print("call get_articlesFromSQLbySingleTAG tag = " + F_ArticleTAG)
    create_and_add_text(F_LogFile,"call send_single_article " + F_CurrentMode  + " 1 " +  F_ArticleTable +" 2 " + F_ArticleTAG,"ADD")
    F_DBconnID = psycopg2.connect(database = F_Connectors.PGDBName, 
                        user = F_Connectors.PGsrvLogin, 
                        host= F_Connectors.PGsrvIPorFQDN,
                        password = F_Connectors.PGsrvPassword,
                        port = F_Connectors.PGPort)
    F_DBconn = F_DBconnID.cursor()
    F_ExecStr =  "SELECT * FROM " + F_ArticleTable + " WHERE " + "'" + F_ArticleTAG +"'" + " = ANY(r5_tags);" 
    # print(F_ExecStr)
    F_DBconn.execute(F_ExecStr)
    F_ReturnSQL = F_DBconn.fetchall()
    F_DBconnID.commit()
    F_DBconnID.close()
    # for F_ID in F_ReturnSQL:
    #    print(F_ID)

    return F_ReturnSQL

def RewriteKillSwitch(F_FileofKS,F_KSInput, F_LogFile):
    print("call RewriteKillSwitch file = " + F_FileofKS)
    create_and_add_text(F_LogFile,"call RewriteKillSwitch " ,"ADD")
    F_KS_OFF = "OFF"
    F_KS_GlobalOff = "Rewrite me to OFF"
    if os.path.isfile(F_FileofKS) == False:
        print("KS not exist")
        with open(F_FileofKS, 'w') as file_handler_1:
            file_handler_1.write(F_KSInput + "\n" ) #"\r" автоматом идет в винде но это не точно
    # KS_GlobalOff изнутри функции жи
    
    if ((F_KSInput != F_KS_OFF and F_KSInput != F_KS_GlobalOff ) and  (os.path.isfile(F_FileofKS) == True)): 
        print("Call rewrite !")
        with open(F_FileofKS, 'w') as file_handler_1:
            file_handler_1.write(F_KSInput + "\n" ) #"\r" автоматом идет в винде но это не точно

    if os.path.isfile(F_FileofKS) == True:
        with open(F_FileofKS, 'r') as file_handler_1:
            F_KSData = []
            F_KSData = file_handler_1.readlines()
            if F_KSData[0].strip('\n') == F_KS_OFF:
                print("Kill switch Current from file = " + F_KS_OFF + "-" + F_KSData[0].strip('\n') )
            else:
                print("call RewriteKillSwitch= " + F_KS_OFF)
                print("Rewrite Kill switch to OFF " + F_KSInput)
                create_and_add_text(F_LogFile,"call RewriteKillSwitch with mode " + F_KS_OFF,"ADD")
                exit() 

def DoSingleMessageFromSQLAnswer(F_SingleSQLAnswer):
    print("call DoSingleMessageFromSQLAnswer")
    print(F_SingleSQLAnswer)
    F_Message = "Про это я знаю только: \n"  + F_SingleSQLAnswer[1] + " : " + F_SingleSQLAnswer[2] + '\n'  
    if F_SingleSQLAnswer[3] != None:
        F_Message = F_Message + "ссылки: " 
        for link in F_SingleSQLAnswer[3]:
            F_Message = F_Message +  link + ' ; ' 
        
    if F_SingleSQLAnswer[4] != None:
        F_Message = F_Message + "\n geo: " 
        for geo in F_SingleSQLAnswer[4]:
            F_Message = F_Message +  geo + '; ' 
    print(type(F_SingleSQLAnswer[5] ))
    if F_SingleSQLAnswer[5] != None:
        F_Message = F_Message + "\n tags: " 
        for tags in F_SingleSQLAnswer[5]:
            F_Message = F_Message +  tags + ' ; ' 
    
    return F_Message

def DoSingleMessageFromTitlesSQLAnswer(F_MultSQLAnswer):
    print("call DoSingleMessageFromTitlesSQLAnswer")
    print(len(F_MultSQLAnswer))
    F_Message = ""
    for F_Title in F_MultSQLAnswer:
        F_Message = F_Message + "Про это знаю: (" + str(F_Title[0]) + ") " + F_Title[1] + '\n'
        print(F_Title[1])
    # print(F_Message)
    return F_Message
# логика обработки запросов. 
# Если запрос не начинается с текста БОТ! (BotMarker) - то сбросить совсем. 
# Если запрос == текст БОТ! - то написать TestBotMessage005
# если запрос + тег, то вывести список статей с данным тегом. 
# или вызвать функцию обработки запросов с таким единичным тегом. 
# Сначала простая функция - отправить единичную статью по id
# и еще тут нет проверок, что запрос из разрешенных чатов, потому что из НЕ разрешенных надо удалять все.
# Не понятно пока с логикой. 
# Сначала надо выкинуть все, что не входят в список разрешенных чатов. 
# и дописать ЕСЛИ запрос с киллсвичем И из чата (приват \ тест) - то сделать киллсвич disabled

def do_PrimaryClearAnswers(F_UnclearedAnswersList, F_KillSwitchChatID,F_KillSwithFile, F_KillMarker, F_MyGlobalReqLog, F_AllPermitedChatsListIDOnly,F_BotMarker,F_ApiID_Token):
    print("call do_PrimaryClearAnswer")
    if len(F_UnclearedAnswersList) == 0:
        print("call do_PrimaryClearAnswer with len eq 0 - so exit ") # конечно это можно и в логи писать.
        exit()
    F_Cleared =[]
    for F_UnicUpdate in F_UnclearedAnswersList:
        print("call do_PrimaryClearAnswer block 1 for ID " + str(F_UnicUpdate['update_id']))
        # print(F_UnicUpdate)
        if 'message' not in F_UnicUpdate:
            F_UniMessageOrEditemMsg = F_UnicUpdate['edited_message'] #оно бывает ['message']) или [edited_message']
        elif 'message' in F_UnicUpdate:
            F_UniMessageOrEditemMsg = F_UnicUpdate['message']
        else:
            print("call do_PrimaryClearAnswer block 999 for ID BOOMS ")
            exit()
        
        if 'text' not in F_UniMessageOrEditemMsg:
            print("do_PrimaryClearAnswers Call block 2 no text in MSG")
        else:
            F_MsgTextLower = F_UniMessageOrEditemMsg['text'].lower()

        if (str(F_UniMessageOrEditemMsg['chat']['id'])) == F_KillSwitchChatID[0] and F_UniMessageOrEditemMsg['text'] == F_KillMarker:
            print("do_PrimaryClearAnswers Call + " + F_KillMarker)
            RewriteKillSwitch(F_KillSwithFile,F_KillMarker , F_MyGlobalReqLog)
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
            exit()

        if (str(F_UniMessageOrEditemMsg['chat']['id'])) not in F_AllPermitedChatsListIDOnly:
            print("do_PrimaryClearAnswers Вызов чистки для чатов вне системы " + " chat_id " + str(F_UniMessageOrEditemMsg['chat']['id']) + " update_id  " + str(F_UnicUpdate['update_id']))
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
        
        # if  UnicUpdate['message'].haskey('text'):
        elif 'text' not in F_UniMessageOrEditemMsg:
            print("do_PrimaryClearAnswers Вызов чистки для текста с фото" + " id " + str(F_UnicUpdate['update_id']))
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
        elif (F_UniMessageOrEditemMsg['text'][:4] != F_BotMarker):
            print("do_PrimaryClearAnswers Mark 5-1 call clear and alive " + str(F_UnicUpdate['update_id'])) #update_id Это видите ли число
            F_Cleared.append(F_UnicUpdate)
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
            # Что-то у меня логика тут хромает. 
        elif ( "drop" in F_MsgTextLower ):
            print("Mark 5-2 call clear drop word" + str(F_UnicUpdate['update_id'])) #update_id Это видите ли число
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
        elif ( "database" in F_MsgTextLower):
            print("do_PrimaryClearAnswers Mark 5-3 call clear database word " + str(F_UnicUpdate['update_id'])) #update_id Это видите ли число
            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
            
        elif (F_UniMessageOrEditemMsg['text'].lower() == F_BotMarker.lower() ) and (str(F_UniMessageOrEditemMsg['chat']['id']) in F_AllPermitedChatsListIDOnly):
            print("do_PrimaryClearAnswers Mark 5-2 call send and clear only bot alive check")
            F_Cleared.append(F_UnicUpdate)
            # send_to_telegram_tests(testchaid1234,testbotid1234,testbotmessage005) #переписать с использованием логов 
            # do_time_test_example(FromDBchannelsforbot, TG_APIID_Example, TestBotMessage005) # сюда кстати тоже надо логи
            # SendToID = F_UnicUpdate['message']['chat']['id'] заменео на F_UniMessageOrEditemMsg
            # RepID = F_UnicUpdate['message']['message_id']
            # do_send_TLG_example2(SendToID, TG_APIID_Example, TestBotMessage005,RepID, MyGlobalReqLog)

            # do_clear_TLG(F_UnicUpdate['update_id']+1,TG_APIID_Example, MyGlobalReqLog)

        else:
            print("do_PrimaryClearAnswers Mark 5-3 base clearing done") # вот сюда надо килл свич прикручивать. 
            F_Cleared.append(F_UnicUpdate)
    print("call do_PrimaryClearAnswer complete, return " + str(len(F_Cleared))) # так, вот это важно для очистки. То есть вернулось 0
    # а мне бы в таком случае можно уже отсюда сделать вызов глобальной чистки.
    if len(F_Cleared) == 0:
           print("Call clear from do_PrimaryClearAnswer with id" + str(F_UnclearedAnswersList[-1]['update_id']) )
           do_clear_TLG(F_UnicUpdate['update_id']+1,F_ApiID_Token, F_MyGlobalReqLog)
    return F_Cleared
# https://stackoverflow.com/questions/57164765/find-all-substring-that-starts-and-ends-with-specific-characters
# https://note.nkmk.me/en/python-str-extract/#extract-a-substring-with-regex-research-refindall
# https://note.nkmk.me/en/python-re-match-search-findall-etc/
# привет, регулярки. 
def do_FindTagsInSingle(F_Cleared01Single): 
    print("Call do_FindTagsInSingle")
    if 'message' not in F_Cleared01Single:
        F_UniMessageOrEditemMsg = F_Cleared01Single['edited_message'] 
    elif 'message' in F_Cleared01Single:
            F_UniMessageOrEditemMsg = F_Cleared01Single['message']
    else:
        print("call do_FindTagsInSingle block 999 for ID BOOMS ")
        exit()
    F_Text = F_UniMessageOrEditemMsg['text'] #

    # print(F_Text)
    # F_TagsStart = [index for index in range(len(F_Text )) if F_Text .startswith('#', index)]
    # F_TagEnd = (F_Text.find(" "))
    # print(re.findall(r"#.*[^a-zA-Z\d\s:]",  F_Text)) ## а зарраза, a-zA-Z0-9 не включает русские буквы! 
    # a-zA-Z0-9А-Яа-я()]/u
    # eng only works fine print(re.findall(r"#[a-zA-Z0-9]+",  F_Text)) 
    # eng only works fine F_Tags = (re.findall(r"#[a-zA-Z0-9]+",  F_Text))
    print(re.findall(r"#[a-zA-Z0-9А-Яa-я]+",  F_Text))
    F_Tags = (re.findall(r"#[a-zA-Z0-9А-Яa-я]+",  F_Text))
    print("F tags done")
    print(F_Tags)
    print("Exit do_FindTagsInSingle")
    return F_Tags


def main():
    CurrentTime = datetime.datetime.now()
    print("Mark 0001 current time:-", CurrentTime)
    # тут нужна проверка kill switch для выключения бота через команду в телеге. 
    # режим работы 
    ScriptDir2 = os.path.dirname(os.path.abspath(sys.argv[0]))
    MyLogPath = ScriptDir2 + "\\" + "Mbot_textlog.4bot"
    MyGlobalReqLog = ScriptDir2 + "\\" + "Mbot_reqlog.txt" #сюда пойдут логи запросов до сброса
    KillSwithFile = ScriptDir2 + "\\" "Mbot_killswitch.txt" #аварийный прерыватель
    KS_GlobalOff = "Rewrite me to OFF" #do not change - see F_KS_GlobalOffF"
    RewriteKillSwitch(KillSwithFile,KS_GlobalOff , MyGlobalReqLog)
    # RewriteKillSwitch(KillSwithFile,"test" , MyGlobalReqLog)

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
    PGConn1 = PgConnect("192.168.266.266", "PGUSER", "PGPassword",  "Exampledb", "1234567890 def 5432")
    #print("Pgmark")
    # print(PGConn1.PGsrvIPorFQDN)
    # PGsrvIP = "192.168.266.266"     # PGsrvLogin  = "PGUSER"    # PGsrvPassword = "PGPassword"     # PGDBName = "Exampledb"    # PGPort = "1234567890 def 5432" #def - 5432

    PGFile = ScriptDir2 + "\\" + "Mbot_pgdata.4bot" #хехе. его как раз бы в паблик не надо - вот этот файл
    if os.path.isfile(PGFile) == False:
        with open(PGFile, 'w') as file_handler_tg:
            file_handler_tg.write(FirstRunID + "\n" + PGConn1.PGsrvIPorFQDN + "\n" + PGConn1.PGsrvLogin +  "\n" + PGConn1.PGsrvPassword + "\n" + PGConn1.PGDBName + "\n"+ PGConn1.PGPort) #"\r" автоматом идет в винде но это не точно
    if os.path.isfile(PGFile) == True:
        # print("Mode tmp PGFile ")
        with open(PGFile, 'r') as file_handler_t2:
            PGData = []
            PGData = file_handler_t2.readlines()
            # print(len(PGData)) #длина - length
            # print(PGData[0])
            # print(PGData[0].strip('\n') )
            # print(FirstRunID)
            PGConn1.PGsrvIPorFQDN = PGData[1].strip('\n') 
            PGConn1.PGsrvLogin = PGData[2].strip('\n') 
            PGConn1.PGsrvPassword = PGData[3].strip('\n') 
            PGConn1.PGDBName = PGData[4].strip('\n')
            PGConn1.PGPort = PGData[5].strip('\n')

            if PGData[0].strip('\n') == FirstRunID:   #учитывать лишний перенос строки!
                print("REWRITE PG ID - IP - PWD - with your data ")

# Все что выше про три файла - надо вынести в функцию. Имя файла, передаваемый лист, считываемый лист, сообщение. 
    # print(PGsrvIP)
    # то что ниже - не используется и оставлено как пример. 
    AnotherTest123 = 123
    if AnotherTest123 == 122:
        DBconnID = psycopg2.connect(database = PGConn1.PGDBName, 
                        user = PGConn1.PGsrvLogin, 
                        host= PGConn1.PGsrvIPorFQDN,
                        password = PGConn1.PGsrvPassword,
                        port = PGConn1.PGPort)

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
# вот это выше бы может тоже в функцию ? Надо в функцию конечно, но выглядит так будто FromDBchannelsforbot не используется. 
# v07 - вот и проверим, вроде не взорвалось
# потому что используется AllPermitedChatsListIDOnly
# AllPermitedChatsListIDOnly = get_AllPermitedChatFromSQL(PGConn1,CurrentMode,MyGlobalReqLog)

    print("Mark 0002")  # примеры работы с массивами и типами данных. 
    # FromDBchannelsforbot - в этой переменной получили array of tuple И есть класс CLChannelsforbot
    # man https://pythonworld.ru/tipy-dannyx-v-python/kortezhi-tuple.html
    ArrayOfChatsInTg = [] #пустой список чатов для рассылки в телегу, но над ли его парсить ??
    # так, нужна функция получения ID бота из файла. А она есть выше в переменную TG_APIID_Example
    testbotmessage1 = "Муйневское время - " + str(CurrentTime) 
    testbotmessage1 = "Я бот молодой, глупенький и про это пока ничего не знаю, напишите большими буквами НОУКА и текст чему научить"
    # print(type(FromDBchannelsforbot[0]))
          
    # do_time_test_example(FromDBchannelsforbot, TG_APIID_Example, testbotmessage1) # сюда кстати тоже надо логи
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
    # print("Mark003 " + str(len(TgAllAnwerListPrimary)))
    
    # а мне бы его конвертировать в массив объектов. 
# json.loads take a string as input and returns a dictionary as output.
# json.dumps take a dictionary as input and returns a string as output.
# https://stackoverflow.com/questions/42354001/json-object-must-be-str-bytes-or-bytearray-not-dict
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
    # TgAllAnwerListSecondary = convert_listofD_inlistofOnj(TgAllAnwerListPrimary)
    # data = TgAllAnwerListPrimary[0]
    # x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    # x = json.dumps(data, object_hook=lambda d: SimpleNamespace(**d))
    # print(x.update_id)
    # это кусок наследия, с которым ПОКА жалко расставаться.
    MarkInfo=10
    if MarkInfo == 11:
        print(TgAllAnwerListPrimary[0]['update_id'])
        print(TgAllAnwerListPrimary[0]['message'])
        print(TgAllAnwerListPrimary[0]['message']['message_id'])
        print(TgAllAnwerListPrimary[0]['message']['from'])
        print(TgAllAnwerListPrimary[0]['message']['from']['id'])
        print(TgAllAnwerListPrimary[0]['message']['from']['is_bot'])
        print(TgAllAnwerListPrimary[0]['message']['from']['first_name'])
        print(TgAllAnwerListPrimary[0]['message']['from']['last_name'])
        print(TgAllAnwerListPrimary[0]['message']['from']['username'])
        print(TgAllAnwerListPrimary[0]['message']['from']['language_code'])
        print(TgAllAnwerListPrimary[0]['message']['from']['last_name'])
        print("----Chat----")
        print(TgAllAnwerListPrimary[0]['message']['chat']) 
        print(TgAllAnwerListPrimary[0]['message']['chat']['id']) 
    # print(TgAllAnwerListPrimary[0]['message']['chat']['title']) # этот только для Public! 
    # АГА. Для Private \ Public разные параметры класса \ json в части чата. Для Паблик и приват - разные.
        print(TgAllAnwerListPrimary[0]['message']['chat']['username']) 
        print(TgAllAnwerListPrimary[0]['message']['chat']['type']) 
        print("----date----")
        print(TgAllAnwerListPrimary[0]['message']['date'])
        print(datetime.datetime.fromtimestamp(TgAllAnwerListPrimary[0]['message']['date']) )
        print("----text----")
        print(TgAllAnwerListPrimary[0]['message']['text'])
    # Это для Private
    # print(TgAllAnwerListPrimary[0]['message']['chat']['first_name']) 
    # print(TgAllAnwerListPrimary[0]['message']['chat']['last_name']) 
    # print(TgAllAnwerListPrimary[0]['message']['chat']['username']) 
    # 
 # Ну ладно, оно работает. 
 # Разберем сброс ответа.  будет сброшено все ДО id, НЕ включая ID. Номера идут подряд. 
    # print("We are here mark 004")
    # do_clear_TLG("12345",TG_APIID_Example, MyGlobalReqLog)
    # первый прогон. # вообще вот тут надо проверять, чего отвечать и кому. Надо бы сразу записать. 
    AllPermitedChatsListIDOnly = get_AllPermitedChatFromSQL(PGConn1,CurrentMode,MyGlobalReqLog)
# вот это не совсем правильно, потому что мало ли где у меня Prod И не только. Надо брать все.

    # print(AllPermitedChatsListIDOnly)
    # print(TgAllAnwerListPrimary[0]['message']['text'][:4])#  The character at this index is not included in the substring.

    KillSwitchChatID = get_AllPermitedChatFromSQLForKillSW(PGConn1,CurrentMode,MyGlobalReqLog)
    TestBotMessage005 = "Я жажду служить"
    BotMarker = "\u0411\u041e\u0422!"
    SwKillMarker = "SIGKILL" 
    print("Начинаем первичную обработку, элементов для обработки " + str(len(TgAllAnwerListPrimary)))
    # Стоп. Что-то такая логика так себе и получается надо не строки сразу дропать, а из массива для дальнейшей обработки чистить.
    # то есть такая логика хороша, если мы сразу в этой процедуре обрабатываем то, что надо дропнуть. 
    # и обрабатываем нормально то, что надо обработать. 
    # а иначе нам (кому-нам ? мне и компьютеру ?) надо дорого!! формировать другой лист для обработки.
    TgAllAnwerListCleared01 = do_PrimaryClearAnswers(TgAllAnwerListPrimary,KillSwitchChatID, KillSwithFile, SwKillMarker, MyGlobalReqLog, AllPermitedChatsListIDOnly, BotMarker, TG_APIID_Example)
    if len(TgAllAnwerListCleared01) > 0:
      print("Обработка завершена, вернулось из первичной обработки " + str(len(TgAllAnwerListCleared01)))
    else:
        print("call do_PrimaryClearAnswer complete, вернулось в основной текст 0" )
        exit()
    print("We are here mark 007")
    Table4Test1 = "generalquestions" #а чо в одной таблице то ищем - ну потом поправлю. Или так и оставлю, посмотрю.
 # так, получили почищенные блоки для обработки. Теперь надо из них вытащить первый тег. скажем #faq
    for Cleared01 in TgAllAnwerListCleared01:
        Tags4Test = do_FindTagsInSingle(Cleared01) #получили список тегов из единичного сообщения.
        # Если тегов нет, то в строке значит ничего не нашлось. Пока так. 
        # Включая вариант, если тег нашелся #ID123
        if len(Tags4Test) == 0:
            SendToID = Cleared01['message']['chat']['id']
            RepID = Cleared01['message']['message_id']
            TestBotMessage010 = "Не нашел вопроса"
            print("Call no tags clear complete")
            do_send_TLG_example2(SendToID, TG_APIID_Example, TestBotMessage010,RepID, MyGlobalReqLog)
            do_clear_TLG(Cleared01['update_id']+1,TG_APIID_Example, MyGlobalReqLog)

        #Tag4Test = "#faq" 
        if (len(Tags4Test) > 0 ):
            # do_FindTagsInDB[Tags[0]]
            ID_Check = "#ID".lower()
            print("We are here mark 008")
            if Tags4Test[0][:3].lower() == ID_Check and len(Tags4Test[0]) >3: #потому что просто #id - это не понятно что
                print("Cell getbyID - " + Tags4Test[0])
                print("Work with ID - " + Tags4Test[0][3:])
                ID99 = Tags4Test[0][3:]
                ReturnFromSQLBySomething = get_SingleArticleFromSQLbyID(PGConn1, CurrentMode, Table4Test1, ID99, MyGlobalReqLog)
                # exit()
            elif Tags4Test[0][:3].lower() != ID_Check:
            # TestReturn = get_articlesFromSQLbySingleTAG(PGConn1, CurrentMode, Table4Test1, Tags4Test[0], MyGlobalReqLog)
                ReturnFromSQLBySomething = get_articlesFromSQLbySingleTAG(PGConn1, CurrentMode, Table4Test1, Tags4Test[0], MyGlobalReqLog)
                print("Из get_articlesFromSQLbySingleTAG вернулось строк " + str(len(ReturnFromSQLBySomething)))
            # так, тут надо прокачать логику. Допустим у нас вернулся единичный тег ID7 и его надо разделить на #ID первые 2 буквы
            # и на число. И уже в таком случае выдавать по ID
            # но тег  #id1234 в списке тегов не значится жи!
            
            if len(ReturnFromSQLBySomething) == 1 :
                Message12 = DoSingleMessageFromSQLAnswer(ReturnFromSQLBySomething[0]) #Вот это вообще собирается из ответа строкой из SQL
                SendToID = Cleared01['message']['chat']['id']
                RepID = Cleared01['message']['message_id']
                do_send_TLG_example2(SendToID, TG_APIID_Example, Message12,RepID, MyGlobalReqLog)
                do_clear_TLG(Cleared01['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
            # 
            if len(ReturnFromSQLBySomething) > 1 : 
                print ("TRR many " + str(len(ReturnFromSQLBySomething)))
                Message12 = DoSingleMessageFromTitlesSQLAnswer(ReturnFromSQLBySomething)
                SendToID = Cleared01['message']['chat']['id']
                RepID = Cleared01['message']['message_id']
                do_send_TLG_example2(SendToID, TG_APIID_Example, Message12,RepID, MyGlobalReqLog)
                do_clear_TLG(Cleared01['update_id']+1,TG_APIID_Example, MyGlobalReqLog)

            if len(ReturnFromSQLBySomething) == 0: # ничего не нашлось
                print("Можно очищать ")
                SendToID = Cleared01['message']['chat']['id']
                RepID = Cleared01['message']['message_id']
                TestBotMessage011 = "Ничего не нашел по этому тегу"
                print("Call no tags clear complete")
                do_send_TLG_example2(SendToID, TG_APIID_Example, TestBotMessage011,RepID, MyGlobalReqLog)
                do_clear_TLG(Cleared01['update_id']+1,TG_APIID_Example, MyGlobalReqLog)
                # do_send_TLG_example2("NNN", TG_APIID_Example, Message12,"noreplay", MyGlobalReqLog)

# Теперь надо его отправить.  

    # Вообще надо из запроса сначала вытащить все теги, потом сделать какой-то джойн того что набралось.
    # и еще надо сделать аварийный выключатель удаленного бота - Kill switch- и вписать его в первые запуски. 
    # но пока запуск ручной, это подождет (а функция готова.) Только надо проверять, какой юзер имеет право на такой запуск
    # можно из базы брать конечно, но можно и достаточно чтобы оманда была из тестового чата, где я и бот. который test




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

#SQL 
 # https://www.w3schools.com/sql/sql_wildcards.asp
    # https://docs.data.world/documentation/sql/concepts/intermediate/Working%20with%20arrays.html
    # https://stackoverflow.com/questions/10738446/postgresql-select-rows-where-column-array
    # https://popsql.com/learn-sql/postgresql/how-to-query-arrays-in-postgresql
    # https://www.commandprompt.com/education/how-to-query-arrays-in-postgresql/
    # https://stackoverflow.com/questions/71647754/how-to-check-if-any-field-of-array-not-contains-substring-in-postgres
    # https://www.commandprompt.com/education/how-to-query-arrays-in-postgresql/

    # https://www.freecodecamp.org/news/python-split-string-how-to-split-a-string-into-a-list-or-array-in-python/
# https://www.w3schools.com/python/ref_string_split.asp

# def send_to_telegram_tests(f_chat, F_ApiID_Token, f_message):
#    print("Call send_to_telegram_tests")
#    apiURL = f'https://api.telegram.org/bot{F_ApiID_Token}/sendMessage'
#    try:
#        response = requests.post(apiURL, json={'chat_id': f_chat, 'text': f_message})
#        print(response.text)
#    except Exception as e:
#        print(e)
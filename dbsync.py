# bubble_col_lengths.cgi
# # !/usr/bin/python
#
# import glob, json, re
#
# print "content-type: text/html\n\n"
# print "<html>"
#
# print "start"
#
# tableList = ["comment", "document", "entry", "image-thing", "preset", "preset-array", "protocol", "protocol-array",
#              "reminder", "scale-option", "ticket", "user", "usr-act-audit"]
# # tableList = ["event", "entry"]
# # database = {}
# columnLengths = {}
# # all of the tables in one dict
# # two layers of lookups 1) table name 2) column name 3) col length
# for tableName in tableList:
#     table_db_name = re.sub("[ -]", "_", tableName.lower())
#     print(tableName, table_db_name)
#     # database[tableName] = {}
#     columnLengths[table_db_name] = {}
#     file_list = glob.glob("bubble_backup_29OCT/" + tableName + "_from_*.txt")
#     # print(file_list)
#     for file_name in file_list:
#         # print(file_name)
#         # TODO: investigate whether 'utf-8' or 'latin-1' is correct encoding for this data
#         with open(file_name) as data_file:
#             data = json.load(data_file)
#         for entry in data["response"]["results"]:
#             # database[tableName][entry["_id"]] = entry
#             for col in entry:
#                 col_db_name = re.sub("[ -]", "_", col.lower())
#                 val_len = 0
#                 try:
#                     val_len = len(entry[col])
#                 except:
#                     val_len = len(str(entry[col]))
#                 if col_db_name in columnLengths[table_db_name]:
#                     columnLengths[table_db_name][col_db_name] = max(columnLengths[table_db_name][col_db_name], val_len)
#                 else:
#                     columnLengths[table_db_name][col_db_name] = val_len
# print columnLengths
#
# for table_db_name in columnLengths:
#     with open("ddls/" + table_db_name + ".ddl", "w") as ddl_file:
#         ddl_file.write("create table " + table_db_name + "(\n")
#         for col_db_name in sorted(columnLengths[table_db_name].keys()):
#             col_db_length = columnLengths[table_db_name][col_db_name]
#             print '#', table_db_name, col_db_name, col_db_length
#             ddl_file.write("    " + col_db_name + " VARCHAR(" + str(col_db_length) + ") CHARACTER SET UTF8,\n")
#         ddl_file.write("    primary key (_id)\n")
#         ddl_file.write(");\n")
#
# print "</html>"
#
# -----------------------------------------------------------------------
# bubble_create_tables.cgi
# # !/usr/bin/python
#
# from subprocess import call
#
# # import MySQLdb,glob
#
# print "content-type: text/html\n\n"
# print "<html>"
#
# print "start"
#
# call(
#     'cat ddls/* | mysql --host="localhost" --user="ua881188_trackwelladmin" --password="ZAQ123$%^wsx" --database="ua881188_trackwell"',
#     shell=True)
#
# print "<p>done"
#
# print "</html>"
#
# -----------------------------------------------------------------------------
# bubble_drop_tables.cgi
# # !/usr/bin/python
#
# from subprocess import call
#
# # import MySQLdb,glob
#
# print "content-type: text/html\n\n"
# print "<html>"
#
# print "start"
#
# # call('cat ddls/* | mysql --host="localhost" --user="ua881188_trackwelladmin" --password="ZAQ123$%^wsx" --database="ua881188_trackwell"', shell=True)
# call(
#     'cat drop_tables.ddl | mysql --host="localhost" --user="ua881188_trackwelladmin" --password="ZAQ123$%^wsx" --database="ua881188_trackwell"',
#     shell=True)
#
# print "<p>done"
#
# print "</html>"
#
# -------------------------------------------------------------------------------
# bubble_initial_backup.cgi
# # !/usr/bin/python
#
# # this script gets all of the data from the api_url in batches
# # batches are the same day of data from all tables
# # the idea is breaking tables up into days will help troubleshoot any problems
# # when I ran this on 28 Oct at 2200 it took 20min and 75-100% cpu capacity
# # ran it the next day and it went a lot longer and got more (all?) data
#
# # total run time
# # total number of https requests
#
#
# print "content-type: text/html\n\n"
# print "<html>"
#
# print "start"
#
# import re
# from urllib2 import urlopen
# from time import gmtime, strftime
# from datetime import datetime, timedelta
# import MySQLdb
# import MySQLdb.cursors as cursors
# import json
# import urllib
# import time
#
# print ", imports done"
#
# backup_folder = "bubble_backup_29OCT"  # CHANGE THIS----------------------------
#
# api_url = "https://track-well.bubbleapps.io/api/1.1/obj/"
# api_token =
# tableList = ["comment", "document", "entry", "image-thing", "preset", "preset-array", "protocol", "protocol-array",
#              "reminder", "scale-option", "ticket", "user", "usr-act-audit"]
#
# print ", tables done"
#
# seedDate = "2017/07/31"  # one day before the date to start getting data
# dayInterval = 1  # number of days to get in one batch
#
# dateRepeatLimit = 100  # max number of date loop iterations
# cursorRepeatLimit = 100  # max number of cursor loop iterations
# getRepeatLimit = 10  # max number of times the get loop will iterate
#
# print("<p>tableList: " + str(tableList))
# # loop through list of tables --------------------------------------------
# for tableName in tableList:
#     print("<p>Begin loop on table: " + tableName + " -----------------------")
#
#     # find out how many items are in the whole table
#     totalItems = 0  # total number of rows in table
#     itemsCopied = 0  # total number of rows copied from table
#     get_total_count_url = (api_url + tableName)
#     print("<p>" + get_total_count_url)
#     data = urlopen(str(get_total_count_url)).read()
#     dataJson = json.loads(data)
#     totalCount = dataJson['response']['count']
#     totalRemaining = dataJson['response']['remaining']
#     totalItems = (totalCount + totalRemaining)
#     print("<p>total items in table: " + str(totalItems))
#
#     fromDate = datetime.strptime(seedDate, "%Y/%m/%d")
#     todayDate = datetime.now()
#     dateRepeatCount = 0
#     # loop through date ranges
#     while fromDate < todayDate:
#         print"<p> begin loop on dates"
#         if dateRepeatCount >= dateRepeatLimit:
#             print ("<p>date repeat limit reached: " + str(dateRepeatCount))
#             break
#         dateRepeatCount = (dateRepeatCount + 1)
#
#         # calc date range for this iteration
#         fromDate = (fromDate + timedelta(days=dayInterval))
#         toDate = (fromDate + timedelta(days=dayInterval))
#         fromDateString = datetime.strftime(fromDate, "%Y-%m-%d")
#         toDateString = datetime.strftime(toDate, "%Y-%m-%d")
#         print "<p> --- begin day " + fromDateString + " to " + toDateString + " --- "
#
#         cursorIndex = 0  # position in list of results
#         remainingCount = 1  # number of items remaining in results
#         countCount = 0  # number of items returned by the search
#         cursorRepeatCount = 0
#         # loop through cursor positions until data exhausted
#         while True:
#             # protect the loop from running too often
#             if remainingCount <= 0:
#                 print ("<p>remaining count <= 0")
#                 break
#             if cursorRepeatCount >= cursorRepeatLimit:
#                 print("<p>repeatLimit " + str(cursorRepeatLimit) + " reached")
#                 break
#             cursorRepeatCount = (cursorRepeatCount + 1)
#             cursorIndex = (cursorIndex + countCount)
#
#             # build the pieces of the URL that gets data out of Bubble's API
#             plain_array = '[{"key":"Created Date","constraint_type":"less than","value":"' + toDateString + 'T00:00:00.000Z"},{"key":"Created Date","constraint_type":"greater than","value":"' + fromDateString + 'T00:00:00.000Z"}]'
#             json_array = urllib.quote_plus(plain_array)
#             final_url = (
#             api_url + tableName + "?" + "constraints=" + json_array + "&sort_field=Created%20Date&descending=false&cursor=" + str(
#                 cursorIndex) + "&api_token=" + api_token)
#             # print("<p>" + final_url + "<p>")
#
#             # get the data from the URL & record file (as required)
#             getSuccess = False  # did Bubble respond to the search appropriately
#             getCount = 0  # number of items in the search results
#             getRepeatCount = 0
#
#             while True:
#                 # protect this loop from running too often
#                 if getSuccess == True:
#                     print "<p>Great success!"
#                     break
#                 if getRepeatCount >= getRepeatLimit:
#                     print "<p>get repeat limit reached"
#                     break
#                 getRepeatCount = (getRepeatCount + 1)
#
#                 try:
#                     data = urlopen(str(final_url)).read()
#                     # getting here means urlopen didn't throw an exception
#                     getSuccess = True
#                     dataJson = json.loads(data)
#                     # print(dataJson.items())
#                     getCount = dataJson['response']['count']
#                     print ("<P>Count: " + str(getCount))
#                     countCount = getCount
#                     remainingCount = dataJson['response']['remaining']
#                     itemsCopied = itemsCopied + getCount
#                     print("<p>copied " + str(itemsCopied) + " of " + str(totalItems))
#                 except Exception as ex:
#                     print("<p>Exception: ")
#                     print(type(ex))
#                     print(ex.args)
#                     print(ex)
#                     # delay to see if the problem resolves itself
#                     time.sleep(5)  # in seconds
#                     continue
#
#                 if getCount <= 0:
#                     break
#
#                 # build the name of the file to save the data in
#                 fileName = (
#                 backup_folder + "/" + tableName + "_from_" + fromDateString + "_to_" + toDateString + "_cursor_" + str(
#                     cursorIndex) + "_saved_" + strftime("%Y-%m-%d--%H-%M-%S" + "GMT", gmtime()) + ".txt")
#                 file = open(fileName, "wb")
#                 file.write(data)
#                 file.close()
#                 print("<p>file saved: " + fileName + "<p>")
#                 # remainingCount = int(re.search('"remaining": *([0-9]*)', data.decode("utf-8")).group(1))
#                 # countCount = int(re.search('"count": *([0-9]*)', data.decode("utf-8")).group(1))
#
# print "</html>"
#
# -----------------------------------------------------------------------------------
# bubble_initial_store_data.cgi
# # !/usr/bin/python
# # bubble_initial_store_data.cgi
# # this will log all of its activity to the same file
# # but it will be a different file for each time this script runs
#
# # look for todo file
# # if it doesn't exist, create it by listing files
# # if it does exist, continue processing files in it
# # process files by adding their json data to database
# # when list is empty, delete to do file
#
# import MySQLdb
# from datetime import datetime
# import glob, json, re
# import os
# from subprocess import call
#
# print "content-type: text/html\n\n"
# print "<html>"
#
# # db = MySQLdb.connect(host="localhost", user="ua881188_trackwelladmin", passwd="ZAQ123$%^wsx", db="ua881188_trackwell")
# # cur = db.cursor()
# scriptFolder = "/home/ua881188/public_html/data.track-well.com/cgi-bin"
# logFolder = "script_logs"
# logDateTime = datetime.utcnow().strftime('%Y-%m-%d--%H-%M-%S-%f')[:-3]
# toDoFile = "bubble_initial_store_data_todo.txt"  # list of things to do
# dataFolder = "bubble_backup_29OCT"
# # shouldn't need tableList since we're not looking up files by table
# '''
# tableList = ["image-thing",
#         "protocol-array",
#         "user",
#         "comment",
#         "preset",
#         "scale-option",
#         "usr-act-audit",
#         "document",
#         "preset-array",
#         "ticket",
#         "entry",
#         "protocol",
#         "reminder"]
# '''
#
#
# # log to file, seems to be most timely and accurate
# # log to browser so I can see something
# def log(message):
#     message = str(datetime.now()) + " " + message
#     print("<p>" + message)
#     with open(logFolder + "/log_store_data_" + logDateTime + "-UTC.txt", "a") as logFile:
#         logFile.write(message + "\n")
#
#
# log("---------begin new log-------------\n")
#
# # check for todo file---------------------------------------------------------
# toDoFileExists = False
# try:
#     log("try toDoFileExists")
#     toDoFileExists = os.path.isfile(toDoFile)
# except Exception as ex:
#     log("toDoFile exception")
#     log(ex)
# log("toDoFileExists: " + str(toDoFileExists))
#
# # todo file doesn't exist, so create it---------------------------------------
# if toDoFileExists == False:
#     # os.chdir("/home/ua881188/public_html/data.track-well.com/cgi-bin")
#     os.chdir(scriptFolder)
#     paths = os.listdir(dataFolder)
#     # write the files, one line at a time, to the todo list file
#     toDoCount = 0
#     with open(toDoFile, "w") as pathList:
#         # print"<p>open yourfile"
#         for line in paths:
#             # print("<p>" + line)
#             pathList.write(line + "\n")
#             toDoCount = (toDoCount + 1)
#             # print"<p>write yourfile"
#     log("added this many items in todo file: " + str(toDoCount))
#     toDoFileExists = os.path.isfile(toDoFile)
#     log("toDoFileExists: " + str(toDoFileExists))
#     todoFileSize = os.path.getsize(toDoFile)
#     log("todofile size: " + str(todoFileSize))
#
# # todo file does exist, so process it-----------------------------------------
# todoLimit = 3
# todoCount = 0
# if toDoFileExists == True:
#     log("open todofileexists = true")
#     db = MySQLdb.connect(host="localhost", user="ua881188_trackwelladmin", passwd="ZAQ123$%^wsx",
#                          db="ua881188_trackwell")
#     cur = db.cursor()
#     log("todoFileExists == true, begin processing")
#     with open(toDoFile, "r") as input:
#         # print"<p>open yourfile"
#         with open("temp_" + toDoFile, "w") as output:
#             # print"<p>open newfile"
#             for workingFileName in input:
#                 removeTodoItem = False
#                 log("workingFileName in input: " + workingFileName)
#                 # if todoCount >= todoLimit:
#                 #    break
#                 # todoCount = todoCount + 1
#                 # this is a filepath without the folder
#                 # for a file with bubble db array in it
#                 # that needs to be added to the hostm db
#                 # sanitize the table and field names first
#                 workingFileName = re.sub("\n", '', workingFileName)
#                 workingFilePath = (dataFolder + "/" + workingFileName)
#                 log(workingFilePath)
#                 with open(workingFilePath, "r") as data_file:
#                     data = json.load(data_file)
#                     tableName = re.sub('\_from_.*', '', workingFileName)
#                     cleanTableName = re.sub("[ -]", "_", tableName)
#                     log("tableName: " + tableName + " cleanTableName: " + cleanTableName)
#                 # each item is a row in the table
#                 # each col is a field in the row
#                 for item in data["response"]["results"]:
#                     log("begin for item in data...")
#                     query1 = "INSERT INTO " + cleanTableName + "("
#                     query2 = "values("
#                     query3 = []  # sets the data type as a list
#                     for col in item:
#                         log("begin for col in item...")
#                         log("col: " + col)
#                         cleanColName = re.sub("[ -]", "_", col.lower())
#                         log("cleanColName: " + cleanColName)
#                         # log("col: " + col + " cleanColName: " + cleanColName)
#                         # create insert statement for the entire row
#                         # create a tuple for all the values in the row
#                         query1 = query1 + cleanColName + ","
#                         log("query1: " + query1)
#                         query2 = query2 + "%s,"
#                         log("query2: " + query2)
#                         entry = item[col]
#                         # log("item[col] " + entry)
#                         try:
#                             # if this works the data is already a string
#                             len(entry[col])  # this will fail if the value is not a string
#                             # val = re.sub("'","''",entry.get(col,None))
#                             val = re.sub("'", "''", entry)
#                             val = re.sub("[^a-zA-Z0-9 \\/\t\r\n;:._,'\"()$!<>+&*%#~?-]", "?",
#                                          val)  # replaces anything that's not a letter/number with a question mark; list built through trial and error(s)
#                             query3.append(val)
#                             log("val: " + val)
#                         except:
#                             # if this works the data is a number
#                             # query3.append(str(entry.get(col,None)))
#                             query3.append(str(entry))
#                         log("whatever 3")
#                         # end for col in item
#
#                     query3 = tuple(query3)  # the mysqldb library wants a tuple, not a list
#                     query12 = query1[:-1] + ") " + query2[:-1] + ");"
#                     log(query12 + " " + str(query3))
#                     try:
#                         if todoCount <= todoLimit:
#                             todoCount = todoCount + 1
#                             cur.execute(query12, query3)
#                             # data added to db, so don't add this workingFileName to the temp_todoFile
#                             removeTodoItem = True
#                     except Exception as ex:
#                         log("Oh no! " + ex)
#                         # log("not added to database: " + workingFilePath)
#                         # data NOT added to db
#                         removeTodoItem = False
#                         # output.write(workingFileName + "\n")
#                         # end for item in data
#
#                 if removeTodoItem == False:
#                     log("not added to database: " + workingFilePath)
#                     output.write(workingFileName + "\n")
#                 db.commit()  # commit after each file
#                 # end workingFileName
#
#             log("finished table " + tableName)
#             # end temp_todoFile
#
#             # end todoFile
#     cur.close()
#     db.commit()
#     db.close()
#     replaceTodoFile = ("'mv temp_" + toDoFile + " " + toDoFile + "'")
#     log("call replacetodofile: " + replaceTodoFile)
#     try:
#         call(replaceTodoFile, shell=True)
#         # call('mv temp_bubble_initial_store_data_todo.txt bubble_initial_store_data_todo.txt', shell = True)
#     except:
#         log("call didn't work")
#     log("done with call")
#     # end todoFileExists == True
#
# # todo file exists, and is empty, so delete it--------------------------------
# todoFileSize = os.path.getsize(toDoFile)
# log("todofile size: " + str(todoFileSize))
# if todoFileSize <= 0:
#     os.remove(toDoFile)
#     log("todofile removed")
#
# print "<p>done"
# print "</html>"
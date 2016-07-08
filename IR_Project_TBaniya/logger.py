def writelog(message):

    message = str(message)


    file_log= None
    try:
        file_log = open("log_file.txt",'a')
        file_log.write(message)
        file_log.write("\r\n")
        file_log.flush()


    except Exception as e:
        pass
    finally:
        if file_log != None:
            file_log.close()
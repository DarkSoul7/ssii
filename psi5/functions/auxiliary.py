# -*- coding: utf-8 -*-
import datetime
from os.path import isfile
from os.path import dirname
from os.path import abspath
import smtplib
from dateutil.relativedelta import relativedelta


def writedata(data):
    dir = dirname(dirname(abspath(__file__))) + '\\files\\orders\\' + \
          str(datetime.datetime.today()).split(' ')[0][:-3] + '.txt'

    with open(dir, mode='a', encoding='utf-8') as file:
        file.writelines(data + ' (' + str(datetime.datetime.today()).split('.')[0] + ')\n')


#No compruebo que el fichero no esté siendo usado por otro usuario
def writelog(isverified):
    dir = dirname(dirname(abspath(__file__))) + '\\files\\reports\\' + \
          str(datetime.datetime.today()).split(' ')[0][:-3] + '.txt'

    if not isfile(dir):
        log = open(dir, mode='w+')
        log.close()

    with open(dir, 'r') as log:
        text = log.readlines()

    with open(dir, mode='w+', encoding='utf-8') as log:
        if not text:
            verified = 0
            unverified = 0
        else:
            verified = int(text[0])
            unverified = int(text[1])

        if isverified == 'Verified':
            verified += 1
        else:
            unverified += 1

        log.writelines(str(verified) + '\n' + str(unverified) + '\n' + str(verified + unverified))


#Actualiza el fichero mensual con los ratios y lo prepara para su posterior envío
def updatefiles(today):
    currentdir = dirname(dirname(abspath(__file__))) + '\\files\\reports\\' + \
          str(today).split(' ')[0][:-3] + '.txt'

    month1 = today + relativedelta(months=-1)
    month1dir = dirname(dirname(abspath(__file__))) + '\\files\\reports\\' + \
          str(month1).split(' ')[0][:-3] + '.txt'

    month2 = today + relativedelta(months=-2)
    month2dir = dirname(dirname(abspath(__file__))) + '\\files\\reports\\' + \
          str(month2).split(' ')[0][:-3] + '.txt'

    if isfile(month1dir):
        log = open(month1dir, mode='r')
        month1percentage = log.readlines()[-1]
        log.close()
    else:
        month1percentage = -1

    if isfile(month2dir):
        log = open(month2dir, mode='r')
        month2percentage = log.readlines()[-1]
        log.close()
    else:
        month2percentage = -1

    with open(currentdir, mode='r') as log:
        text = log.readlines()
        currentpercentage = int(text[0])/int(text[2])

    if currentpercentage > month1percentage and currentpercentage > month2percentage:
        text.append('\nTENDENCIA POSITIVA\n')
    elif currentpercentage == month1percentage and currentpercentage == month2percentage:
        text.append('\nTENDENCIA NULA\n')
    else:
        text.append('\nTENDENCIA NEGATIVA\n')

    text.append(str(currentpercentage))

    with open(currentdir, mode='w+', encoding='utf-8') as log:
        log.writelines(text)

    text[0] = 'Pedidos verificados: ' + text[0]
    text[1] = 'Pedidos no verificados: ' + text[1]
    text[2] = 'Pedidos totales: ' + text[2]
    text[4] = 'Porcentaje de aciertos: ' + text[4]

    return '\n'.join(text)


#Envía el informe mensual
def sendemail(file):
    date = datetime.datetime.today()
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(user='pruebasuniversidad15@gmail.com', password='proofuniversity15')
    email = 'Informe de ' + str(date.month) + '/' + str(date.year) + '\n\n' + file
    server.sendmail("'pruebasuniversidad15@gmail.com'", 'pruebasuniversidad15@gmail.com', email)
    server.quit()

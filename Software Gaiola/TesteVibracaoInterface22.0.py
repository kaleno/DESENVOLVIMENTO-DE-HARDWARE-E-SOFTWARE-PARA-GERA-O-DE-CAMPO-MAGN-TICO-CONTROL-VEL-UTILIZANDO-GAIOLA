import PySimpleGUI as sg
import random
import threading
import serial
import serial.tools.list_ports
import time
from time import ctime, strftime, gmtime, localtime
import base64
import traceback
ports = serial.tools.list_ports.comports(include_links=False)
checkports = True
kill = False # Variavel que mata as Theads
authorization = [False, False, False]       # Vetor que autoriza a thead a continuar a Comunicação.
ComControler = ['','','']    # Vetor que fornece a porta com dos terminais 1,2 e 3 com os respectivos SN:4400004,4400007 e 4400011


#Terminal 1     COM16 e COM17
#RS422-1        COM50
#Terminal 2     COM21 e COM22
#RS422-2        COM51
#Terminal 3     COM23 e COM24
#RS422-3        COM52

#------------------------------------------------------------------------------------------------------Função Responsável por Procurar e configurar e autorizar as portas COM. 
def configports(window):
    global authorization
    global ComControler
    global checkports
    tempo_arquivo = strftime("-%d_%m_%Y-%H_%M_%S",localtime(time.time()))
    while True:
        try:
            if not((authorization[0]) and (authorization[1]) and (authorization[2])):
                if checkports == True:
                    start = time.time()
                    ports = serial.tools.list_ports.comports(include_links=False)
                    portlist =[]
                    for port in ports :
                        print(port.device)
                        if not([port.device] in portlist):
                            portlist += [port.device]
                    print(portlist)
                    h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    h.write('\n'+str(tempo)+"[Teste]Portas Disponíveis:"+str(portlist))
                    h.close()
                    Consoleports =[]
                    for porta in portlist: # ADICIONAR A COM SUCESSIVA COMO CASO DE USO >> or porta == ComControler[0][0:3] + str(int(ComControler[0][3:5])+1)
                        if (len(ComControler[0])> 2):
                            if (porta == ComControler[0] or porta == ComControler[0][0:3] + str(int(ComControler[0][3:5])+1)) and (authorization[0] == True):
                                print ("Pular porta:",porta,"!")
                                continue
                        if (len(ComControler[1])> 2):
                            if (porta == ComControler[1] or porta == ComControler[1][0:3] + str(int(ComControler[1][3:5])+1)) and (authorization[1] == True):
                                print ("Pular porta:",porta,"!")
                                continue
                        if (len(ComControler[2])> 2):
                            if (porta == ComControler[2] or porta == ComControler[2][0:3] + str(int(ComControler[2][3:5])+1)) and (authorization[2] == True):
                                print ("Pular porta:",porta,"!")
                                continue
                        if porta in ["COM33","COM34","COM35","COM36"]:
                            print ("Pular porta do MOXA:[",porta,"]!")
                            continue
                            
                        try:
                            terminal = serial.Serial(porta, baudrate=9600,timeout = 0.5)#timeout=1
                            BufferRead = b''
                            time.sleep(0.2)
                            terminal.write(b'$INV;')
                            BufferRead = terminal.read(250).decode("utf-8")
                            h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            h.write('\n'+str(tempo)+"["+porta+"]"+BufferRead)
                            h.close()
                            if '[INF]' in BufferRead:
                                Consoleports += [porta]
                            print("Porta:[",porta,"]",BufferRead)
                            terminal.close()
                        except:
                            print("Erro:",traceback.format_exc())
                            if 'terminal' in locals():
                                print("Porta:[",porta,"]"+" Em falha")
                                h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                h.write('\n'+str(tempo)+"[Teste]"+porta+" Em falha")
                                h.write('\n'+str(tempo)+"[Teste]["+porta+"]"+traceback.format_exc())
                                h.close()
                                terminal.close()
                            print("Porta:", porta," fechada")
                            continue
                            
                print("Portas de console:",Consoleports)
                h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                h.write('\n'+str(tempo)+"[Teste]Portas de Console que responderam:"+str(Consoleports))
                h.close()
                print("Perguntando SN de cada Porta")
                for porta in Consoleports:
                    try:
                        if porta in ComControler:
                            print(porta)
                            if (len(ComControler[0])> 2):
                                if (porta == ComControler[0] or porta == ComControler[0][0:3] + str(int(ComControler[0][3:5])+1)) and (authorization[0] == True):
                                    print ("Pular porta(Console):",porta,"!")
                                    continue
                            if (len(ComControler[1])> 2):
                                if (porta == ComControler[1] or porta == ComControler[1][0:3] + str(int(ComControler[1][3:5])+1)) and (authorization[1] == True):
                                    print ("Pular porta(Console):",porta,"!")
                                    continue
                            if (len(ComControler[2])> 2):
                                if (porta == ComControler[2] or porta == ComControler[2][0:3] + str(int(ComControler[2][3:5])+1)) and (authorization[2] == True):
                                    print ("Pular porta(Console):",porta,"!")
                                    continue
                        terminal = serial.Serial(porta, baudrate=9600,timeout = 0.5)#timeout=1
                        terminal.write("console\n".encode('utf-8'))
                        BufferRead = b''
                        time.sleep(0.2)
                        BufferRead = terminal.read(50).decode("utf-8")
                        h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                        h.write('\n'+str(tempo)+"["+porta+"]"+BufferRead)
                        h.close()
                        Login = False
                        for i in range(15):
                            if ("correct!" in BufferRead) or ("Command not recognized" in BufferRead):
                                Login = True
                                print("Login bem sucedido ")
                                break;
                            if "Password:" in BufferRead:
                                terminal.write("#TrmDual\n".encode('utf-8'))
                                print("->:#TrmDual\n")
                            else:
                                terminal.write("console\n".encode('utf-8'))
                                print("->:console\n")
                            BufferRead = terminal.read(50).decode("utf-8")
                            time.sleep(1)
                        
                        terminal.write("hwinfo\n".encode('utf-8'))
                        #print("->:hwinfo\n")
                        time.sleep(1)
                        BufferRead = terminal.read(50).decode("utf-8")
                        h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                        h.write('\n'+str(tempo)+"["+porta+"]"+BufferRead)
                        h.close()
                        SN = False
                        for i in range(15):
                            if ("Serial Number:" in BufferRead):
                                SN = True
                                linhas = BufferRead.split('\n')
                                for frase in linhas:
                                    if "Serial Number:" in frase:
                                        Serial = frase.split(' ')[3]
                                        Serial = Serial.split('\r')[0]
                                        print("SN:",Serial,"Porta:",porta)
                                        print(Serial)
                                        if Serial == '00009':
                                            ComControler[0] = porta
                                            authorization[0] = True
                                            print("Terminal 1 -00009-"+porta+" autorizado")
                                            h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                            h.write('\n'+str(tempo)+"[Teste]Terminal 1 -00009-"+porta+" autorizado")
                                            h.close()
                                        if Serial == '4400007':
                                            ComControler[1] = porta
                                            authorization[1] = True
                                            print("Terminal 2 -4400007-"+porta+" autorizado")
                                            h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                            h.write('\n'+str(tempo)+"[Teste]Terminal 2 -4400007-"+porta+" autorizado")
                                            h.close()
                                        if Serial == '4400011':
                                            ComControler[2] = porta
                                            authorization[2] = True
                                            print("Terminal 3 -4400011-"+porta+" autorizado")
                                            h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                            h.write('\n'+str(tempo)+"[Teste]Terminal 3 -4400011-"+porta+" autorizado")
                                            h.close()
                                                            
                                break;
                            else:
                                terminal.write("hwinfo\n".encode('utf-8'))
                                print("->:hwinfo\n")
                            time.sleep(0.5)
                            BufferRead = terminal.read(50).decode("utf-8")
                            h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            h.write('\n'+str(tempo)+"["+porta+"]"+BufferRead)
                            h.close()
                            time.sleep(0.5)
                    except:
                        print("Falha na Configuração de Portas")
                        print("Erro:",traceback.format_exc())
                        if 'h' in locals():
                            try:
                                if h.isOpen():
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    h.write('\n'+str(tempo)+"[Teste]["+porta+"]"+traceback.format_exc())
                                    h.close()
                                else:
                                    h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    h.write('\n'+str(tempo)+"[Teste]["+porta+"]"+traceback.format_exc())
                                    h.close()
                                if 'terminal' in locals():
                                    terminal.close()
                            except:
                                 print("Falha na documentação do erro!")
                                 print("Erro:",traceback.format_exc())
                        time.sleep(1)        
                        continue
                       
                
                print("ComControler:",ComControler)
                print("authorization:",authorization)
                if(authorization[0] and authorization[1] and authorization[2]):
                    if checkports == True:
                        window['Start'].update(disabled = False, text = "Iniciar")
                    Consoleports = ComControler
                    checkports == False
                #end = time.time()
                #print(end - start)
                time.sleep(1)
                terminal.close()

            else:
                time.sleep(0.02)
                continue
        except:
            print("Falha na Configuração de Portas")
            print("Erro:",traceback.format_exc())
            if 'h' in locals():
                try:
                    if h.isOpen():
                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                        h.write('\n'+str(tempo)+"[Teste]["+porta+"]"+traceback.format_exc())
                        h.close()
                    else:
                        h = open("data/Log_Console_test_vibracao)_COM_Controller"+tempo_arquivo+".txt", "a")
                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                        h.write('\n'+str(tempo)+"[Teste]["+porta+"]"+traceback.format_exc())
                        h.close()
                    if 'terminal' in locals():
                        terminal.close()
                except:
                     print("Falha na documentação do erro!")
                     print("Erro:",traceback.format_exc())
            time.sleep(1)        
            continue
        
#------------------------------------------------------------------------------------------------------Utilizado para mostrar as coisas na interface       
def printt(texto,window,TestNumber):
    window['-ML'+str(TestNumber)+'-'+sg.WRITE_ONLY_KEY].print(texto,end='')

#------------------------------------------------------------------------------------------------------Barrinha que gira quando o programa está funcionando.
def carregando(n):
    if n == 0:
        return '—'
    elif n == 1:
        return '\\'
    elif n == 2:
        return '|'
    elif n == 3:
        return '/'

#------------------------------------------------------------------------------------------------------Report (Ainda sem uso)
def report(sucess,local): # funcão responsável por escrever em sempre que tiver sucesso ou falha.
    if sucess == True:
        print("funcionou")
    else:
        print("falha em ",local)
        
#------------------------------------------------------------------------------------------------------Função Responsável por executar o teste caso as portas COM sejam autorizadas. 
def TestUnit(ComNumberRS422,TestNumber,eixo,window):
    global kill
    global ComControler
    global authorization
    tempo_arquivo = strftime("-%d_%m_%Y-%H_%M_%S",localtime(time.time()))
    estado = 0
    f = open("data/Log_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
    f.write("Data-Hora,Porta Terminal Aberta,RxTerminal,TerminalPass,Porta 422 Aberta,Rx422,422Pass, Comunication Ok")
    f.close()
    while True:
        if authorization[TestNumber-1]:
            try:            
                # Configuração Terminal
                Rs422pass = False
                terminalpass = False
                recebidoRs422 =''
                recebitoterminal=''
                try:
                # Adicionar cometários do programa no Log do console
                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    g.write('\n'+str(tempo)+"[Teste]Tentativa de Abrir a Porta do Console em "+ComControler[TestNumber - 1])
                    g.close()
                    port = ComControler[TestNumber-1]
                    terminal = serial.Serial(ComControler[TestNumber-1], baudrate=9600,timeout = 0.5)#timeout=1
                    BufferRead = b''
                    BufferRead = terminal.read(250)
                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    g.write('\n'+str(tempo)+BufferRead.decode("utf-8"))
                    g.close()
                    printt(BufferRead.decode("utf-8"),window,TestNumber)
                    printt(port +' OK',window,TestNumber)
                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    g.write('\n'+str(tempo)+"[Teste]"+ComControler[TestNumber - 1]+" Aberta")
                    g.close()
                except:
                    printt('\n'+port+' NOK',window,TestNumber)
                    time.sleep(1)
                    continue
                # Configuração RS422
                try:
                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    g.write('\n'+str(tempo)+"[Teste]Tentativa de Abrir a Porta da RS422 em COM"+str(ComNumberRS422))
                    g.close()
                    portrs = "COM"+str(ComNumberRS422)
                    Rs422 = serial.Serial(portrs, baudrate=19200,timeout = 1)#timeout=1
                    BufferReadRs = b''
                    BufferReadRs = Rs422.read(250)
                    printt(BufferReadRs.decode("utf-8"),window,TestNumber)
                    printt(portrs+ " OK",window,TestNumber)
                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                    g.write('\n'+str(tempo)+"[Teste]COM"+str(ComNumberRS422)+" Aberta")
                    g.close()
                except:
                    print('\n'+portrs+' NOK',window,TestNumber)
                    time.sleep(1)
                    continue

                # Estados de Configuração
                configureport = False
                Senha = False
                while True:
                    Rs422pass = False
                    terminalpass = False
                    if (terminal.isOpen() == True)and(Rs422.isOpen() == True): # Caso a porta do terminal esteja aberta
                        if Senha == False: #LOGAR NO CONSOLE
                            g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            g.write('\n'+str(tempo)+"[Teste]Tentativa de Logar no Console")
                            g.close()
                            terminal.write("console\n".encode('utf-8'))
                            printt("->:console\n",window,TestNumber)
                            time.sleep(0.01)
                            BufferRead = terminal.read(250).decode("utf-8")
                            g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            g.write('\n'+str(tempo)+BufferRead)
                            g.close()
                            printt(BufferRead,window,TestNumber)
                            for i in range(15):
                                if ("correct!" in BufferRead) or ("Command not recognized" in BufferRead):
                                    Senha = not(Senha)
                                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    g.write('\n'+str(tempo)+"[Teste]Login bem sucedido")
                                    g.close()
                                    printt("Login bem sucedido " + str(Senha),window,TestNumber)
                                    break;
                                if "Password:" in BufferRead:
                                    terminal.write("#TrmDual\n".encode('utf-8'))
                                    printt("->:#TrmDual\n",window,TestNumber)
                                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    g.write('\n'+str(tempo)+"[Teste]Adicionando Senha no Console")
                                    g.close()
                                else:
                                    terminal.write("console\n".encode('utf-8'))
                                    printt("->:console\n",window,TestNumber)
                                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    g.write('\n'+str(tempo)+"[Teste]Pedindo Console novamente")
                                    g.close()
                                BufferRead = terminal.read(250).decode("utf-8")
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+ BufferRead)
                                g.close()
                                printt(BufferRead,window,TestNumber)
                                time.sleep(1)
                        else:
                            if configureport == False: #CONFIGURAR PORTA
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+"[Teste]Configurando Modo de Comunicação RS422")
                                g.close()
                                terminal.write("comm set 422 raw\n".encode('utf-8'))
                                printt("->:comm set 422 raw\n",window,TestNumber)
                                BufferRead = terminal.read(250).decode("utf-8")
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+ BufferRead)
                                g.close()
                                printt(BufferRead,window,TestNumber)
                                if "comm set 422 raw" in BufferRead:
                                    terminal.write("comm log on\n".encode('utf-8'))
                                    printt("->:comm log on\n",window,TestNumber)
                                    BufferRead = str(terminal.read(250))
                                    printt(BufferRead,window,TestNumber)
                                    if "comm log on" in BufferRead:
                                        if terminal.isOpen() == True:
                                            configureport = True
                                            printt("Porta configurada",window,TestNumber)
                                            g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                            g.write('\n'+str(tempo)+"[Teste]Comunicação Rs422 Configurada!")
                                            g.write('\n'+str(tempo)+"[Teste]Sistema pronto para trocar mensagens")
                                            g.close()
                            else: #Terminal Configurado e Logado (Pronto para trocar mensagens)

                                
                                # Autotrac (Terminal => Rs232
                                send = '========================================\n'
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+"[Teste]Enviando \'Autotrac\' (Console => Rs422)")
                                g.close()
                                terminal.write("comm send Autotrac\n\n".encode('utf-8'))
                                send += "Autotrac (Console => Rs422)          "+ carregando(estado)+"\n"
                                estado = estado + 1
                                if estado == 4 :
                                    estado = 0
                                BufferReadRs = str(Rs422.read(250).decode("utf-8"))
                                recebidoRs422 = BufferReadRs
                                if BufferReadRs =="Autotrac":
                                    Rs422pass = True
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+"[Teste]Recebido:\'"+BufferReadRs+"\' Status:"+str(Rs422pass))
                                g.close()
                                time.sleep(0.3)
                                send +="Recebido Rs422:"+BufferReadRs+("\t-PASS" if Rs422pass else "\t-FAIL") +"\n"
                                # Autotrac (Terminal <= Rs232)
                                send += "Autotrac (Console <= Rs422)\n"
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+"[Teste]Enviando \'Autotrac\' (Console <= Rs422)")
                                g.close()
                                time.sleep(0.3)
                                Rs422.write("Autotrac".encode('utf-8'))
                                BufferRead = str(terminal.read(250).decode("utf-8"))
                                g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                g.write('\n'+str(tempo)+BufferRead)
                                g.close()
                                processBuffer = BufferRead[:]
                                processBuffer = processBuffer.split("\n")
                                recebidoterminal =""
                                for i in processBuffer:
                                    if ("[RAW RECV]" in i) and len(i) > 38:
                                        #print("valor de i:",i.split("[RAW RECV][00]") )
                                        i = i.split("? [RAW RECV][00] ")[1]
                                        #print("valor de i:",i[0:24])
                                        recebidoterminal = bytearray.fromhex(i).decode()
                                        if recebidoterminal == "Autotrac":
                                            terminalpass = True
                                        send += "Recebido Console:"+ recebidoterminal +("\t-PASS" if terminalpass else "\t-FAIL") +"\n"
                                        g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                        g.write('\n'+str(tempo)+"[Teste]Recebido:\'"+recebidoterminal+"\' Status:"+str(terminalpass))
                                        g.close()
                                if terminalpass == False:
                                    send += "Recebido Console:"+recebidoterminal+("\t-PASS" if terminalpass else "\t-FAIL") + "\n"
                                    g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                    tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                                    g.write('\n'+str(tempo)+"[Teste]Recebido:\'"+recebidoterminal+"\' Status:"+str(terminalpass))
                                    g.close()
                                tempo = strftime("%d/%m/%Y-%H:%M:%S",localtime(time.time()))
                                f = open("data/Log_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                                f.write("\n"+str(tempo)+","+str(terminal.isOpen())+"," + str(recebidoterminal)+","+str(terminalpass)+","+ str(Rs422.isOpen())+","+ str(recebidoRs422)+","+str(Rs422pass)+","+ str(Rs422pass and terminalpass))
                                f.close()
                                send+= "========================================"
                                printt(send,window,TestNumber)
                                
                                                        
                            
                    else: # Caso a porta do terminal tenha sido fechada
                        report(False,ComControler[TestNumber - 1])
                        authorization[TestNumber-1] = False
                        ComControler[TestNumber-1] = " "
                        configureport = False
                        port = ComControler[TestNumber - 1]
                        terminal = serial.Serial(port, baudrate=9600,timeout = 0.5)#timeout=1
                        g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                        tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                        g.write('\n'+str(tempo)+"[Teste]Porta COM fechada")
                        g.close()
                    if kill:
                        break
                    else:
                        continue
                    
            except:
                printt("\nFalha de Comunicação!                 "+carregando(estado)+"\n"+str(ComControler)+"\n"+str(authorization)+"\n\n",window,TestNumber)
                estado = estado + 1
                if estado == 4 :
                    estado = 0
                printt("========================================",window,TestNumber)
                listports = []
                ports = serial.tools.list_ports.comports(include_links=False)
                for j in ports :
                    listports +=[j.device]
                tempo = strftime("%d/%m/%Y-%H:%M:%S",localtime(time.time()))
                if 'g' in locals():
                    try:
                        if g.isOpen():
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            g.write('\n'+str(tempo)+traceback.format_exc())
                            g.close()
                        else:
                            g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            g.write('\n'+str(tempo)+traceback.format_exc())
                            g.close()
                    except:
                        print("Falha na documentação do erro em log Console")
                if 'f' in locals():
                    try:
                        if f.isOpen():
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            f.write("\n"+str(tempo)+","+str(True if port in listports else False)+"," + str(recebidoterminal)+","+str(terminalpass)+","+ str(True if portrs in listports else False)+","+ str(recebidoRs422)+","+str(Rs422pass)+","+ str(Rs422pass and terminalpass))
                            f.close()
                        else:
                            f = open("data/Log_test_vibracao"+str(TestNumber)+" "+tempo_arquivo+".txt", "a")
                            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
                            f.write("\n"+str(tempo)+","+str(True if port in listports else False)+"," + str(recebidoterminal)+","+str(terminalpass)+","+ str(True if portrs in listports else False)+","+ str(recebidoRs422)+","+str(Rs422pass)+","+ str(Rs422pass and terminalpass))
                            f.close()
                    except:
                        print("Falha na documentação do erro na Tabela de teste")
                        f.close()
                if 'Rs422' in locals():
                    Rs422.close()
                if 'terminal' in locals():
                    terminal.close()
                authorization[TestNumber-1] = False
                ComControler[TestNumber-1] = " "
                time.sleep(1)
                if not(kill):
                    continue
                else:
                    break
        else:
            printt("\nConfigurando Porta!                 "+carregando(estado)+"\n"+str(ComControler)+"\n"+str(authorization)+"\n\n",window,TestNumber)
            estado = estado + 1
            if estado == 4 :
                estado = 0
            printt("========================================",window,TestNumber)
            g = open("data/Log_Console_test_vibracao"+str(TestNumber)+eixo+tempo_arquivo+".txt", "a")
            tempo = strftime("[%d/%m/%Y-%H:%M:%S]",localtime(time.time()))
            g.write('\n'+str(tempo)+"[Teste]Tentativa de configuração da Porta COM")
            g.close()
            time.sleep(1)
            if not(kill):
                continue
            else:
                break
            
#------------------------------------------------------------------------------------------------------Fim do teste 











#------------------------------------------------------------------------------------------------------Inicio da interface

# Class holding the button graphic info. At this time only the state is kept
    
    
# Main function that creates the layout, window and has event loop
sg.theme('DarkBlue14')

Texto_eixos = 'XYZ'
def main():
    global ComControler
    global authorization
    global kill
    eixos = ['','X','Y','Z']
    
    
    Title_layout = [[sg.Text('Teste de Vibração Terminal Dual',size=(95,1),justification = "center",text_color='white',background_color = "royalblue4")]]
    
    cbox1_layout = [[sg.Text('Terminal Dual 1- Eixo:',size=(17,1),justification = "left",text_color='white',background_color = "royalblue4"),sg.Combo(eixos, size=(5, 4), key='-EIXO1-',tooltip ="Eixo de Vibração",enable_events = True)],
                    [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(40,6),font=("Lucida Console", 10),do_not_clear = False)]]
    
    cbox2_layout = [[sg.Text('Terminal Dual 2- Eixo:',size=(17,1),justification = "left",text_color='white',background_color = "royalblue4"),sg.Combo(eixos, size=(5, 4), key='-EIXO2-',tooltip ="Eixo de Vibração",enable_events = True)],
                    [sg.MLine(key='-ML2-'+sg.WRITE_ONLY_KEY, size=(40,6),font=("Lucida Console", 10),do_not_clear = False)]]
    
    cbox3_layout = [[sg.Text('Terminal Dual 3- Eixo:',size=(17,1),justification = "left",text_color='white',background_color = "royalblue4"),sg.Combo(eixos, size=(5, 4), key='-EIXO3-',tooltip ="Eixo de Vibração",enable_events = True)],
                    [sg.MLine(key='-ML3-'+sg.WRITE_ONLY_KEY, size=(40,6),font=("Lucida Console", 10),do_not_clear = False)]]

    Button_layout = [[sg.Button(k="Start",button_text ="Carregando",disabled = True),sg.Button(k="Stop",button_text ="Parar",disabled = True)]]

    layout = [[sg.Column(Title_layout,justification = 'center',background_color = "royalblue4",size = (1070,30))],

              [sg.Column(cbox1_layout,justification = 'center',background_color = "royalblue4",size = (350,150)),sg.Column(cbox2_layout,justification = 'center',background_color = "royalblue4",size = (350,150)),sg.Column(cbox3_layout, background_color = "royalblue4",size = (350,150))],

              [sg.Column(Button_layout,element_justification  = 'center',background_color = "royalblue4",size = (1070,80))]]



    window = sg.Window('Teste de Vibração Terminal Dual', layout, font='_ 14', finalize=True,element_justification='c')
    Conf = threading.Thread(target=configports, args=(window,), daemon=True).start()
    # Iniciando a Configuração de portas de cada uma das unidades.
   
    
    while True:             # Event Loop
        try:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break 
            #print("Event:",event)
            #print("Values:",values)
            noteixos =''
            Addineixos =''
            #print(event)
            if 'EIXO' in event:
                if values.get('-EIXO1-') != '':
                    noteixos += values.get('-EIXO1-')
                if values.get('-EIXO2-') != '':
                    noteixos += values.get('-EIXO2-')
                if values.get('-EIXO3-') != '':
                    noteixos += values.get('-EIXO3-')
                #print(noteixos)
                for i in Texto_eixos:
                    if not(i in noteixos):
                         Addineixos +=i
                #print(Addineixos)
                eixos = ['']
                for j in Addineixos:
                    eixos += [j]
                #print("eixos:",eixos)
                window['-EIXO1-'].update(values.get('-EIXO1-'),values = eixos)
                window['-EIXO2-'].update(values.get('-EIXO2-'),values = eixos)
                window['-EIXO3-'].update(values.get('-EIXO3-'),values = eixos)
                
                
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            # Where all the magic happens. 2 things happen when button is clicked
            # 1. The state toggles
            # 2. The buton graphic changes
            if 'Start' in event:
                kill = False
                if (values.get('-EIXO1-')!= '' and values.get('-EIXO2-')!= '' and values.get('-EIXO3-')!= ''):
                    window['-EIXO1-'].update(values.get('-EIXO1-'),values = eixos,disabled = True)
                    window['-EIXO2-'].update(values.get('-EIXO2-'),values = eixos,disabled = True)
                    window['-EIXO3-'].update(values.get('-EIXO3-'),values = eixos,disabled = True)
                    window['Start'].update(disabled = True)
                    window['Stop'].update(disabled = False)
                    t1 = threading.Thread(target=TestUnit, args=(33,1,values.get('-EIXO1-'), window,), daemon=True).start()
                    t2 = threading.Thread(target=TestUnit, args=(34,2,values.get('-EIXO2-'), window,), daemon=True).start()
                    t3 = threading.Thread(target=TestUnit, args=(35,3,values.get('-EIXO3-'), window,), daemon=True).start()
                else:
                    sg.popup('Defina os eixos de vibração!',title = '')
            
            if 'Stop' in event:
                eixos = ['','X','Y','Z']
                window['-EIXO1-'].update('',values = eixos,disabled = False)
                window['-EIXO2-'].update('',values = eixos,disabled = False)
                window['-EIXO3-'].update('',values = eixos,disabled = False)
                window['Start'].update(disabled = False)
                window['Stop'].update(disabled = True)
                kill = True
                #window.close()
                #break # fecha quando pede para PARAR
                #stop_threads = True
        except:
            continue
        
    window.close()
#------------------------------------------------------------------------------------------------------Fim da interface

# Iniciando o Programa
if __name__ == '__main__':
    main()

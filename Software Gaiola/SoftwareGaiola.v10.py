# Autor principal: Thiago Henrique Ferreira da Silva-LODESTAR-UNB
# Colaboração: Danilo Queirós de Freitas e Gabriel Lima Sertão

# Colaboração:
# Este código apresenta a função TLEtoMAG, que retorna 3 strigs no formato JSON
# com os valores de campo magnético nos eixos X, Y e Z para cada timestamp, 
# experimentados pelo satélite de número de identificação n, especificando os 
# tempos de observação e o período de amostragem em minutos.

# Documentação das bibliotecas:
# https://rhodesmill.org/skyfield/earth-satellites.html
# https://rhodesmill.org/skyfield/time.html
# https://github.com/klaundal/ppigrf




import serial
from threading import *  
import math
import time
import serial.tools.list_ports
import traceback
import pyvisa
import pygpib as gpib
import PySimpleGUI as sg
import threading
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from datetime import datetime
import json



sg.theme('DarkBlue14')

rm = pyvisa.ResourceManager()

ports = [comport.device for comport in serial.tools.list_ports.comports()]
arduino =[]
magnet =[]
calimagnet = []
calibob =[0,0,0,0,0,0,0,0,0,0,0,0] #A,B,C,D,E,F,G,H,I,H0X,H0Y,H0Z
a =""
Bref = [0.0,0.0,0.0]    # Referência de Campo que se tem como objetivo alcançar
V = [0.0,0.0,0.0]       # Tensão atual das fontes.
Hread = [0.0,0.0,0.0] 
kd = 0.0                # Contstante proporcional do controle de malha fechada
ki = 0.0                # Contstante integral do controle de malha fechada
T = 1.0                 # Tempo de amostragem do controle em malha fechada
Estimardor = True       # Cria uma estimativa se a diferença de alguma componente de campo se 2 uT.
Control = False
VecBxyz = []            # Vetor de Campo magnético que será simulado na Gaiola.
serialmag = Semaphore(1)
try:
    ga = rm.open_resource('GPIB2::5::INSTR')
    gb = rm.open_resource('GPIB0::5::0::INSTR')
    gc = rm.open_resource('GPIB1::5::INSTR')
    time.sleep(4)
    gb.write(f"CURR 6")
    gc.write(f"ISET 6")
    ga.write(f"ISET 6")
    
except:
    a ="Falha de comunicação com as fontes,\npor favor checar os cabos e reiniciar o software!"

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def corrx(adcx):
    resp = 5 + 10*(adcx - 576)/(132)
    return resp
def corry(adcy):
    resp = 5 + 10*(adcy - 577)/(134)
    return resp
def corrz(adcz):
    resp = -5 - 10*(adcz - 577)/(134)
    return resp

def JSON_to_Vector(arquivoX,arquivoY,arquivoZ):
    global VecBxyz
    try:
        datax = open(arquivoX,"r")
        datay = open(arquivoY,"r")
        dataz = open(arquivoZ,"r")
    except:
        ("Falha de leitura de arquivo")
    VecBx = json.load(datax)
    VecBy = json.load(datay)
    VecBz = json.load(dataz)
    stringdata = VecBx[0]["Satellite Timestamp (UTC)"]   #2022-07-02 01:24:25.061Z
    d = datetime.strptime(stringdata[:-5], "%Y-%m-%d %H:%M:%S")
    floatdata0 = time.mktime(d.timetuple())
    if not(len(VecBx) == len(VecBy) == len(VecBz)):
        print("Falha do tamanho dos vetores")
        return
    for i in range(len(VecBx)): # Checar se o formato do arquivo está adequado e se o Timestamp dos arquiveos bates e converter de mG para uT.
        try:
            if len(VecBx[i]["Satellite Timestamp (UTC)"]) == len(VecBy[i]["Satellite Timestamp (UTC)"]) == len(VecBz[i]["Satellite Timestamp (UTC)"]):
                stringdata = VecBx[i]["Satellite Timestamp (UTC)"]   #2022-07-02 01:24:25.061Z
                d = datetime.strptime(stringdata[:-5], "%Y-%m-%d %H:%M:%S")
                floatdata = time.mktime(d.timetuple())
                VecBxyz += [{"Bx":0.1*VecBx[i]["Value (mG)"],"By":0.1*VecBy[i]["Value (mG)"],"Bz":0.1*VecBz[i]["Value (mG)"],"t":(floatdata - floatdata0)}]
            else:
                print("Falha na timestamp.")
                return
        except:
            print("Falha no formato do arquivo.")
            return
    print("Importação bem sucedida")

def Refcontroler():
    global VecBxyz
    global Href
    global Control
    t0 = time.time()
    for B in VecBxyz:
        Bref[0],Bref[1],Bref[2] = B["Bx"],B["By"],B["Bz"] #realizando a mudânça de referência.
        #Bset(B["Bx"],B["By"],B["Bz"])
        while(time.time()-t0 < B["t"]):
            time.sleep(0.1)
    print("Simulação finalizada!")
    Control = False
def magnetwritereadline(bytesmag):
    #serialmag.acquire()
    for i in range(15):
        #try:
        magnet.write(bytesmag)
        time.sleep(0.5)
        data = magnet.read(50) #50
        if len(data) != 28:
            print("------------------------Falha de serial")
            print(data, len(data))
            time.sleep(1)
            #magnet.write(b'*00C\r*00C\r')
            continue
        else:
            break
    #serialmag.release()
        #except:
            #print("Falha na Comunicação do magnetômetro"+i)
            #if i==4:
                #serialmag.release()
    return data
##def magnetreadline():
##    serialmag.acquire()
##    for i in range(5):
##        try:
##            data = magnet.readline()
##            #print(data,"||",len(data))
##            if len(data)!= 28:
##                continue
##            serialmag.release()
##            break
##        except:
##            print("Falha na Comunicação do magnetômetro"+i)
##            if i ==4:
##                serialmag.release()
##    return data
def magnetread(data):
    
    print(data)
    global magnet
    global Hread
    global calimagnet
    if (len(calimagnet) <6): #Caso o magnetômetro ainda não tenha sido calibrado
        linha =data.decode()
        linha = linha.split("\r")
        print(linha)
        linha = linha[0]
        print(linha)
        dadox = linha[0:7].replace(" ","").replace(",","")
        dadoy = linha[8:16].replace(" ","").replace(",","")
        dadoz = linha[18:25].replace(" ","").replace(",","")
        dadox = float(dadox)/150
        dadoy = float(dadoy)/150
        dadoz = float(dadoz)/150
        Hread[0],Hread[1],Hread[2] = dadox, dadoy, dadoz
        
        #print(f"Bx:{dadox:.2f}uT\tBy:{dadoy:.2f}uT\tBz:{dadoz:.2f}uT")
        read = f"{dadox}\t{dadoy}\t{dadoz}\n"
    else:
        linha = data.decode() #Caso o magnetômetro ainda já tenha sido calibrado
        dadox = linha[0:7].replace(" ","").replace(",","")
        dadoy = linha[8:16].replace(" ","").replace(",","")
        dadoz = linha[18:25].replace(" ","").replace(",","")
        dadox = float(dadox)/150
        dadoy = float(dadoy)/150
        dadoz = float(dadoz)/150
        Hread[0],Hread[1],Hread[2] = (dadox-calimagnet[0])/calimagnet[3],(dadoy-calimagnet[1])/calimagnet[4],(dadoz-calimagnet[2])/calimagnet[5]
        #print(f"Bx:{(dadox-calimagnet[0])/calimagnet[3]:.2f}uT\tBy:{(dadoy-calimagnet[1])/calimagnet[4]:.2f}uT\tBz:{(dadoz-calimagnet[2])/calimagnet[5]:.2f}uT")
        read = f"{(dadox-calimagnet[0])/calimagnet[3]}\t{(dadoy-calimagnet[1])/calimagnet[4]}\t{(dadoz-calimagnet[2])/calimagnet[5]}\n"

    return read
#--------------------------------------------------------------------------CONTROLE DO CAMPO MAGNETICO NA GAIOLA

def Magcontroler(data,window): # Essa função tem por objetivo controlar o campo magnético em cada um dos eixos.
    global Hread
    global Bref
    global Control
    global V
    global kd
    global ki
    global T
    global Estimardor
    global calimagnet
    global calibob
    sumErrx = 0.0
    sumErry = 0.0
    sumErrz = 0.0
    t0 = time.time()
    log = open('log.txt','a')
    while Control == True:     # Iniciar o controle do sistema sempre que a variável Control estiver em True.
        try:
            data = magnetwritereadline(b'*00P\r')
            Bx,By,Bz = magnetread(data).split("\t")
            #print("Bx:",Bx,"By:",By,"Bz:",Bz)
            Bx,By,Bz =float(Bx),float(By),float(Bz)
            t = time.time()
            log.write(f"{t-t0}\t{Bref[0]}\t{Hread[0]}\t{Bref[1]}\t{Hread[1]}\t{Bref[2]}\t{Hread[2]}\n".replace(".",","))
            print(f"{t-t0}\t{Bref[0]}\t{Hread[0]}\t{Bref[1]}\t{Hread[1]}\t{Bref[2]}\t{Hread[2]}".replace(".",","))
            Hread[0],Hread[1],Hread[2] = Bx,By,Bz
            window['-HX-'].update(value = f"Hx = {Hread[0]:.2f} [uT]")
            window['-HY-'].update(value = f"Hy = {Hread[1]:.2f} [uT]")
            window['-HZ-'].update(value = f"Hx = {Hread[2]:.2f} [uT]")
            if ((abs(Bref[0] - Bx)>3) or (abs(Bref[1] - By)>3) or (abs(Bref[2] - Bz)>3))and Estimardor == True : #and( )
                Bset(Bref[0],Bref[1],Bref[2])
            else:
                ex = Bref[0] - Bx
                ey = Bref[1] - By
                ez = Bref[2] - Bz
                sumErrx += T*ex
                sumErry += T*ey
                sumErrz += T*ex
                Vx = V[0] + (kd*ex + ki*sumErrx)/calibob[0]
                Vy = V[1] + (kd*ey + ki*sumErry)/calibob[4]
                Vz = V[2] + (kd*ez + ki*sumErrz)/calibob[8]
                Vset(Vx,Vy,Vz)
                #window['-VFX-'].update(value = f"Vx = {V[0]:.2f} [V]")
                #window['-VFY-'].update(value = f"Vy = {V[1]:.2f} [V]")
                #window['-VFZ-'].update(value = f"Vz = {V[2]:.2f} [V]")
        except:
            print("falha no controlador")
            continue
        time.sleep(T)
    log.close()
            
        
#--------------------------------------------------------------------------CALIBRAÇÃO DO MAGNETÔMETRO
'''
Desejamos encontrar x0, y0, z0, a,b,c tais que ajustem a seguinte equação:

(x-x0)**2/a**2 + (y-y0)**2/b**2 + (z-z0)**2/c**2 = R**2

x,y,z são as componentes de campo coletadas do magnetômetro e R é o valor do módulo esperado no ambiente. 



1) Resolver o caso para os Mínimos Quadrados com a finalidade de encontrar x0, y0, z0.

M  =[[ X**2   , X*Y    , X*Z    , -X*Y**2    , -X*Z**2    , X   ],
     [ Y*X    , Y**2   , Y*Z    , -Y**3      , -Y*Z**2    , Y   ],
     [ Z*X    , Z*Y    , Z**2   , -Z*Y**2    , -Z**3      , Z   ],
     [ X*Y**2 , Y**3   , Z*Y**2 , -Y**4      , -Z**2*Y**2 , Y**2],
     [ X*Z**2 , Y*Z**2 , Z**3   , -Y**2*Z**2 , -Z**4      , Z**2],
     [ X      , Y      , Z      , -Y**2      , -Z**2      , 1   ]]

N = [ X**3      , Y*X**2    , Z*X**2    , Y**2*X**2 , Z**2*X**2 , X**2  ]

Note que:
N =M*W => M**(-1) * N = W

W = [ A , B , C , D , E , F]

Assim,
x0 = A/2
y0 = B/(2*D)
z0 = C/(2*E)

2) Reajustar as amostras de forma que x' = x - x0; y' = y - y0; z' = z - z0;

Desejamos encontrar a,b,c tais que ajustem a seguinte equação:

(x')**2/a**2 + (y')**2/b**2 + (z')**2/c**2 = R**2

x',y',z' são as componentes de campo coletadas e reajustadas e R é o valor do módulo esperado no ambiente.

Resolver o caso para os Mínimos Quadrados com a finalidade de encontrar a, b, c.

M = [[ Y**4      , Z**2*Y**2 , -Y**2],
     [ Y**2*Z**2 , Z**4      , -Z**2],
     [ Y**2      , Z**2      , -1   ]]

N = [-X**2*Y**2, -X**2*Z**2 ,-X**2]

Note que:

N = M*W => M**(-1)*N = W

W = [ G, H, I]

Assim,

a = (I/(R**2))**(0.5)
b = (I/(G*R**2))**(0.5)
c = (I/(H*R**2))**(0.5)

Logo obteve-se o valor de x0,y0,z0,a,b,c e pode-se corrigir as medidas do sensor com as seguinte fórmula.

xr = (x-x0)/a
yr = (y-y0)/b
zr = (z-z0)/c
'''
def caliB(eixo,window):
    global calibob
    print("------------------------------------------")
    print("Calibração iniciada!....")
    Vset(0,0,0)
    time.sleep(2)
    H_0 = [0.0,0.0,0.0]
    print("Capturando as leituras do magnetômetro....")
    for _ in range(50):
        data = magnetwritereadline(b'*00P\r')
        x,y,z = magnetread(data).split("\t")
        #print("x ",x," y:",y," z:",z)
        H_0[0] += float(x)
        H_0[1] += float(y)
        H_0[2] += float(z)
        time.sleep(0.5)
    H_0[0] = H_0[0]/50
    H_0[1] = H_0[1]/50
    H_0[2] = H_0[2]/50
    print("------------------------------------------")
    print("Calibrando a Fonte X....")
    print("H_0:",H_0)
    calibob[9]  = H_0[0]
    calibob[10] = H_0[1]
    calibob[11] = H_0[2] # Definição do vetor ambiente ( campo magnético da terra)
    if eixo in ["x","y","z"]:
        Vset(-10,0,0)
        time.sleep(0.5)
        Vset(-20,0,0)
        time.sleep(0.5)
        Vset(-30,0,0)
        time.sleep(0.5)
        Vset(-40,0,0)
        time.sleep(2)
        leitura = ""
        for x in range(0,81,4):
            window['PROGRESS_2'].update(x+1)
            Vset(x-40,0,0)
            time.sleep(1)
            data = magnetwritereadline(b'*00P\r')
            resp = magnetread(data)
            leitura += str(x-40)+"\t"+ resp                            
        SA,SD,SG,S = 0.0,0.0,0.0,0.0
        for linha in leitura.split("\n"):
            if linha == "":
                continue
            SA += (float(linha.split("\t")[1])-H_0[0])*float(linha.split("\t")[0])
            SD += (float(linha.split("\t")[2])-H_0[1])*float(linha.split("\t")[0])
            SG += (float(linha.split("\t")[3])-H_0[2])*float(linha.split("\t")[0])
            S  += (float(linha.split("\t")[0]))**2
        A = SA/S
        D = SD/S
        G = SG/S
        calibob[0] = A
        calibob[3] = D
        calibob[6] = G
        print("A:{A:.2f}","D:{D:.2f}","G:{G:.2f}",sep="\n")
        print(leitura)
        Vset(0,0,0)
        print("------------------------------------------")
        window['-IMG7-'].update(image_data = ok)
    #elif eixo == "y": ------------------------------------------------------- Calibração Bobina Y
        print("Calibrando a Fonte Y....")
        Vset(0,-10,0)
        time.sleep(0.5)
        Vset(0,-20,0)
        time.sleep(0.5)
        Vset(0,-30,0)
        time.sleep(0.5)
        Vset(0,-40,0)
        time.sleep(2)
        leitura = ""
        for x in range(0,81,4):
            window['PROGRESS_3'].update(x+1)
            Vset(0,x-40,0)
            time.sleep(1)
            data = magnetwritereadline(b'*00P\r')
            resp = magnetread(data)
            leitura += str(x-40)+"\t"+ resp
        SB,SE,SH,S = 0.0,0.0,0.0,0.0
        for linha in leitura.split("\n"):
            if linha == "":
                continue
            SB += (float(linha.split("\t")[1])-H_0[0])*float(linha.split("\t")[0])
            SE += (float(linha.split("\t")[2])-H_0[1])*float(linha.split("\t")[0])
            SH += (float(linha.split("\t")[3])-H_0[2])*float(linha.split("\t")[0])
            S  += (float(linha.split("\t")[0]))**2
        B = SB/S
        E = SE/S
        H = SH/S
        calibob[1] = B
        calibob[4] = E
        calibob[7] = H
        print(f"B:{B:.2f}\nE:{E:.2f}\nH:{H:.2f}",sep="\n")
        print(leitura)
        Vset(0,0,0)
        print("------------------------------------------")
        window['-IMG8-'].update(image_data = ok)
    #elif eixo == "z": ------------------------------------------------------- Calibração Bobina Z
        print("Calibrando a Fonte Z....")
        Vset(0,0,-10)
        time.sleep(0.5)
        Vset(0,0,-20)
        time.sleep(0.5)
        Vset(0,0,-30)
        time.sleep(0.5)
        Vset(0,0,-40)
        time.sleep(2)  
        leitura = ""
        for x in range(0,81,4):
            window['PROGRESS_4'].update(x+1)
            Vset(0,0,x-40)
            time.sleep(1)
            data = magnetwritereadline(b'*00P\r')
            resp = magnetread(data)
            leitura += str(x-40)+"\t"+ resp
        SC,SF,SI,S = 0.0,0.0,0.0,0.0
        for linha in leitura.split("\n"):
            if linha == "":
                continue
            SC += (float(linha.split("\t")[1])-H_0[0])*float(linha.split("\t")[0])
            SF += (float(linha.split("\t")[2])-H_0[1])*float(linha.split("\t")[0])
            SI += (float(linha.split("\t")[3])-H_0[2])*float(linha.split("\t")[0])
            S  += (float(linha.split("\t")[0]))**2
        C = SC/S
        F = SF/S
        I = SI/S
        calibob[2] = C
        calibob[5] = F
        calibob[8] = I
        print(f"C:{C:.2f}\tF:{F:.2f}\tI:{I:.2f}",sep="\n")
        print(leitura)
        Vset(0,0,0)
        print("------------------------------------------")
        window['-IMG9-'].update(image_data = ok)
        print(f"A:{A:.2f}\tB:{B:.2f}\tC:{C:.2f}")
        print(f"D:{D:.2f}\tE:{E:.2f}\tF:{F:.2f}")
        print(f"G:{G:.2f}\tH:{H:.2f}\tI:{I:.2f}")
        print("H_0:",H_0)
        print("Calibração finalizada!")
    
def calibramag(R,window):
    global calimagnet    
    leitura = ""
    #data = magnetwritereadline(b'*00WE *00ZN\r')
    for i in range(200):
        window['PROGRESS_1'].update(i+1)
        data = magnetwritereadline(b'*00P\r')
        #time.sleep(0.5)
        linha =data.decode()
        dadox = linha[0:7].replace(" ","").replace(",","")
        dadoy = linha[8:16].replace(" ","").replace(",","")
        dadoz = linha[18:25].replace(" ","").replace(",","")
        dadox = float(dadox)/150
        dadoy = float(dadoy)/150
        dadoz = float(dadoz)/150
        read = str(dadox) + "\t"+  str(dadoy) + "\t"+ str(dadoz) + "\n"
        leitura += read
        print(f"{dadox:.2f}\t{dadoy:.2f}\t{dadoz:.2f}")
    D = []
    for linha in leitura.split("\n"):
        if linha == "":
            continue
        #print(linha)
        Bx = float(linha.split("\t")[0])
        By = float(linha.split("\t")[1])
        Bz = float(linha.split("\t")[2])
        D += [[Bx,By,Bz]]
    M = np.array([[ 0.0    , 0.0    , 0.0      , 0.0          , 0.0          , 0.0   ],
                  [ 0.0    , 0.0    , 0.0      , 0.0          , 0.0          , 0.0   ],
                  [ 0.0    , 0.0    , 0.0      , 0.0          , 0.0          , 0.0   ],
                  [ 0.0    , 0.0    , 0.0      , 0.0          , 0.0          , 0.0   ],
                  [ 0.0    , 0.0    , 0.0      , 0.0          , 0.0          , 0.0   ],
                  [ 0.0    , 0.0    , 0.0     , 0.0           , 0.0          , 0.0   ]])
    
    N = np.array([0.0,     0.0,     0.0,     0.0,     0.0,     0.0])
    
    for B in D:
        X = float(B[0])
        Y = float(B[1])
        Z = float(B[2])
        M += np.array([[ X**2   , X*Y    , X*Z    , -X*Y**2    , -X*Z**2    , X   ],
                       [ Y*X    , Y**2   , Y*Z    , -Y**3      , -Y*Z**2    , Y   ],
                       [ Z*X    , Z*Y    , Z**2   , -Z*Y**2    , -Z**3      , Z   ],
                       [ X*Y**2 , Y**3   , Z*Y**2 , -Y**4      , -Z**2*Y**2 , Y**2],
                       [ X*Z**2 , Y*Z**2 , Z**3   , -Y**2*Z**2 , -Z**4      , Z**2],
                       [ X      , Y      , Z      , -Y**2      , -Z**2      , 1.0 ]])
        
        N += np.array([ X**3 , Y*X**2 , Z*X**2 , Y**2*X**2 , Z**2*X**2 , X**2 ])
    C = np.linalg.solve(M, N)
    X0 = C[0]/2 
    Y0 = C[1]/(2*C[3])
    Z0 = C[2]/(2*C[4])
    #print(D[0])
    #print(X0)
    #print(Y0)
    #print(Z0)
    for i in range(len(D)):
        D[i][0], D[i][1], D[i][2] = D[i][0] - X0, D[i][1] - Y0, D[i][2] - Z0
    #print(D[0])
    M = np.array([[ 0.0 , 0.0  , 0.0],
                  [ 0.0 , 0.0  , 0.0],
                  [ 0.0 , 0.0  , 0.0]])
        
    N = np.array([0.0 , 0.0  , 0.0 ])
    for B in D:
        X = float(B[0])
        Y = float(B[1])
        Z = float(B[2])
        M += np.array([[ Y**4      , Z**2*Y**2 , -Y**2],
                       [ Y**2*Z**2 , Z**4      , -Z**2],
                       [ Y**2      , Z**2      , -1.0  ]])
        
        N += np.array([-X**2*Y**2, -X**2*Z**2 ,-X**2])
        
    C = np.linalg.solve(M, N)
    #print(C)
    a = (C[2]/(R**2))**0.5
    b = (C[2]/(C[0]*R**2))**0.5
    c = (C[2]/(C[1]*R**2))**0.5
    for i in range(len(D)):
        D[i][0], D[i][1], D[i][2] = D[i][0]/a, D[i][1]/b, D[i][2]/c
    #print(D[0])
    print("X0:",X0,"\nY0:",Y0,"\nZ0:",Z0,"\na:",a,"\nb:",b,"\nc:",c)
    if math.isnan (X0) or math.isnan (Y0) or math.isnan (Z0) or math.isnan (a) or math.isnan (b) or math.isnan (c):
        window['-IMG6-'].update(image_data = error)
    else:
        window['-IMG6-'].update(image_data = ok)
    calimagnet = [X0,Y0,Z0,a,b,c][:]
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Criar um V_func que retorna Vx,Vy,Vz
            
def Vx_func(Bx_gauss):
    global calibob
    if(calibob[0] ==0 or calibob[1] ==0 or calibob[2] ==0 or calibob[3] ==0 or calibob[4] ==0 or calibob[5] ==0):
        sg.Popup('Por favor, calibrar as bobinas!', keep_on_top=True)
    else:
        return (calibob[0]*Bx_gauss + calibob[1])
def Vy_func(By_gauss):
    global calibob
    if(calibob[0] ==0 or calibob[1] ==0 or calibob[2] ==0 or calibob[3] ==0 or calibob[4] ==0 or calibob[5] ==0):
        sg.Popup('Por favor, calibrar as bobinas!', keep_on_top=True)
    else:
        return (calibob[2]*By_gauss + calibob[3])
def Vz_func(Bz_gauss):
    global calibob
    if(calibob[0] ==0 or calibob[1] ==0 or calibob[2] ==0 or calibob[3] ==0 or calibob[4] ==0 or calibob[5] ==0):
        sg.Popup('Por favor, calibrar as bobinas!', keep_on_top=True)
    else:
        return (calibob[4]*Bz_gauss + calibob[5])
def Inv(Vx,Vy,Vz):# Função responsável por inverter o sentido das correntes. Primeiro Digito z, segundo digito y, terceiro digito x (Podemos inverter futuramente no código do Arduino)
    if Vx < 0:
        if Vy <0:
            if Vz < 0:
                return b'$INV111;'
            else:
                return b'$INV011;'
        else:
            if Vz < 0:
                return b'$INV101;'
            else:
                return b'$INV001;'
    else:
        if Vy <0:
            if Vz < 0:
                return b'$INV110;'
            else:
                return b'$INV010;'
        else:
            if Vz < 0:
                return b'$INV100;'
            else:
                return b'$INV000;'

def Vset(Vx,Vy,Vz):
    global V
    #print(f"Tensões de Referência:\n Vx = {Vx:.3f} V | Vy = {Vy:.3f} V | Vz = {Vz:.3f} V ")
    if (Vx >40 or Vx >40 or Vz > 40):
        print("Falha de tensão! Tensão maior que 40V")                    
    if abs(Vx)>40:
        if Vx>0:
            Vx = 40
        else:
            Vx = -40
    if abs(Vy)>40:
        if Vy>0:
            Vy = 40
        else:
            Vy = -40
    if abs(Vz) > 40:
        if Vz>0:
            Vz = 40
        else:
            Vz = -40
    V  = [Vx,Vy,Vz]
    if (abs(Vx) >40 or abs(Vx) >40 or abs(Vz) > 40):
        print(f"Tensões Corrigidas:\n Vx = {Vx:.2f} V | Vy = {Vy:.2f} V | Vz = {Vz:.2f} V ")
    ga.write(f"VSET {abs(Vy):.5f}") 
    gb.write(f"VOLT {abs(Vz):.5f}")
    gc.write(f"VSET {abs(Vx):.5f}")
    inv = Inv(Vx,Vy,Vz)
    a = arduino.write(inv)
    data = arduino.readline().decode("utf-8").replace(";\r\n","")
    #ix = corrx(int(data.split(" ")[1]))
    #iy = corry(int(data.split(" ")[2]))
    #iz = corrz(int(data.split(" ")[3]))
    #print(f"Correntes Medidas:\n Ix = {ix:.2f} A | Iy = {iy:.2f} A | Iz = {iz:.2f} A ")
    #print(data)

def Bset(Bx,By,Bz):
    global calibob
    global Bref
    global Estimardor
    Bref[0],Bref[1],Bref[2]= Bx,By,Bz
    #print(f"Valores de referência:\n Bx = {Bx} uT | By = {By} uT | Bz = {Bz} uT ")
    M = np.array([[ calibob[0] , calibob[1] , calibob[2]],
                   [ calibob[3] , calibob[4] , calibob[5]],
                   [ calibob[6] , calibob[7] , calibob[8]]])
    
    H = np.array([calibob[9], calibob[10] ,calibob[11]])
    B = np.array([Bx, By ,Bz])
    C = np.linalg.solve(M, B-H)
    Vset(C[0],C[1],C[2])


##while True:
##    num = input("Enter a number: ")
##    value = str(write_read(num))
##    print(value)

    


# Class holding the button graphic info. At this time only the state is kept

# Main function that creates the layout, window and has event loop
def main():
    global Bref
    global Control
    global V
    global kd
    global ki
    global T
    global Estimardor
    global Hread
    global recarregar
    global ok
    global error
    global arduino
    global magnet
    global a
    global calimagnet
    PortasAbertas = [comport.device for comport in serial.tools.list_ports.comports()]
    PortasAbertas += ['']
    Title_layout = [[sg.Text('GAIOLA DE HELMHOLTZ v3.0',font = '_ 30',size=(35,1),justification = "left",text_color='white',background_color = "royalblue4"),sg.Image(data = logo,background_color ="royalblue4", s = (75,75))]]
    cbox1_layout = [[sg.T('CONFIGURAÇÃO', text_color='white',justification = "center")],
                    [sg.T('PONTE H:\t', justification = "center", text_color='white',background_color = "royalblue4"),sg.Combo(PortasAbertas, size=(7, 1), key='-LIST1-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG1-')],
                    [sg.T('MAGNETÔMETRO:\t', justification = "center", text_color='white',background_color = "royalblue4"),sg.Combo(PortasAbertas, key='-LIST2-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG2-')],
                    [sg.T('FONTE A:\t\t', justification = "center", text_color='white',background_color = "royalblue4"),sg.Button(image_data =recarregar,image_size =(32, 32), key = '-IMG3-')],
                    [sg.T('FONTE B:\t\t', justification = "center", text_color='white',background_color = "royalblue4"),sg.Button(image_data =recarregar, key = '-IMG4-')],
                    [sg.T('FONTE C:\t\t', justification = "center", text_color='white',background_color = "royalblue4"),sg.Button(image_data =recarregar, key = '-IMG5-')],
                    [sg.T('CALIBRAÇÃO', text_color='white',justification = "center")],
                    [sg.T('MAGNETÔMETRO:\t', justification = "center", text_color='white',background_color = "royalblue4", key='-LIST6-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG6-')],
                    [sg.ProgressBar(max_value=200, orientation='h', size=(20, 20), key='PROGRESS_1')],
                    [sg.T('BOBINA X:\t', justification = "center", text_color='white',background_color = "royalblue4", key='-LIST7-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG7-')],
                    [sg.ProgressBar(max_value=80, orientation='h', size=(20, 20), key='PROGRESS_2')],
                    [sg.T('BOBINA Y:\t', justification = "center", text_color='white',background_color = "royalblue4", key='-LIST8-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG8-')],
                    [sg.ProgressBar(max_value=80, orientation='h', size=(20, 20), key='PROGRESS_3')],
                    [sg.T('BOBINA Z:\t', justification = "center", text_color='white',background_color = "royalblue4", key='-LIST9-',enable_events = True),sg.Button(image_data =recarregar,key = '-IMG9-')],
                    [sg.ProgressBar(max_value=80, orientation='h', size=(20, 20), key='PROGRESS_4')]]
    
    cbox2_layout = [[sg.T('PROPAGAÇÃO', text_color='white',justification = "center")],
                    [sg.Text('TLE',background_color = "royalblue4", size=(15, 1)), sg.Input(size=(16, 1)), sg.FileBrowse()],
                    [sg.T('OBTENÇÃO DE CAMPO MAGNÉTICO', text_color='white',justification = "center")],
                    [sg.Text('VETOR DE CAMPO X',background_color = "royalblue4", size=(18, 1)), sg.Input(size=(16, 1),key = '-CMPX-'), sg.FileBrowse()],
                    [sg.Text('VETOR DE CAMPO Y',background_color = "royalblue4", size=(18, 1)), sg.Input(size=(16, 1),key = '-CMPY-'), sg.FileBrowse()],
                    [sg.Text('VETOR DE CAMPO Z',background_color = "royalblue4", size=(18, 1)), sg.Input(size=(16, 1),key = '-CMPZ-'), sg.FileBrowse()],
                    [sg.Button('Importar Vetores',key = '-SEND0-'),sg.Button('Iniciar Simulação',key = '-SEND3-')],
                    [sg.T('CAMPO MAGNÉTICO CONSTANTE', text_color='white',justification = "center")],
                    [sg.Text('CAMPO BOBINA X [uT]',background_color = "royalblue4", size=(19, 1)), sg.Input(size=(10, 1),key ='-BX-'),sg.Text('Hx = 0.00 [uT]',background_color = "royalblue4", size=(15, 1),key ='-HX-')],
                    [sg.Text('CAMPO BOBINA Y [uT]',background_color = "royalblue4", size=(19, 1)), sg.Input(size=(10, 1),key ='-BY-'),sg.Text('Hy = 0.00 [uT]',background_color = "royalblue4", size=(15, 1),key ='-HY-')],
                    [sg.Text('CAMPO BOBINA Z [uT]',background_color = "royalblue4", size=(19, 1)), sg.Input(size=(10, 1),key ='-BZ-'),sg.Text('Hz = 0.00 [uT]',background_color = "royalblue4", size=(15, 1),key ='-HZ-')],
                    [sg.Button('Enviar para as Fontes',key = '-SEND1-')],
                    [sg.T('TENSÃO CONSTANTE', text_color='white',justification = "center")],
                    [sg.Text('TENSÃO EM X [V]',background_color = "royalblue4", size=(17, 1)), sg.Input(size=(10, 1),key ='-VX-'),sg.Text('Vx = 0.00 [V]',background_color = "royalblue4", size=(15, 1),key ='-VFX-')],
                    [sg.Text('TENSÃO EM Y [V]',background_color = "royalblue4", size=(17, 1)), sg.Input(size=(10, 1),key ='-VY-'),sg.Text('Vy = 0.00 [V]',background_color = "royalblue4", size=(15, 1),key ='-VFY-')],
                    [sg.Text('TENSÃO EM Z [V]',background_color = "royalblue4", size=(17, 1)), sg.Input(size=(10, 1),key ='-VZ-'),sg.Text('Vz = 0.00 [V]',background_color = "royalblue4", size=(15, 1),key ='-VFZ-')],
                    [sg.Button('Enviar para as Fontes',key = '-SEND2-')],
                    [sg.T('SISTEMA DE CONTROLE DE CAMPO (PI)', text_color='white',justification = "center")],
                    [sg.Text('KD',background_color = "royalblue4", size=(2, 1)), sg.Input(default_text ="0.50",size=(10, 1),key ='-KD-'),sg.Text('KI',background_color = "royalblue4", size=(2, 1)), sg.Input(default_text ="0.47",size=(10, 1),key ='-KI-')],
                    [sg.Text('ESTIMAÇÃO INICIAL',background_color = "royalblue4", size=(23, 1)), sg.Combo(["LIGADO","DESLIGADO"],default_value = "LIGADO", size=(10, 1), key='-ESTIN-',enable_events = True)],
                    [sg.Text('PERÍODO DE AMOSTRAGEM',background_color = "royalblue4", size=(25, 1)), sg.Input(default_text ="2.00",size=(10, 1),key ='-T-',enable_events = True)],
                    [sg.Button('Ligar Sistema de Controle',key = '-CONTROL-')]]
    
    
    cbox3_layout = [[sg.T('SIMULAÇÃO',text_color='white',justification = "center")],
                    [sg.Image(data = mapa,background_color ="royalblue4", s = (350,180))],
                    [sg.Output(size=(45,20))]]
    
    layout = [[sg.Column(Title_layout,justification = 'center',background_color = "royalblue4",size = (1090,85))],

              [sg.Column(cbox1_layout,justification = 'center',background_color = "royalblue4",size = (350,680)),sg.Column(cbox2_layout,justification = 'center',background_color = "royalblue4",size = (360,680)),sg.Column(cbox3_layout, background_color = "royalblue4",size = (360,680))]]

    window = sg.Window('GAIOLA DE HELMOTZ v3.0', layout, font='_ 8',resizable = True, finalize=True,auto_size_text = True, auto_size_buttons = True)
    if a != "":
        print(a)
    while True:             # Event Loop
        #PortasAbertas = [comport.device for comport in serial.tools.list_ports.comports()]
        #PortasAbertas += ['']
        #print(PortasAbertas)
        event, values = window.read(timeout = 100)#
        window['-HX-'].update(value = f"Hx = {Hread[0]:.2f} [uT]")
        window['-HY-'].update(value = f"Hy = {Hread[1]:.2f} [uT]")
        window['-HZ-'].update(value = f"Hz = {Hread[2]:.2f} [uT]")
        window['-VFX-'].update(value = f"Vx = {V[0]:.2f} [V]")
        window['-VFY-'].update(value = f"Vy = {V[1]:.2f} [V]")
        window['-VFZ-'].update(value = f"Vz = {V[2]:.2f} [V]")
        window['-LIST1-'].update(value = values["-LIST1-"],values = PortasAbertas)
        window['-LIST2-'].update(value = values["-LIST2-"],values = PortasAbertas)
        if '-ESTIN-' in event:
            if values['-ESTIN-'] == "LIGADO":
                Estimardor = True
            else:
                Estimardor = False
        if '-LIST1-' in event:
            if arduino != []:
                try:
                    arduino.close()
                    arduino = serial.Serial(port=values["-LIST1-"], baudrate=9600, timeout=1)
                    time.sleep(1)
                    print("Ponte H configurada com sucesso")
                except:
                    print("Falha na Comunicação da Ponte H")
            else:
                try:
                    arduino = serial.Serial(port=values["-LIST1-"], baudrate=9600, timeout=1)
                    time.sleep(1)
                    print("Ponte H configurada com sucesso")
                except:
                    print("Falha na Comunicação da Ponte H")
        if '-SEND0-' in event:
            arquivoX = values['-CMPX-']
            arquivoY = values['-CMPY-']
            arquivoZ = values['-CMPZ-']            
            t4 = threading.Thread(target=JSON_to_Vector, args=(arquivoX,arquivoY,arquivoZ,),daemon=True).start()
        if '-SEND3-' in event:
            #LIGANDO O SITEMA DE ATUAÇÃO
            if window['-CONTROL-'].get_text() == 'Ligar Sistema de Controle':
                window['-CONTROL-'].update(text ='Desligar Sistema de Controle') 
                Control = True
                kd = float(values["-KD-"].replace(",","."))
                ki = float(values["-KI-"].replace(",","."))
                T = float(values["-T-"].replace(",","."))
                t5 = threading.Thread(target=Magcontroler, args=(data,window),daemon=True).start()  #,
                print("Ligado")
            else:
                window['-CONTROL-'].update(text ='Ligar Sistema de Controle')
                Control = False
                print("Desligado")
            t6 = threading.Thread(target=Refcontroler,daemon=True).start()
                    
        if '-IMG1-' in event:
            print("Verificando conexão com a Ponte H...")
            print(values["-LIST1-"])
            #try:
            a = arduino.write(b'$INV;')
            data = arduino.readline()
            print(data)
            if (b'$INV' in data):
                window['-IMG1-'].update(image_data = ok)
            else:
                window['-IMG1-'].update(image_data = error)
        if '-LIST2-' in event:
            if magnet != []:
                try:
                    magnet.close()
                    magnet = serial.Serial(port=values["-LIST2-"], baudrate=9600, timeout=0.2,write_timeout = 0.2)#xonxoff=True
                    print("Magnetômetro configurado com sucesso")
                except:
                    print("Falha na Comunicação do Magnetômetro")
            else:
                try:
                    magnet = serial.Serial(port=values["-LIST2-"], baudrate=9600, timeout=0.2,write_timeout = 0.2)#xonxoff=True
                    print("Magnetômetro configurado com sucesso")
                except:
                    print("Falha na Comunicação do Magnetômetro")
                    
        if '-IMG2-' in event:
            #print(calimagnet)
            #try:
            print("Verificando conexão com o Magnetômetro...")
            print(values["-LIST2-"])
            #try:
            data = magnetwritereadline(b'*00P\r')
            resp = magnetread(data)
            #print(resp)
            if len(resp.split("\t"))==3 :
                window['-IMG2-'].update(image_data = ok)
            else:
                window['-IMG2-'].update(image_data = error)
            #except:
                #window['-IMG2-'].update(image_data = error)
        if '-IMG3-' in event:
            try:
                resp = ga.query("ID?")
                print(resp)
                if resp == 'ID HP6032A\r\n' :
                    window['-IMG3-'].update(image_data = ok)
                    print("Fonte A configurada com sucesso")
                else:
                    window['-IMG3-'].update(image_data = error)
                    print("Falha na Comunicação com a Fonte A")
            except:
                window['-IMG3-'].update(image_data = error)
                print("Falha na Comunicação com a Fonte A")
        if '-IMG4-' in event:
            try:
                resp = gb.query("*IDN?")
                print(resp)
                if resp == 'HEWLETT-PACKARD,6032A,0,sA.00.00pA.00.02\n' :
                    window['-IMG4-'].update(image_data = ok)
                    print("Fonte B configurada com sucesso")
                else:
                    window['-IMG4-'].update(image_data = error)
                    print("Falha na Comunicação com a Fonte B")
            except:
                window['-IMG4-'].update(image_data = error)
                print("Falha na Comunicação com a Fonte B")
        if '-IMG5-' in event:
            try:
                resp = gc.query("ID?")
                print(resp)
                if resp == 'ID HP6032A\r\n' :
                    window['-IMG5-'].update(image_data = ok)
                    print("Fonte C configurada com sucesso")
                else:
                    window['-IMG5-'].update(image_data = error)
                    print("Falha na Comunicação com a Fonte C")
            except:
                window['-IMG5-'].update(image_data = error)
                print("Falha na Comunicação com a Fonte C")
        if '-CONTROL-' in event:
            if window['-CONTROL-'].get_text() == 'Ligar Sistema de Controle':
                window['-CONTROL-'].update(text ='Desligar Sistema de Controle') 
                Control = True
                kd = float(values["-KD-"].replace(",","."))
                ki = float(values["-KI-"].replace(",","."))
                T = float(values["-T-"].replace(",","."))
                t3 = threading.Thread(target=Magcontroler, args=(data,window),daemon=True).start()  #,
                print("Ligado")
            else:
                window['-CONTROL-'].update(text ='Ligar Sistema de Controle')
                Control = False
                print("Desligado")
        if '-SEND1-' in event:
            Bx = float(values["-BX-"].replace(",","."))
            By = float(values["-BY-"].replace(",","."))
            Bz = float(values["-BZ-"].replace(",","."))
            Bset(Bx,By,Bz)
            print(data)
        if '-SEND2-' in event:
            Vx = float(values["-VX-"].replace(",","."))
            Vy = float(values["-VY-"].replace(",","."))
            Vz = float(values["-VZ-"].replace(",","."))
            Vset(Vx,Vy,Vz)
        if '-IMG6-' in event:
            Vset(0,0,0)
            sg.Popup('Inicie os movimentos com o Magnetômetro!', keep_on_top=True)
            t1 = threading.Thread(target=calibramag, args=(25.7337,window), daemon=True).start()
        if '-IMG7-' in event:
            Vset(0,0,0)
            time.sleep(1)
            sg.Popup('Posicione o magnetômetro corretamente no centro da Gaiola!', keep_on_top=True)
            if (calimagnet ==[]):
                window['-IMG7-'].update(image_data = error)
            else:
                try:
                    t2 = threading.Thread(target=caliB, args=("x",window), daemon=True).start()
                except:
                    window['-IMG7-'].update(image_data = error)
        if '-IMG8-' in event:
            Vset(0,0,0)
            sg.Popup('Posicione o magnetômetro corretamente no centro da Gaiola!', keep_on_top=True)
            if (calimagnet ==[]):
                window['-IMG8-'].update(image_data = error)
            else:
                try:   
                    t2 = threading.Thread(target=caliB, args=("y",window), daemon=True).start()
                except:
                    window['-IMG8-'].update(image_data = error)
        if '-IMG9-' in event:
            Vset(0,0,0)
            sg.Popup('Posicione o magnetômetro corretamente no centro da Gaiola!', keep_on_top=True)
            if (calimagnet ==[]):
                window['-IMG9-'].update(image_data = error)
            else:
                try:   
                    t2 = threading.Thread(target=caliB, args=("z",window), daemon=True).start()
                except:
                    window['-IMG9-'].update(image_data = error)                

        #print(values["-LIST1-"])
        if event in (sg.WIN_CLOSED, 'Exit'):
            arduino.close()
            magnet.close()
            Vset(0,0,0)
            break
        #print(event)
        

    window.close()

# Define the button graphic base 64 strings and then call the main function
if __name__ == '__main__':
    recarregar = b'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'
    ok = b'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'
    error = b'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'
    logo = b'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'
    mapa = b'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'
    on ="data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiPjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iYSI+PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjMTZmZjZhIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMDA5MGE1Ii8+PC9saW5lYXJHcmFkaWVudD48bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgxPSIxMDczLjQwMyIgeDI9IjEwOTcuMTE2IiB5MT0iNTE2LjQ1MSIgeTI9IjU0NC4zMDgiIGdyYWRpZW50VHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEwOTUuOTE1IDQ5MS42ODIpIHNjYWxlKDEuMDI1MjQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeGxpbms6aHJlZj0iI2EiLz48L2RlZnM+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCAtMTAyMC4zNjIpIj48cmVjdCB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHk9IjEwMjAuMzYyIiBmaWxsPSJ1cmwoI2IpIiByeD0iNi43NjMiIHJ5PSI2Ljc2MyIvPjxwYXRoIHN0eWxlPSJ0ZXh0LWluZGVudDowO3RleHQtYWxpZ246c3RhcnQ7bGluZS1oZWlnaHQ6bm9ybWFsO3RleHQtdHJhbnNmb3JtOm5vbmU7YmxvY2stcHJvZ3Jlc3Npb246dGIiIGZpbGw9IiNmZmYiIGQ9Ik0xNS45MDYgOC41YS41LjUgMCAwIDAtLjQwNi41djRhLjUuNSAwIDEgMCAxIDBWOWEuNS41IDAgMCAwLS41LS41LjUuNSAwIDAgMC0uMDk0IDB6bS0yIDEuMzEzYS41LjUgMCAwIDAtLjAzMS4wMyA2Ljk3IDYuOTcgMCAwIDAtNC43ODEgNy43MkE3LjAwOCA3LjAwOCAwIDAgMCAxNiAyMy41YTYuOTg0IDYuOTg0IDAgMCAwIDYuOTA2LTUuOTA2IDcuMDA2IDcuMDA2IDAgMCAwLTQuNzgxLTcuNzUuNS41IDAgMCAwLS4zMTMuOTM3YzIuODIuOSA0LjU4MyAzLjczMyA0LjEyNSA2LjY1NkE1Ljk5MiA1Ljk5MiAwIDAgMSAxNiAyMi41YTYuMDE3IDYuMDE3IDAgMCAxLTUuOTM4LTUuMDk0IDUuOTk0IDUuOTk0IDAgMCAxIDQuMTI2LTYuNjI1LjUuNSAwIDAgMC0uMTU3LS45NjkuNS41IDAgMCAwLS4xMjUgMHoiIGNvbG9yPSIjMDAwIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC13ZWlnaHQ9IjQwMCIgb3ZlcmZsb3c9InZpc2libGUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAyMC4zNjIpIi8+PC9nPjwvc3ZnPg=="
    off ="data:image/svg+xml;utf8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiI+PHBhdGggZD0iTTYuNzYyIDBBNi43NDYgNi43NDYgMCAwIDAgMCA2Ljc2MnYxOC40NzZBNi43NDYgNi43NDYgMCAwIDAgNi43NjIgMzJoMTguNDc2QTYuNzQ2IDYuNzQ2IDAgMCAwIDMyIDI1LjIzOFY2Ljc2MkE2Ljc0NiA2Ljc0NiAwIDAgMCAyNS4yMzggMEg2Ljc2MnptOS4xODcgOC40OThBLjUuNSAwIDAgMSAxNiA4LjVhLjUuNSAwIDAgMSAuNS41djRhLjUuNSAwIDEgMS0xIDBWOWEuNS41IDAgMCAxIC40MDYtLjUuNS41IDAgMCAxIC4wNDMtLjAwMnptLTEuOTY5IDEuMzFhLjUuNSAwIDAgMSAuMDUxLjAwNS41LjUgMCAwIDEgLjE1Ni45NjggNS45OTQgNS45OTQgMCAwIDAtNC4xMjQgNi42MjVBNi4wMTcgNi4wMTcgMCAwIDAgMTYgMjIuNWE1Ljk5MiA1Ljk5MiAwIDAgMCA1LjkzOC01LjA2M2MuNDU3LTIuOTIzLTEuMzA2LTUuNzU1LTQuMTI1LTYuNjU2YS41LjUgMCAwIDEgLjMxMi0uOTM3IDcuMDA2IDcuMDA2IDAgMCAxIDQuNzgxIDcuNzVBNi45ODQgNi45ODQgMCAwIDEgMTYgMjMuNWE3LjAwOCA3LjAwOCAwIDAgMS02LjkwNi01LjkzOCA2Ljk3IDYuOTcgMCAwIDEgNC43ODEtNy43MTguNS41IDAgMCAxIC4wMzEtLjAzMS41LjUgMCAwIDEgLjA3NC0uMDA0eiIvPjwvc3ZnPg=="
    main()

import serial
magnet = serial.Serial("COM3", baudrate=9600, timeout=0.1)
leitura = ""
for i in range(20):
    a = magnet.write(b'*00P\r')
    data = magnet.readline()
    linha =data.decode()
    dadox = linha[0:7].replace(" ","").replace(",","")
    dadoy = linha[8:16].replace(" ","").replace(",","")
    dadoz = linha[18:25].replace(" ","").replace(",","")
    dadox = float(dadox)/150
    dadoy = float(dadoy)/150
    dadoz = float(dadoz)/150
    read = str(dadox) + "\t"+  str(dadoy) + "\t"+ str(dadoz) + "\n"
    leitura += read
    print(f"{dadox:.2f}\t{dadoy:.2f}\t{dadoz:.2f}\n")


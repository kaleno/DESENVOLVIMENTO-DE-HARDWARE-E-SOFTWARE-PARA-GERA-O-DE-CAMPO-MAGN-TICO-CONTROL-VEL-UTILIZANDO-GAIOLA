from datetime import datetime
import json
arquivoX = "C:\\Users\\LAICA2-SG11-UnB\\Desktop\\Software Gaiola\\Telemetria\\Epoca1\\JSON\\Telemetria_Xaxis_Mag_Epoca1.json"
arquivoY = "C:\\Users\\LAICA2-SG11-UnB\\Desktop\\Software Gaiola\\Telemetria\\Epoca1\\JSON\\Telemetria_Yaxis_Mag_Epoca1.json"
arquivoZ = "C:\\Users\\LAICA2-SG11-UnB\\Desktop\\Software Gaiola\\Telemetria\\Epoca1\\JSON\\Telemetria_Zaxis_Mag_Epoca1.json"

def JSON_to_Vector(arquivoX,arquivoY,arquivoZ):
    datax = open(arquivoX,"r")
    datay = open(arquivoY,"r")
    dataz = open(arquivoZ,"r")
    VecBx = json.load(datax)
    VecBy = json.load(datay)
    VecBz = json.load(dataz)
    print(VecBx[0])
    print(VecBy[0])
    print(VecBz[0])
    checkx = (f.readline()== "X-axis OBC magnetometer measure;\n")
    checky = (g.readline()== "Y-axis OBC magnetometer measure;\n")
    checkz = (h.readline()== "Z-axis OBC magnetometer measure;\n")
    if not(checkx and checky and checkz):
        print("Os Arquivos selecionados não tem o formato padrão")
        return
    s1 = f.readline()
    s2 = g.readline()
    s3 = h.readline()
    s1 = f.readline()
    s2 = g.readline()
    s3 = h.readline()
    V =[]
    segzero = 0
    seg = 0
    while (s1 != "" and s2 != "" and s3 != ""):
        s1 = f.readline()
        s2 = g.readline()
        s3 = h.readline()
        if (s1 =="") or (s2 =="") or (s3 ==""):
            break
        if (s1.split(";")[1] == s2.split(";")[1]) and (s2.split(";")[1] == s3.split(";")[1]):
            print(s1.split(";")[1].replace("Z",""))
            dat = datetime.strptime(s1.split(";")[1].replace("Z","").replace("\n",""),"%Y-%m-%d %H:%M:%S.%f")
            segzero = seg
            seg = datetime.timestamp(dat)
            V += [[float(s1.split(";")[0])/10,float(s2.split(";")[0])/10,float(s3.split(";")[0])/10,seg-segzero]]
    for i in V:
        print (str(i[3]).replace(".",","))
    
JSON_to_Vector(arquivoX,arquivoY,arquivoZ)

# current date and time
now = datetime.strptime("2022-04-03 02:30:19.578", "%Y-%m-%d %H:%M:%S.%f")




timestamp = datetime.timestamp(now)
print("timestamp =", timestamp)

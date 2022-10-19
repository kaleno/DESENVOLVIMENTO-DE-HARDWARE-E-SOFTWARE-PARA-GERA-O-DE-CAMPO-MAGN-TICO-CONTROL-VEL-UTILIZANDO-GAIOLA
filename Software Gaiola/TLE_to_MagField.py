# Por Danilo Queirós de Freitas e Gabriel Lima Sertão

# Este código apresenta a função TLEtoMAG, que retorna 3 strigs no formato JSON
# com os valores de campo magnético nos eixos X, Y e Z para cada timestamp, 
# experimentados pelo satélite de número de identificação n, especificando os 
# tempos de observação e o período de amostragem em minutos.

# Documentação das bibliotecas:
# https://rhodesmill.org/skyfield/earth-satellites.html
# https://rhodesmill.org/skyfield/time.html
# https://github.com/klaundal/ppigrf

pip install skyfield
pip install ppigrf

import skyfield.api as skyf
import ppigrf


def MagField(satellite, t):

  # Posição -----------------------
  geocentric = satellite.at(t)
  lat, lon = skyf.wgs84.latlon_of(geocentric)
  hei = skyf.wgs84.height_of(geocentric)

  # Campo gmagnético (IGRF 13) ----    
  Be, Bn, Bu = ppigrf.igrf(lon.degrees, lat.degrees, hei.km, t.utc_datetime().replace(tzinfo=None)) # returns east, north, up

  # Norte = X, Leste = -Y, Cima = Z
  x = float(Bn)/1000
  y = -float(Be)/1000
  z = float(Bu)/1000

  print('.', end='')

  return x, y, z

def TLEtoMAG(sat_num, t_inicial, t_final, t_sample):
  
  # Importação do TLE -------------
  option = input('Importação do TLE por arquivo .txt ou por NORAD ID pela web? 1-(txt), 2-(ID)\n')
  if option == '1':
    filename = input('Nome do arquivo (sem extensão): ')
    f = open(filename + ".txt", "r")
    satname = f.readline()
    line1 = f.readline()
    line2 = f.readline()
    f.close()
    satellite = skyf.EarthSatellite(line1, line2, satname)
  elif option == '2':
    # sat_num = input('NORAD ID do satélite: ') # Ativar essa linha caso queira selecionar o ID manualmente
    url = 'https://celestrak.org/NORAD/elements/gp.php?CATNR={}'.format(sat_num)
    satellite = skyf.load.tle_file(url,reload=True)
    satellite = satellite[0]

  print('\nInformações do satélite:\t',end='')
  print(satellite)
  print()

  # Tempo -------------------------
  ts = skyf.load.timescale()
  t_atual = ts.now()  # Tempo atual

  days = t_atual - satellite.epoch
  hours = (days - int(days)) * 24
  print('Tempo desde à época do TLE:\t', int(days), ' dias e ', int(hours), ' horas.', sep='')
  print()

  n_samples = round((t_final - t_inicial) * 86400 / t_sample) + 1
  print('Número de amostras:\t\t', n_samples, sep='')
  print()

  print('Modelo geomagnético usado:\tIGRF')
  print()  

  tempo = ts.linspace(t_inicial, t_inicial + (n_samples-1)/86400 * t_sample, num = n_samples)

  x, y, z = zip(*[MagField(satellite, i) for i in tempo])

  print('\nFinalizado!')

  x_json = ('[\n')
  for i in range(len(tempo)-1):
    x_json = (x_json + 
              '  {\n    "Value (mG)": ' + str(x[i]*10) +
              ',\n    "Satellite Timestamp (UTC)": "' + str(tempo[i].utc_iso()).replace("T"," ").replace("Z",".000Z") + 
              '"\n  },\n')
  x_json = (x_json + 
              '  {\n    "Value (mG)": ' + str(x[len(tempo)-1]*10) +
              ',\n    "Satellite Timestamp (UTC)": "' + str(tempo[len(tempo)-1].utc_iso()).replace("T"," ").replace("Z",".000Z") + 
              '"\n  }\n')
  x_json = x_json +  ']'

  y_json = ('[\n')
  for i in range(len(tempo)-1):
    y_json = (y_json + 
              '  {\n    "Value (mG)": ' + str(y[i]*10) +
              ',\n    "Satellite Timestamp (UTC)": "' + str(tempo[i].utc_iso()).replace("T"," ").replace("Z",".000Z") + 
              '"\n  },\n')
  y_json = (y_json + 
              '  {\n    "Value (mG)": ' + str(y[len(tempo)-1]*10) +
              ',\n    "Satellite Timestamp (UTC)": "' + str(tempo[len(tempo)-1].utc_iso()).replace("T"," ").replace("Z",".000Z") + 
              '"\n  }\n')
  y_json = y_json +  ']'
  
  z_json = ('[\n')
  for i in range(len(tempo)-1):
    z_json = (z_json + 
              '  {\n    "Value (mG)": ' + str(z[i]*10) +
              ',\n     "Satellite Timestamp (UTC)": "' + str(tempo[i].utc_iso()).replace("T"," ").replace("Z",".000Z") +
              '"\n  },\n')
  z_json = (z_json + 
              '  {\n    "Value (mG)": ' + str(z[len(tempo)-1]*10) +
              ',\n     "Satellite Timestamp (UTC)": "' + str(tempo[len(tempo)-1].utc_iso()).replace("T"," ").replace("Z",".000Z") +
              '"\n  }\n')
  z_json = z_json +  ']'

  return x_json, y_json, z_json
ts = skyf.load.timescale()
data_inicial = ts.utc(2022, 9, 15, 21, 0, 0)  # Data inicial de observação
data_final = ts.utc(2022, 9, 15, 21, 5, 0)    # Data final de observação
t_sample = 2                                  # Período de amostragem em segundos
n = 52160                                     # Número do satélite (ALFACRUX)

# As saídas da função são 3 strings em formato JSON
x_mag, y_mag, z_mag = TLEtoMAG(n, data_inicial, data_final, t_sample)

# Criação de 3 arquivos JSON
with open("X_MagField_from_TLE.json", "w") as text_file:
    text_file.write(x_mag)
with open("Y_MagField_from_TLE.json", "w") as text_file:
    text_file.write(y_mag)
with open("Z_MagField_from_TLE.json", "w") as text_file:
    text_file.write(z_mag)

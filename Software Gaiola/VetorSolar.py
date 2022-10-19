#Vetor solar em ECI.
t = ts.utc(2022, 8, 19,6,0)
sun, venus, earth = eph['sun'], eph['venus'], eph['earth']
astrometric = eph['earth'].at(t).observe(eph['sun'])
x = astrometric.ecliptic_position()
print(x)

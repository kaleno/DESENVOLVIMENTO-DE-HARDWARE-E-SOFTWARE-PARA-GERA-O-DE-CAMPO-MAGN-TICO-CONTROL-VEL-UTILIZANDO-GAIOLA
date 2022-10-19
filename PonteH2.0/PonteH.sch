EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 6
Title "Ponte H"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 6550 4950 550  400 
U 6220F55D
F0 "PonteHx" 50
F1 "PonteHx.sch" 50
F2 "D7" I L 6550 5250 50 
F3 "ND7" I L 6550 5150 50 
F4 "Ix" O L 6550 5000 50 
F5 "XA" I R 7100 5150 50 
F6 "XB" I R 7100 5050 50 
$EndSheet
$Sheet
S 6550 4350 550  400 
U 6220F5F2
F0 "PonteHy" 50
F1 "PonteHy.sch" 50
F2 "D6" I L 6550 4650 50 
F3 "ND6" I L 6550 4550 50 
F4 "Iy" O L 6550 4400 50 
F5 "YA" I R 7100 4600 50 
F6 "YB" I R 7100 4500 50 
$EndSheet
$Sheet
S 6550 3700 550  400 
U 6220F661
F0 "PonteHz" 50
F1 "PonteHz.sch" 50
F2 "D5" I L 6550 4000 50 
F3 "ND5" I L 6550 3900 50 
F4 "Iz" O L 6550 3750 50 
F5 "ZA" I R 7100 3950 50 
F6 "ZB" I R 7100 3850 50 
$EndSheet
$Sheet
S 7300 3650 1000 1700
U 623A29C5
F0 "Ociladores" 50
F1 "Ociladores.sch" 50
F2 "XA" O L 7300 5150 50 
F3 "XB" O L 7300 5050 50 
F4 "YA" O L 7300 4600 50 
F5 "YB" O L 7300 4500 50 
F6 "ZA" O L 7300 3950 50 
F7 "ZB" O L 7300 3850 50 
$EndSheet
Wire Wire Line
	7300 5050 7100 5050
Wire Wire Line
	7300 5150 7100 5150
Wire Wire Line
	7300 4500 7100 4500
Wire Wire Line
	7300 4600 7100 4600
Wire Wire Line
	7300 3850 7100 3850
Wire Wire Line
	7300 3950 7100 3950
$Comp
L 74xx:74HC04 U1
U 1 1 623B91AA
P 6000 5150
F 0 "U1" H 5500 5300 50  0000 C CNN
F 1 "74HC04" H 5500 5200 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 6000 5150 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 6000 5150 50  0001 C CNN
	1    6000 5150
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 2 1 623BA166
P 6000 4550
F 0 "U1" H 5500 4700 50  0000 C CNN
F 1 "74HC04" H 5500 4600 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 6000 4550 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 6000 4550 50  0001 C CNN
	2    6000 4550
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 3 1 623BB325
P 5950 3900
F 0 "U1" H 5450 4050 50  0000 C CNN
F 1 "74HC04" H 5450 3950 50  0000 C CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 5950 3900 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 5950 3900 50  0001 C CNN
	3    5950 3900
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HC04 U1
U 7 1 623BCFA2
P 5900 2400
F 0 "U1" H 6130 2446 50  0000 L CNN
F 1 "74HC04" H 6130 2355 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 5900 2400 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT04.pdf" H 5900 2400 50  0001 C CNN
	7    5900 2400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 623C40CB
P 5900 2900
F 0 "#PWR0101" H 5900 2650 50  0001 C CNN
F 1 "GND" H 5905 2727 50  0000 C CNN
F 2 "" H 5900 2900 50  0001 C CNN
F 3 "" H 5900 2900 50  0001 C CNN
	1    5900 2900
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0102
U 1 1 623C47C8
P 5900 1900
F 0 "#PWR0102" H 5900 1750 50  0001 C CNN
F 1 "+5V" H 5915 2073 50  0000 C CNN
F 2 "" H 5900 1900 50  0001 C CNN
F 3 "" H 5900 1900 50  0001 C CNN
	1    5900 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 3900 6550 3900
Wire Wire Line
	6300 4550 6550 4550
Wire Wire Line
	6300 5150 6550 5150
Wire Wire Line
	6550 4000 6450 4000
Wire Wire Line
	6450 4000 6450 4100
Wire Wire Line
	6450 4100 5650 4100
Wire Wire Line
	5650 4100 5650 3900
Wire Wire Line
	6550 4650 6500 4650
Wire Wire Line
	6500 4650 6500 4750
Wire Wire Line
	6500 4750 5700 4750
Wire Wire Line
	5700 4750 5700 4550
Wire Wire Line
	6550 5250 6500 5250
Wire Wire Line
	6500 5250 6500 5350
Wire Wire Line
	6500 5350 5700 5350
Wire Wire Line
	5700 5350 5700 5150
$Sheet
S 4450 3650 550  1600
U 623CCD4D
F0 "ArduinoUno" 50
F1 "ArduinoUno.sch" 50
F2 "D7" O R 5000 5150 50 
F3 "D6" O R 5000 4550 50 
F4 "D5" O R 5000 3900 50 
F5 "Ix" I R 5000 4950 50 
F6 "Iy" I R 5000 4350 50 
F7 "Iz" I R 5000 3700 50 
$EndSheet
Wire Wire Line
	5000 3900 5650 3900
Connection ~ 5650 3900
Wire Wire Line
	5000 4550 5700 4550
Connection ~ 5700 4550
Wire Wire Line
	5000 5150 5700 5150
Connection ~ 5700 5150
Wire Wire Line
	6550 5000 6500 5000
Wire Wire Line
	6500 5000 6500 4950
Wire Wire Line
	6500 4950 5000 4950
Wire Wire Line
	6550 4400 6500 4400
Wire Wire Line
	6500 4400 6500 4350
Wire Wire Line
	6500 4350 5000 4350
Wire Wire Line
	6550 3750 6450 3750
Wire Wire Line
	6450 3750 6450 3700
Wire Wire Line
	6450 3700 5000 3700
$Comp
L Connector:Barrel_Jack_Switch J7
U 1 1 623E0B54
P 1900 1650
F 0 "J7" H 1957 1967 50  0000 C CNN
F 1 "Barrel_Jack_Switch" H 1957 1876 50  0000 C CNN
F 2 "Connector_BarrelJack:BarrelJack_Wuerth_6941xx301002" H 1950 1610 50  0001 C CNN
F 3 "~" H 1950 1610 50  0001 C CNN
	1    1900 1650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0128
U 1 1 623E1C66
P 2200 1850
F 0 "#PWR0128" H 2200 1600 50  0001 C CNN
F 1 "GND" H 2205 1677 50  0000 C CNN
F 2 "" H 2200 1850 50  0001 C CNN
F 3 "" H 2200 1850 50  0001 C CNN
	1    2200 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 1750 2200 1850
$Comp
L power:+12V #PWR0129
U 1 1 623E2DA9
P 2450 1550
F 0 "#PWR0129" H 2450 1400 50  0001 C CNN
F 1 "+12V" H 2465 1723 50  0000 C CNN
F 2 "" H 2450 1550 50  0001 C CNN
F 3 "" H 2450 1550 50  0001 C CNN
	1    2450 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 1550 2450 1550
NoConn ~ 2200 1650
$EndSCHEMATC

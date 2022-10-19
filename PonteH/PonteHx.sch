EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 6
Title "Ponte H eixo x"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:Q_NMOS_GDS Q1
U 1 1 62400DAD
P 4400 3700
F 0 "Q1" H 4604 3746 50  0000 L CNN
F 1 "IRFZ44N" H 4604 3655 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 4600 3800 50  0001 C CNN
F 3 "~" H 4400 3700 50  0001 C CNN
	1    4400 3700
	1    0    0    -1  
$EndComp
$Comp
L Device:Q_NMOS_GDS Q2
U 1 1 623FC6D9
P 4400 4350
F 0 "Q2" H 4604 4396 50  0000 L CNN
F 1 "IRFZ44N" H 4604 4305 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 4600 4450 50  0001 C CNN
F 3 "~" H 4400 4350 50  0001 C CNN
	1    4400 4350
	1    0    0    -1  
$EndComp
$Comp
L Device:Q_NMOS_GDS Q3
U 1 1 62400DA2
P 7050 3700
F 0 "Q3" H 7255 3746 50  0000 L CNN
F 1 "IRFZ44N" H 7255 3655 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 7250 3800 50  0001 C CNN
F 3 "~" H 7050 3700 50  0001 C CNN
	1    7050 3700
	-1   0    0    -1  
$EndComp
$Comp
L Device:Q_NMOS_GDS Q4
U 1 1 62219B25
P 7050 4350
F 0 "Q4" H 7255 4396 50  0000 L CNN
F 1 "IRFZ44N" H 7255 4305 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 7250 4450 50  0001 C CNN
F 3 "~" H 7050 4350 50  0001 C CNN
	1    7050 4350
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_Small R5
U 1 1 62400D9E
P 7350 4350
F 0 "R5" V 7154 4350 50  0000 C CNN
F 1 "22R" V 7245 4350 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 7350 4350 50  0001 C CNN
F 3 "~" H 7350 4350 50  0001 C CNN
	1    7350 4350
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R4
U 1 1 623FA576
P 7350 3700
F 0 "R4" V 7154 3700 50  0000 C CNN
F 1 "22R" V 7245 3700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 7350 3700 50  0001 C CNN
F 3 "~" H 7350 3700 50  0001 C CNN
	1    7350 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R2
U 1 1 6226747F
P 4100 3700
F 0 "R2" V 3904 3700 50  0000 C CNN
F 1 "22R" V 3995 3700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4100 3700 50  0001 C CNN
F 3 "~" H 4100 3700 50  0001 C CNN
	1    4100 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R3
U 1 1 6226766E
P 4100 4350
F 0 "R3" V 3904 4350 50  0000 C CNN
F 1 "22R" V 3995 4350 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 4100 4350 50  0001 C CNN
F 3 "~" H 4100 4350 50  0001 C CNN
	1    4100 4350
	0    1    1    0   
$EndComp
$Comp
L Connector:Screw_Terminal_01x02 J1
U 1 1 62400DA3
P 5000 3800
F 0 "J1" V 4964 3612 50  0000 R CNN
F 1 "Bobinax" V 5100 3850 50  0000 R CNN
F 2 "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" H 5000 3800 50  0001 C CNN
F 3 "~" H 5000 3800 50  0001 C CNN
	1    5000 3800
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4500 3900 4500 4000
Connection ~ 4500 4000
Wire Wire Line
	4500 4000 4500 4150
Wire Wire Line
	6950 3900 6950 4000
Connection ~ 6950 4000
Wire Wire Line
	6950 4000 6950 4150
Wire Wire Line
	4500 4550 5800 4550
$Comp
L Connector:Screw_Terminal_01x02 J2
U 1 1 62278748
P 5600 3650
F 0 "J2" V 5564 3462 50  0000 R CNN
F 1 "Fontex" V 5700 3700 50  0000 R CNN
F 2 "TerminalBlock:TerminalBlock_bornier-2_P5.08mm" H 5600 3650 50  0001 C CNN
F 3 "~" H 5600 3650 50  0001 C CNN
	1    5600 3650
	-1   0    0    -1  
$EndComp
Connection ~ 5800 4550
Wire Wire Line
	5800 4550 6950 4550
$Comp
L Driver_FET:IR2183 U2
U 1 1 62400DA4
P 2800 3950
F 0 "U2" H 2450 4400 50  0000 C CNN
F 1 "IR2183" H 2450 4300 50  0000 C CNN
F 2 "Package_DIP:DIP-8_W7.62mm_LongPads" H 2800 3150 50  0000 C CIN
F 3 "https://www.infineon.com/dgdl/ir2183.pdf?fileId=5546d462533600a4015355c9490e16d1" H 2800 3950 50  0001 C CNN
	1    2800 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 3950 2500 4050
$Comp
L Driver_FET:IR2183 U4
U 1 1 62400DA5
P 8550 3950
F 0 "U4" H 8200 4400 50  0000 C CNN
F 1 "IR2183" H 8200 4300 50  0000 C CNN
F 2 "Package_DIP:DIP-8_W7.62mm_LongPads" H 8550 3050 50  0000 C CIN
F 3 "https://www.infineon.com/dgdl/ir2183.pdf?fileId=5546d462533600a4015355c9490e16d1" H 8550 3950 50  0001 C CNN
	1    8550 3950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8850 4050 8850 3950
$Comp
L power:GND #PWR0103
U 1 1 623FA57D
P 2800 4500
F 0 "#PWR0103" H 2800 4250 50  0001 C CNN
F 1 "GND" H 2805 4327 50  0000 C CNN
F 2 "" H 2800 4500 50  0001 C CNN
F 3 "" H 2800 4500 50  0001 C CNN
	1    2800 4500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 62400DA1
P 8550 4450
F 0 "#PWR0104" H 8550 4200 50  0001 C CNN
F 1 "GND" H 8555 4277 50  0000 C CNN
F 2 "" H 8550 4450 50  0001 C CNN
F 3 "" H 8550 4450 50  0001 C CNN
	1    8550 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 3750 3800 3750
Wire Wire Line
	4000 3700 3800 3700
Wire Wire Line
	3800 3700 3800 3750
Wire Wire Line
	4000 4350 3850 4350
Wire Wire Line
	3850 4350 3850 4250
Wire Wire Line
	3850 4250 3100 4250
Wire Wire Line
	3100 4150 3250 4150
Wire Wire Line
	3250 4150 3250 4000
Wire Wire Line
	3250 4000 3500 4000
Wire Wire Line
	7550 3750 7550 3700
Wire Wire Line
	7550 3700 7450 3700
Wire Wire Line
	8250 4150 7850 4150
Wire Wire Line
	7850 4150 7850 4000
Wire Wire Line
	7850 4000 7750 4000
Wire Wire Line
	7600 4250 7600 4350
Wire Wire Line
	7600 4350 7450 4350
Wire Wire Line
	7600 4250 8250 4250
Text HLabel 2350 3950 0    50   Input ~ 0
D7
Text HLabel 9050 3950 2    50   Input ~ 0
ND7
Wire Wire Line
	2500 3950 2350 3950
Connection ~ 2500 3950
Wire Wire Line
	9050 3950 8850 3950
Connection ~ 8850 3950
$Comp
L Sensor_Current:ACS715MOD U3
U 1 1 623FC6C9
P 6150 3000
F 0 "U3" H 5962 3071 50  0000 R CNN
F 1 "ACS715MOD" H 5962 2980 50  0000 R CNN
F 2 "PonteH:ACS712" H 6000 3050 50  0001 C CNN
F 3 "" H 6000 3050 50  0001 C CNN
	1    6150 3000
	-1   0    0    -1  
$EndComp
Wire Wire Line
	6050 3350 6050 4000
Wire Wire Line
	6250 3350 6250 4000
Wire Wire Line
	6250 4000 6950 4000
$Comp
L power:GND #PWR0105
U 1 1 623FC6CA
P 6450 2600
F 0 "#PWR0105" H 6450 2350 50  0001 C CNN
F 1 "GND" H 6455 2427 50  0000 C CNN
F 2 "" H 6450 2600 50  0001 C CNN
F 3 "" H 6450 2600 50  0001 C CNN
	1    6450 2600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0106
U 1 1 62400DA8
P 6050 2600
F 0 "#PWR0106" H 6050 2450 50  0001 C CNN
F 1 "+5V" H 6065 2773 50  0000 C CNN
F 2 "" H 6050 2600 50  0001 C CNN
F 3 "" H 6050 2600 50  0001 C CNN
	1    6050 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 2600 6450 2600
Text HLabel 6250 2550 2    50   Output ~ 0
Ix
Wire Wire Line
	6150 2550 6150 2600
Wire Wire Line
	6250 2550 6150 2550
$Comp
L power:+12V #PWR0107
U 1 1 623E7B1A
P 2800 3400
F 0 "#PWR0107" H 2800 3250 50  0001 C CNN
F 1 "+12V" H 2815 3573 50  0000 C CNN
F 2 "" H 2800 3400 50  0001 C CNN
F 3 "" H 2800 3400 50  0001 C CNN
	1    2800 3400
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR0108
U 1 1 62400D9A
P 8550 3450
F 0 "#PWR0108" H 8550 3300 50  0001 C CNN
F 1 "+12V" H 8565 3623 50  0000 C CNN
F 2 "" H 8550 3450 50  0001 C CNN
F 3 "" H 8550 3450 50  0001 C CNN
	1    8550 3450
	1    0    0    -1  
$EndComp
Text HLabel 1700 2550 0    50   Input ~ 0
XA
Text HLabel 9550 2650 2    50   Input ~ 0
XB
$Comp
L Device:R_Small R1
U 1 1 623C2D41
P 2200 2550
F 0 "R1" V 2004 2550 50  0000 C CNN
F 1 "470R" V 2095 2550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 2200 2550 50  0001 C CNN
F 3 "~" H 2200 2550 50  0001 C CNN
	1    2200 2550
	0    1    1    0   
$EndComp
$Comp
L Diode:1N5819 D1
U 1 1 623C50E6
P 3150 2850
F 0 "D1" H 3150 3067 50  0000 C CNN
F 1 "1N5819" H 3150 2976 50  0000 C CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 3150 2675 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88525/1n5817.pdf" H 3150 2850 50  0001 C CNN
	1    3150 2850
	0    -1   -1   0   
$EndComp
$Comp
L Diode:1N5819 D2
U 1 1 623C5B0C
P 3500 2850
F 0 "D2" H 3500 2633 50  0000 C CNN
F 1 "1N5819" H 3500 2724 50  0000 C CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 3500 2675 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88525/1n5817.pdf" H 3500 2850 50  0001 C CNN
	1    3500 2850
	0    1    1    0   
$EndComp
$Comp
L Device:C C1
U 1 1 62400DA9
P 2700 2550
F 0 "C1" V 2448 2550 50  0000 C CNN
F 1 "100nF" V 2539 2550 50  0000 C CNN
F 2 "Capacitor_THT:C_Rect_L16.5mm_W7.0mm_P15.00mm_MKT" H 2738 2400 50  0001 C CNN
F 3 "~" H 2700 2550 50  0001 C CNN
	1    2700 2550
	0    1    1    0   
$EndComp
$Comp
L Device:C C2
U 1 1 62400DAA
P 3350 3350
F 0 "C2" V 3098 3350 50  0000 C CNN
F 1 "100nF" V 3189 3350 50  0000 C CNN
F 2 "Capacitor_THT:C_Rect_L16.5mm_W7.0mm_P15.00mm_MKT" H 3388 3200 50  0001 C CNN
F 3 "~" H 3350 3350 50  0001 C CNN
	1    3350 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 3350 3500 4000
Connection ~ 3500 4000
Wire Wire Line
	3500 4000 4500 4000
Wire Wire Line
	3500 3350 3500 3000
Connection ~ 3500 3350
Wire Wire Line
	3150 3000 3150 3350
Wire Wire Line
	3150 3650 3100 3650
Wire Wire Line
	3200 3350 3150 3350
Connection ~ 3150 3350
Wire Wire Line
	3150 3350 3150 3650
Wire Wire Line
	3150 2700 3150 2550
Wire Wire Line
	3150 2550 2850 2550
Wire Wire Line
	3150 2550 3500 2550
Wire Wire Line
	3500 2550 3500 2700
Connection ~ 3150 2550
Wire Wire Line
	2550 2550 2300 2550
Wire Wire Line
	2100 2550 1700 2550
$Comp
L Device:R_Small R6
U 1 1 623EEA05
P 9050 2650
F 0 "R6" V 8854 2650 50  0000 C CNN
F 1 "470R" V 8945 2650 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" H 9050 2650 50  0001 C CNN
F 3 "~" H 9050 2650 50  0001 C CNN
	1    9050 2650
	0    -1   1    0   
$EndComp
$Comp
L Diode:1N5819 D4
U 1 1 623FC6D4
P 8100 2950
F 0 "D4" H 8100 3167 50  0000 C CNN
F 1 "1N5819" H 8100 3076 50  0000 C CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 8100 2775 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88525/1n5817.pdf" H 8100 2950 50  0001 C CNN
	1    8100 2950
	0    1    -1   0   
$EndComp
$Comp
L Diode:1N5819 D3
U 1 1 623FC6D5
P 7750 2950
F 0 "D3" H 7750 2733 50  0000 C CNN
F 1 "1N5819" H 7750 2824 50  0000 C CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 7750 2775 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88525/1n5817.pdf" H 7750 2950 50  0001 C CNN
	1    7750 2950
	0    -1   1    0   
$EndComp
$Comp
L Device:C C4
U 1 1 62400D9C
P 8550 2650
F 0 "C4" V 8298 2650 50  0000 C CNN
F 1 "100nF" V 8389 2650 50  0000 C CNN
F 2 "Capacitor_THT:C_Rect_L16.5mm_W7.0mm_P15.00mm_MKT" H 8588 2500 50  0001 C CNN
F 3 "~" H 8550 2650 50  0001 C CNN
	1    8550 2650
	0    -1   1    0   
$EndComp
$Comp
L Device:C C3
U 1 1 623EEA1D
P 7900 3450
F 0 "C3" V 7648 3450 50  0000 C CNN
F 1 "100nF" V 7739 3450 50  0000 C CNN
F 2 "Capacitor_THT:C_Rect_L16.5mm_W7.0mm_P15.00mm_MKT" H 7938 3300 50  0001 C CNN
F 3 "~" H 7900 3450 50  0001 C CNN
	1    7900 3450
	0    -1   1    0   
$EndComp
Wire Wire Line
	7750 3450 7750 3100
Wire Wire Line
	8100 3100 8100 3450
Wire Wire Line
	8050 3450 8100 3450
Wire Wire Line
	8100 2800 8100 2650
Wire Wire Line
	8100 2650 8400 2650
Wire Wire Line
	8100 2650 7750 2650
Wire Wire Line
	7750 2650 7750 2800
Connection ~ 8100 2650
Wire Wire Line
	8700 2650 8950 2650
Wire Wire Line
	9150 2650 9550 2650
Wire Wire Line
	7750 3450 7750 4000
Connection ~ 7750 3450
Connection ~ 7750 4000
Wire Wire Line
	7750 4000 6950 4000
Wire Wire Line
	5000 4000 4500 4000
Wire Wire Line
	5100 4000 6050 4000
Wire Wire Line
	4500 3500 5800 3500
Wire Wire Line
	5800 4550 5800 3750
Wire Wire Line
	5800 3650 5800 3500
Connection ~ 5800 3500
Wire Wire Line
	5800 3500 6950 3500
Wire Wire Line
	7550 3750 8250 3750
Wire Wire Line
	8250 3650 8100 3650
Wire Wire Line
	8100 3650 8100 3450
Connection ~ 8100 3450
Wire Wire Line
	2800 3400 2800 3450
Wire Wire Line
	2800 4450 2800 4500
$EndSCHEMATC


CHAIN_LIFT_FLAGS = 1 << 7

LIFT_HILL_SPEED = 7 # *2
BLOCK_BRAKE_BASE_SPEED = 0x20364

Unk9A37E4 = [ # used for g-force calculations
    2147483647,  2106585154,  1985590284,  1636362342,  1127484953,  2106585154,  1985590284,  1636362342,  1127484953,
    58579923,    0,           -555809667,  -1073741824, -1518500249, -1859775391, -2074309916, -2147483647, 58579923,
    0,           -555809667,  -1073741824, -1518500249, -1859775391, -2074309916, 1859775393,  1073741824,  0,
    -1073741824, -1859775393, 1859775393,  1073741824,  0,           -1073741824, -1859775393, 1859775393,  1073741824,
    0,           -1073741824, -1859775393, 1859775393,  1073741824,  0,           -1073741824, -1859775393, 2144540595,
    2139311823,  2144540595,  2139311823,  2135719507,  2135719507,  2125953864,  2061796213,  1411702590,  2125953864,
    2061796213,  1411702590,  1985590284,  1636362342,  1127484953,  2115506168]

Unk9A39C4 = [
    2147483647, 2096579710, 1946281152, 2096579710,  1946281152,  1380375879, 555809667,  -372906620, -1231746017, -1859775391,
    1380375879, 555809667,  -372906620, -1231746017, -1859775391, 0,          2096579710, 1946281152, 2096579710,  1946281152]

AccelerationFromPitch = [
          0,    # Flat
    -124548,    # 1 Slope Up 12.5
    -243318,    # 2 Slope Up 25
    -416016,    # 3 Slope Up 42.5
    -546342,    # 4 Slope Up 60
     124548,    # 5 Slope Down 12.5
     243318,    # 6 Slope Down 25
     416016,    # 7 Slope Down 42.5
     546342,    # 8 Slope Down 60
    -617604,    # 9 Slope Up 75
    -642000,    # 10 Slope Up 90
    -620172,    # 11 Slope Up 105
    -555972,    # 12 Slope Up 120
    -453894,    # 13 Slope Up 135
    -321000,    # 14 Slope Up 150
    -166278,    # 15 Slope Up 165
          0,    # 16 Fully Inverted
     617604,    # 17 Slope Down 75
     642000,    # 18 Slope Down 90
     620172,    # 19 Slope Down 105
     555972,    # 20 Slope Down 120
     453894,    # 21 Slope Down 135
     321000,    # 22 Slope Down 150
     166278,    # 23 Slope Down 165
    -321000,    # 24 Corkscrew Right Up 0
    -555972,    # 25 Corkscrew Right Up 1
    -642000,    # 26 Corkscrew Right Up 2
    -555972,    # 27 Corkscrew Right Up 3
    -321000,    # 28 Corkscrew Right Up 4
     321000,    # 29 Corkscrew Right Down 4
     555972,    # 30 Corkscrew Right Down 3
     642000,    # 31 Corkscrew Right Down 2
     555972,    # 32 Corkscrew Right Down 1
     321000,    # 33 Corkscrew Right Down 0
    -321000,    # 34 Corkscrew Left Up 0
    -555972,    # 35 Corkscrew Left Up 1
    -642000,    # 36 Corkscrew Left Up 2
    -555972,    # 37 Corkscrew Left Up 3
    -321000,    # 38 Corkscrew Left Up 4
     321000,    # 39 Corkscrew Left Down 4
     555972,    # 40 Corkscrew Left Down 2
     642000,    # 41 Corkscrew Left Down 1
     555972,    # 42 Corkscrew Left Down 1
     321000,    # 43 Corkscrew Left Down 0
     -33384,    # 44 Half Helix Up Large
     -55854,    # 45 Half Helix Up Small
      33384,    # 46 Half Helix Down Large
      55854,    # 47 Half Helix Down Small
     -66768,    # 48 Quarter Helix Up
      66768,    # 49 Quarter Helix Down
     -90522,    # 50 Diag Slope Up 12.5
    -179760,    # 51 Diag Slope Up 25
                # DiagUp25ToUp60 has transition slopes of 2 and 3
    -484068,    # 52 Diag Slope Up 60
      90522,    # 53 Diag Slope Down 12.5
     179760,    # 54 Diag Slope Down 25
                # DiagDown25ToDown60 has transition slopes of 6 and 7
     484068,    # 55 Diag Slope Down 60
     243318,    # 56 Inverting Loop Down 25
     416016,    # 57 Inverting Loop Down 42.5
     546342,    # 58 Inverting Loop Down 60
    -110424,    # 59 Slope Up Spiral Lift Hill
]

GFORCE_VERT = {
    "ELEM_FLAT_TO_25_DEG_UP": 103,   
    "ELEM_25_DEG_DOWN_TO_FLAT": 103, 
    "ELEM_LEFT_BANK_TO_25_DEG_UP": 103,
    "ELEM_RIGHT_BANK_TO_25_DEG_UP": 103,
    "ELEM_25_DEG_UP_TO_LEFT_BANK": 103,
    "ELEM_25_DEG_UP_TO_RIGHT_BANK": 103,
    "LeftBankedFlatToLeftBankedUp25": 103,
    "RightBankedFlatToRightBankedUp25": 103,
    "LeftBankedDown25ToLeftBankedFlat": 103,
    "RightBankedDown25ToRightBankedFlat": 103,
    "FlatToLeftBankedUp25": 103,
    "FlatToRightBankedUp25": 103,
    "LeftBankedDown25ToFlat": 103,
    "RightBankedDown25ToFlat": 103,
    
    "ELEM_25_DEG_UP_TO_FLAT": -103,   
    "ELEM_FLAT_TO_25_DEG_DOWN": -103, 
    "ELEM_25_DEG_UP_TO_LEFT_BANK": -103,
    "ELEM_25_DEG_UP_TO_RIGHT_BANK": -103,
    "ELEM_LEFT_BANK_TO_25_DEG_DOWN": -103,
    "ELEM_RIGHT_BANK_TO_25_DEG_DOWN": -103,
    "LeftBankedUp25ToLeftBankedFlat": -103,
    "RightBankedUp25ToRightBankedFlat": -103,
    "LeftBankedFlatToLeftBankedDown25": -103,
    "RightBankedFlatToRightBankedDown25": -103,
    "LeftBankedUp25ToFlat": -103,
    "RightBankedUp25ToFlat": -103,
    "FlatToLeftBankedDown25": -103,
    "FlatToRightBankedDown25": -103,
    
    "ELEM_25_DEG_UP_TO_60_DEG_UP": 82,
    "ELEM_60_DEG_DOWN_TO_25_DEG_DOWN": 82,
    
    "ELEM_60_DEG_UP_TO_25_DEG_UP": -82,
    "ELEM_25_DEG_DOWN_TO_60_DEG_DOWN": -82,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES": 200,
    "ELEM_LEFT_HALF_BANKED_HELIX_UP_LARGE": 200,
    "ELEM_LEFT_HALF_BANKED_HELIX_DOWN_LARGE": 200,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_UP": 200,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_DOWN": 200,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES": 200,
    "ELEM_RIGHT_HALF_BANKED_HELIX_UP_LARGE": 200,
    "ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_LARGE": 200,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_UP": 200,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_DOWN": 200,
    
    "ELEM_LEFT_QUARTER_TURN_3_TILES_BANK": 100,
    "ELEM_LEFT_HALF_BANKED_HELIX_UP_SMALL": 100,
    "ELEM_LEFT_HALF_BANKED_HELIX_DOWN_SMALL": 100,
    
    "ELEM_RIGHT_QUARTER_TURN_3_TILES_BANK": 100,
    "ELEM_RIGHT_HALF_BANKED_HELIX_UP_SMALL": 100,
    "ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_SMALL": 100,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP": 200,
    "ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN": 200,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP": 200,
    "ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN": 200,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP": 200,
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN": 200,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP": 200,
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN": 200,
    
    "ELEM_LEFT_EIGHTH_BANK_TO_DIAG": 270,
    "ELEM_LEFT_EIGHTH_BANK_TO_ORTHOGONAL": 270,
    
    "ELEM_RIGHT_EIGHTH_BANK_TO_DIAG": 270,
    "ELEM_RIGHT_EIGHTH_BANK_TO_ORTHOGONAL": 270,
    
    "ELEM_DIAG_FLAT_TO_25_DEG_UP": 113,
    "ELEM_DIAG_25_DEG_DOWN_TO_FLAT": 113,
    "ELEM_DIAG_LEFT_BANK_TO_25_DEG_UP": 113,
    "ELEM_DIAG_RIGHT_BANK_TO_25_DEG_UP": 113,
    "ELEM_DIAG_25_DEG_DOWN_TO_LEFT_BANK": 113,
    "ELEM_DIAG_25_DEG_DOWN_TO_RIGHT_BANK": 113,
    "ELEM_DIAG_25_DEG_UP_TO_FLAT": -113,
    "ELEM_DIAG_FLAT_TO_25_DEG_DOWN": -113,
    "ELEM_DIAG_25_DEG_UP_TO_LEFT_BANK": -113,
    "ELEM_DIAG_25_DEG_UP_TO_RIGHT_BANK": -113,
    "ELEM_DIAG_LEFT_BANK_TO_25_DEG_DOWN": -113,
    "ELEM_DIAG_RIGHT_BANK_TO_25_DEG_DOWN": -113,
    "ELEM_DIAG_25_DEG_UP_TO_60_DEG_UP": 95,
    "ELEM_DIAG_60_DEG_DOWN_TO_25_DEG_DOWN": 95,
    "ELEM_DIAG_60_DEG_UP_TO_25_DEG_UP": -95,
    "ELEM_DIAG_25_DEG_DOWN_TO_60_DEG_DOWN": -95,
    "ELEM_DIAG_FLAT_TO_60_DEG_UP": 60,
    "ELEM_DIAG_60_DEG_DOWN_TO_FLAT": 60,
    "ELEM_DIAG_60_DEG_UP_TO_FLAT": -60,
    "ELEM_DIAG_FLAT_TO_60_DEG_DOWN": -60,
}

GFORCE_LAT = {
    "ELEM_LEFT_QUARTER_TURN_5_TILES": 98,
    "ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP": 98,
    "ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN": 98,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_UP": 98,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_DOWN": 98,
    
    "ELEM_RIGHT_QUARTER_TURN_5_TILES": -98,
    "ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP": -98,
    "ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN": -98,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_UP": -98,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_DOWN": -98,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES": 160,
    "ELEM_LEFT_HALF_BANKED_HELIX_UP_LARGE": 160,
    "ELEM_LEFT_HALF_BANKED_HELIX_DOWN_LARGE": 160,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_UP": 160,
    "ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_DOWN": 160,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES": -160,
    "ELEM_RIGHT_HALF_BANKED_HELIX_UP_LARGE": -160,
    "ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_LARGE": -160,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_UP": -160,
    "ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_DOWN": -160,
    
    "ELEM_LEFT_QUARTER_TURN_3_TILES": 59,
    "ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP": 59,
    "ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN": 59,
    
    "ELEM_RIGHT_QUARTER_TURN_3_TILES": -59,
    "ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP": -59,
    "ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN": -59,
    
    "ELEM_LEFT_QUARTER_TURN_3_TILES_BANK": 100,
    "ELEM_LEFT_HALF_BANKED_HELIX_UP_SMALL": 100,
    "ELEM_LEFT_HALF_BANKED_HELIX_DOWN_SMALL": 100,
    
    "ELEM_RIGHT_QUARTER_TURN_3_TILES_BANK": -100,
    "ELEM_RIGHT_HALF_BANKED_HELIX_UP_SMALL": -100,
    "ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_SMALL": -100,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP": 100,
    "ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN": 100,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP": -100,
    "ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN": -100,
    
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP": 160,
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN": 160,
    
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP": -160,
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN": -160,
    
    "ELEM_LEFT_EIGHTH_TO_DIAG": 137,
    "ELEM_LEFT_EIGHTH_TO_ORTHOGONAL": 137,
    
    "ELEM_RIGHT_EIGHTH_TO_DIAG": -137,
    "ELEM_RIGHT_EIGHTH_TO_ORTHOGONAL": -137,
    
    "ELEM_LEFT_EIGHTH_BANK_TO_DIAG": 200,
    "ELEM_LEFT_EIGHTH_BANK_TO_ORTHOGONAL": 200,
    
    "ELEM_RIGHT_EIGHTH_BANK_TO_DIAG": -200,
    "ELEM_RIGHT_EIGHTH_BANK_TO_ORTHOGONAL": -200
}

def findNextPowerOf2(n):
    if n == 1: return 2
    # decrement `n` (to handle cases when `n` itself
    # is a power of 2)
    n = n - 1
 
    # do till only one bit is left
    while n & n - 1:
        n = n & n - 1       # unset rightmost bit
 
    # `n` is now a power of two (less than `n`)
 
    # return next power of 2
    return n << 1

def rct2speed_to_mph(verbose, speedMph):
    if not verbose:
        return -1
    #print("Trying to convert", speedMph)
    return ((speedMph) * 9) >> 18
    return speedMph / 65536
    neg = 1
    if str(speedMph)[0] == '-':
        speedMph = int(str(speedMph)[1:])
        neg = -1

    x = ((speedMph) * 9) >> 18
    if len(str(x)) == 5:
        return float("0."+str(x))
    
    front = str(speedMph)[:-5]
    decimals = str(speedMph)[-5:]
    return neg * float(front + "." + decimals)
    
    wholeNumber = speedMph
    fraction = (speedMph - wholeNumber) * 100000
    
    print(wholeNumber, fraction)
    
    left = wholeNumber
    if left == 0:
        return 0
    right = fraction / 100000
    if right == 0:
        return neg * left
    return neg * float(str(left) + "." + str(right))
    # return int(wholeNumber << 16) | int(((fraction << 16) / 100000))
    
    #return (abs(speed) * 9) >> 18
    '''
    neg = False
    if str(speed)[0] == '-':
        speed = int(str(speed)[1:])
        neg = True
    if speed == 0:
        return 0
    if type(speed) is float:
        speed = int(speed)
    h2 = hex(speed)[2]
    y = int(h2, 16)
    if len(str(speed)) >= 4:
        h3 = hex(speed)[3]
        y += int(h3, 16)/16
    if neg:
        y *= -1
    return y
    '''

def mph_to_rct2speed(speed):
    neg = False
    if speed < neg:
        neg = True
        #speed *= -1
    whole_number = int(speed)
    fraction = int(int(speed * 1000) - whole_number * 1000)
    num = whole_number << 16 | ((fraction << 16) // 1000)
    #num = str(num)
    #if neg:
    #    num = '-' + num
    return num

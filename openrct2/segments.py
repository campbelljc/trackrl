from .track_definitions import *
from .speed import *

SEGMENTS = [
	"ELEM_FLAT",                                                 #0
	"ELEM_END_STATION",                                          #1
	"ELEM_BEGIN_STATION",                                        #2
	"ELEM_MIDDLE_STATION",                                       #3
	"ELEM_25_DEG_UP",                                            #4
	"ELEM_60_DEG_UP",                                            #5
	"ELEM_FLAT_TO_25_DEG_UP",                                    #6
	"ELEM_25_DEG_UP_TO_60_DEG_UP",                               #7
	"ELEM_60_DEG_UP_TO_25_DEG_UP",                               #8
	"ELEM_25_DEG_UP_TO_FLAT",                                    #9
	"ELEM_25_DEG_DOWN",                                          #A
	"ELEM_60_DEG_DOWN",                                          #B
	"ELEM_FLAT_TO_25_DEG_DOWN",                                  #C
	"ELEM_25_DEG_DOWN_TO_60_DEG_DOWN",                           #D
	"ELEM_60_DEG_DOWN_TO_25_DEG_DOWN",                           #E
	"ELEM_25_DEG_DOWN_TO_FLAT",                                  #F
	"ELEM_LEFT_QUARTER_TURN_5_TILES",                            #10
	"ELEM_RIGHT_QUARTER_TURN_5_TILES",                           #11
	"ELEM_FLAT_TO_LEFT_BANK",                                    #12
	"ELEM_FLAT_TO_RIGHT_BANK",                                   #13
	"ELEM_LEFT_BANK_TO_FLAT",                                    #14
	"ELEM_RIGHT_BANK_TO_FLAT",                                   #15
	"ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES",                     #16
	"ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES",                    #17
	"ELEM_LEFT_BANK_TO_25_DEG_UP",                               #18
	"ELEM_RIGHT_BANK_TO_25_DEG_UP",                              #19
	"ELEM_25_DEG_UP_TO_LEFT_BANK",                               #1A
	"ELEM_25_DEG_UP_TO_RIGHT_BANK",                              #1B
	"ELEM_LEFT_BANK_TO_25_DEG_DOWN",                             #1C
	"ELEM_RIGHT_BANK_TO_25_DEG_DOWN",                            #1D
	"ELEM_25_DEG_DOWN_TO_LEFT_BANK",                             #1E
	"ELEM_25_DEG_DOWN_TO_RIGHT_BANK",                            #1F
	"ELEM_LEFT_BANK",                                            #20
	"ELEM_RIGHT_BANK",                                           #21
	"ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP",                  #22
	"ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP",                 #23
	"ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN",                #24
	"ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN",               #25
	"ELEM_S_BEND_LEFT",                                          #26
	"ELEM_S_BEND_RIGHT",                                         #27
	"ELEM_LEFT_VERTICAL_LOOP",                                   #28
	"ELEM_RIGHT_VERTICAL_LOOP",                                  #29
	"ELEM_LEFT_QUARTER_TURN_3_TILES",                            #2A
	"ELEM_RIGHT_QUARTER_TURN_3_TILES",                           #2B
	"ELEM_LEFT_QUARTER_TURN_3_TILES_BANK",                       #2C
	"ELEM_RIGHT_QUARTER_TURN_3_TILES_BANK",                      #2D
	"ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP",                  #2E
	"ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP",                 #2F
	"ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN",                #30
	"ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN",               #31
	"ELEM_LEFT_QUARTER_TURN_1_TILE",                             #32
	"ELEM_RIGHT_QUARTER_TURN_1_TILE",                            #33
	"ELEM_LEFT_TWIST_DOWN_TO_UP",                                #34
	"ELEM_RIGHT_TWIST_DOWN_TO_UP",                               #35
	"ELEM_LEFT_TWIST_UP_TO_DOWN",                                #36
	"ELEM_RIGHT_TWIST_UP_TO_DOWN",                               #37
	"ELEM_HALF_LOOP_UP",                                         #38
	"ELEM_HALF_LOOP_DOWN",                                       #39
	"ELEM_LEFT_CORKSCREW_UP",                                    #3A
	"ELEM_RIGHT_CORKSCREW_UP",                                   #3B
	"ELEM_LEFT_CORKSCREW_DOWN",                                  #3C
	"ELEM_RIGHT_CORKSCREW_DOWN",                                 #3D
	"ELEM_FLAT_TO_60_DEG_UP",                                    #3E
	"ELEM_60_DEG_UP_TO_FLAT",                                    #3F
	"ELEM_FLAT_TO_60_DEG_DOWN",                                  #40
	"ELEM_60_DEG_DOWN_TO_FLAT",                                  #41
	"ELEM_TOWER_BASE",                                           #42
	"ELEM_TOWER_SECTION",                                        #43
	"ELEM_FLAT_COVERED",                                         #44
	"ELEM_25_DEG_UP_COVERED",                                    #45
	"ELEM_60_DEG_UP_COVERED",                                    #46
	"ELEM_FLAT_TO_25_DEG_UP_COVERED",                            #47
	"ELEM_25_DEG_UP_TO_60_DEG_UP_COVERED",                       #48
	"ELEM_60_DEG_UP_TO_25_DEG_UP_COVERED",                       #49
	"ELEM_25_DEG_UP_TO_FLAT_COVERED",                            #4A
	"ELEM_25_DEG_DOWN_COVERED",                                  #4B
	"ELEM_60_DEG_DOWN_COVERED",                                  #4C
	"ELEM_FLAT_TO_25_DEG_DOWN_COVERED",                          #4D
	"ELEM_25_DEG_DOWN_TO_60_DEG_DOWN_COVERED",                   #4E
	"ELEM_60_DEG_DOWN_TO_25_DEG_DOWN_COVERED",                   #4F
	"ELEM_25_DEG_DOWN_TO_FLAT_COVERED",                          #50
	"ELEM_LEFT_QUARTER_TURN_5_TILES_COVERED",                    #51
	"ELEM_RIGHT_QUARTER_TURN_5_TILES_COVERED",                   #52
	"ELEM_S_BEND_LEFT_COVERED",                                  #53
	"ELEM_S_BEND_RIGHT_COVERED",                                 #54
	"ELEM_LEFT_QUARTER_TURN_3_TILES_COVERED",                    #55
	"ELEM_RIGHT_QUARTER_TURN_3_TILES_COVERED",                   #56
	"ELEM_LEFT_HALF_BANKED_HELIX_UP_SMALL",                      #57
	"ELEM_RIGHT_HALF_BANKED_HELIX_UP_SMALL",                     #58
	"ELEM_LEFT_HALF_BANKED_HELIX_DOWN_SMALL",                    #59
	"ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_SMALL",                   #5A
	"ELEM_LEFT_HALF_BANKED_HELIX_UP_LARGE",                      #5B
	"ELEM_RIGHT_HALF_BANKED_HELIX_UP_LARGE",                     #5C
	"ELEM_LEFT_HALF_BANKED_HELIX_DOWN_LARGE",                    #5D
	"ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_LARGE",                   #5E
	"ELEM_LEFT_QUARTER_TURN_1_TILE_60_DEG_UP",                   #5F
	"ELEM_RIGHT_QUARTER_TURN_1_TILE_60_DEG_UP",                  #60
	"ELEM_LEFT_QUARTER_TURN_1_TILE_60_DEG_DOWN",                 #61
	"ELEM_RIGHT_QUARTER_TURN_1_TILE_60_DEG_DOWN",                #62
	"ELEM_BRAKES",                                               #63
	"ELEM_ROTATION_CONTROL_TOGGLE",                              #64
	"ELEM_INVERTED_90_DEG_UP_TO_FLAT_QUARTER_LOOP",              #65
	"ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_UP",                   #66
	"ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_UP",                  #67
	"ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_DOWN",                 #68
	"ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_DOWN",                #69
	"ELEM_LEFT_QUARTER_HELIX_LARGE_UP",                          #6A
	"ELEM_RIGHT_QUARTER_HELIX_LARGE_UP",                         #6B
	"ELEM_LEFT_QUARTER_HELIX_LARGE_DOWN",                        #6C
	"ELEM_RIGHT_QUARTER_HELIX_LARGE_DOWN",                       #6D
	"ELEM_25_DEG_UP_LEFT_BANKED",                                #6E
	"ELEM_25_DEG_UP_RIGHT_BANKED",                               #6F
	"ELEM_WATERFALL",                                            #70
	"ELEM_RAPIDS",                                               #71
	"ELEM_ON_RIDE_PHOTO",                                        #72
	"ELEM_25_DEG_DOWN_LEFT_BANKED",                              #73
	"ELEM_25_DEG_DOWN_RIGHT_BANKED",                             #74
	"ELEM_WATER_SPLASH",                                         #75
	"ELEM_FLAT_TO_60_DEG_UP_LONG_BASE",                          #76
	"ELEM_60_DEG_UP_TO_FLAT_LONG_BASE",                          #77
	"ELEM_WHIRLPOOL",                                            #78
	"ELEM_60_DEG_DOWN_TO_FLAT_LONG_BASE",                        #79
	"ELEM_FLAT_TO_60_DEG_DOWN_LONG_BASE",                        #7A
	"ELEM_CABLE_LIFT_HILL",                                      #7B
	"ELEM_REVERSE_WHOA_BELLY_SLOPE",                             #7C
	"ELEM_REVERSE_WHOA_BELLY_VERTICAL",                          #7D
	"ELEM_90_DEG_UP",                                            #7E
	"ELEM_90_DEG_DOWN",                                          #7F
	"ELEM_60_DEG_UP_TO_90_DEG_UP",                               #80
	"ELEM_90_DEG_DOWN_TO_60_DEG_DOWN",                           #81
	"ELEM_90_DEG_UP_TO_60_DEG_UP",                               #82
	"ELEM_60_DEG_DOWN_TO_90_DEG_DOWN",                           #83
	"ELEM_BRAKE_FOR_DROP",                                       #84
	"ELEM_LEFT_EIGHTH_TO_DIAG",                                  #85
	"ELEM_RIGHT_EIGHTH_TO_DIAG",                                 #86
	"ELEM_LEFT_EIGHTH_TO_ORTHOGONAL",                            #87
	"ELEM_RIGHT_EIGHTH_TO_ORTHOGONAL",                           #88
	"ELEM_LEFT_EIGHTH_BANK_TO_DIAG",                             #89
	"ELEM_RIGHT_EIGHTH_BANK_TO_DIAG",                            #8A
	"ELEM_LEFT_EIGHTH_BANK_TO_ORTHOGONAL",                       #8B
	"ELEM_RIGHT_EIGHTH_BANK_TO_ORTHOGONAL",                      #8C
	"ELEM_DIAG_FLAT",                                            #8D
	"ELEM_DIAG_25_DEG_UP",                                       #8E
	"ELEM_DIAG_60_DEG_UP",                                       #8F
	"ELEM_DIAG_FLAT_TO_25_DEG_UP",                               #90
	"ELEM_DIAG_25_DEG_UP_TO_60_DEG_UP",                          #91
	"ELEM_DIAG_60_DEG_UP_TO_25_DEG_UP",                          #92
	"ELEM_DIAG_25_DEG_UP_TO_FLAT",                               #93
	"ELEM_DIAG_25_DEG_DOWN",                                     #94
	"ELEM_DIAG_60_DEG_DOWN",                                     #95
	"ELEM_DIAG_FLAT_TO_25_DEG_DOWN",                             #96
	"ELEM_DIAG_25_DEG_DOWN_TO_60_DEG_DOWN",                      #97
	"ELEM_DIAG_60_DEG_DOWN_TO_25_DEG_DOWN",                      #98
	"ELEM_DIAG_25_DEG_DOWN_TO_FLAT",                             #99
	"ELEM_DIAG_FLAT_TO_60_DEG_UP",                               #9A
	"ELEM_DIAG_60_DEG_UP_TO_FLAT",                               #9B
	"ELEM_DIAG_FLAT_TO_60_DEG_DOWN",                             #9C
	"ELEM_DIAG_60_DEG_DOWN_TO_FLAT",                             #9D
	"ELEM_DIAG_FLAT_TO_LEFT_BANK",                               #9E
	"ELEM_DIAG_FLAT_TO_RIGHT_BANK",                              #9F
	"ELEM_DIAG_LEFT_BANK_TO_FLAT",                               #A0
	"ELEM_DIAG_RIGHT_BANK_TO_FLAT",                              #A1
	"ELEM_DIAG_LEFT_BANK_TO_25_DEG_UP",                          #A2
	"ELEM_DIAG_RIGHT_BANK_TO_25_DEG_UP",                         #A3
	"ELEM_DIAG_25_DEG_UP_TO_LEFT_BANK",                          #A4
	"ELEM_DIAG_25_DEG_UP_TO_RIGHT_BANK",                         #A5
	"ELEM_DIAG_LEFT_BANK_TO_25_DEG_DOWN",                        #A6
	"ELEM_DIAG_RIGHT_BANK_TO_25_DEG_DOWN",                       #A7
	"ELEM_DIAG_25_DEG_DOWN_TO_LEFT_BANK",                        #A8
	"ELEM_DIAG_25_DEG_DOWN_TO_RIGHT_BANK",                       #A9
	"ELEM_DIAG_LEFT_BANK",                                       #AA
	"ELEM_DIAG_RIGHT_BANK",                                      #AB
	"ELEM_LOG_FLUME_REVERSER",                                   #AC
	"ELEM_SPINNING_TUNNEL",                                      #AD
	"ELEM_LEFT_BARREL_ROLL_UP_TO_DOWN",                          #AE
	"ELEM_RIGHT_BARREL_ROLL_UP_TO_DOWN",                         #AF
	"ELEM_LEFT_BARREL_ROLL_DOWN_TO_UP",                          #B0
	"ELEM_RIGHT_BARREL_ROLL_DOWN_TO_UP",                         #B1
	"ELEM_LEFT_BANK_TO_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP",     #B2
	"ELEM_RIGHT_BANK_TO_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP",   #B3
	"ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_LEFT_BANK",   #B4
	"ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_RIGHT_BANK", #B5
	"ELEM_POWERED_LIFT",                                         #B6
	"ELEM_LEFT_LARGE_HALF_LOOP_UP",                              #B7
	"ELEM_RIGHT_LARGE_HALF_LOOP_UP",                             #B8
	"ELEM_RIGHT_LARGE_HALF_LOOP_DOWN",                           #B9
	"ELEM_LEFT_LARGE_HALF_LOOP_DOWN",                            #BA
	"ELEM_LEFT_FLYER_TWIST_UP_TO_DOWN",                          #BB
	"ELEM_RIGHT_FLYER_TWIST_UP_TO_DOWN",                         #BC
	"ELEM_LEFT_FLYER_TWIST_DOWN_TO_UP",                          #BD
	"ELEM_RIGHT_FLYER_TWIST_DOWN_TO_UP",                         #BE
	"ELEM_FLYER_HALF_LOOP_UP",                                   #BF
	"ELEM_FLYER_HALF_LOOP_DOWN",                                 #C0
	"ELEM_LEFT_FLY_CORKSCREW_UP_TO_DOWN",                        #C1
	"ELEM_RIGHT_FLY_CORKSCREW_UP_TO_DOWN",                       #C2
	"ELEM_LEFT_FLY_CORKSCREW_DOWN_TO_UP",                        #C3
	"ELEM_RIGHT_FLY_CORKSCREW_DOWN_TO_UP",                       #C4
	"ELEM_HEARTLINE_TRANSFER_UP",                                #C5
	"ELEM_HEARTLINE_TRANSFER_DOWN",                              #C6
	"ELEM_LEFT_HEARTLINE_ROLL",                                  #C7
	"ELEM_RIGHT_HEARTLINE_ROLL",                                 #C8
	"ELEM_MINI_GOLF_HOLE_A",                                     #C9
	"ELEM_MINI_GOLF_HOLE_B",                                     #CA
	"ELEM_MINI_GOLF_HOLE_C",                                     #CB
	"ELEM_MINI_GOLF_HOLE_D",                                     #CC
	"ELEM_MINI_GOLF_HOLE_E",                                     #CD
	"ELEM_INVERTED_FLAT_TO_90_DEG_DOWN_QUARTER_LOOP",            #CE
	"ELEM_90_DEG_UP_QUARTER_LOOP_TO_INVERTED",                   #CF
	"ELEM_QUARTER_LOOP_INVERT_TO_90_DEG_DOWN",                   #D0
	"ELEM_LEFT_CURVED_LIFT_HILL",                                #D1
	"ELEM_RIGHT_CURVED_LIFT_HILL",                               #D2
	"ELEM_LEFT_REVERSER",                                        #D3
	"ELEM_RIGHT_REVERSER",                                       #D4
	"ELEM_AIR_THRUST_TOP_CAP",                                   #D5
	"ELEM_AIR_THRUST_VERTICAL_DOWN",                             #D6
	"ELEM_AIR_THRUST_VERTICAL_DOWN_TO_LEVEL",                    #D7
	"ELEM_BLOCK_BRAKES",                                         #D8
	"ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP",           #D9
	"ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP",           #DA
    "ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN", #'LeftBankedQuarterTurn3TileDown25',
    "ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN", #'RightBankedQuarterTurn3TileDown25',
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP", #'LeftBankedQuarterTurn5TileUp25',
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP", #'RightBankedQuarterTurn5TileUp25',
    "ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN", #'LeftBankedQuarterTurn5TileDown25',
    "ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN", #'RightBankedQuarterTurn5TileDown25',
    "ELEM_25_DEG_UP_TO_BANKED_LEFT_25_DEG_UP", #'Up25ToLeftBankedUp25',
    'Up25ToRightBankedUp25',
    'LeftBankedUp25ToUp25',
    'RightBankedUp25ToUp25',
    'Down25ToLeftBankedDown25',
    'Down25ToRightBankedDown25',
    'LeftBankedDown25ToDown25',
    'RightBankedDown25ToDown25',
    'LeftBankedFlatToLeftBankedUp25',
    'RightBankedFlatToRightBankedUp25',
    'LeftBankedUp25ToLeftBankedFlat',
    'RightBankedUp25ToRightBankedFlat',
    'LeftBankedFlatToLeftBankedDown25',
    'RightBankedFlatToRightBankedDown25',
    'LeftBankedDown25ToLeftBankedFlat',
    'RightBankedDown25ToRightBankedFlat',
    'FlatToLeftBankedUp25',
    'FlatToRightBankedUp25',
    'LeftBankedUp25ToFlat',
    'RightBankedUp25ToFlat',
    'FlatToLeftBankedDown25',
    'FlatToRightBankedDown25',
    'LeftBankedDown25ToFlat',
    'RightBankedDown25ToFlat',
    'LeftQuarterTurn1TileUp90',
    'RightQuarterTurn1TileUp90',
    'LeftQuarterTurn1TileDown90',
    'RightQuarterTurn1TileDown90',
    'MultiDimUp90ToInvertedFlatQuarterLoop',
    'MultiDimFlatToDown90QuarterLoop',
    'MultiDimInvertedUp90ToFlatQuarterLoop',
    'RotationControlToggle'
]
segment_dict = {k: v for k, v in enumerate(SEGMENTS)}
SEGMENT_NUMS = {v: k for k, v in enumerate(SEGMENTS)}

BLACKLIST = [
    #"ELEM_BRAKES", # temporarily
    
    # not supported by wooden RC
    "ELEM_FLAT_TO_60_DEG_UP_LONG_BASE",
    "ELEM_60_DEG_UP_TO_FLAT_LONG_BASE",
    "ELEM_60_DEG_DOWN_TO_FLAT_LONG_BASE",
    "ELEM_FLAT_TO_60_DEG_DOWN_LONG_BASE",
    "ELEM_INVERTED_90_DEG_UP_TO_FLAT_QUARTER_LOOP",
    "ELEM_RIGHT_QUARTER_TURN_1_TILE",
    "ELEM_LEFT_QUARTER_TURN_1_TILE",
    "RightQuarterTurn1TileDown90",
    "RightQuarterTurn1TileUp90",
    "LeftQuarterTurn1TileDown90",
    "LeftQuarterTurn1TileUp90",
    'ELEM_60_DEG_DOWN_TO_90_DEG_DOWN',
    'ELEM_60_DEG_DOWN_TO_FLAT',
    'ELEM_60_DEG_UP_TO_90_DEG_UP',
    'ELEM_60_DEG_UP_TO_FLAT',
    'ELEM_90_DEG_DOWN',
    'ELEM_90_DEG_DOWN_TO_60_DEG_DOWN',
    'ELEM_90_DEG_UP',
    'ELEM_90_DEG_UP_TO_60_DEG_UP',
    'ELEM_DIAG_60_DEG_DOWN_TO_FLAT',
    'ELEM_DIAG_60_DEG_UP_TO_FLAT',
    'ELEM_DIAG_FLAT_TO_60_DEG_DOWN',
    'ELEM_DIAG_FLAT_TO_60_DEG_UP',
    'ELEM_FLAT_TO_60_DEG_DOWN',
    'ELEM_FLAT_TO_60_DEG_UP'
]
blacklist_indices = [SEGMENT_NUMS[segment] for segment in BLACKLIST]

def get_next_piece_to_flat(coords, track_def):
    if coords.rotation_end & 4:
        if track_def.vangle_end == TRACK_SLOPE_NONE:
            if track_def.bank_end == TRACK_BANK_NONE:
                return [("ELEM_DIAG_FLAT", CHAIN_LIFT_FLAGS), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
            elif track_def.bank_end == TRACK_BANK_LEFT:
                return [("ELEM_DIAG_LEFT_BANK_TO_FLAT", 0), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
            elif track_def.bank_end == TRACK_BANK_RIGHT:
                return [("ELEM_DIAG_RIGHT_BANK_TO_FLAT", 0), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_UP_25:
            assert track_def.bank_end == TRACK_BANK_NONE
            return [("ELEM_DIAG_25_DEG_UP_TO_FLAT", CHAIN_LIFT_FLAGS), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]

        elif track_def.vangle_end == TRACK_SLOPE_DOWN_25:
            assert track_def.bank_end == TRACK_BANK_NONE
            return [("ELEM_DIAG_25_DEG_DOWN_TO_FLAT", 0), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_UP_60:
            assert track_def.bank_end == TRACK_BANK_NONE
            return [("ELEM_DIAG_60_DEG_UP_TO_25_DEG_UP", CHAIN_LIFT_FLAGS), ("ELEM_DIAG_25_DEG_UP_TO_FLAT", CHAIN_LIFT_FLAGS), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_DOWN_60:
            return [("ELEM_DIAG_60_DEG_DOWN_TO_25_DEG_DOWN", 0), ("ELEM_DIAG_25_DEG_DOWN_TO_FLAT", 0), ("ELEM_LEFT_EIGHTH_TO_ORTHOGONAL", 0)]
        
        assert False, track_def.vangle_end
    else:
        if track_def.vangle_end == TRACK_SLOPE_NONE:
            if track_def.bank_end == TRACK_BANK_NONE:
                # problem: we check for a following piece with chain lift here. but in next iteration,
                # since flat is not an up piece, we will not check speed(?) so won't catch collision
                return [("ELEM_FLAT", 0)]
            elif track_def.bank_end == TRACK_BANK_LEFT:
                return [("ELEM_LEFT_BANK_TO_FLAT", 0)]
            elif track_def.bank_end == TRACK_BANK_RIGHT:
                return [("ELEM_RIGHT_BANK_TO_FLAT", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_UP_25:
            if track_def.bank_end == TRACK_BANK_NONE:
                return [("ELEM_25_DEG_UP_TO_FLAT", CHAIN_LIFT_FLAGS)]
            elif track_def.bank_end == TRACK_BANK_LEFT:
                return [("LeftBankedUp25ToFlat", 0)]
            elif track_def.bank_end == TRACK_BANK_RIGHT:
                return [("RightBankedUp25ToFlat", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_DOWN_25:
            if track_def.bank_end == TRACK_BANK_NONE:
                return [("ELEM_25_DEG_DOWN_TO_FLAT", 0)]
            elif track_def.bank_end == TRACK_BANK_LEFT:
                return [("LeftBankedDown25ToFlat", 0)]
            elif track_def.bank_end == TRACK_BANK_RIGHT:
                return [("RightBankedDown25ToFlat", 0)]
    
        elif track_def.vangle_end == TRACK_SLOPE_UP_60:
            assert track_def.bank_end == TRACK_BANK_NONE
            return [("ELEM_60_DEG_UP_TO_25_DEG_UP", CHAIN_LIFT_FLAGS), ("ELEM_25_DEG_UP_TO_FLAT", CHAIN_LIFT_FLAGS)]
    
        elif track_def.vangle_end == TRACK_SLOPE_DOWN_60:
            assert track_def.bank_end == TRACK_BANK_NONE
            return [("ELEM_60_DEG_DOWN_TO_25_DEG_DOWN", 0), ("ELEM_25_DEG_DOWN_TO_FLAT", 0)]
                
        assert False, track_def.vangle_end
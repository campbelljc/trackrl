
class TrackCoords:
    def __init__(self, a, b, c, d, e, f):
        self.rotation_begin = a
        self.rotation_end = b
        self.z_begin = c
        self.z_end = d
        self.x = e
        self.y = f

TRACK_COORDINATES = [
        # RB RE ZB ZE  X  Y
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_FLAT
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_END_STATION
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_BEGIN_STATION
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_MIDDLE_STATION
        [ 0, 0, 0, 16, 0, 0 ],      # ELEM_25_DEG_UP
        [ 0, 0, 0, 64, 0, 0 ],      # ELEM_60_DEG_UP
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_FLAT_TO_25_DEG_UP
        [ 0, 0, 0, 32, 0, 0 ],      # ELEM_25_DEG_UP_TO_60_DEG_UP
        [ 0, 0, 0, 32, 0, 0 ],      # ELEM_60_DEG_UP_TO_25_DEG_UP
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_25_DEG_UP_TO_FLAT
        [ 0, 0, 16, 0, 0, 0 ],      # ELEM_25_DEG_DOWN
        [ 0, 0, 64, 0, 0, 0 ],      # ELEM_60_DEG_DOWN
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_FLAT_TO_25_DEG_DOWN
        [ 0, 0, 32, 0, 0, 0 ],      # ELEM_25_DEG_DOWN_TO_60_DEG_DOWN
        [ 0, 0, 32, 0, 0, 0 ],      # ELEM_60_DEG_DOWN_TO_25_DEG_DOWN
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_25_DEG_DOWN_TO_FLAT
        [ 0, 3, 0, 0, -64, -64 ],   # ELEM_LEFT_QUARTER_TURN_5_TILES
        [ 0, 1, 0, 0, -64, 64 ],    # ELEM_RIGHT_QUARTER_TURN_5_TILES
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_FLAT_TO_LEFT_BANK
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_FLAT_TO_RIGHT_BANK
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_LEFT_BANK_TO_FLAT
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_RIGHT_BANK_TO_FLAT
        [ 0, 3, 0, 0, -64, -64 ],   # ELEM_BANKED_LEFT_QUARTER_TURN_5_TILES
        [ 0, 1, 0, 0, -64, 64 ],    # ELEM_BANKED_RIGHT_QUARTER_TURN_5_TILES
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_LEFT_BANK_TO_25_DEG_UP
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_RIGHT_BANK_TO_25_DEG_UP
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_25_DEG_UP_TO_LEFT_BANK
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_25_DEG_UP_TO_RIGHT_BANK
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_LEFT_BANK_TO_25_DEG_DOWN
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_RIGHT_BANK_TO_25_DEG_DOWN
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_25_DEG_DOWN_TO_LEFT_BANK
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_25_DEG_DOWN_TO_RIGHT_BANK
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_LEFT_BANK
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_RIGHT_BANK
        [ 0, 3, 0, 64, -64, -64 ],  # ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_UP
        [ 0, 1, 0, 64, -64, 64 ],   # ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_UP
        [ 0, 3, 64, 0, -64, -64 ],  # ELEM_LEFT_QUARTER_TURN_5_TILES_25_DEG_DOWN
        [ 0, 1, 64, 0, -64, 64 ],   # ELEM_RIGHT_QUARTER_TURN_5_TILES_25_DEG_DOWN
        [ 0, 0, 0, 0, -64, -32 ],   # ELEM_S_BEND_LEFT
        [ 0, 0, 0, 0, -64, 32 ],    # ELEM_S_BEND_RIGHT
        [ 0, 0, 0, 0, -32, -32 ],   # ELEM_LEFT_VERTICAL_LOOP
        [ 0, 0, 0, 0, -32, 32 ],    # ELEM_RIGHT_VERTICAL_LOOP
        [ 0, 3, 0, 0, -32, -32 ],   # ELEM_LEFT_QUARTER_TURN_3_TILES
        [ 0, 1, 0, 0, -32, 32 ],    # ELEM_RIGHT_QUARTER_TURN_3_TILES
        [ 0, 3, 0, 0, -32, -32 ],   # ELEM_LEFT_QUARTER_TURN_3_TILES_BANK
        [ 0, 1, 0, 0, -32, 32 ],    # ELEM_RIGHT_QUARTER_TURN_3_TILES_BANK
        [ 0, 3, 0, 32, -32, -32 ],  # ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 1, 0, 32, -32, 32 ],   # ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 3, 32, 0, -32, -32 ],  # ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN
        [ 0, 1, 32, 0, -32, 32 ],   # ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN
        [ 0, 3, 0, 0, 0, 0 ],       # ELEM_LEFT_QUARTER_TURN_1_TILE
        [ 0, 1, 0, 0, 0, 0 ],       # ELEM_RIGHT_QUARTER_TURN_1_TILE
        [ 0, 0, 0, 16, -64, 0 ],    # ELEM_LEFT_TWIST_DOWN_TO_UP
        [ 0, 0, 0, 16, -64, 0 ],    # ELEM_RIGHT_TWIST_DOWN_TO_UP
        [ 0, 0, 0, -16, -64, 0 ],   # ELEM_LEFT_TWIST_UP_TO_DOWN
        [ 0, 0, 0, -16, -64, 0 ],   # ELEM_RIGHT_TWIST_UP_TO_DOWN
        [ 0, 2, 0, 152, -32, 0 ],   # ELEM_HALF_LOOP_UP
        [ 0, 2, 0, -152, 32, 0 ],   # ELEM_HALF_LOOP_DOWN
        [ 0, 3, 0, 80, -32, -32 ],  # ELEM_LEFT_CORKSCREW_UP
        [ 0, 1, 0, 80, -32, 32 ],   # ELEM_RIGHT_CORKSCREW_UP
        [ 0, 3, 0, -80, -32, -32 ], # ELEM_LEFT_CORKSCREW_DOWN
        [ 0, 1, 0, -80, -32, 32 ],  # ELEM_RIGHT_CORKSCREW_DOWN
        [ 0, 0, 0, 24, 0, 0 ],      # ELEM_FLAT_TO_60_DEG_UP
        [ 0, 0, 0, 24, 0, 0 ],      # ELEM_60_DEG_UP_TO_FLAT
        [ 0, 0, 24, 0, 0, 0 ],      # ELEM_FLAT_TO_60_DEG_DOWN
        [ 0, 0, 24, 0, 0, 0 ],      # ELEM_60_DEG_DOWN_TO_FLAT
        [ 0, 0, 0, 96, 32, 0 ],     # ELEM_TOWER_BASE
        [ 0, 0, 0, 32, 32, 0 ],     # ELEM_TOWER_SECTION
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_FLAT_COVERED
        [ 0, 0, 0, 16, 0, 0 ],      # ELEM_25_DEG_UP_COVERED
        [ 0, 0, 0, 64, 0, 0 ],      # ELEM_60_DEG_UP_COVERED
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_FLAT_TO_25_DEG_UP_COVERED
        [ 0, 0, 0, 32, 0, 0 ],      # ELEM_25_DEG_UP_TO_60_DEG_UP_COVERED
        [ 0, 0, 0, 32, 0, 0 ],      # ELEM_60_DEG_UP_TO_25_DEG_UP_COVERED
        [ 0, 0, 0, 8, 0, 0 ],       # ELEM_25_DEG_UP_TO_FLAT_COVERED
        [ 0, 0, 16, 0, 0, 0 ],      # ELEM_25_DEG_DOWN_COVERED
        [ 0, 0, 64, 0, 0, 0 ],      # ELEM_60_DEG_DOWN_COVERED
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_FLAT_TO_25_DEG_DOWN_COVERED
        [ 0, 0, 32, 0, 0, 0 ],      # ELEM_25_DEG_DOWN_TO_60_DEG_DOWN_COVERED
        [ 0, 0, 32, 0, 0, 0 ],      # ELEM_60_DEG_DOWN_TO_25_DEG_DOWN_COVERED
        [ 0, 0, 8, 0, 0, 0 ],       # ELEM_25_DEG_DOWN_TO_FLAT_COVERED
        [ 0, 3, 0, 0, -64, -64 ],   # ELEM_LEFT_QUARTER_TURN_5_TILES_COVERED
        [ 0, 1, 0, 0, -64, 64 ],    # ELEM_RIGHT_QUARTER_TURN_5_TILES_COVERED
        [ 0, 0, 0, 0, -64, -32 ],   # ELEM_S_BEND_LEFT_COVERED
        [ 0, 0, 0, 0, -64, 32 ],    # ELEM_S_BEND_RIGHT_COVERED
        [ 0, 3, 0, 0, -32, -32 ],   # ELEM_LEFT_QUARTER_TURN_3_TILES_COVERED
        [ 0, 1, 0, 0, -32, 32 ],    # ELEM_RIGHT_QUARTER_TURN_3_TILES_COVERED
        [ 0, 2, 0, 16, 0, -96 ],    # ELEM_LEFT_HALF_BANKED_HELIX_UP_SMALL
        [ 0, 2, 0, 16, 0, 96 ],     # ELEM_RIGHT_HALF_BANKED_HELIX_UP_SMALL
        [ 0, 2, 16, 0, 0, -96 ],    # ELEM_LEFT_HALF_BANKED_HELIX_DOWN_SMALL
        [ 0, 2, 16, 0, 0, 96 ],     # ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_SMALL
        [ 0, 2, 0, 16, 0, -160 ],   # ELEM_LEFT_HALF_BANKED_HELIX_UP_LARGE
        [ 0, 2, 0, 16, 0, 160 ],    # ELEM_RIGHT_HALF_BANKED_HELIX_UP_LARGE
        [ 0, 2, 16, 0, 0, -160 ],   # ELEM_LEFT_HALF_BANKED_HELIX_DOWN_LARGE
        [ 0, 2, 16, 0, 0, 160 ],    # ELEM_RIGHT_HALF_BANKED_HELIX_DOWN_LARGE
        [ 0, 3, 0, 64, 0, 0 ],      # ELEM_LEFT_QUARTER_TURN_1_TILE_60_DEG_UP
        [ 0, 1, 0, 64, 0, 0 ],      # ELEM_RIGHT_QUARTER_TURN_1_TILE_60_DEG_UP
        [ 0, 3, 64, 0, 0, 0 ],      # ELEM_LEFT_QUARTER_TURN_1_TILE_60_DEG_DOWN
        [ 0, 1, 64, 0, 0, 0 ],      # ELEM_RIGHT_QUARTER_TURN_1_TILE_60_DEG_DOWN
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_BRAKES
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_ROTATION_CONTROL_TOGGLE
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_INVERTED_90_DEG_UP_TO_FLAT_QUARTER_LOOP
        [ 0, 3, 0, 16, -64, -64 ],  # ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_UP
        [ 0, 1, 0, 16, -64, 64 ],   # ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_UP
        [ 0, 3, 16, 0, -64, -64 ],  # ELEM_LEFT_QUARTER_BANKED_HELIX_LARGE_DOWN
        [ 0, 1, 16, 0, -64, 64 ],   # ELEM_RIGHT_QUARTER_BANKED_HELIX_LARGE_DOWN
        [ 0, 3, 0, 16, -64, -64 ],  # ELEM_LEFT_QUARTER_HELIX_LARGE_UP
        [ 0, 1, 0, 16, -64, 64 ],   # ELEM_RIGHT_QUARTER_HELIX_LARGE_UP
        [ 0, 3, 16, 0, -64, -64 ],  # ELEM_LEFT_QUARTER_HELIX_LARGE_DOWN
        [ 0, 1, 16, 0, -64, 64 ],   # ELEM_RIGHT_QUARTER_HELIX_LARGE_DOWN
        [ 0, 0, 0, 16, 0, 0 ],      # ELEM_25_DEG_UP_LEFT_BANKED
        [ 0, 0, 0, 16, 0, 0 ],      # ELEM_25_DEG_UP_RIGHT_BANKED
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_WATERFALL
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_RAPIDS
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_ON_RIDE_PHOTO
        [ 0, 0, 16, 0, 0, 0 ],      # ELEM_25_DEG_DOWN_LEFT_BANKED
        [ 0, 0, 16, 0, 0, 0 ],      # ELEM_25_DEG_DOWN_RIGHT_BANKED
        [ 0, 0, 16, 16, -128, 0 ],  # ELEM_WATER_SPLASH
        [ 0, 0, 0, 88, -96, 0 ],    # ELEM_FLAT_TO_60_DEG_UP_LONG_BASE
        [ 0, 0, 0, 88, -96, 0 ],    # ELEM_60_DEG_UP_TO_FLAT_LONG_BASE
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_WHIRLPOOL
        [ 0, 0, 88, 0, -96, 0 ],    # ELEM_60_DEG_DOWN_TO_FLAT_LONG_BASE
        [ 0, 0, 88, 0, -96, 0 ],    # ELEM_FLAT_TO_60_DEG_DOWN_LONG_BASE
        [ 0, 0, 0, -96, -96, 0 ],   # ELEM_CABLE_LIFT_HILL
        [ 0, 0, 0, 240, -160, 0 ],  # ELEM_REVERSE_FREEFALL_SLOPE
        [ 0, 0, 0, 80, 32, 0 ],     # ELEM_REVERSE_FREEFALL_VERTICAL
        [ 0, 0, 0, 32, 32, 0 ],     # ELEM_90_DEG_UP
        [ 0, 0, 32, 0, 32, 0 ],     # ELEM_90_DEG_DOWN
        [ 0, 0, 0, 56, 32, 0 ],     # ELEM_60_DEG_UP_TO_90_DEG_UP
        [ 0, 0, 56, 0, 0, 0 ],      # ELEM_90_DEG_DOWN_TO_60_DEG_DOWN
        [ 0, 0, 0, 56, 0, 0 ],      # ELEM_90_DEG_UP_TO_60_DEG_UP
        [ 0, 0, 56, 0, 32, 0 ],     # ELEM_60_DEG_DOWN_TO_90_DEG_DOWN
        [ 0, 0, 24, 0, 0, 0 ],      # ELEM_BRAKE_FOR_DROP
        [ 0, 7, 0, 0, -64, -32 ],   # ELEM_LEFT_EIGHTH_TO_DIAG
        [ 0, 4, 0, 0, -64, 32 ],    # ELEM_RIGHT_EIGHTH_TO_DIAG
        [ 4, 0, 0, 0, -64, 32 ],    # ELEM_LEFT_EIGHTH_TO_ORTHOGONAL
        [ 4, 1, 0, 0, -32, 64 ],    # ELEM_RIGHT_EIGHTH_TO_ORTHOGONAL
        [ 0, 7, 0, 0, -64, -32 ],   # ELEM_LEFT_EIGHTH_BANK_TO_DIAG
        [ 0, 4, 0, 0, -64, 32 ],    # ELEM_RIGHT_EIGHTH_BANK_TO_DIAG
        [ 4, 0, 0, 0, -64, 32 ],    # ELEM_LEFT_EIGHTH_BANK_TO_ORTHOGONAL
        [ 4, 1, 0, 0, -32, 64 ],    # ELEM_RIGHT_EIGHTH_BANK_TO_ORTHOGONAL
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_FLAT
        [ 4, 4, 0, 16, -32, 32 ],   # ELEM_DIAG_25_DEG_UP
        [ 4, 4, 0, 64, -32, 32 ],   # ELEM_DIAG_60_DEG_UP
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_FLAT_TO_25_DEG_UP
        [ 4, 4, 0, 32, -32, 32 ],   # ELEM_DIAG_25_DEG_UP_TO_60_DEG_UP
        [ 4, 4, 0, 32, -32, 32 ],   # ELEM_DIAG_60_DEG_UP_TO_25_DEG_UP
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_25_DEG_UP_TO_FLAT
        [ 4, 4, 16, 0, -32, 32 ],   # ELEM_DIAG_25_DEG_DOWN
        [ 4, 4, 64, 0, -32, 32 ],   # ELEM_DIAG_60_DEG_DOWN
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_FLAT_TO_25_DEG_DOWN
        [ 4, 4, 32, 0, -32, 32 ],   # ELEM_DIAG_25_DEG_DOWN_TO_60_DEG_DOWN
        [ 4, 4, 32, 0, -32, 32 ],   # ELEM_DIAG_60_DEG_DOWN_TO_25_DEG_DOWN
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_25_DEG_DOWN_TO_FLAT
        [ 4, 4, 0, 24, -32, 32 ],   # ELEM_DIAG_FLAT_TO_60_DEG_UP
        [ 4, 4, 0, 24, -32, 32 ],   # ELEM_DIAG_60_DEG_UP_TO_FLAT
        [ 4, 4, 24, 0, -32, 32 ],   # ELEM_DIAG_FLAT_TO_60_DEG_DOWN
        [ 4, 4, 24, 0, -32, 32 ],   # ELEM_DIAG_60_DEG_DOWN_TO_FLAT
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_FLAT_TO_LEFT_BANK
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_FLAT_TO_RIGHT_BANK
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_LEFT_BANK_TO_FLAT
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_RIGHT_BANK_TO_FLAT
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_LEFT_BANK_TO_25_DEG_UP
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_RIGHT_BANK_TO_25_DEG_UP
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_25_DEG_UP_TO_LEFT_BANK
        [ 4, 4, 0, 8, -32, 32 ],    # ELEM_DIAG_25_DEG_UP_TO_RIGHT_BANK
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_LEFT_BANK_TO_25_DEG_DOWN
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_RIGHT_BANK_TO_25_DEG_DOWN
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_25_DEG_DOWN_TO_LEFT_BANK
        [ 4, 4, 8, 0, -32, 32 ],    # ELEM_DIAG_25_DEG_DOWN_TO_RIGHT_BANK
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_LEFT_BANK
        [ 4, 4, 0, 0, -32, 32 ],    # ELEM_DIAG_RIGHT_BANK
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_LOG_FLUME_REVERSER
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_SPINNING_TUNNEL
        [ 0, 0, 0, 32, -64, 0 ],    # ELEM_LEFT_BARREL_ROLL_UP_TO_DOWN
        [ 0, 0, 0, 32, -64, 0 ],    # ELEM_RIGHT_BARREL_ROLL_UP_TO_DOWN
        [ 0, 0, 0, -32, -64, 0 ],   # ELEM_LEFT_BARREL_ROLL_DOWN_TO_UP
        [ 0, 0, 0, -32, -64, 0 ],   # ELEM_RIGHT_BARREL_ROLL_DOWN_TO_UP
        [ 0, 3, 0, 24, -32, -32 ],  # ELEM_LEFT_BANK_TO_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 1, 0, 24, -32, 32 ],   # ELEM_RIGHT_BANK_TO_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 3, 24, 0, -32, -32 ],  # ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_LEFT_BANK
        [ 0, 1, 24, 0, -32, 32 ],   # ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_RIGHT_BANK
        [ 0, 0, 0, 16, 0, 0 ],      # ELEM_POWERED_LIFT
        [ 0, 2, 0, 280, -64, -32 ], # ELEM_LEFT_LARGE_HALF_LOOP_UP
        [ 0, 2, 0, 280, -64, 32 ],  # ELEM_RIGHT_LARGE_HALF_LOOP_UP
        [ 0, 2, 0, -280, 64, -32 ], # ELEM_RIGHT_LARGE_HALF_LOOP_DOWN
        [ 0, 2, 0, -280, 64, 32 ],  # ELEM_LEFT_LARGE_HALF_LOOP_DOWN
        [ 0, 0, 0, -16, -64, 0 ],   # ELEM_LEFT_FLYER_TWIST_UP_TO_DOWN
        [ 0, 0, 0, -16, -64, 0 ],   # ELEM_RIGHT_FLYER_TWIST_UP_TO_DOWN
        [ 0, 0, 0, 16, -64, 0 ],    # ELEM_LEFT_FLYER_TWIST_DOWN_TO_UP
        [ 0, 0, 0, 16, -64, 0 ],    # ELEM_RIGHT_FLYER_TWIST_DOWN_TO_UP
        [ 0, 2, 0, 120, -32, 0 ],   # ELEM_FLYER_HALF_LOOP_UP
        [ 0, 2, 0, -120, 32, 0 ],   # ELEM_FLYER_HALF_LOOP_DOWN
        [ 0, 3, 0, 48, -32, -32 ],  # ELEM_LEFT_FLY_CORKSCREW_UP_TO_DOWN
        [ 0, 1, 0, 48, -32, 32 ],   # ELEM_RIGHT_FLY_CORKSCREW_UP_TO_DOWN
        [ 0, 3, 0, -48, -32, -32 ], # ELEM_LEFT_FLY_CORKSCREW_DOWN_TO_UP
        [ 0, 1, 0, -48, -32, 32 ],  # ELEM_RIGHT_FLY_CORKSCREW_DOWN_TO_UP
        [ 0, 2, 0, 32, 0, 0 ],      # ELEM_HEARTLINE_TRANSFER_UP
        [ 0, 2, 0, -32, 0, 0 ],     # ELEM_HEARTLINE_TRANSFER_DOWN
        [ 0, 0, 0, 0, -160, 0 ],    # ELEM_LEFT_HEARTLINE_ROLL
        [ 0, 0, 0, 0, -160, 0 ],    # ELEM_RIGHT_HEARTLINE_ROLL
        [ 0, 0, 0, 0, -32, 0 ],     # ELEM_MINI_GOLF_HOLE_A
        [ 0, 0, 0, 0, -32, 0 ],     # ELEM_MINI_GOLF_HOLE_B
        [ 0, 0, 0, 0, -32, 0 ],     # ELEM_MINI_GOLF_HOLE_C
        [ 0, 1, 0, 0, -32, 32 ],    # ELEM_MINI_GOLF_HOLE_D
        [ 0, 3, 0, 0, -32, -32 ],   # ELEM_MINI_GOLF_HOLE_E
        [ 0, 2, 0, -96, -96, 0 ],   # ELEM_INVERTED_FLAT_TO_90_DEG_DOWN_QUARTER_LOOP
        [ 0, 2, 0, 128, 64, 0 ],    # ELEM_90_DEG_UP_QUARTER_LOOP_TO_INVERTED
        [ 0, 2, 0, -128, -96, 0 ],  # ELEM_QUARTER_LOOP_INVERT_TO_90_DEG_DOWN
        [ 0, 3, 0, 16, -32, -32 ],  # ELEM_LEFT_CURVED_LIFT_HILL
        [ 0, 1, 0, 16, -32, 32 ],   # ELEM_RIGHT_CURVED_LIFT_HILL
        [ 0, 0, 0, 0, -64, 0 ],     # ELEM_LEFT_REVERSER
        [ 0, 0, 0, 0, -64, 0 ],     # ELEM_RIGHT_REVERSER
        [ 0, 0, 0, 0, -32, 0 ],     # ELEM_AIR_THRUST_TOP_CAP
        [ 0, 0, 80, 0, 32, 0 ],     # ELEM_AIR_THRUST_VERTICAL_DOWN
        [ 0, 0, 240, 0, -160, 0 ],  # ELEM_AIR_THRUST_VERTICAL_DOWN_TO_LEVEL
        [ 0, 0, 0, 0, 0, 0 ],       # ELEM_BLOCK_BRAKES
        [ 0, 3, 0, 32, -32, -32 ],  # ELEM_BANKED_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 1, 0, 32, -32, 32 ],   # ELEM_BANKED_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP
        [ 0, 3, 32, 0, -32, -32 ], #l
        [ 0, 1, 32, 0, -32, 32 ],  #r
        [ 0, 3, 0, 64, -64, -64 ], #l
        [ 0, 1, 0, 64, -64, 64 ],  # r
        [ 0, 3, 64, 0, -64, -64 ],# l
        [ 0, 1, 64, 0, -64, 64 ], #r
        [ 0, 0, 0, 16, 0, 0 ], #up25
        [ 0, 0, 0, 16, 0, 0 ], #up25
        [ 0, 0, 0, 16, 0, 0 ],
        [ 0, 0, 0, 16, 0, 0 ],
        [ 0, 0, 16, 0, 0, 0 ],
        [ 0, 0, 16, 0, 0, 0 ],
        [ 0, 0, 16, 0, 0, 0 ],
        [ 0, 0, 16, 0, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 0, 8, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 0, 8, 0, 0, 0 ],
        [ 0, 3, 0, 96, 0, 32 ],
        [ 0, 1, 0, 96, 0, -32 ],
        [ 0, 3, 96, 0, 0, 32 ],
        [ 0, 1, 96, 0, 0, -32 ],
        [ 0, 2, 0, 96, 64, 0 ],
        [ 0, 2, 0, -128, -96, 0 ],
        [ 0, 2, 0, 128, 64, 0 ],
        [ 0, 0, 0, 0, 0, 0 ],
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x4A
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack2x2
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack4x4
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack2x4
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x5
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x1A
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x4B
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x1B
        [    0,    2,    0,    0,    0,   32 ], # TrackElemType::FlatTrack1x4C
        [    0,    0,    0,   96,   32,    0 ], # TrackElemType::FlatTrack3x3
]
TRACK_COORDINATES = [TrackCoords(*x) for x in TRACK_COORDINATES]
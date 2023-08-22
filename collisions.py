import os, traceback, math
from collections import defaultdict
from collections.abc import Iterable
from copy import deepcopy
import copy

import dill
import numpy as np
from tabulate import tabulate

from geo import *
from openrct2 import *
import astar

import sys
np.set_printoptions(threshold=sys.maxsize)

def copy_vars(_vars):
    vars_copy = dict(_vars)
    vars_copy['cars'] = list(vars_copy['cars'])
    for i in range(len(vars_copy['cars'])):
        vars_copy['cars'][i] = dict(vars_copy['cars'][i])
        vars_copy['cars'][i]['update_flags'] = list(vars_copy['cars'][i]['update_flags'])
    vars_copy['ProximityScores'] = list(vars_copy['ProximityScores'])
    vars_copy['speeds'] = list(vars_copy['speeds'])
    vars_copy['speeds_mph'] = list(vars_copy['speeds_mph'])
    return vars_copy

class CollisionData:
    def __init__(self, collided, col_d, v, speed, gfV, gfL, s, max_gfL, pieces, num_consecutive_flat_segments, _vars, cur_p, points, blocks, new_points, speed_mph):
        self.collided = collided
        self.col_d = col_d
        self.v = v
        self.speed = speed
        self.speed_mph = speed_mph
        self.gfV = gfV
        self.gfL = gfL
        self.s = s
        self.max_gfL = max_gfL
        self.pieces = pieces
        self.num_consecutive_flat_segments = num_consecutive_flat_segments
        self._vars = _vars
        
        self.cur_p = cur_p
        self.points = points
        self.blocks = blocks
        self.new_points = new_points
        self.err_msg = ""
    
    def copy(self):
        col_d = copy.copy(self.col_d)
        for k in col_d:
            col_d[k] = list(col_d[k])
        v = Vector(self.v)
        vars_copy = copy_vars(self._vars)
        
        return CollisionData(self.collided, col_d, v, self.speed, self.gfV, self.gfL, s=self.s, max_gfL=self.max_gfL, pieces=list(self.pieces), num_consecutive_flat_segments=self.num_consecutive_flat_segments, _vars=vars_copy, cur_p=self.cur_p, points=dict(self.points), blocks=list(self.blocks), new_points=list(self.new_points), speed_mph=self.speed_mph)
    
    @classmethod
    def new(cls, pt=None):
        #assert pt is None or type(pt) is Point, type(pt)
        cars = []
        
        if pt is None:
            start_pt = Point()
        else:
            start_pt = Point.from_Point(pt)
        
        # CreateVehicles
        remainingDistance = 0;
        chosenLoc = Point.from_Point(start_pt) #1000, 1000, 500)
        # vehicle_create_trains
        #for (vehicleIndex = 0; vehicleIndex < ride->num_vehicles; vehicleIndex++):
            #train_ref train = vehicle_create_train(rideIndex, trainsPos, vehicleIndex, &remainingDistance, trackElement);
            # vehicle_create_train
        for i in range(4): # (carIndex = 0; carIndex < ride->num_cars_per_train; carIndex++):
            #auto vehicle = ride_entry_get_vehicle_at_position(ride->subtype, ride->num_cars_per_train, carIndex);       
            #rct_ride_entry* rideEntry = get_ride_entry(rideEntryIndex);
            #if (position == 0 && rideEntry->front_vehicle != 255)
            #    return rideEntry->front_vehicle;
            #_legacyType.FrontCar = Json::GetNumber<uint8_t>(headCars[0], 0xFF);
            
            #auto car = vehicle_create_car(
            #    rideIndex, 0, carIndex, vehicleIndex, trainPos, remainingDistance, trackElement)
            # vehicle_create_car
            
            edx = 174320 >> 1
            remainingDistance -= edx
            cars.append({
                'remaining_distance': remainingDistance,
                'mass': 350,
                'velocity': 0,
                'acceleration': 0,
                'sub_state': 0,
                'Pitch': 0,
                'bank_rotation': 0,
                'TrackLocation': None,
                'pt': Point.from_Point(chosenLoc),
                'track_progress': 31,
                'status': STATUS_DEPARTING, #MOVINGTOENDOFSTATION,
                'update_flags': [],
                #'seg_num': 0,
            })
            remainingDistance -= edx
            delta = Point(-word_9A2A60[0][0]/32, -word_9A2A60[0][1]/32, 0)
            #print(type(delta), type(chosenLoc))
            chosenLoc += delta #8//8)
            
        _vars = {
            'status': STATUS_MOVINGTOENDOFSTATION,
            '_vehicleVelocityF64E08': 0, # set in UpdateVelocity
            '_vehicleVelocityF64E0C': 0, # set in UpdateVelocity
            '_vehicleStationIndex': None,
            'cars': cars,
            
            # measurements
            'average_speed_test_timeout': 0,
            'max_speed': 0,
            'average_speed': 0,
            'max_speed_mph': 0,
            'average_speed_mph': 0,
            'speeds': [],
            'speeds_mph': [], 
            'SegmentTime': 0,
            'SegmentLength': 0,
            'previous_vertical_g': 0,
            'previous_lateral_g': 0,
            'total_air_time': 0,
            'max_positive_vertical_g': FIXED_2DP(1, 0),
            'max_negative_vertical_g': FIXED_2DP(1, 0),
            'max_lateral_g': 0,
            'CurTestTrackLocation': None,
            'testing_flags': 0,
            'drops': 0,
            'special_track_elements': 0,
            'turn_count_default': 0,
            'turn_count_banked': 0,
            'turn_count_sloped': 0,
            'highest_drop_height': 0,
            'start_drop_height': 0,
            'inversions': 0,
            'num_cars_per_train': 3,
            'ProximityScores': [0] * 26,
            'min_z': pt.z if pt is not None else 0, #1000,
        }
        return cls(collided=False,
                     col_d=defaultdict(list),
                     v=Vector(start_pt, 0), # 1000, 1000, 500
                     speed=6, speed_mph=6,
                     gfV=0, gfL=0, s=0, max_gfL=0,
                     pieces=[], num_consecutive_flat_segments=0,
                     _vars=_vars, cur_p=0, points=dict(), blocks=[], new_points=[])
    
    def __hash__(self):
        return hash(tuple((self.v.pt.x, self.v.pt.y, self.v.pt.z, self.v.direction))) #self.v.pt.d, 
    
    def __lt__(self, other):
        if self.pieces[-1] == 'ELEM_FLAT':
            return True
        elif other.pieces[-1] == 'ELEM_FLAT':
            return False
        else:
            return len(self.col_d) < len(other.col_d)
    
    def __eq__(self, other):
        return self.pieces[-1][0] == other.pieces[-1][0] and self.v.direction == other.v.direction and self.v.pt.x == other.v.pt.x and self.v.pt.y == other.v.pt.y and self.v.pt.z == other.v.pt.z

    def get_ordered_points(self):
        pts = {}
        for pt_to_reserve, lst in self.col_d.items():
            for s, segment, seg_name, seg_flags, v, base_z, clearance_z, quarters, k in lst:
                pts[s] = {
                    'segment': segment,
                    'seg_name': seg_name,
                    'seg_flags': seg_flags,
                    'v': v,
                    'pt': Point(pt_to_reserve[0], pt_to_reserve[1], base_z),
                }
        return pts

def get_pts_to_reserve(seg_num, cur_v, ignore_preview=False):
    blocks = TRACK_BLOCKS[seg_num]
    coords = TRACK_COORDINATES[seg_num]
    temp_z = -coords.z_begin//8 + coords.z_end//8
    
    pts_to_reserve = []
    for k, block in enumerate(blocks):
        if block == TRACK_BLOCK_END:
            break
        if ignore_preview and block.flags & RCT_PREVIEW_TRACK_FLAG_0:
            continue
        rot = Point(-block.x//32, -block.y//32).Rotate(cur_v.direction)
        rot.z = block.z//8
        map_loc = cur_v.pt + rot
        assert int(block.z/8) == block.z//8
    
        base_z = floor2(map_loc.z, 1)
        if temp_z < 0:
            base_z += temp_z

        clearance_z = block.clearanceZ + 3*8 # keep multiplied by 8 so floorZ will work with fractional values
        # ***** 4*8
        clearance_z = floor2(clearance_z, 1)//8 + base_z
            
        quarters = block.var_08.Rotate(cur_v.direction & 3)
        pts_to_reserve.append((map_loc, base_z, clearance_z, quarters, k))
    return pts_to_reserve

def get_collision_for_segment(segment, col_data, update=True, verbose=False, stop_early=False, skip_flat=False, copy=True, increase_speed=False, ignore_preview=False, limit_intensity=False):
    if copy:
        col_data = col_data.copy()
    col_data.err_msg = ""

    #verboseprint = print if verbose else lambda *a, **k: print(*a, **k) if any(isinstance(k, Iterable) and '***' in k for k in a) else ''
    verboseprint = print if verbose else lambda *a, **k: ''
    
    col_data.pieces.append(segment)    
    seg_num, seg_flags = segment
    seg_name = SEGMENTS[seg_num]
    coords = TRACK_COORDINATES[seg_num]
    track_def = TRACK_DEFINITIONS[seg_num]
    
    verboseprint("\n", col_data.s, seg_name)
    #print("Start analysis of", seg_name, col_data.s)
    
    
    ####
    ## Flat pieces (not strictly collision)
    ####
    
    col_data.num_consecutive_flat_segments += 1
    if track_def.vangle_end != TRACK_SLOPE_NONE:
        col_data.num_consecutive_flat_segments = 0
    
    if col_data.num_consecutive_flat_segments > 10 and 'STATION' not in seg_name and not skip_flat:
        col_data.collided = True
        col_data.err_msg = "*** COLLISION: More than 10 consec flat segments."
        verboseprint(col_data.err_msg)
        if stop_early:
            return col_data
    
    ####
    ## Find coordinates to reserve for this track piece
    ####
    
    v = col_data.v # alias

    pts_to_reserve = get_pts_to_reserve(seg_num, v, ignore_preview=ignore_preview)
    
    #orig_pt = Point.from_Point(v.pt)
    delta = Point(coords.x//32, coords.y//32).Rotate(v.direction^2)
    v.pt = v.pt + delta
    v.pt.z = v.pt.z - coords.z_begin//8 + coords.z_end//8
    
    v.direction &= 3
    v.direction = (v.direction + coords.rotation_end - coords.rotation_begin) & 3
    if coords.rotation_end & 4:
        v.direction |= 4
    
    #verboseprint(f"Orig: {orig_pt} and new: {v.pt}, direction: {v.direction}")

    # advance by one
    if not (v.direction & 4):
        v.pt = v.pt + Point(-CoordsDirectionDelta[v.direction].x//32, -CoordsDirectionDelta[v.direction].y//32)
    
    
    ####
    ## Try to reserve the coordinates.
    ####
    
    coords = []
    col_data.new_points = []
    for map_loc, base_z, clearance_z, quarters, k in pts_to_reserve:
        pt_to_reserve = (map_loc.x, map_loc.y) #, z)
        verboseprint(f"Piece {col_data.s} {seg_name} reserving {pt_to_reserve} from {base_z} to {clearance_z} quarters {quarters}")
        
        #for col_pt in :
        #if len(col_data.col_d[pt_to_reserve]) > 0:
        # get the potentially colliding points.
        #col_pts = col_data.col_d[pt_to_reserve]
        collided = False
        for s_, _, seg_name_, _, _, base_z_, clearance_z_, quarters_, _ in col_data.col_d[pt_to_reserve]:
            if s_ in [col_data.s, col_data.s-1]:
                continue
            if base_z < clearance_z_ and clearance_z > base_z_:
                if (quarters_.tileQuarter & quarters.tileQuarter) or "QUARTER_TURN_3_TILES" in seg_name or "QUARTER_TURN_3_TILES" in seg_name_:
                    collided = True
                    break
    
        if collided:
            data_s = tabulate([[col_data.s, segment, seg_name, seg_flags, col_data.v, base_z, clearance_z, quarters, k], *col_data.col_d[pt_to_reserve]])
            col_data.collided = True
            col_data.err_msg = f"\n\n*** COLLISION at block {k} for position {pt_to_reserve}\n{data_s}"
            verboseprint(col_data.err_msg)
            if stop_early:
                #print("Collision reserving coordinates, returning early")
                return col_data #.set_collision(copy)

        if update:
            #reserved.add(pt_to_reserve)
            copy_v = Vector(col_data.v)
            col_data.col_d[pt_to_reserve].append((col_data.s, segment, seg_name, seg_flags, copy_v, base_z, clearance_z, quarters, k))
            col_data.points[col_data.cur_p] = {
                'segment': segment,
                'seg_name': seg_name,
                'seg_flags': seg_flags,
                'v': copy_v,
                'pt': Point(pt_to_reserve[0], pt_to_reserve[1], base_z),
                'def': TRACK_DEFINITIONS[seg_num]
            }
            coords.append(col_data.points[col_data.cur_p])
            col_data.new_points.append((col_data.cur_p, col_data.points[col_data.cur_p]))
            #print("Setting", cur_p)
            col_data.cur_p += 1
    
    col_data.blocks.append(coords)
    #print(blocks_)
    #print(len(blocks_), s, seg_name)
    assert len(col_data.blocks) == col_data.s+1, f"The number of recorded block sets ({len(col_data.blocks)}) does not match the current segment number ({col_data.s+1}). Current blocks are: {[[SEGMENTS[d['segment'][0]] for d in lst] for lst in col_data.blocks]}"
        
    ####
    ## Speed + G-forces calculation
    ####
    
    #'''
    vars_copy = col_data._vars
    for car in vars_copy['cars']:
        car['next_segment'] = False
        if car['TrackLocation'] is None:
            car['TrackLocation'] = col_data.points[0]
            car['TrackDirection'] = col_data.points[0]['v'].direction
            car['TrackType'] = col_data.points[0]['segment'][0]
            car['cur_block'] = 0
            car['SegName'] = col_data.points[0]['seg_name']
            car['SegFlags'] = col_data.points[0]['seg_flags']
    
    #print("Checking speed for cur segment", seg_name, seg_flags)
    #print("Vars:", col_data.points, vars_copy, col_data.col_d, col_data.blocks)
    ct = 0
    speed = 0
    while True:
        ct += 1
        if ct > 1000:
            #print(vars_copy['cars'][0]['velocity'])
            #assert False
            col_data.collided = True
            col_data.err_msg = f"Bad speed?"
            verboseprint(col_data.err_msg)
            break
        if vars_copy['cars'][0]['velocity'] <= 0:
            vars_copy['cars'][0]['velocity'] = 50000
            vars_copy['cars'][0]['acceleration'] = 50000
        
        vars_copy = copy_vars(vars_copy)
        err = False
        try:
            if get_bad_speeds_for_segment(col_data.points, vars_copy, col_data.col_d, col_data.blocks, verbose=verbose, at_end='stop'):
                break
        except ValueError:
            #verboseprint(traceback.format_exc())
            err = True
            #col_data.err_msg = traceback.format_exc()
        
        cur_seg_num, speed = vars_copy['cars'][0]['cur_block'], vars_copy['cars'][0]['velocity'] #???
        #verboseprint("Speed:", speed, rct2speed_to_mph(verbose, speed))        
        if err or (speed <= 0 and cur_seg_num > 0 and vars_copy['status'] == STATUS_TRAVELLING):
            col_data.collided = True
            col_data.err_msg = f"*** COLLISION: Velocity too low. Err: {err}; speed: {speed}. Seg: {seg_name}; previous: {SEGMENTS[col_data.pieces[-2][0]]}"
            verboseprint(col_data.err_msg)            
            col_data.speed = -1
            col_data.speed_mph = -1
            if stop_early:
                #print("Bad speed, returning early")
                return col_data #.set_collision(copy)
        
        if vars_copy['cars'][0]['next_segment']:
            # car has surpassed current seg num.
            break
        col_data._vars = vars_copy
    
    ride_ratings_calc(col_data._vars, col_data.col_d, verbose=verbose)
        
    col_data.speed = speed
    col_data.speed_mph = rct2speed_to_mph(True, speed)
    col_data._vars['max_speed_mph'] = max(col_data._vars['max_speed_mph'], col_data.speed_mph)
    col_data._vars['speeds_mph'].append(col_data.speed_mph)
    col_data.gfV, col_data.gfL = col_data._vars['previous_vertical_g'], col_data._vars['previous_lateral_g']
    
    verboseprint("Speed:", col_data.speed, col_data.speed_mph)     
    verboseprint(f"G-forces: +{col_data.gfV/2} vertical, +{col_data.gfL/2} lateral")
    
    verboseprint(f"Excitement: {col_data._vars['excitement']}; intensity: {col_data._vars['intensity']}; nausea: {col_data._vars['nausea']}")
    verboseprint(f"Total value: {col_data._vars['value']}")
    
    if limit_intensity and col_data._vars['intensity'] > 1000:
        col_data.collided = True
        col_data.err_msg = f"*** COLLISION: Intensity too high ({col_data._vars['intensity']})"
        verboseprint(col_data.err_msg)            
        if stop_early:
            return col_data
    
    verboseprint("End analysis of", seg_name, col_data.s)
    col_data.s += 1
    col_data.max_gfL = max(col_data.max_gfL, col_data.gfL)
    return col_data

speed_cache = {}
def get_next_segment_validities(elmt_mapping, pieces, v, col_d, s, _vars, cur_speed_mph, col_data, verbose=False, max_size=None, constraint_dict=None, forbidden=[], max_flats=math.inf):
    if type(max_size) is int:
        max_size = (max_size, max_size, math.inf)
    #print("Getting next segment validities for", SEGMENTS[pieces[-1][0]])
    vars_copy = copy_vars(_vars)
    
    assert len(pieces) > 0 # starts with stations(?)
    
    for car in vars_copy['cars']:
        car['next_segment'] = False
        car['looping'] = False
        if car['TrackLocation'] is None:
            assert col_data.s > 1
            car['TrackLocation'] = col_data.points[0]
            car['TrackDirection'] = col_data.points[0]['v'].direction
            car['TrackType'] = col_data.points[0]['segment'][0]
            car['cur_block'] = 0
            car['SegName'] = col_data.points[0]['seg_name']
            car['SegFlags'] = col_data.points[0]['seg_flags']
    
    #pieces_tup = tuple(pieces)
    
    next_segment_validities = np.zeros(len(elmt_mapping)+1, dtype=int)
    for (seg_num, seg_flags), i in elmt_mapping.items():
        cur_p = col_data.cur_p
        points = dict(col_data.points)
        
        seg_name = SEGMENTS[seg_num]
        
        if (seg_num, seg_flags) in forbidden: #[pieces_tup]: #or seg_num in forbidden[1][pieces_tup]):
            if verbose: print(f"Skipping {seg_name} since it was previously tried and did not work.")
            continue
        
        if "STATION" in seg_name:
            if verbose: print(f"Skipping {seg_name} (station)")
            continue
        if seg_name == "ELEM_ON_RIDE_PHOTO" and any(SEGMENTS[segment[0]] == "ELEM_ON_RIDE_PHOTO" for segment in pieces):
            if verbose: print(f"Skipping {seg_name} (more than one already present)")
            continue
        if constraint_dict != None and len(pieces) > 0 and pieces[-1] in constraint_dict and (seg_num, seg_flags) not in constraint_dict[pieces[-1]]:
            if verbose: print(f"Skipping {seg_name} because it is not in the constraint dictionary for {SEGMENTS[pieces[-1][0]]}")
            continue
                
        track_def = TRACK_DEFINITIONS[seg_num]
        #if ending:
        #    if v.pt.z > 0 and track_def.vangle_end in [TRACK_SLOPE_UP_25, TRACK_SLOPE_UP_60, TRACK_SLOPE_UP_90]:
        #         if verbose: print("Skipping {seg_name} since we are ending and it is an up-angled piece.")
        #        continue
        #    elif v.pt.z < 0 and track_def.vangle_end in [TRACK_SLOPE_DOWN_25, TRACK_SLOPE_DOWN_60, TRACK_SLOPE_DOWN_90]:
        #        if verbose: print("Skipping {seg_name} since we are ending and it is a down-angled piece.")
        #        continue
        if track_def.vangle_end == TRACK_SLOPE_NONE and col_data.num_consecutive_flat_segments+1 >= max_flats:
            if verbose: print(f"Skipping {seg_name}: >= {max_flats} flat segments.")
            continue

        #if reached_max_length and coords.rotation_begin == coords.rotation_end and (len(pieces) < max_track_segments or track_def.vangle_end not in [TRACK_SLOPE_DOWN_25, TRACK_SLOPE_DOWN_60, TRACK_SLOPE_DOWN_90]):
        #    if verbose: print(f"Skipping {seg_name} since we have reached max length and it is a straight piece.")
        #    continue
        
        seg_name_prev = SEGMENTS[pieces[-1][0]]
        track_def_prev = TRACK_DEFINITIONS[pieces[-1][0]]
        #print(track_def_prev.vangle_end, track_def_prev.bank_end, "(", seg_name_prev, ")->", track_def.vangle_start, track_def.bank_start, "(", seg_name, ")")
        if (track_def.vangle_start, track_def.bank_start) != (track_def_prev.vangle_end, track_def_prev.bank_end):
            if verbose: print(f"Skipping {seg_name} (angle/banking does not match)")
            continue

        next_starts_diagonal = False
        if seg_name in TRACK_DESCRIPTORS:
            next_starts_diagonal = TRACK_DESCRIPTORS[seg_name].starts_diagonal
        prev_ends_diagonal = (v.direction & (1<<2)) != 0
        if prev_ends_diagonal != next_starts_diagonal:
            if verbose: print(f"Skipping {seg_name} (diagonal does not match)")
            continue
        
        if "S_BEND" in seg_name_prev or seg_name_prev == "ELEM_END_STATION":
            '''
            uint8_t startSlope = _previousTrackSlopeEnd;
            uint8_t endSlope = _currentTrackSlopeEnd;
            uint8_t startBank = _previousTrackBankEnd;
            uint8_t endBank = _currentTrackBankEnd;
            '''
            if track_def_prev.vangle_end != TRACK_SLOPE_NONE or track_def.vangle_start != TRACK_SLOPE_NONE:
                if verbose: print(f"Skipping {seg_name} (501)")
                continue
            if track_def_prev.bank_end != TRACK_BANK_NONE or track_def.bank_start != TRACK_BANK_NONE:
                if verbose: print(f"Skipping {seg_name} (504)")
                continue
        if "VERTICAL_LOOP" in seg_name_prev:
            if track_def_prev.bank_end != TRACK_BANK_NONE or track_def.bank_start != TRACK_BANK_NONE:
                if verbose: print(f"Skipping {seg_name} (508)")
                continue
            if track_def_prev.vangle_end != TRACK_SLOPE_UP_25:
                if verbose: print(f"Skipping {seg_name} (511)")
                continue
        
        # check if next block can fit.
        collided = False
        pts_to_reserve = get_pts_to_reserve(seg_num, v)
        
        def check_point_collision(seg_name, max_size, col_d, s, map_loc, base_z, clearance_z, quarters):
            if base_z < 0:
                if verbose: print(f"Skipping {seg_name} (outside of grid: z={base_z})")
                return True
            if max_size is not None:
                x, y = map_loc.x, map_loc.y
                if x < 0 or x >= max_size[0] or y < 0 or y >= max_size[1] or base_z >= max_size[2]:
                    if verbose: print(f"Skipping {seg_name} (outside of grid: {x, y, base_z})")
                    return True
            
            pt_to_reserve = (map_loc.x, map_loc.y)
            for s_, _, seg_name_, _, _, base_z_, clearance_z_, quarters_, _ in col_d[pt_to_reserve]:
                if s_ == s-1:
                    continue
                if base_z < clearance_z_ and clearance_z > base_z_:
                    if (quarters_.tileQuarter & quarters.tileQuarter) or "QUARTER_TURN_3_TILES" in seg_name or "QUARTER_TURN_3_TILES" in seg_name_:
                        if verbose: print(f"Skipping {seg_name} (obstructed by {s_} {seg_name_} between {base_z}-{clearance_z} to {base_z_}-{clearance_z_})")
                        return True
            return False
        
        coords_ = []
        for map_loc, base_z, clearance_z, quarters, _ in pts_to_reserve:
            if check_point_collision(seg_name, max_size, col_d, s, map_loc, base_z, clearance_z, quarters):
                collided = True
                break
            
            # did not collide -- add to points
            points[cur_p] = {
                'segment': (seg_num, seg_flags),
                'seg_name': seg_name,
                'seg_flags': seg_flags,
                'v': v,
                'pt': Point(map_loc.x, map_loc.y, base_z),
                'def': track_def
            }
            coords_.append(points[cur_p])
            cur_p += 1
        
        if collided:
            #print(i, 'd', seg_num, seg_flags, seg_name)
            continue
        
        # calculate final coordinate
        coords = TRACK_COORDINATES[seg_num]
        pt = v.pt + Point(coords.x//32, coords.y//32).Rotate(v.direction^2)
        d = v.direction
        d &= 3
        d = (d + coords.rotation_end - coords.rotation_begin) & 3
        if coords.rotation_end & 4:
            d |= 4
        if not (d & 4):
            pt = pt + Point(-CoordsDirectionDelta[d].x//32, -CoordsDirectionDelta[d].y//32)   
        
        if check_point_collision(seg_name, max_size, col_d, s, pt, pt.z, pts_to_reserve[-1][2], pts_to_reserve[-1][3]):
            continue
            
        #pt = v.pt + Point(32//32, 32//32).Rotate(v.direction^2)
        #d = v.direction
        #d &= 3
        #d = (d + coords.rotation_end - coords.rotation_begin) & 3
        #if coords.rotation_end & 4:
        #    d |= 4
        #if not (d & 4):
        #    pt2 = pt + Point(-CoordsDirectionDelta[d].x//32, -CoordsDirectionDelta[d].y//32)   
        
        #if check_point_collision(seg_name, max_size, col_d, s, pt2, pt2.z, pts_to_reserve[-1][2], pts_to_reserve[-1][3]):
        #    continue
        # check if final coordinate is outside of grid
        #if max_size is not None:
        #    x, y = pt.x, pt.y #-1000, pt.y-1000
        #    #print(x, y, max_size)
        #    if x < 0 or x+1 >= max_size[0] or y < 0 or y+1 >= max_size[1]:
        #        if verbose: print(f"Skipping {seg_name} (next piece would go outside of grid: {x, y})")
        #        continue
        
        
        # speed
        track_flags = TRACK_FLAGS[seg_num]
        special_track = ["ELEM_WATER_SPLASH", "ELEM_LEFT_VERTICAL_LOOP", "ELEM_RIGHT_VERTICAL_LOOP"]
        cur_piece_up = (track_flags & TRACK_ELEM_FLAG_UP or coords.z_begin < coords.z_end) and not (seg_flags & CHAIN_LIFT_FLAGS)
        last_piece_up = TRACK_FLAGS[pieces[-1][0]] & TRACK_ELEM_FLAG_UP and not (pieces[-1][1] & CHAIN_LIFT_FLAGS)
        if special_track or cur_piece_up or last_piece_up:
            if verbose: print("Checking speed for", SEGMENTS[pieces[-1][0]], " --> speed for", SEGMENTS[seg_num], seg_num, seg_flags)
            #if (((track_flags & TRACK_ELEM_FLAG_UP) or (coords.z_begin < coords.z_end) or (TRACK_FLAGS[pieces[-1][0]] & TRACK_ELEM_FLAG_UP and not (pieces[-1][1] & CHAIN_LIFT_FLAGS))) and not (seg_flags & CHAIN_LIFT_FLAGS):
            # check cache.
            #data = (pieces[-1], cur_speed_mph, (seg_num, seg_flags))
            data = (pieces[-1], _vars['cars'][0]['velocity']//1000, cur_speed_mph, (seg_num, seg_flags))
            if data not in speed_cache:
                #print("Not in cache: ", pieces[-1], cur_speed_mph, (seg_num, seg_flags))
                if verbose: print("Not in cache: ", data)
                vars_copy2 = copy_vars(vars_copy)
                
                # add a compatible piece after the one under the analysis
                # to make sure the end of the car can traverse the current piece.
                new_v = Vector(pt, d)                
                # ending angle and banking will determine next piece...
                continuation = get_next_piece_to_flat(coords, track_def)[0]
                continuing_seg_num, continuing_seg_flags = SEGMENT_NUMS[continuation[0]], continuation[1]

                #print("Adding", SEGMENTS[continuing_seg_num], continuing_seg_flags, "to end")
                pts_to_reserve = get_pts_to_reserve(continuing_seg_num, new_v)
                #assert len(pts_to_reserve) > 0
                coords_2 = []
                for map_loc, base_z, clearance_z, quarters, k in pts_to_reserve:
                    pt_to_reserve = (map_loc.x, map_loc.y)
                    # ignore collisions
                    points[cur_p] = {
                        'segment': (continuing_seg_num, continuing_seg_flags),
                        'seg_name': SEGMENTS[continuing_seg_num],
                        'seg_flags': continuing_seg_flags,
                        'v': new_v,
                        'pt': Point(pt_to_reserve[0], pt_to_reserve[1], base_z),
                        'def': TRACK_DEFINITIONS[continuing_seg_num]
                    }
                    coords_2.append(points[cur_p])
                    cur_p += 1
                
                ct = 0
                while not vars_copy2['cars'][-1]['next_segment']:
                    ct += 1
                    if ct > 2000:
                        print(f"{seg_name} taking a while...")
                    #assert ct <= 1000
                            
                    err = False
                    try:
                        if get_bad_speeds_for_segment(points, vars_copy2, col_d, col_data.blocks+[coords_]+[coords_2], verbose=False, at_end='stop', measurements=False):
                            break
                    except ValueError:
                        err = True
                    
                    # must check speed on car[0].
                    cur_seg_num, speed = vars_copy2['cars'][0]['cur_block'], vars_copy2['cars'][0]['velocity'] #???
                    #verboseprint("Speed:", speed, rct2speed_to_mph(verbose, speed))        
                    if err or (speed <= 0 and cur_seg_num > 0 and vars_copy2['status'] == STATUS_TRAVELLING):
                        #verboseprint("*** COLLISION: Velocity too low.")
                        collided = True
                        break
                #print(speed)
                speed_cache[data] = collided
            #else:
            #    print("*** already in cache:", data, speed_cache[data])
            collided = speed_cache[data]
        
        if collided:
            if verbose: print(f"Skipping {seg_name} (speed is no good)")
            continue
        
        if verbose: print(f"*** VALID: {seg_name} {seg_flags}")
        # x[i] -> 1 if action valid else 0
        next_segment_validities[i] = 1
    return next_segment_validities

clamp = lambda x, l, u: max(l, min(u, x))
clamp_int16 = lambda x: clamp(x, -32768, 32767)
clamp_int32 = lambda x: clamp(x, -2147483648, 2147483647)

VEHICLE_INFO_CACHE = {}

def get_bad_speeds_for_segment(points, vars, col_d, blocks, verbose=False, at_end='loop', measurements=True):
    # Note: Updates vars.
    #verboseprint = print if verbose else lambda *a, **k: print(*a, **k) if any(isinstance(k, Iterable) and '***' in k for k in a) else ''
    verboseprint = print if verbose else lambda *a, **k: ''
    
    
    # Notes
    #
    
    def GetAccelerationDecrease2(velocity, totalMass):
        accelerationDecrease2 = velocity >> 8;
        accelerationDecrease2 *= accelerationDecrease2;
        if velocity < 0:
            accelerationDecrease2 = -accelerationDecrease2;
        accelerationDecrease2 >>= 4;
        if totalMass != 0:
            return int(accelerationDecrease2 // totalMass)
        return accelerationDecrease2
    
    def UpdateTrackMotionForwardsGetNewTrack(car, vars):
        #TileElement* tileElement = map_get_track_element_at_of_type_seq(TrackLocation, trackType, 0);

        #int32_t curZ, direction;
        #CoordsXYE xyElement = { TrackLocation, tileElement };
        #if (!track_block_get_next(&xyElement, &xyElement, &curZ, &direction))
        #{
        #    return false;
        #}
        #tileElement = xyElement.element;
        
        #if car['seg_num']+1 >= len(points):
        #print(car['cur_block']+1, len(blocks))
        if car['cur_block']+1 >= len(blocks):
            if at_end == 'loop':
                #car['seg_num'] = 0
                car['cur_block'] = 0
                car['looping'] = True
                car['next_segment'] = True
                return False
            elif at_end == 'stop':
                #print("should stop here, reached end of segment")
                #return False
                car['next_segment'] = True
                return False
            else:
                raise Exception("bad arg for at_end:", at_end)
            
        #location = points[car['seg_num']+1] # { xyElement, curZ, static_cast<Direction>(direction) };
        #track_def2 = TRACK_DEFINITIONS[points[car['seg_num']+1]['segment'][0]]
        track_def = TRACK_DEFINITIONS[car['TrackType']]
        track_def2 = TRACK_DEFINITIONS[blocks[car['cur_block']+1][0]['segment'][0]]
        assert (track_def2.vangle_start, track_def2.bank_start) == (track_def.vangle_end, track_def.bank_end), f"angles/banks did not match: {SEGMENTS[blocks[car['cur_block']][0]['segment'][0]]}, --> {SEGMENTS[blocks[car['cur_block']+1][0]['segment'][0]]}"
                
        #curZ, direction = None, None
        #xyElement = (v.pt, tileElement)
        #if (!track_block_get_next(&xyElement, &xyElement, &curZ, &direction)):
        #    return false;

        #tileElement = xyElement.element; # NEXT element...
        #location = Point(xyElement.x, xyElement.z, curZ, direction)
        #car['seg_num'] += 1
        car['cur_block'] += 1
        car['TrackLocation'] = blocks[car['cur_block']][0] #points[car['seg_num']]
        # TrackLocation = location
        car['TrackDirection'] = blocks[car['cur_block']][0]['v'].direction #points[car['seg_num']]['v'].direction
        car['TrackType'] = blocks[car['cur_block']][0]['segment'][0] # points[car['seg_num']]['segment'][0]
        car['SegName'] = blocks[car['cur_block']][0]['seg_name'] # points[...]
        car['SegFlags'] = blocks[car['cur_block']][0]['seg_flags'] # points[...]
        
        # for surface proximity check
        if car['TrackLocation']['pt'].z < vars['min_z']:
            vars['min_z'] = car['TrackLocation']['pt'].z
                
        # loc_6DB500
        if VEHICLE_UPDATE_FLAG_ON_LIFT_HILL in car['update_flags']:
            car['update_flags'].remove(VEHICLE_UPDATE_FLAG_ON_LIFT_HILL)
        if car['SegFlags'] & CHAIN_LIFT_FLAGS:
            car['update_flags'].append(VEHICLE_UPDATE_FLAG_ON_LIFT_HILL)
            #verboseprint("Setting lift hill")
        
        if "BRAKES" in car['SegName']: # points[car['seg_num']]['seg_name']:
            car['brake_speed'] = (car['SegFlags'] & 0x0F) #* 2
            verboseprint("brakes:", car['SegFlags'], car['brake_speed'])

        return True;
    
    def UpdateTrackMotionForwards(car, vars):
        #x=False
        ct = 0
        while True:
            ct += 1
            assert ct <= 1000
            if car['SegName'] == "ELEM_BRAKES": # points[car['seg_num']]['seg_name']
                brakeSpeed = car['brake_speed'] << 16;
                verboseprint("brake speed:", brakeSpeed, "and velF64:", vars['_vehicleVelocityF64E08'])
                if brakeSpeed < vars['_vehicleVelocityF64E08']:
                    car['acceleration'] = -vars['_vehicleVelocityF64E08'] * 16;
                    verboseprint("Changing car acc (brake speed)", rct2speed_to_mph(verbose, car['acceleration']))

            newTrackProgress = car['track_progress'] + 1;
                        
            trackType = car['TrackType'] #points[car['seg_num']]['segment'][0]
            direction = car['TrackDirection'] #points[car['seg_num']]['v'].direction
            
            #trackTotalProgress = vehicle_get_move_info_size(TrackSubposition, GetTrackType(), GetTrackDirection());
            #typeAndDirection = (type << 2) | (direction & 3);
            #gTrackVehicleInfo[static_cast<uint8_t>(trackSubposition)][typeAndDirection]->size;
            
            vehicle_info_key = (trackType, direction)
            if vehicle_info_key not in VEHICLE_INFO_CACHE:
                VEHICLE_INFO_CACHE[vehicle_info_key] = TrackVehicleInfoListDefault[(trackType << 2) | (direction & 3)]
            trackTotalProgress = len(VEHICLE_INFO_CACHE[vehicle_info_key])
            #print(f"progress: {newTrackProgress} of {trackTotalProgress}")
            if newTrackProgress >= trackTotalProgress:
                #print(" "*10, "next track?")
                if at_end == 'loop' and 'looping' in car and car['looping']:
                    return
                if not UpdateTrackMotionForwardsGetNewTrack(car, vars):
                    if car['next_segment']:
                        #print("at end of this segment")
                        return
                    vars['_vehicleMotionTrackFlags'] |= VEHICLE_UPDATE_MOTION_TRACK_FLAG_5;
                    vars['_vehicleVelocityF64E0C'] -= car['remaining_distance'] + 1;
                    car['remaining_distance'] = -1;
                    print("utmfGNT was false")
                    assert False
                    return False
                newTrackProgress = 0;

            car['track_progress'] = newTrackProgress;

            #def vehicle_get_move_info(type_, direction, offset):
            #    typeAndDirection = (type_ << 2) | (direction & 3)
            #    return TrackVehicleInfoListDefault[typeAndDirection][offset];

            # loc_6DB706
            trackType = car['TrackType'] #points[car['seg_num']]['segment'][0]
            direction = car['TrackDirection'] #points[car['seg_num']]['v'].direction
            #print(SEGMENTS[blocks[car['cur_block']-1][0]['segment'][0]], "-->", SEGMENTS[blocks[car['cur_block']][0]['segment'][0]])
            
            vehicle_info_key = (trackType, direction)
            if vehicle_info_key not in VEHICLE_INFO_CACHE:
                VEHICLE_INFO_CACHE[vehicle_info_key] = TrackVehicleInfoListDefault[(trackType << 2) | (direction & 3)]
            
            moveInfo = VEHICLE_INFO_CACHE[vehicle_info_key][car['track_progress']]
            #moveInfo = vehicle_get_move_info(0, GetTrackType(), GetTrackDirection(), track_progress);
            
            nextVehiclePosition = car['TrackLocation']['pt'] + moveInfo.pt
                        
            remainingDistanceFlags = 0;
            if (nextVehiclePosition.x != vars['_vehicleCurPosition'].x):
                remainingDistanceFlags |= 1;
            if (nextVehiclePosition.y != vars['_vehicleCurPosition'].y):
                remainingDistanceFlags |= 2;
            if (nextVehiclePosition.z != vars['_vehicleCurPosition'].z):
                remainingDistanceFlags |= 4;
        
            # loc_6DB8A5
            car['remaining_distance'] -= SubpositionTranslationDistances[remainingDistanceFlags];
            vars['_vehicleCurPosition'] = nextVehiclePosition #Point.from_Point()
            #sprite_direction = moveInfo->direction;
            car['bank_rotation'] = moveInfo.bank_rotation
            car['Pitch'] = moveInfo.Pitch;
            
            moveInfovehicleSpriteType = moveInfo.Pitch;
            
            if car['remaining_distance'] < 0x368A:
                return True

            car['acceleration'] += AccelerationFromPitch[moveInfovehicleSpriteType];
            #if x:
            #    print("Adding acc from pitch UTMF:", rct2speed_to_mph(verbose, car['acceleration']))
            vars['_vehicleUnkF64E10'] += 1
    
    def Sub6DBF3E(car, vars):
        car['acceleration'] = int(car['acceleration'] // vars['_vehicleUnkF64E10'])
        #verboseprint("Car acc in sub:", rct2speed_to_mph(verbose, car['acceleration']))

        if 'STATION' in car['SegName']: # points[car['seg_num']]['seg_name']:
            vars['_vehicleMotionTrackFlags'] |= VEHICLE_UPDATE_MOTION_TRACK_FLAG_3;
            
            if vars['_vehicleStationIndex'] is None:
                vars['_vehicleStationIndex'] = car['cur_block'] #points[car['seg_num']]

            if car['SegName'] == "ELEM_END_STATION" and ((vars['_vehicleVelocityF64E08'] < 0 and car['track_progress'] <= 22) or car['track_progress'] > 17):
                # *** OR this != gCurrentVehicle
                
                vars['_vehicleMotionTrackFlags'] |= VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_AT_STATION;
        
    def UpdateTrackMotion(vars):
        def CheckAndApplyBlockSectionStopSite(vars):
            def ApplyNonStopBlockBrake(vars):
                if vars['cars'][0]['velocity'] >= 0:
                    if vars['cars'][0]['velocity'] <= BLOCK_BRAKE_BASE_SPEED:
                        vars['cars'][0]['velocity'] = BLOCK_BRAKE_BASE_SPEED # boost
                        vars['cars'][0]['acceleration'] = 0
                    else:
                        vars['cars'][0]['velocity'] -= vars['cars'][0]['velocity'] >> 4
                        vars['cars'][0]['acceleration'] = 0
            if vars['cars'][0]['SegName'] == "ELEM_BLOCK_BRAKES":
                ApplyNonStopBlockBrake(vars)
                verboseprint("Vehicle after brake", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
    
        def UpdateVelocity(vars):
            nextVelocity = vars['cars'][0]['acceleration'] + vars['cars'][0]['velocity']
            verboseprint("Next velocity: A", rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']), "+ V", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), "=", rct2speed_to_mph(verbose, nextVelocity))
            vars['cars'][0]['velocity'] = nextVelocity
            #verboseprint("Vehicle velocity in updateVel:", vars['cars'][0]['velocity'], rct2speed_to_mph(verbose, vars['cars'][0]['velocity']))
            vars['_vehicleVelocityF64E08'] = nextVelocity;
            vars['_vehicleVelocityF64E0C'] = (nextVelocity >> 10) * 42;
        
        vars['_vehicleStationIndex'] = None
        vars['_vehicleMotionTrackFlags'] = 0
        CheckAndApplyBlockSectionStopSite(vars)
        UpdateVelocity(vars)
        
        if vars['_vehicleVelocityF64E08'] < 0:
            raise ValueError
    
        for c, car in enumerate(vars['cars']):
            if True: # c == 0: # if car->Entry() == nullptr
                car['acceleration'] = AccelerationFromPitch[car['Pitch']];
                #verboseprint("Changing car acc (pitch in UTM)", rct2speed_to_mph(verbose, car['acceleration']))
                #assert type(car['acceleration']) is int
                vars['_vehicleUnkF64E10'] = 1
                car['remaining_distance'] += vars['_vehicleVelocityF64E0C'];
                
                vars['_vehicleCurPosition'] = car['pt'] # Point.from_Point
                update_dist = True
                ct = 0
                while True:
                    ct += 1
                    assert ct <= 1000
                    #print(c, car['SegName'], car['remaining_distance'])
                    assert car['remaining_distance'] >= 0 or "STATION" in car['SegName'], "going backward?"
                    if (car['remaining_distance'] < 0x368A):
                        # Location found
                        update_dist = False
                        #print("update dist false")
                        break;
                    if UpdateTrackMotionForwards(car, vars):
                        #print("UTMF true")
                        break;
                    #print("UTMF was false")
                    if car['next_segment']:
                        break

                    if (car['remaining_distance'] >= 0):
                        break;
                    car['acceleration'] = AccelerationFromPitch[car['Pitch']];
                    verboseprint("Changing car acc (pitch in UTM after forwards)", rct2speed_to_mph(verbose, car['acceleration']))                
                    vars['_vehicleUnkF64E10'] ++ 1
                if update_dist:
                    car['pt'] = vars['_vehicleCurPosition'] # Point.from_Point( # car->MoveTo(_vehicleCurPosition);
    
            if car['next_segment']:
                continue
                    
            Sub6DBF3E(car, vars)
            
            if VEHICLE_UPDATE_FLAG_ON_LIFT_HILL in car['update_flags']:
                vars['_vehicleMotionTrackFlags'] |= VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_ON_LIFT_HILL;
                #verboseprint("Car is on chain lift. Vehicle?", bool(vars['_vehicleMotionTrackFlags'] & VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_ON_LIFT_HILL))
            
            if vars['_vehicleVelocityF64E08'] < 0:
                raise ValueError
        
        totalAcceleration = 0
        totalMass = 0
        numVehicles = 0
        for car in vars['cars']:
            numVehicles += 1
            totalMass += car['mass']
            totalAcceleration += car['acceleration']
        
        newAcceleration = int(totalAcceleration // numVehicles) * 21;
        if newAcceleration < 0:
            newAcceleration += 511;
        newAcceleration >>= 9;

        curAcceleration = newAcceleration;
        curAcceleration -= int(vars['cars'][0]['velocity'] // 4096)
        curAcceleration -= GetAccelerationDecrease2(vars['cars'][0]['velocity'], totalMass);
    
        if curAcceleration <= 0 and curAcceleration >= -500:
            if vars['cars'][0]['velocity'] <= 0x8000 and vars['cars'][0]['velocity'] >= 0:
                # Vehicle is creeping forwards very slowly (less than ~2km/h), boost speed a bit.
                verboseprint("Vehicle is creeping forwards very slowly (less than ~2km/h), boost speed a bit.")
                curAcceleration += 400;
        
        if vars['cars'][0]['SegName'] == "ELEM_WATER_SPLASH":
            if vars['cars'][0]['track_progress'] >= 48 and vars['cars'][0]['track_progress'] <= 128:
                curAcceleration -= vars['cars'][0]['velocity'] >> 6
        
        vars['cars'][0]['acceleration'] = curAcceleration
        #verboseprint("Changing vehicle acc to cur", rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        #assert type(vars['cars'][0]['acceleration']) is int, vars['cars'][0]['acceleration']
        
        return vars['_vehicleMotionTrackFlags']
    
    def UpdateMovingToEndOfStation(vars):
        verboseprint("\nMoving to end of station")
        if (vars['cars'][0]['velocity'] <= 131940):
            vars['cars'][0]['acceleration'] = 3298;
            verboseprint("Changing vehicle (velocity too low at end of station)", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        if (vars['cars'][0]['velocity'] > 131940):
            vars['cars'][0]['velocity'] -= int(vars['cars'][0]['velocity'] / 16)
            vars['cars'][0]['acceleration'] = 0;
            verboseprint("Changing vehicle (velocity too high at end of station)", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        assert type(vars['cars'][0]['acceleration']) is int, vars['cars'][0]['acceleration']

        #station = None
        curFlags = UpdateTrackMotion(vars) #&station);

        if (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_1):
            vars['cars'][0]['velocity'] = 0;
            vars['cars'][0]['acceleration'] = 0;
            vars['cars'][0]['sub_state'] += 1
            verboseprint("Changing vehicle (flag1)", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        else:
            if (vars['cars'][0]['velocity'] > 98955):
                vars['cars'][0]['sub_state'] = 0;

        if not (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_AT_STATION):
            return;

        #current_station = StationIndex::FromUnderlying(station);
        vars['current_station'] = vars['cars'][0]['cur_block'] #['seg_num']
        vars['cars'][0]['velocity'] = 0;
        vars['cars'][0]['acceleration'] = 0;
        verboseprint("Changing vehicle (to 0 - departing)", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        vars['status'] = STATUS_DEPARTING
    
    def UpdateDeparting(vars):
        verboseprint("\nDeparting")
        if (vars['cars'][0]['velocity'] <= 131940):
            vars['cars'][0]['acceleration'] = 3298;
            verboseprint("Changing vehicle acc (velocity too low when departing)", rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
        curFlags = UpdateTrackMotion(vars);

        if (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_ON_LIFT_HILL):
            if vars['cars'][0]['velocity'] <= LIFT_HILL_SPEED * 31079:
                vars['cars'][0]['acceleration'] = 15539;
                verboseprint("Changing vehicle acc (lift hill at end of station)", rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))

        if (not (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_3)) or vars['_vehicleStationIndex'] != vars['current_station']:
            vars['status'] = STATUS_TRAVELLING
            if (vars['cars'][0]['velocity'] < 0):
                vars['cars'][0]['sub_state'] = 0;
            
    def UpdateTravelling(vars):
        verboseprint("\nTravelling, current car0 coord:", vars['cars'][0]['TrackLocation']['pt'], "and progress", vars['cars'][0]['track_progress'])
        if (vars['cars'][0]['sub_state'] == 2):
            vars['cars'][0]['velocity'] = 0;
            vars['cars'][0]['acceleration'] = 0;
            verboseprint("Changing vehicle (travelling substate0)", rct2speed_to_mph(verbose, vars['cars'][0]['velocity']), rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
            #? var_C0--;
            #? if (var_C0 == 0):
            vars['cars'][0]['sub_state'] = 0;

        curFlags = UpdateTrackMotion(vars);
        if vars['cars'][0]['cur_block'] >= len(blocks) and at_end == "stop":
            return

        if (curFlags & (VEHICLE_UPDATE_MOTION_TRACK_FLAG_5 | VEHICLE_UPDATE_MOTION_TRACK_FLAG_12)):
            #if (sub_state != 0):
            #    UpdateCrashSetup();
            #    return;
            sub_state = 1;
            velocity = 0;

        if (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_VEHICLE_ON_LIFT_HILL):
            if vars['cars'][0]['velocity'] <= LIFT_HILL_SPEED * 31079:
                vars['cars'][0]['acceleration'] = 15539;
                verboseprint("Vehicle on lift hill. Changing acc.", rct2speed_to_mph(verbose, vars['cars'][0]['acceleration']))
            else:
                verboseprint("Vehicle on lift hill, but velocity larger than", rct2speed_to_mph(verbose, LIFT_HILL_SPEED*31079))
        #else:
        #    verboseprint("lift hill flag not set")

        if not (curFlags & VEHICLE_UPDATE_MOTION_TRACK_FLAG_3) or vars['cars'][0]['SegName'] != 'ELEM_BEGIN_STATION':
            return;

        vars['status'] = STATUS_ARRIVING
        vars['current_station'] = vars['_vehicleStationIndex'];
        #var_C0 = 0;
        if (vars['cars'][0]['velocity'] < 0):
            vars['cars'][0]['sub_state'] = 1;
    
    def UpdateMeasurements(vars):
        #const auto& currentStation = curRide->GetStation(curRide->current_test_station);
        #if (!currentStation.Entrance.IsNull())
        #uint8_t test_segment = vars['current_test_segment'];
        #StationIndex stationIndex = StationIndex::FromUnderlying(test_segment);
        #auto& stationForTestSegment = curRide->GetStation(stationIndex);

        vars['average_speed_test_timeout'] += 1
        if (vars['average_speed_test_timeout'] >= 32):
            vars['average_speed_test_timeout'] = 0;

        absVelocity = abs(vars['cars'][0]['velocity']);
        if (absVelocity > vars['max_speed']):
            vars['max_speed'] = absVelocity;

        if (vars['average_speed_test_timeout'] == 0 and absVelocity > 0x8000):
            vars['average_speed'] = clamp_int32(vars['average_speed'] + absVelocity)
            vars['SegmentTime'] += 1
            vars['speeds'].append(absVelocity)

        distance = abs(((vars['cars'][0]['velocity'] + vars['cars'][0]['acceleration']) >> 10) * 42);
        #if (NumLaps == 0)
        vars['SegmentLength'] = clamp_int32(vars['SegmentLength'] + distance)

        def GetGForces(vars):
            Pitch, bank_rotation, velocity, track_progress = vars['cars'][0]['Pitch'], vars['cars'][0]['bank_rotation'], vars['cars'][0]['velocity'], vars['cars'][0]['track_progress']
            
            gForceVert = (0x280000 * Unk9A37E4[Pitch]) >> 32;
            #assert type(0x280000 * Unk9A37E4[Pitch]) is int
            gForceVert = (gForceVert * Unk9A39C4[bank_rotation]) >> 32;
            #assert type(gForceVert) is int
            gForceLateral = 0;
            
            lateralFactor = 0
            vertFactor = 0
            
            ttype = vars['cars'][0]['SegName'] #points[vars['cars'][0]['seg_num']]['seg_name']
            vertFactor = GFORCE_VERT.get(ttype, 0)
            lateralFactor = GFORCE_LAT.get(ttype, 0)
            
            # special checks for track progress
            if ttype in ["ELEM_S_BEND_LEFT"]:
                lateralFactor = 98 if track_progress < 48 else -98
            elif ttype in ["ELEM_S_BEND_RIGHT"]:
                lateralFactor = -98 if track_progress < 48 else 98
            elif ttype in ["ELEM_WATER_SPLASH"]:
                vertFactor = -150;
                if (track_progress >= 32):
                    vertFactor = 150;
                    if (track_progress >= 64):
                        vertFactor = 0;
                        if (track_progress >= 96):
                            vertFactor = 150;
                            if (track_progress >= 128):
                                vertFactor = -150;
            elif ttype in ["ELEM_LEFT_BANK_TO_LEFT_QUARTER_TURN_3_TILES_25_DEG_UP"]:
                vertFactor = -(track_progress // 2) + 134;
                lateralFactor = 90;
            elif ttype in ["ELEM_RIGHT_BANK_TO_RIGHT_QUARTER_TURN_3_TILES_25_DEG_UP"]:
                vertFactor = -(track_progress // 2) + 134;
                lateralFactor = -90;
            elif ttype in ["ELEM_LEFT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_LEFT_BANK"]:
                vertFactor = -(track_progress // 2) + 134;
                lateralFactor = 90;
            elif ttype in ["ELEM_RIGHT_QUARTER_TURN_3_TILES_25_DEG_DOWN_TO_RIGHT_BANK"]:
                vertFactor = -(track_progress // 2) + 134;
                lateralFactor = -90;
            elif ttype in ["ELEM_LEFT_VERTICAL_LOOP", "ELEM_RIGHT_VERTICAL_LOOP"]:
                vertFactor = (abs(track_progress - 155) // 2) + 28
            elif ttype in ["ELEM_HALF_LOOP_UP", "ELEM_HALF_LOOP_DOWN"]:
                assert False
            
            if (vertFactor != 0):
                gForceVert += abs(velocity) * 98 // vertFactor;

            if (lateralFactor != 0):
                gForceLateral += abs(velocity) * 98 // lateralFactor;

            gForceVert *= 10;
            gForceLateral *= 10;
            gForceVert >>= 16;
            gForceLateral >>= 16;
            
            gForceVert = np.array(gForceVert & 0xFFFF).astype(np.int16) #np.int16(gForceVert & 0xFFFF)
            gForceLateral = np.array(gForceLateral & 0xFFFF).astype(np.int16) #np.int16(gForceLateral & 0xFFFF)

            return {'VerticalG': gForceVert.item(), 'LateralG': gForceLateral.item()}
                
        gForces = GetGForces(vars);
        gForces['VerticalG'] += vars['previous_vertical_g'];
        gForces['LateralG'] += vars['previous_lateral_g'];
        gForces['VerticalG'] //= 2;
        gForces['LateralG'] //= 2;

        vars['previous_vertical_g'] = gForces['VerticalG'];
        vars['previous_lateral_g'] = gForces['LateralG'];
        if (gForces['VerticalG'] <= 0):
            vars['total_air_time'] += 1

        if (gForces['VerticalG'] > vars['max_positive_vertical_g']):
            vars['max_positive_vertical_g'] = gForces['VerticalG'];

        if (gForces['VerticalG'] < vars['max_negative_vertical_g']):
            vars['max_negative_vertical_g'] = gForces['VerticalG'];

        m16 = lambda x: x & 0xFFFF
        
        gForces['LateralG'] = abs(gForces['LateralG']);
        vars['max_lateral_g'] = max(vars['max_lateral_g'], gForces['LateralG']) #***# #m16(gForces['LateralG']))

        # If we have already evaluated this track piece skip to next section
        if (vars['cars'][0]['TrackLocation']['pt'] != vars['CurTestTrackLocation']):
            vars['CurTestTrackLocation'] = vars['cars'][0]['TrackLocation']['pt'] #Point.from_Point(

            if VEHICLE_UPDATE_FLAG_ON_LIFT_HILL in vars['cars'][0]['update_flags']:
                vars['testing_flags'] |= RIDE_TESTING_POWERED_LIFT;
                if (vars['drops'] + 64 < 0xFF):
                    vars['drops'] += 64;
            else:
                vars['testing_flags'] &= ~RIDE_TESTING_POWERED_LIFT;
            
            if vars['cars'][0]['SegName'] == "ELEM_WATER_SPLASH":
                if vars['cars'][0]['velocity'] >= 0xB0000:
                    vars['special_track_elements'] |= RIDE_ELEMENT_TUNNEL_SPLASH_OR_RAPIDS;

            trackFlags = TRACK_FLAGS[vars['cars'][0]['TrackType']]

            testingFlags = vars['testing_flags'];
            if (testingFlags & RIDE_TESTING_TURN_LEFT and trackFlags & TRACK_ELEM_FLAG_TURN_LEFT):
                # 0x800 as this is masked to CURRENT_TURN_COUNT_MASK
                vars['turn_count_default'] += 0x800;
            elif (testingFlags & RIDE_TESTING_TURN_RIGHT and trackFlags & TRACK_ELEM_FLAG_TURN_RIGHT):
                # 0x800 as this is masked to CURRENT_TURN_COUNT_MASK
                vars['turn_count_default'] += 0x800;
            elif (testingFlags & RIDE_TESTING_TURN_RIGHT or testingFlags & RIDE_TESTING_TURN_LEFT):
                vars['testing_flags'] &= ~(
                    RIDE_TESTING_TURN_LEFT | RIDE_TESTING_TURN_RIGHT | RIDE_TESTING_TURN_BANKED | RIDE_TESTING_TURN_SLOPED);

                def increment_turn_count_1_element(vars, ttype):
                    if ttype == 0:
                        i = 'turn_count_default' 
                    elif ttype == 1:
                        i = 'turn_count_banked' 
                    elif ttype == 2:
                        i = 'turn_count_sloped'
                    else:
                        return
                    
                    value = (vars[i] & TURN_MASK_1_ELEMENT) + 1;
                    vars[i] &= ~TURN_MASK_1_ELEMENT;

                    if (value > TURN_MASK_1_ELEMENT):
                        value = TURN_MASK_1_ELEMENT;
                    vars[i] |= value;
                    
                def increment_turn_count_2_elements(vars, ttype):
                    if ttype == 0:
                        i = 'turn_count_default' 
                    elif ttype == 1:
                        i = 'turn_count_banked' 
                    elif ttype == 2:
                        i = 'turn_count_sloped'
                    else:
                        return
                    
                    value = (vars[i] & TURN_MASK_2_ELEMENTS) + 0x20;
                    vars[i] &= ~TURN_MASK_2_ELEMENTS;

                    if (value > TURN_MASK_2_ELEMENTS):
                        value = TURN_MASK_2_ELEMENTS;
                    vars[i] |= value;

                def increment_turn_count_3_elements(vars, ttype):
                    if ttype == 0:
                        i = 'turn_count_default' 
                    elif ttype == 1:
                        i = 'turn_count_banked' 
                    elif ttype == 2:
                        i = 'turn_count_sloped'
                    else:
                        return
                    
                    value = (vars[i] & TURN_MASK_3_ELEMENTS) + 0x100;
                    vars[i] &= ~TURN_MASK_3_ELEMENTS;

                    if (value > TURN_MASK_3_ELEMENTS):
                        value = TURN_MASK_3_ELEMENTS;
                    vars[i] |= value;

                def increment_turn_count_4_plus_elements(vars, ttype):
                    if ttype in [0, 1]:
                        increment_turn_count_3_elements(vars, ttype)
                        return
                    elif ttype == 2:
                        i = 'turn_count_sloped'
                    else:
                        return
                    
                    value = (vars[i] & TURN_MASK_4_PLUS_ELEMENTS) + 0x800;
                    vars[i] &= ~TURN_MASK_4_PLUS_ELEMENTS;

                    if (value > TURN_MASK_4_PLUS_ELEMENTS):
                        value = TURN_MASK_4_PLUS_ELEMENTS;
                    vars[i] |= value;

                turnType = 1;
                if (not (testingFlags & RIDE_TESTING_TURN_BANKED)):
                    turnType = 2;
                    if (not (testingFlags & RIDE_TESTING_TURN_SLOPED)):
                        turnType = 0;

                x = vars['turn_count_default'] >> 11
                if x == 0:
                    increment_turn_count_1_element(vars, turnType);
                elif x == 1:
                    increment_turn_count_2_elements(vars, turnType);
                elif x == 2:
                    increment_turn_count_3_elements(vars, turnType);
                else:
                    increment_turn_count_4_plus_elements(vars, turnType);
            else:
                if (trackFlags & TRACK_ELEM_FLAG_TURN_LEFT):
                    vars['testing_flags'] |= RIDE_TESTING_TURN_LEFT;
                    vars['turn_count_default'] &= ~CURRENT_TURN_COUNT_MASK;

                    if (trackFlags & TRACK_ELEM_FLAG_TURN_BANKED):
                        vars['testing_flags'] |= RIDE_TESTING_TURN_BANKED;
                    if (trackFlags & TRACK_ELEM_FLAG_TURN_SLOPED):
                        vars['testing_flags'] |= RIDE_TESTING_TURN_SLOPED;

                if (trackFlags & TRACK_ELEM_FLAG_TURN_RIGHT):
                    vars['testing_flags'] |= RIDE_TESTING_TURN_RIGHT;
                    vars['turn_count_default'] &= ~CURRENT_TURN_COUNT_MASK;

                    if (trackFlags & TRACK_ELEM_FLAG_TURN_BANKED):
                        vars['testing_flags'] |= RIDE_TESTING_TURN_BANKED;
                    if (trackFlags & TRACK_ELEM_FLAG_TURN_SLOPED):
                        vars['testing_flags'] |= RIDE_TESTING_TURN_SLOPED;

            if (testingFlags & RIDE_TESTING_DROP_DOWN):
                if (vars['cars'][0]['velocity'] < 0 or not (trackFlags & TRACK_ELEM_FLAG_DOWN)):
                    vars['testing_flags'] &= ~RIDE_TESTING_DROP_DOWN;

                    curZ = vars['_vehicleCurPosition'].z - vars['start_drop_height']; # COORDS_Z_STEP
                    if (curZ < 0):
                        curZ = abs(curZ);
                        if (curZ > vars['highest_drop_height']):
                            vars['highest_drop_height'] = min(curZ, 255) #static_cast<uint8_t>(curZ);
            
            elif (trackFlags & TRACK_ELEM_FLAG_DOWN and vars['cars'][0]['velocity'] >= 0):
                vars['testing_flags'] &= ~RIDE_TESTING_DROP_UP;
                vars['testing_flags'] |= RIDE_TESTING_DROP_DOWN;

                drops = vars['drops'] & 0x3F;
                if (drops != 0x3F):
                    drops += 1
                vars['drops'] &= ~0x3F;
                vars['drops'] |= drops;

                vars['start_drop_height'] = vars['_vehicleCurPosition'].z # COORDS_Z_STEP
                testingFlags &= ~RIDE_TESTING_DROP_UP;

            if (testingFlags & RIDE_TESTING_DROP_UP):
                if (vars['cars'][0]['velocity'] > 0 or not (trackFlags & TRACK_ELEM_FLAG_UP)):
                    vars['testing_flags'] &= ~RIDE_TESTING_DROP_UP;

                    curZ = vars['_vehicleCurPosition'].z - vars['start_drop_height']; # COORDS_Z_STEP
                    if (curZ < 0):
                        curZ = abs(curZ);
                        if (curZ > vars['highest_drop_height']):
                            vars['highest_drop_height'] = min(curZ, 255) #static_cast<uint8_t>(curZ);
            elif (trackFlags & TRACK_ELEM_FLAG_UP and vars['cars'][0]['velocity'] <= 0):
                vars['testing_flags'] &= ~RIDE_TESTING_DROP_DOWN;
                vars['testing_flags'] |= RIDE_TESTING_DROP_UP;

                drops = vars['drops'] & 0x3F;
                if (drops != 0x3F):
                    drops += 1
                vars['drops'] &= ~0x3F;
                vars['drops'] |= drops;

                vars['start_drop_height'] = vars['_vehicleCurPosition'].z # COORDS_Z_STEP

            if (trackFlags & TRACK_ELEM_FLAG_NORMAL_TO_INVERSION):
                if (vars['inversions'] < 31): #OpenRCT2::Limits::MaxInversions)
                    #print(vars['CurTestTrackLocation'])
                    #input("inc inv by 1")
                    vars['inversions'] += 1

            if (trackFlags & TRACK_ELEM_FLAG_HELIX):
                helixes = vars['special_track_elements'] & 0x1F
                if (helixes != 31): #OpenRCT2::Limits::MaxHelices)
                    helixes += 1

                vars['special_track_elements'] &= ~0x1F;
                vars['special_track_elements'] |= helixes;

        # scenery check  (if (sceneryEntry->HasFlag(SMALL_SCENERY_FLAG_FULL_TILE)) above current track)
        # (removed)
        
    def Update(vars):
        if measurements:
            UpdateMeasurements(vars)
        
        status = vars['status']
        if status == STATUS_MOVINGTOENDOFSTATION:
            UpdateMovingToEndOfStation(vars);
        #if status == Vehicle::Status::WaitingForPassengers:
        #    UpdateWaitingForPassengers();
        #if status == Vehicle::Status::WaitingToDepart:
        #    UpdateWaitingToDepart();
        elif status == STATUS_DEPARTING:
            UpdateDeparting(vars);
        elif status == STATUS_TRAVELLING:
            UpdateTravelling(vars);
        elif status == STATUS_ARRIVING:
            verboseprint("ARRIVED AT STATION")
            return True
        #if status == Vehicle::Status::UnloadingPassengers:
        #    UpdateUnloadingPassengers();
        return False
    
    return Update(vars)

def get_bad_speeds(final_col_d, stop_early=True):
    points = final_col_d.get_ordered_points()
    print("pts:", len(points))
    vars = final_col_d._vars
    speeds = []
    bad_speeds = []
    cur_speed_s = -1
    while True:
        err = False
        try:
            vars, done = get_bad_speeds_for_segment(points, vars, final_col_d.col_d, stop_early=stop_early, verbose=True, at_end='loop')
            if done:
                break
        except ValueError:
            print("excep", traceback.format_exc())
            err = True
        s, speed = vars['cars'][0]['cur_block'], vars['cars'][0]['velocity'] #????
        
        if s > cur_speed_s:
            cur_speed_s = s
            speeds.append(rct2speed_to_mph(speed))
        
        if err or (speed <= 0 and s > 0 and vars['status'] == STATUS_TRAVELLING):
            bad_speeds.append(s)
            if stop_early:
                break

        data = points[s]
        print(" "*50, s, data['seg_name'], speed, rct2speed_to_mph(verbose, speed), vars['previous_lateral_g'], vars['previous_vertical_g'])
    
    return speeds, bad_speeds
    
def proximity_score_increment(vars, type_):
    vars['ProximityScores'][type_] += 1

class Ratings:
    def __init__(self, e=0, i=0, n=0):
        self.excitement = e
        self.intensity = i
        self.nausea = n
    def __add__(self, x):
        if type(x) is tuple:
            assert len(x) == 3
            self.excitement += x[0]
            self.intensity += x[1]
            self.nausea += x[2]
        elif type(x) is Ratings:
            self.excitement += x.excitement
            self.intensity += x.intensity
            self.nausea += x.nausea
        else:
            raise Exception
    def __str__(self):
        return f"{self.excitement} {self.intensity} {self.nausea}"

FIXED_XDP = lambda x, whole, fraction: ((whole) * (10 * (x)) + (fraction))
FIXED_2DP = lambda whole, fraction: FIXED_XDP(10, whole, fraction)
RIDE_RATING = lambda whole, fraction: FIXED_2DP(whole, fraction)

def ride_ratings_add(ratings, e, i, n):
    return ratings + (e, i, n)

def ride_ratings_calculate_wooden_roller_coaster(vars, verbose=False): #(RideRatingUpdateState& state)
    def ride_ratings_apply_length(ratings, maxLength, excitementMultiplier):
        ride_ratings_add(ratings, (min(vars['SegmentLength'] >> 16, maxLength) * excitementMultiplier) >> 16, 0, 0);
    def ride_ratings_apply_train_length(ratings, excitementMultiplier):
        ride_ratings_add(ratings, ((vars['num_cars_per_train'] - 1) * excitementMultiplier) >> 16, 0, 0);
    def ride_ratings_apply_max_speed(ratings, excitementMultiplier, intensityMultiplier, nauseaMultiplier):
        modifier = vars['max_speed'] >> 16;
        ride_ratings_add(ratings, (modifier * excitementMultiplier) >> 16, (modifier * intensityMultiplier) >> 16, (modifier * nauseaMultiplier) >> 16);
    def ride_ratings_apply_average_speed(ratings, excitementMultiplier, intensityMultiplier):
        average_speed = sum(vars['speeds']) // vars['SegmentTime'] if vars['SegmentTime'] > 0 else 0
        vars['average_speed'] = average_speed
        modifier = average_speed >> 16;
        ride_ratings_add(ratings, (modifier * excitementMultiplier) >> 16, (modifier * intensityMultiplier) >> 16, 0);
    def ride_ratings_apply_duration(ratings, maxDuration, excitementMultiplier):
        ride_ratings_add(ratings, (min(vars['SegmentTime'], maxDuration) * excitementMultiplier) >> 16, 0, 0);
    def ride_ratings_apply_gforces(ratings, excitementMultiplier, intensityMultiplier, nauseaMultiplier):
        def ride_ratings_get_gforce_ratings(vars):
            result = Ratings(0, 0, 0)

            # Apply maximum positive G force factor
            result.excitement += (vars['max_positive_vertical_g'] * 5242) >> 16;
            result.intensity += (vars['max_positive_vertical_g'] * 52428) >> 16;
            result.nausea += (vars['max_positive_vertical_g'] * 17039) >> 16;

            # Apply maximum negative G force factor
            gforce = clamp_int16(vars['max_negative_vertical_g'])
            result.excitement += (clamp_int16(clamp(gforce, -FIXED_2DP(2, 50), FIXED_2DP(0, 00))) * -15728) >> 16; # *** clamp to int16?
            result.intensity += ((gforce - FIXED_2DP(1, 00)) * -52428) >> 16;
            result.nausea += ((gforce - FIXED_2DP(1, 00)) * -14563) >> 16;

            # Apply lateral G force factor
            result.excitement += (clamp_int16(min(FIXED_2DP(1, 50), vars['max_lateral_g'])) * 26214) >> 16;
            result.intensity += vars['max_lateral_g'];
            result.nausea += (vars['max_lateral_g'] * 21845) >> 16;

            return result;

        subRating = ride_ratings_get_gforce_ratings(vars);
        ride_ratings_add(
            ratings, (subRating.excitement * excitementMultiplier) >> 16, (subRating.intensity * intensityMultiplier) >> 16,
            (subRating.nausea * nauseaMultiplier) >> 16);
    def ride_ratings_apply_turns(ratings, excitementMultiplier, intensityMultiplier, nauseaMultiplier):
        def ride_ratings_get_turns_ratings(vars):
            def get_turn_count_1_element(ttype):
                if ttype == 0:
                    i = 'turn_count_default' 
                elif ttype == 1:
                    i = 'turn_count_banked' 
                elif ttype == 2:
                    i = 'turn_count_sloped'
                else:
                    return 0
                return vars[i] & TURN_MASK_1_ELEMENT;

            def get_turn_count_2_elements(ttype):
                if ttype == 0:
                    i = 'turn_count_default' 
                elif ttype == 1:
                    i = 'turn_count_banked' 
                elif ttype == 2:
                    i = 'turn_count_sloped'
                else:
                    return 0
                return (vars[i] & TURN_MASK_2_ELEMENTS) >> 5

            def get_turn_count_3_elements(ttype):
                if ttype == 0:
                    i = 'turn_count_default' 
                elif ttype == 1:
                    i = 'turn_count_banked' 
                elif ttype == 2:
                    i = 'turn_count_sloped'
                else:
                    return 0
                return (vars[i] & TURN_MASK_3_ELEMENTS) >> 8
            
            def get_turn_count_4_plus_elements(ttype):
                if ttype in [0, 1]:
                    return 0
                elif ttype == 2:
                    i = 'turn_count_sloped'
                else:
                    return 0
                return (vars[i] & TURN_MASK_4_PLUS_ELEMENTS) >> 11
            
            def get_special_track_elements_rating(vars):
                excitement, intensity, nausea = 0, 0, 0

                if vars['special_track_elements'] & RIDE_ELEMENT_TUNNEL_SPLASH_OR_RAPIDS:
                    excitement += 50;
                    intensity += 30;
                    nausea += 20;

                helixSections = vars['special_track_elements'] & 0x1F;

                helixesUpTo9 = min(helixSections, 9);
                excitement += (helixesUpTo9 * 254862) >> 16;

                helixesUpTo11 = min(helixSections, 11);
                intensity += (helixesUpTo11 * 148945) >> 16;

                helixesOver5UpTo10 = clamp(helixSections - 5, 0, 10);
                nausea += (helixesOver5UpTo10 * 0x140000) >> 16;

                return Ratings(clamp_int16(excitement), clamp_int16(intensity), clamp_int16(nausea));
            
            def get_flat_turns_rating():
                num3PlusTurns = get_turn_count_3_elements(0);
                num2Turns = get_turn_count_2_elements(0);
                num1Turns = get_turn_count_1_element(0);

                rating = Ratings()
                rating.excitement = (num3PlusTurns * 0x28000) >> 16;
                rating.excitement += (num2Turns * 0x30000) >> 16;
                rating.excitement += (num1Turns * 63421) >> 16;

                rating.intensity = (num3PlusTurns * 81920) >> 16;
                rating.intensity += (num2Turns * 49152) >> 16;
                rating.intensity += (num1Turns * 21140) >> 16;

                rating.nausea = (num3PlusTurns * 0x50000) >> 16;
                rating.nausea += (num2Turns * 0x32000) >> 16;
                rating.nausea += (num1Turns * 42281) >> 16;

                return rating;
            
            def get_banked_turns_rating():
                num3PlusTurns = get_turn_count_3_elements(1);
                num2Turns = get_turn_count_2_elements(1);
                num1Turns = get_turn_count_1_element(1);

                rating = Ratings()
                rating.excitement = (num3PlusTurns * 0x3C000) >> 16;
                rating.excitement += (num2Turns * 0x3C000) >> 16;
                rating.excitement += (num1Turns * 73992) >> 16;

                rating.intensity = (num3PlusTurns * 0x14000) >> 16;
                rating.intensity += (num2Turns * 49152) >> 16;
                rating.intensity += (num1Turns * 21140) >> 16;

                rating.nausea = (num3PlusTurns * 0x50000) >> 16;
                rating.nausea += (num2Turns * 0x32000) >> 16;
                rating.nausea += (num1Turns * 48623) >> 16;

                return rating;
            
            def get_sloped_turns_rating():
                rating = Ratings()

                num4PlusTurns = get_turn_count_4_plus_elements(2);
                num3Turns = get_turn_count_3_elements(2);
                num2Turns = get_turn_count_2_elements(2);
                num1Turns = get_turn_count_1_element(2);

                rating.excitement = (min(num4PlusTurns, 4) * 0x78000) >> 16;
                rating.excitement += (min(num3Turns, 6) * 273066) >> 16;
                rating.excitement += (min(num2Turns, 6) * 0x3AAAA) >> 16;
                rating.excitement += (min(num1Turns, 7) * 187245) >> 16;
                rating.intensity = 0;
                rating.nausea = (min(num4PlusTurns, 8) * 0x78000) >> 16;

                return rating;
            
            def get_inversions_ratings(inversions):
                rating = Ratings()

                rating.excitement = (min(inversions, 6) * 0x1AAAAA) >> 16;
                rating.intensity = (inversions * 0x320000) >> 16;
                rating.nausea = (inversions * 0x15AAAA) >> 16;

                return rating;
            
            excitement, intensity, nausea = 0, 0, 0

            specialTrackElementsRating = get_special_track_elements_rating(vars);
            excitement += specialTrackElementsRating.excitement;
            intensity += specialTrackElementsRating.intensity;
            nausea += specialTrackElementsRating.nausea;

            flatTurnsRating = get_flat_turns_rating();
            excitement += flatTurnsRating.excitement;
            intensity += flatTurnsRating.intensity;
            nausea += flatTurnsRating.nausea;
            vars['flat_turns'] = get_turn_count_3_elements(0) + get_turn_count_2_elements(0) + get_turn_count_1_element(0)

            bankedTurnsRating = get_banked_turns_rating();
            excitement += bankedTurnsRating.excitement;
            intensity += bankedTurnsRating.intensity;
            nausea += bankedTurnsRating.nausea;
            vars['banked_turns'] = get_turn_count_3_elements(1) + get_turn_count_2_elements(1) + get_turn_count_1_element(1)

            slopedTurnsRating = get_sloped_turns_rating();
            excitement += slopedTurnsRating.excitement;
            intensity += slopedTurnsRating.intensity;
            nausea += slopedTurnsRating.nausea;
            vars['sloped_turns'] = get_turn_count_4_plus_elements(2) + get_turn_count_3_elements(2) + get_turn_count_2_elements(2) + get_turn_count_1_element(2)

            inversionsRating = get_inversions_ratings(vars['inversions']);
            excitement += inversionsRating.excitement;
            intensity += inversionsRating.intensity;
            nausea += inversionsRating.nausea;

            return Ratings(clamp_int16(excitement), clamp_int16(intensity), clamp_int16(nausea));
        
        subRating = ride_ratings_get_turns_ratings(vars);
        ride_ratings_add(
            ratings, (subRating.excitement * excitementMultiplier) >> 16, (subRating.intensity * intensityMultiplier) >> 16,
            (subRating.nausea * nauseaMultiplier) >> 16);
    def ride_ratings_apply_drops(ratings, excitementMultiplier, intensityMultiplier, nauseaMultiplier):
        def ride_ratings_get_drop_ratings(vars):
            result = Ratings()

            # Apply number of drops factor
            drops = vars['drops'] & 0x3F;
            result.excitement += (min(9, drops) * 728177) >> 16;
            result.intensity += (drops * 928426) >> 16;
            result.nausea += (drops * 655360) >> 16;

            # Apply highest drop factor
            ride_ratings_add(
                result, ((vars['highest_drop_height'] * 2) * 16000) >> 16, ((vars['highest_drop_height'] * 2) * 32000) >> 16,
                ((vars['highest_drop_height'] * 2) * 10240) >> 16);

            return result;
        
        subRating = ride_ratings_get_drop_ratings(vars);
        ride_ratings_add(
            ratings, (subRating.excitement * excitementMultiplier) >> 16, (subRating.intensity * intensityMultiplier) >> 16,
            (subRating.nausea * nauseaMultiplier) >> 16);
    def ride_ratings_apply_highest_drop_height_penalty(ratings, minHighestDropHeight, excitementPenalty, intensityPenalty, nauseaPenalty):
        if vars['highest_drop_height'] < minHighestDropHeight:
            ratings.excitement //= excitementPenalty;
            ratings.intensity //= intensityPenalty;
            ratings.nausea //= nauseaPenalty;
    def ride_ratings_apply_max_speed_penalty(ratings, minMaxSpeed, excitementPenalty, intensityPenalty, nauseaPenalty):
        if vars['max_speed'] < minMaxSpeed:
            ratings.excitement //= excitementPenalty;
            ratings.intensity //= intensityPenalty;
            ratings.nausea //= nauseaPenalty;
    def ride_ratings_apply_max_negative_g_penalty(ratings, maxMaxNegativeVerticalG, excitementPenalty, intensityPenalty, nauseaPenalty):
        if vars['max_negative_vertical_g'] >= maxMaxNegativeVerticalG:
            ratings.excitement //= excitementPenalty;
            ratings.intensity //= intensityPenalty;
            ratings.nausea //= nauseaPenalty;
    def ride_ratings_apply_first_length_penalty(ratings, minFirstLength, excitementPenalty, intensityPenalty, nauseaPenalty):
        if vars['SegmentLength'] < minFirstLength:
            ratings.excitement //= excitementPenalty;
            ratings.intensity //= intensityPenalty;
            ratings.nausea //= nauseaPenalty;
    def ride_ratings_apply_num_drops_penalty(ratings, minNumDrops, excitementPenalty, intensityPenalty, nauseaPenalty):
        if ((vars['drops'] & 0x3F) < minNumDrops):
            ratings.excitement //= excitementPenalty;
            ratings.intensity //= intensityPenalty;
            ratings.nausea //= nauseaPenalty;
    def ride_ratings_apply_excessive_lateral_g_penalty(ratings, excitementMultiplier, intensityMultiplier, nauseaMultiplier):
        def ride_ratings_get_excessive_lateral_g_penalty():
            result = Ratings()
            if (vars['max_lateral_g'] > FIXED_2DP(2, 80)):
                result.intensity = FIXED_2DP(3, 75);
                result.nausea = FIXED_2DP(2, 00);

            if (vars['max_lateral_g'] > FIXED_2DP(3, 10)):
                # Remove half of the ride_ratings_get_gforce_ratings
                result.excitement = (vars['max_positive_vertical_g'] * 5242) >> 16;

                # Apply maximum negative G force factor
                gforce = clamp_int16(vars['max_negative_vertical_g'])
                result.excitement += (clamp_int16(clamp(gforce, -FIXED_2DP(2, 50), FIXED_2DP(0, 00))) * -15728) >> 16;

                # Apply lateral G force factor
                result.excitement += (clamp_int16(min(FIXED_2DP(1, 50), vars['max_lateral_g'])) * 26214) >> 16;

                # Remove half of the ride_ratings_get_gforce_ratings
                result.excitement //= 2;
                result.excitement *= -1;
                result.intensity = FIXED_2DP(12, 25);
                result.nausea = FIXED_2DP(6, 00);
            return result;
        subRating = ride_ratings_get_excessive_lateral_g_penalty();
        ride_ratings_add(
            ratings, (subRating.excitement * excitementMultiplier) >> 16, (subRating.intensity * intensityMultiplier) >> 16,
            (subRating.nausea * nauseaMultiplier) >> 16);
    def ride_ratings_apply_intensity_penalty(ratings):
        intensityBounds = [ 1000, 1100, 1200, 1320, 1450 ];
        excitement = ratings.excitement;
        for intensityBound in intensityBounds:
            if (ratings.intensity >= intensityBound):
                excitement -= excitement // 4;
        ratings.excitement = excitement;
    def ride_ratings_apply_adjustments(ratings):
        # Apply ride entry multipliers
        # 52, 33, 8
        #ride_ratings_add(
        #    ratings, ((ratings.excitement) * 52) >> 7,
        #    ((ratings.intensity) * 33) >> 7,
        #    ((ratings.nausea) * 8) >> 7);

        # Apply total air time
        excitementModifier = vars['total_air_time'] // 8;
        nauseaModifier = vars['total_air_time'] // 16;

        ride_ratings_add(ratings, excitementModifier, 0, nauseaModifier);

    def ride_ratings_apply_proximity(vars, ratings, excitementMultiplier):
        def ride_ratings_get_proximity_score(vars):
            def get_proximity_score_helper_1(x, max_, multiplier):
                return (min(x, max_) * multiplier) >> 16;
            def get_proximity_score_helper_2(x, additionIfNotZero, max_, multiplier):
                result = x;
                if (result != 0):
                    result += additionIfNotZero;
                return (min(result, max_) * multiplier) >> 16;
            def get_proximity_score_helper_3(x, resultIfNotZero):
                return 0 if x == 0 else resultIfNotZero;
            
            scores = vars['ProximityScores']
            vars['prox_scores'] = sum(scores)

            result = 0;
            #result += get_proximity_score_helper_1(scores[PROXIMITY_WATER_OVER], 60, 0x00AAAA);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_WATER_TOUCH], 22, 0x0245D1);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_WATER_LOW], 10, 0x020000);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_WATER_HIGH], 40, 0x00A000);
            result += get_proximity_score_helper_1(scores[PROXIMITY_SURFACE_TOUCH], 70, 0x01B6DB);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_QUEUE_PATH_OVER] + 8, 12, 0x064000);
            #result += get_proximity_score_helper_3(scores[PROXIMITY_QUEUE_PATH_TOUCH_ABOVE], 40);
            #result += get_proximity_score_helper_3(scores[PROXIMITY_QUEUE_PATH_TOUCH_UNDER], 45);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_PATH_TOUCH_ABOVE], 10, 20, 0x03C000);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_PATH_TOUCH_UNDER], 10, 20, 0x044000);
            result += get_proximity_score_helper_2(scores[PROXIMITY_OWN_TRACK_TOUCH_ABOVE], 10, 15, 0x035555);
            result += get_proximity_score_helper_1(scores[PROXIMITY_OWN_TRACK_CLOSE_ABOVE], 5, 0x060000);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_FOREIGN_TRACK_ABOVE_OR_BELOW], 10, 15, 0x02AAAA);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_FOREIGN_TRACK_TOUCH_ABOVE], 10, 15, 0x04AAAA);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_FOREIGN_TRACK_CLOSE_ABOVE], 5, 0x090000);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_SCENERY_SIDE_BELOW], 35, 0x016DB6);
            #result += get_proximity_score_helper_1(scores[PROXIMITY_SCENERY_SIDE_ABOVE], 35, 0x00DB6D);
            result += get_proximity_score_helper_3(scores[PROXIMITY_OWN_STATION_TOUCH_ABOVE], 55);
            result += get_proximity_score_helper_3(scores[PROXIMITY_OWN_STATION_CLOSE_ABOVE], 25);
            result += get_proximity_score_helper_2(scores[PROXIMITY_TRACK_THROUGH_VERTICAL_LOOP], 4, 6, 0x140000);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_PATH_TROUGH_VERTICAL_LOOP], 4, 6, 0x0F0000);
            result += get_proximity_score_helper_3(scores[PROXIMITY_INTERSECTING_VERTICAL_LOOP], 100);
            result += get_proximity_score_helper_2(scores[PROXIMITY_THROUGH_VERTICAL_LOOP], 4, 6, 0x0A0000);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_PATH_SIDE_CLOSE], 10, 20, 0x01C000);
            #result += get_proximity_score_helper_2(scores[PROXIMITY_FOREIGN_TRACK_SIDE_CLOSE], 10, 20, 0x024000);
            ###result += get_proximity_score_helper_2(scores[PROXIMITY_SURFACE_SIDE_CLOSE], 10, 20, 0x028000);
            return result;
        ride_ratings_add(ratings, (ride_ratings_get_proximity_score(vars) * excitementMultiplier) >> 16, 0, 0);

    x = 1
    
    ratings = Ratings(RIDE_RATING(3, 20), RIDE_RATING(2, 60), RIDE_RATING(2, 00))
    if verbose: print(x, ratings); x+= 1
    
    ride_ratings_apply_length(ratings, 6000, 873);
    if verbose: print(x, ratings); x+= 1
    #ride_ratings_apply_synchronisation(ratings, RIDE_RATING(0, 40), RIDE_RATING(0, 05));
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_train_length(ratings, 187245);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_max_speed(ratings, 44281, 88562, 35424);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_average_speed(ratings, 364088, 655360);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_duration(ratings, 150, 26214);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_gforces(ratings, 40960, 34555, 49648);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_turns(ratings, 26749, 43458, 45749);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_drops(ratings, 40777, 46811, 49152);
    if verbose: print(x, ratings); x+= 1
    #ride_ratings_apply_sheltered_ratings(ratings, 16705, 30583, 35108);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_proximity(vars, ratings, 22367); # TODO
    if verbose: print(x, ratings); x+= 1
    #ride_ratings_apply_scenery(ratings, 11155);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_highest_drop_height_penalty(ratings, 12, 2, 2, 2);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_max_speed_penalty(ratings, 0xA0000, 2, 2, 2);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_max_negative_g_penalty(ratings, FIXED_2DP(0, 10), 2, 2, 2);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_first_length_penalty(ratings, 0x1720000, 2, 2, 2);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_num_drops_penalty(ratings, 2, 2, 2, 2);
    if verbose: print(x, ratings); x+= 1

    ride_ratings_apply_excessive_lateral_g_penalty(ratings, 40960, 34555, 49648);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_intensity_penalty(ratings);
    if verbose: print(x, ratings); x+= 1
    ride_ratings_apply_adjustments(ratings);
    if verbose: print(x, ratings); x+= 1

    if verbose: print("avg:", sum(vars['speeds']) // vars['SegmentTime'] if vars['SegmentTime'] > 0 else 0)
    if verbose: print("max:", vars['max_speed'])
    if verbose: print("invs:", vars['inversions'])
    if verbose: print("seg length", vars['SegmentLength'])

    #ride->upkeep_cost = ride_compute_upkeep(state, ride);
    return ratings

def ride_ratings_calculate_value(vars):
    value = (((vars['excitement'] * 52) * 32) >> 15) + (((vars['intensity'] * 33) * 32) >> 15) + (((vars['nausea'] * 8) * 32) >> 15);
    
    # age modifier - newly built
    value = (value * 3) / 2 + 0;
    
    vars['value'] = value

def ride_ratings_score_close_proximity_loops_helper(vars, col_d, inputTileElement, pt):
    s, segment, seg_name, seg_flags, v, base_z, clearance_z, quarters, block_index = inputTileElement
    if pt not in col_d:
        return
    for s_, segment_, seg_name_, seg_flags_, v_, base_z_, clearance_z_, quarters_, block_index_ in col_d[pt]:
        if s == s_:
            continue
        
        elementsAreAt90DegAngle = ((v.direction ^ v_.direction) & 1) != 0
        if (elementsAreAt90DegAngle):
            zDiff = base_z - base_z_ # todo: check?
            #zDiff = static_cast<int32_t>(tileElement->base_height) - static_cast<int32_t>(coordsElement.element->base_height);
            if (zDiff >= 0 and zDiff <= 16):
                proximity_score_increment(vars, PROXIMITY_TRACK_THROUGH_VERTICAL_LOOP);
                if seg_name in ["ELEM_LEFT_VERTICAL_LOOP", "ELEM_RIGHT_VERTICAL_LOOP"]:
                    proximity_score_increment(vars, PROXIMITY_INTERSECTING_VERTICAL_LOOP);

def calculate_proximity(vars, col_d):
    for pt_to_reserve, lst in col_d.items():
        for x in lst:
            s, segment, seg_name, seg_flags, v, base_z, clearance_z, quarters, block_index = x
            # ride_ratings_score_close_proximity
        
            # check if this piece is touching the bottom.
            if base_z == vars['min_z']:
                proximity_score_increment(vars, PROXIMITY_SURFACE_TOUCH);
        
            # check other pieces at same x,y coordinate (above/below)
            for s_, segment_, seg_name_, seg_flags_, v_, base_z_, clearance_z_, quarters_, block_index_ in lst:
                if s == s_:
                    continue
                if seg_name_ in ["ELEM_LEFT_VERTICAL_LOOP", "ELEM_RIGHT_VERTICAL_LOOP"]:
                    if block_index_ in [3, 6]:
                        if base_z_ - clearance_z <= 10:
                            proximity_score_increment(vars, PROXIMITY_THROUGH_VERTICAL_LOOP);

                if clearance_z_ == base_z:
                    proximity_score_increment(vars, PROXIMITY_OWN_TRACK_TOUCH_ABOVE);
                    if 'STATION' in seg_name_:
                        proximity_score_increment(vars, PROXIMITY_OWN_STATION_TOUCH_ABOVE);
                
                if clearance_z_ + 2 <= base_z:
                    if clearance_z_ + 10 >= base_z:
                        proximity_score_increment(vars, PROXIMITY_OWN_TRACK_CLOSE_ABOVE);
                        if 'STATION' in seg_name_:
                            proximity_score_increment(vars, PROXIMITY_OWN_STATION_CLOSE_ABOVE);
                
                if clearance_z == base_z_:
                    proximity_score_increment(vars, PROXIMITY_OWN_TRACK_TOUCH_ABOVE);
                    if 'STATION' in seg_name_:
                        proximity_score_increment(vars, PROXIMITY_OWN_STATION_TOUCH_ABOVE);
                
                if clearance_z + 2 <= base_z_:
                    if clearance_z + 10 >= base_z_:
                        proximity_score_increment(vars, PROXIMITY_OWN_TRACK_CLOSE_ABOVE);
                        if 'STATION' in seg_name_:
                            proximity_score_increment(vars, PROXIMITY_OWN_STATION_CLOSE_ABOVE);

            #direction = v.direction
            #ride_ratings_score_close_proximity_in_direction(vars, col_d, x, pt_to_reserve, (direction + 1) & 3);
            #ride_ratings_score_close_proximity_in_direction(vars, col_d, x, pt_to_reserve, (direction - 1) & 3);
            
            # ride_ratings_score_close_proximity_loops
            if seg_name in ["ELEM_LEFT_VERTICAL_LOOP", "ELEM_RIGHT_VERTICAL_LOOP"]:
                ride_ratings_score_close_proximity_loops_helper(vars, col_d, x, pt_to_reserve)
                ride_ratings_score_close_proximity_loops_helper(vars, col_d, x, Point(pt_to_reserve[0], pt_to_reserve[1]) + CoordsDirectionDelta[v.direction])

def ride_ratings_calc(vars, col_d, verbose=False):
    # proximity
    calculate_proximity(vars, col_d)
    
    ratings = ride_ratings_calculate_wooden_roller_coaster(vars, verbose=verbose)
    vars['excitement'] = ratings.excitement
    vars['intensity'] = ratings.intensity
    vars['nausea'] = ratings.nausea
    
    ride_ratings_calculate_value(vars)

SPECIAL_FLAGS = {
    "ELEM_BEGIN_STATION": 1,
    "ELEM_MIDDLE_STATION": 1,
    "ELEM_END_STATION": 1,
    "ELEM_ON_RIDE_PHOTO": 2,
    "ELEM_BLOCK_BRAKES": 3,
    "ELEM_WATER_SPLASH": 4,
}

def get_collisions(elements, coords=[], speeds=[], gfv=[], gfl=[], grids=[], verbose=True, skip_flat=False, stop_early=False, increase_speed=False, make_grids=False, grid_bound=None):
    col_data = CollisionData.new()
    ct = 0
    cols = []
    
    if make_grids:
        max_sz = (300,)*3
        grid = np.zeros(max_sz, dtype=int)
        chain_lift = np.zeros(max_sz, dtype=int)
        vangle_start = np.zeros(max_sz, dtype=np.byte)
        vangle_end = np.zeros(max_sz, dtype=np.byte)
        bank_start = np.zeros(max_sz, dtype=np.byte)
        bank_end = np.zeros(max_sz, dtype=np.byte)
        special_flags = np.zeros(max_sz, dtype=np.byte)
        brakes = np.zeros(max_sz, dtype=np.byte)
        num_coords = np.array([0], dtype=np.byte)
        speed = np.array([0], dtype=np.byte)
        end_coords = np.array([0, 0, 0], dtype=np.byte)
        
        #cur_grid = np.zeros((grid_bound[0], grid_bound[1], grid_bound[2]))
        
        wx, wy, wz = grid_bound
        wx, wy, wz = wx//2, wy//2, wz//2
    
    for s, segment in enumerate(elements):
        col_data = get_collision_for_segment(segment, col_data, verbose=verbose, skip_flat=skip_flat, stop_early=stop_early, increase_speed=increase_speed)
        
        if make_grids:
            for _, pt_dict in col_data.new_points:
                ox, oy, oz = pt_dict['pt'].tuple()
                x, y, z = ox+(max_sz[0]//2), oy+(max_sz[1]//2), oz+(max_sz[2]//2)
                defn = pt_dict['def']
                grid[x, y, z] = 1
                chain_lift[x, y, z] = 1 if pt_dict['seg_flags'] & CHAIN_LIFT_FLAGS else 0
                vangle_start[x, y, z] = VANGLE_MAPPING[defn.vangle_start]
                vangle_end[x, y, z] = VANGLE_MAPPING[defn.vangle_end]
                bank_start[x, y, z] = BANK_MAPPING[defn.bank_start]
                bank_end[x, y, z] = BANK_MAPPING[defn.bank_end]
                special_flags[x, y, z] = SPECIAL_FLAGS.get(pt_dict['seg_name'], 0)
                brakes[x, y, z] = pt_dict['seg_flags'] if pt_dict['seg_name'] == "ELEM_BRAKES" else 0
                num_coords[0] += 1
            speed[0] = col_data.speed_mph
            end_coords[:] = [ox, oy, oz]
            
            names = ['grid', 'chain_lift', 'vangle_start', 'vangle_end', 'bank_start', 'bank_end', 'special_flags', 'brakes', 'num_coords', 'speed', 'end_coords']
            
            # constrain to grid_bound, copy and add to grids list.
            #squares = []
            bad_size = False
            
            '''
            arrs = {}
            for name, arr in zip(names[:-3], [grid, chain_lift, vangle_start, vangle_end, bank_start, bank_end, special_flags, brakes]):
                arrs[name] = arr[x-wx:x+wx, y-wy:y+wy, z-wz:z+wz]
                
                if arrs[name].shape != grid_bound:
                    bad_size = True
                    print(f"{y-wy}:{y+wy}, {z-wz}:{z+wz}")
                    break
                #assert arrs[name].shape == grid_bound, f"{name}-{arrs[name]}-{arrs[name].shape}{x-wx}:{x+wx}, {y-wy}:{y+wy}, {z-wz}:{z+wz}-{grid_bound}"
            '''
            
            squares = [] #***3D***
            for name, arr in zip(names[:-3], [grid, chain_lift, vangle_start, vangle_end, bank_start, bank_end, special_flags, brakes]):
                squares.append(arr[x-wx:x+wx, y-wy:y+wy, z-wz:z+wz])
                if squares[-1].shape != grid_bound:
                    bad_size = True
                    print(f"{y-wy}:{y+wy}, {z-wz}:{z+wz}")
                    break
            
            arrs = {}
            arrs['grid_obs'] = np.stack(squares, axis=-1) #***3D***
            #print(arrs['grid_obs'].shape)
            #input()
            
            if bad_size:
                ct += 1
                cols.append(s)
                if verbose: print("Collision:", col_data.err_msg)
                if stop_early:
                    if verbose: print("Stopping early")
                    break
                col_data.collided = False
            #arrs['grid_obs'] = np.stack(squares, axis=-1)
            for name, arr in zip(names[-3:], [num_coords, speed, end_coords]):
                arrs[name] = np.array(arr)
            grids.append(arrs)
            #print(arrs)
            #input()
            
        
        coords.append((col_data.v.pt.x, col_data.v.pt.y, col_data.v.pt.z))
        gfv.append(col_data.gfV)
        gfl.append(col_data.gfL)
        speeds.append(col_data.speed_mph)
        if col_data.collided:
            ct += 1
            cols.append(s)
            if verbose: print("Collision:", col_data.err_msg)
            if stop_early:
                if verbose: print("Stopping early")
                break
            col_data.collided = False
        if s > 0:
            track_def1, track_def2 = TRACK_DEFINITIONS[elements[s-1][0]], TRACK_DEFINITIONS[segment[0]]
            assert (track_def1.vangle_end, track_def1.bank_end) == (track_def2.vangle_start, track_def2.bank_start)
    
    if verbose and len(cols) > 0:
        print("cols:", cols)
    return ct, col_data

if __name__ == "__main__":
    from track_io import load_tracks, load_track
    #tracks, _ = load_tracks(50, 300, track_dir="/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks") 
    #for track in [load_track("/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/tracks-badspeeds/err_X_completed_100.td9")]:
    for track in [load_track("/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/RLCoasterEnv_-02-01_22-12-34-0.td9")]:
        #if track.name != "Jak Rabbit":
        #    continue
        print("\n\n\n\n\n\n", track.name)
        print(track.lift_hill_speed)
        ct, _ = get_collisions(track.elements, verbose=True, skip_flat=True, stop_early=True)
        if ct > 0:
            print(track.name, ct)
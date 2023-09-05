import math, random

import tensorflow as tf
tf.compat.v1.enable_eager_execution()
from ray.rllib.algorithms.algorithm import Algorithm

import astar
from collisions import *
from coaster_envs import *

class TrackGen:
    def __init__(self, elmt_mapping, max_track_length, max_track_height, max_track_segments, limit_flats):
        self.size = (*max_track_length, max_track_height)

        self.max_track_length = max_track_length
        self.max_track_height = max_track_height
        self.max_track_segments = max_track_segments
        self.limit_flats = limit_flats
        self.model = None
        
        self.elmt_mapping = elmt_mapping
        self.elmt_mapping_inv = {v: k for k, v in elmt_mapping.items()}
    
    def setup_gen(self, initial):
        pass
    
    def complete_track(self, elements, start_c=None, goal_c=None, vert_down=False):
        if start_c == None:
            if self.max_track_length == math.inf:
                start_point = Point(100, 100, 0)
            else:
                start_point = Point(self.max_track_length[0]//2, self.max_track_length[1]//2, 0)
            goal_c = CollisionData.new(start_point)
            start_c = goal_c.copy()
        
        col_datas = []
        for s, segment in enumerate(elements):
            #print(s, segment, SEGMENTS[segment[0]])
            start_c = get_collision_for_segment(segment, start_c, verbose=False, skip_flat=True, stop_early=True)
            col_datas.append(start_c)
            #start_c.s += 1
            assert not start_c.collided, start_c.err_msg
        
        goal_c.pieces = [elements[0]]
        start_c.pieces = [elements[-1]]
        assert elements[0] != (0, 0)
                
        def neighbor_func(d):
            assert not d.collided
            assert len(self.constraint_dict) > 0
            verbose = False
            
            neighbors = []
            for seg_num, seg_name in COMPLETION_PIECES:
                if verbose: print(seg_num, seg_name)
                #if disallowed(seg_name):
                #    if verbose:
                #        print("A", seg_name)
                #    continue
                #else:
                if d.pieces[-1] not in self.constraint_dict:
                    print("Unrecognized piece:", d.pieces[-1], SEGMENTS[d.pieces[-1][0]])
                    print("constraint dict:", self.constraint_dict)
                    raise Exception
                
                next_pieces = self.constraint_dict[d.pieces[-1]]
                if not any(seg_num == np[0] for np in next_pieces):
                    if verbose:
                        print("E", seg_num, seg_name, next_pieces)
                    continue
                
                seg_flag = 0 #15 if seg_name == "ELEM_BRAKES" else 0
                col_data = get_collision_for_segment((seg_num, seg_flag), d, verbose=False, stop_early=True, skip_flat=True)
                #if col_data.v.pt.x > max_x or col_data.v.pt.x < min_x: # or col_data.v.pt.y > max_y or col_data.v.pt.y < min_y:
                #    continue
                
                #col_data.s += 1
                if col_data.collided:
                    if verbose:
                        print("F", seg_name)
                    continue
                #print(seg, seg_name)
                #assert seg != 0
                track_def = TRACK_DEFINITIONS[seg_num]
                if track_def.vangle_start in [TRACK_SLOPE_UP_25, TRACK_SLOPE_UP_60, TRACK_SLOPE_UP_90]:
                    col_data.pieces.append((seg_num, CHAIN_LIFT_FLAGS))
                else:
                    col_data.pieces.append((seg_num, seg_flag))
                neighbors.append(col_data)
            return neighbors
            
        def out_of_bounds_func(d):
            return -500 > d.v.pt.x or 500 < d.v.pt.x or -500 > d.v.pt.y or 500 < d.v.pt.y or 0 > d.v.pt.z or 250 < d.v.pt.z
        
        def heuristic2(c1, c2):
            a, b = c1.v.pt, c2.v.pt
                        
            manhattan_dist = abs(b.x-a.x) + abs(b.y-a.y) + abs(b.z - a.z)
            
            # check if ending degree is same as next starting degree...
            
            track_def1, track_def2 = TRACK_DEFINITIONS[c1.pieces[-1][0]], TRACK_DEFINITIONS[c2.pieces[-1][0]]
            
            if vert_down and abs(b.z - a.z) == 0 and track_def1.vangle_end != track_def2.vangle_start: # TS_MAP[SEGMENTS[c1.pieces[-1][0]]]['OutputDegree'] != TS_MAP[SEGMENTS[c2.pieces[-1][0]]]['InputDegree']:
                manhattan_dist += 10
            
            s_ab_x, s_ab_y = math.copysign(1, b.x-a.x), math.copysign(1, b.y-a.y)
            
            
            c = c1.v.pt + Point(-CoordsDirectionDelta[c1.v.direction].x//32, -CoordsDirectionDelta[c1.v.direction].y//32)
            
            #c = AdvanceVector(c1.v, "ELEM_FLAT", verbose=False).pt
            
            #print(f"A: {a}({c1.v.direction}), B: {b}({c2.v.direction}), C: {c}")
            
            s_ac_x, s_ac_y = math.copysign(1, c.x-a.x), math.copysign(1, c.y-a.y)
            
            # 3, 6, 9
            
            
            
            # if 3 turn needed -> 9      ....3 turn needed if: 1) moving away, and 2) 90*
            # elif 2 turn needed -> 6    ....2 turn needed if:                     1) 180*
            # elif 1 turn needed -> 3    ....1 turn needed if: 1) moving closer,   2) 90*
            
            if b.x-a.x != 0 and c.x-a.x != 0 and s_ab_x != s_ac_x:
                #print("Three turns x")
                manhattan_dist += 9 # three turns
            elif b.y-a.y != 0 and c.y-a.y != 0 and s_ab_y != s_ac_y:
                #print("Three turns y")
                manhattan_dist += 9 # three turns
            
            ## extra based on direction
            #if c2.v.direction == c1.v.direction:
            #    pass
            elif c2.v.direction-c1.v.direction == 180 or c1.v.direction-c2.v.direction == 180:
                #print("Two turns - opposite direction")
                manhattan_dist += 6 # two turns
            #elif c1.v.direction == DIR_STRAIGHT and c2.v.direction == DIR_90_DEG_RIGHT:
            #    manhattan_dist += 3 # need turn
            #    #return connect2DRightFacingTrackPieces(trackEnd, stationStart)
            #elif c1.v.direction == DIR_STRAIGHT and c2.v.direction == DIR_90_DEG_LEFT:
            #    manhattan_dist += 3
            
            elif abs(c2.v.direction-c1.v.direction) == 90:
                manhattan_dist += 3 # one turn
            #else:
            #    print("No turn needed - going in right direction")
            
            return manhattan_dist
                
        COMPLETION_PIECES = ["ELEM_RIGHT_QUARTER_TURN_3_TILES", "ELEM_LEFT_QUARTER_TURN_3_TILES",  "ELEM_FLAT", "ELEM_S_BEND_LEFT", "ELEM_S_BEND_RIGHT"] #, "ELEM_BRAKES", "ELEM_RIGHT_QUARTER_TURN_3_TILES_BANK", "ELEM_LEFT_QUARTER_TURN_3_TILES_BANK", ELEM_LEFT_BANK_TO_FLAT", "ELEM_RIGHT_BANK_TO_FLAT", "ELEM_FLAT_TO_LEFT_BANK", "ELEM_FLAT_TO_RIGHT_BANK"
        if vert_down:
            COMPLETION_PIECES = ["ELEM_FLAT_TO_25_DEG_DOWN", "ELEM_25_DEG_DOWN_TO_FLAT", "ELEM_25_DEG_DOWN"] + COMPLETION_PIECES
        COMPLETION_PIECES = [(SEGMENT_NUMS[s], s) for s in COMPLETION_PIECES]
        
        def eq_func(c1, c2):
            track_def1, track_def2 = TRACK_DEFINITIONS[c1.pieces[-1][0]], TRACK_DEFINITIONS[c2.pieces[-1][0]]
            
            return c1.v == c2.v and track_def1.bank_end == track_def2.bank_start # TS_MAP[SEGMENTS[c1.pieces[-1][0]]]['EndingBank'] == TS_MAP[SEGMENTS[c2.pieces[-1][0]]]['StartingBank'] #.pt.z == c2.v.pt.z
        
        #print(first_c.piece, SEGMENTS[first_c.piece[0]])
        #input()
        
        print("Completing track. Starting at", start_c.v, "to end at", goal_c.v)
        path = astar.astar(start=start_c, goal=goal_c, out_of_bounds_func=out_of_bounds_func, neighbor_func=neighbor_func, heuristic=heuristic2, eq_func=eq_func) 
        if type(path) != bool:
            col_datas.extend(path[::-1])
        #assert len(path) > 0
        #print([d.pieces[-1] for d in path[::-1]])
        #input()
        return ([d.pieces[-1] for d in path[::-1]], col_datas) if type(path) != bool else ([], [])
    
    def gen_track(self, num):
        print("Generating track", num)
        
        self.gen_track_ex()
        
        env = self.env
        col_data = env.col_datas[-1]
        pieces = env.track_elements_inv
        
        # get piece to flat
        #print("Getting continuation piece")
        continuation = get_next_piece_to_flat(TRACK_COORDINATES[pieces[-1][0]], TRACK_DEFINITIONS[pieces[-1][0]])
        for seg_name, seg_flag in continuation:
            print(seg_name, seg_flag)
            piece = (SEGMENT_NUMS[seg_name], seg_flag)
            col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data.collided:
                #input("E1")
                return None
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])

        if col_data.v.pt.z > 0: # need to go down
            piece = (SEGMENT_NUMS["ELEM_FLAT_TO_25_DEG_DOWN"], 0)
            col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data.collided:
                #input("E1")
                return None
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
            
            k = 0
            piece = (SEGMENT_NUMS["ELEM_25_DEG_DOWN"], 0)
            while col_data.v.pt.z > 2:
                col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
                if col_data.collided:
                    #input("E2--" + str(k))
                    return None
                k += 1
                pieces.append(piece)
                #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
            
            piece = (SEGMENT_NUMS["ELEM_25_DEG_DOWN_TO_FLAT"], 0)
            col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data.collided:
                #input("E3")
                return None
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
        
        elif col_data.v.pt.z < 0: # need to go up
            piece = (SEGMENT_NUMS["ELEM_FLAT_TO_25_DEG_UP"], CHAIN_LIFT_FLAGS)
            col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data.collided:
                #input("E1")
                return None
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
            
            k = 0
            piece = (SEGMENT_NUMS["ELEM_25_DEG_UP"], CHAIN_LIFT_FLAGS)
            while col_data.v.pt.z < -2:
                col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
                if col_data.collided:
                    #input("E2--" + str(k))
                    return None
                k += 1
                pieces.append(piece)
                #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
            
            piece = (SEGMENT_NUMS["ELEM_25_DEG_UP_TO_FLAT"], CHAIN_LIFT_FLAGS)
            col_data = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data.collided:
                #input("E3")
                return None
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
        
        assert col_data.v.pt.z == 0
        
        while col_data.speed_mph > 20:
            print("Adding some brakes since speed before completion is", col_data.speed_mph)
            brake_speed = 6 #min(64, findNextPowerOf2(col_data.speed_mph) // 2)
            piece = (SEGMENT_NUMS["ELEM_BRAKES"], brake_speed)
            col_data2 = get_collision_for_segment(piece, col_data, verbose=False, stop_early=True, skip_flat=True)
            if col_data2.collided:
                break
            col_data = col_data2
            pieces.append(piece)
            #speeds.append([col_data.speed, col_data.gfV, col_data.gfL])
        
        print("Finished generating")
        
        #segments = [(2, 4), (3, 4), (1, 4)] + segments + [(3, 4), (1, 4)]
        track = copy.copy(self.tracks[0])
        track.elements = pieces
        track.num_backtracks = env.num_backtracks
        if hasattr(env, 'target_ratios'):
            track.target_ratios = env.target_ratios
            track.cur_ratios = env.cur_ratios
        track.name = f'{self.__class__.__name__}_{num}'
        #print("num backtracks:", track.num_backtracks)
        return track

class RLTrackGen(TrackGen):
    def __init__(self, elmt_mapping, max_track_length, max_track_height, max_track_segments, limit_flats, limit_intensity, checkpoint_folder, bridge):
        super().__init__(elmt_mapping, max_track_length, max_track_height, max_track_segments, limit_flats=limit_flats)
        self.env = TargetGridCoasterEnv({"size": self.size, "limit_flats": limit_flats, "limit_intensity": limit_intensity, "max_track_coords": max_track_segments, "elmt_mapping": elmt_mapping})
        self.checkpoint_folder = checkpoint_folder
        
        self.model = Algorithm.from_checkpoint(checkpoint_folder)
    
    def gen_track_ex(self):
        env = self.env
        obs = env.reset()
        
        done = False
        while not done:
            a = self.model.compute_single_action(
                observation=obs,
                explore=True,
                policy_id="default_policy",
            )
            obs, reward, done, info = env.step(a)
            assert not env.col_datas[-1].collided
        print("Env is done")
        env.pieces = env.track_elements_inv

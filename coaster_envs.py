import random
from collections import defaultdict

import gym
from gym.spaces import Box, Dict, Discrete
import numpy as np

from openrct2.segments import *
from collisions import *
from track_io import *

import sys
np.set_printoptions(threshold=sys.maxsize)

class BaseCoasterEnv(gym.Env):
    def __init__(self, config):
        self.size = config['size']
        if type(self.size) is int:
            self.size = (self.size,)*3
        else:
            assert len(self.size) == 3
        if 'elmt_mapping' in config:
            self.elmt_mapping = config['elmt_mapping']
        else:
            self.elmt_mapping = get_elmt_mapping()
        self.limit_flats = config.get("limit_flats", False)
        self.limit_intensity = config.get("limit_intensity", False)
        self.max_track_coords = config.get('max_track_coords', 232)
        self.elmt_mapping_inv = {v: k for k, v in self.elmt_mapping.items()}

    def _fix_action_mask(self):
        final_col_data = self.col_datas[-1]
        self.valid_actions = get_next_segment_validities(self.elmt_mapping, final_col_data.pieces, final_col_data.v, final_col_data.col_d, final_col_data.s, final_col_data._vars, final_col_data.speed_mph, final_col_data, max_size=self.size, forbidden=self.failed_pieces, max_flats=10 if self.limit_flats else math.inf)
        state = tuple(self.track_elements)
        if state in self.prev_valid_actions:
            existing = self.prev_valid_actions[state]
            self.valid_actions = np.logical_and(existing, self.valid_actions)
        self.prev_valid_actions[state] = self.valid_actions

    def update_physics(self, piece, from_scratch=False):
        if piece is not None:
            col_data = get_collision_for_segment(self.elmt_mapping_inv[piece], self.col_datas[-1], stop_early=True, copy=True, verbose=False, skip_flat=True, limit_intensity=self.limit_intensity)
            self.col_datas.append(col_data)
            self.speeds.append([col_data.speed_mph, col_data.gfV, col_data.gfL])
        if self.col_datas[-1].v == self.col_datas[0].v and self.col_datas[-1].s > 3:
            self.reached_station_end = True
    
    def make_starting_track(self):
        # start track with station pieces.
        self.num = 3
        self.speeds = []
        self.pieces = []
        self.track_elements = []
        self.track_elements.append(self.elmt_mapping[(SEGMENT_NUMS["ELEM_BEGIN_STATION"], 0)])
        self.track_elements.append(self.elmt_mapping[(SEGMENT_NUMS["ELEM_MIDDLE_STATION"], 0)])
        self.track_elements.append(self.elmt_mapping[(SEGMENT_NUMS["ELEM_END_STATION"], 1<<3)])
        
        # get physics data.
        self.start_point = Point() #self.size[0]//4, self.size[1]//4, 0)
        self.col_datas = [CollisionData.new(self.start_point)]
        for piece in self.track_elements[:3]:
            self.pieces.append(self.elmt_mapping_inv[piece])
            self.update_physics(piece)
            assert not self.col_datas[-1].collided

    def reset(self, seed=None, options=None):
        self.step_num = 0
        self.num_backtracks = 0        
        self.prev_valid_actions = {}
        self.failed_pieces = defaultdict(set)
        
        super().reset(seed=seed)
        
        self.reached_station_end = False
        self.make_starting_track()
        
        self._fix_action_mask()
        assert np.sum(self.valid_actions) > 0, "No valid actions at start of episode?"
    
    def reset_obs(self):
        pass

    def is_done(self):
        last_col_data = self.col_datas[-1]
        cur_num_pts = len(last_col_data.points)
        
        # manhattan distance from current endpoint to start.
        end_pt = last_col_data.v.pt
        start_pt = self.start_point
        remaining_dist = abs(end_pt.x-start_pt.x) + abs(end_pt.y-start_pt.y) + abs(end_pt.z-start_pt.z)
        return self.num_backtracks > 1000 or cur_num_pts + remaining_dist >= self.max_track_coords

    def get_probs(self, state=None, speeds=None, col_data=None):
        return [1] * len(self.elmt_mapping_inv)

    def step(self, action, verbose=True):
        assert action != 0
        assert self.valid_actions[action], f"Invalid action sent to env: {action}"

        # add piece to track
        self.track_elements.append(action)
        self.pieces.append(self.elmt_mapping_inv[action])
        self.num += 1
        self.step_num += 1
        
        if verbose: print(len(self.track_elements), self.pieces[-1], SEGMENTS[self.pieces[-1][0]], self.col_datas[-1].v)
    
        self.update_physics(action)        
        self._fix_action_mask()
                
        backtracked = False
        backtrack_exp = 0
        while np.sum(self.valid_actions) == 0 or self.col_datas[-1].collided: # backtrack
            assert not self.col_datas[-1].collided or (self.col_datas[-1].speed <= 0 or self.col_datas[-1]._vars['intensity'] > 1000), self.col_datas[-1].err_msg
            
            num_to_backtrack = min(9, 3**backtrack_exp, len(self.track_elements)-3)
            if verbose: print("Backtracking:", num_to_backtrack)
            for i in range(num_to_backtrack):
                self.col_datas.pop()
                self.speeds.pop()
                last_piece = self.pieces.pop()
                last_action = self.track_elements.pop()
                self.num -= 1
                
                self.valid_actions = self.prev_valid_actions[tuple(self.track_elements)]
                
                pieces_tup = tuple(self.pieces)
                self.valid_actions[last_action] = 0
                self.failed_pieces[pieces_tup].add(last_piece)
                
                ls, lf = last_piece
                
                if lf & CHAIN_LIFT_FLAGS:
                    # if piece has chain lift and was invalid, then also set non-chain lift to invalid
                    self.failed_pieces[pieces_tup].add((ls, 0))
                    self.valid_actions[self.elmt_mapping[(ls, 0)]] = 0
                elif SEGMENTS[ls] in ["ELEM_BRAKES", "ELEM_BLOCK_BRAKES", "ELEM_ON_RIDE_PHOTO", "ELEM_FLAT"]:
                    # set all to invalid
                    ls1 = SEGMENT_NUMS["ELEM_ON_RIDE_PHOTO"]
                    self.failed_pieces[pieces_tup].add((ls1, 0))
                    self.valid_actions[self.elmt_mapping[(ls1, 0)]] = 0
                    
                    ls2 = SEGMENT_NUMS["ELEM_BLOCK_BRAKES"]
                    self.failed_pieces[pieces_tup].add((ls2, 0))
                    self.valid_actions[self.elmt_mapping[(ls2, 0)]] = 0
                    
                    ls3 = SEGMENT_NUMS["ELEM_BRAKES"]
                    for brake_speed in range(1, 16):
                        self.failed_pieces[pieces_tup].add((ls3, brake_speed))
                        self.valid_actions[self.elmt_mapping[(ls3, brake_speed)]] = 0
                    
                    ls4 = SEGMENT_NUMS["ELEM_FLAT"]
                    self.failed_pieces[pieces_tup].add((ls4, 0))
                    self.valid_actions[self.elmt_mapping[(ls4, 0)]] = 0
                
                self.prev_valid_actions[tuple(self.track_elements)] = self.valid_actions
            
            backtrack_exp += 1
            backtracked = True
            self.num_backtracks += 1
        
        if backtracked:
            self.reset_obs() # recalculate observations
            self.update_physics(piece=None, from_scratch=True)

class CoasterEnv(BaseCoasterEnv):
    def __init__(self, config):
        super().__init__(config)
        self._skip_env_checking = True
                        
        self.action_space = Discrete(len(self.elmt_mapping)+1)
        self.observation_space = Dict({
            "action_mask": Box(low=0, high=1, shape=(len(self.elmt_mapping)+1,), dtype=int),
            "observations": Box(low=0, high=len(self.elmt_mapping)+1, shape=(64,), dtype=int),
            "value": Discrete(1),
        })
        
        self.iter = 0
        self.render = config.get("render", False)
        if self.render:
            plt.ion() # enable interactive mode (continue graphing without having to close the window)
            plt.show() # show the plot
            
            self.axes = plt.axes(projection='3d')
    
    def _get_obs(self):
        #assert self.valid_actions.shape[0] == len(ELMT_MAPPING)+1
        return {
            "action_mask": self.valid_actions,
            "observations": np.array(self.track_elements[:64]),
            "value": self.col_datas[-1]._vars['value'],
        }

    def _get_info(self):
        return {}
    
    def reset(self, seed=None, options=None):
        if self.iter > 0 and self.render:
            self._render_frame()
        self.iter += 1
                
        self.reset_obs()
        self.rewards = []

        super().reset(seed=seed)
                
        observation = self._get_obs()
        info = self._get_info()
        return observation #, info

    #def is_done(self):
    #    return self.num >= 64 or self.reached_station_end
    
    def get_reward(self):
        if self.reached_station_end:
            return self.col_datas[-1]._vars['value']
        return 0
    
    def get_done_and_reward(self):
        return self.is_done(), self.get_reward()
    
    def step(self, action, verbose=False):
        bt = self.num_backtracks
        cur_num = self.num
        super().step(action, verbose)
        
        terminated, reward = self.get_done_and_reward()
        if self.num_backtracks > bt:
            reward = 0
            num_lost_rewards = cur_num - self.num
            for i in range(num_lost_rewards):
                reward -= self.rewards.pop()
        else:
            self.rewards.append(reward)
        
        observation = self._get_obs()
        info = self._get_info()
        
        if terminated and verbose: print("End of episode")
        
        
        return observation, reward, terminated, info
    
    def reset_obs(self):
        pass
    
    def _render_frame(self):
        self.axes.clear() # clear the previous window contents
        
        # set the axis bounds
        self.axes.set_xlim(0, self.size[0])
        self.axes.set_ylim(0, self.size[1])
        self.axes.set_zlim(0, self.size[2])
        self.axes.set_xticks(list(range(self.size[0]+1)))
        self.axes.set_yticks(list(range(self.size[1]+1)))
        self.axes.set_zticks(list(range(self.size[2]+1)))
        self.axes.tick_params(axis='both', which='minor', labelsize=8)
        
        xs, ys, zs = [], [], []
        for p, pt in self.col_datas[-1].points.items():
            pt = pt['pt']
            xs.append(pt.x)
            ys.append(pt.y)
            zs.append(pt.z)
        
        # ref: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
        self.axes.plot3D(xs, ys, zs)
        plt.draw()
        plt.pause(0.5)
    
    def save_track(self, name):
        track = copy.copy(TRACK_TEMPLATE)
        print(self.track_elements)
        track.elements = []
        elements = self.track_elements #[:-1]
        if self.col_datas[-1].collided:
            elements = elements[:-1]
        for piece in elements:
            if piece == 0:
                break
            track.elements.append(self.elmt_mapping_inv[piece])
        track.name = f'{type(self).__name__}_{name}'
        track.num_backtracks = self.num_backtracks
        save_track(track, track_dir='/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks')
        return track

TARGET_RANGES = {
    'track_elements': (100, 175),
    'max_speed': (40, 60),
    'avg_speed': (20, 30),
    'drops': (4, 10),
    'airtime': (75, 150),
    'excitement_ratio': (800, 800), # constant
    "intensity_ratio": (400, 900),
}
class TargetGridCoasterEnv(CoasterEnv):
    def __init__(self, config):
        super().__init__(config)
        assert 'size' in config, "Grid size must be bounded."
        
        # sample from targets
        self.target_ranges = TARGET_RANGES
        
        self.cur_values = { target: 0 for target in self.target_ranges }
        
        size = self.size
        self.observation_space = Dict({
            "action_mask": Box(low=0, high=1, shape=(len(self.elmt_mapping)+1,), dtype=bool),
            "observations": Dict({
                # track info
                "grid": Box(low=0, high=1, shape=size, dtype=bool),
                "chain_lift": Box(low=0, high=1, shape=size, dtype=bool),
                "vangle_start": Box(low=0, high=5, shape=size, dtype=np.byte),
                "vangle_end": Box(low=0, high=5, shape=size, dtype=np.byte),
                "bank_start": Box(low=0, high=4, shape=size, dtype=np.byte),
                "bank_end": Box(low=0, high=4, shape=size, dtype=np.byte),
                "special_flags": Box(low=0, high=4, shape=size, dtype=np.byte),
                "brakes": Box(low=0, high=16, shape=size, dtype=np.byte),
                "targets": Box(low=-1, high=1, shape=(len(self.target_ranges),)),
                "values": Box(low=-1, high=1, shape=(len(self.target_ranges),)),
                #**{f'target_{target}': Box(low=-1, high=1, shape=(1,)) for target in self.target_ranges},
                #**{f'cur_{target}': Box(low=-1, high=1, shape=(1,)) for target in self.target_ranges},
            }),
            # metrics for tensorboard (not part of state)
            "value": Box(0, 10000, shape=(1,), dtype=np.float32),
            "excitement":  Box(0, 10000, shape=(1,), dtype=np.float32),
            "intensity": Box(0, 10000, shape=(1,), dtype=np.float32),
            "nausea": Box(0, 10000, shape=(1,), dtype=np.float32),
            "reached_station": Box(0, 1, shape=(1,), dtype=bool),
            "backtracks": Box(0, 10000, shape=(1,), dtype=int),
            
            **{f'{target}': Box(-1, 10000, shape=(1,)) for target in self.target_ranges},
        })
    
    def _get_obs(self):
        final_col_data = self.col_datas[-1]
        return {
            "action_mask": self.valid_actions,
            "observations": {
                "grid": self.grid,
                "chain_lift": self.chain_lift,
                "vangle_start": self.vangle_start,
                "vangle_end": self.vangle_end,
                "bank_start": self.bank_start,
                "bank_end": self.bank_end,
                "special_flags": self.special_flags,
                "brakes": self.brakes,
                "targets": self.targets_array,
                "values": self.values_array,
                
                #**{f'target_{target}': np.array([self.target_ratios[target]]) for target in self.target_ranges},
                #**{f'cur_{target}': np.array([self.cur_ratios[target]]) for target in self.target_ranges},
            },
            "value": np.array([final_col_data._vars['value']]),
            "excitement": np.array([final_col_data._vars['excitement']]),
            "intensity": np.array([final_col_data._vars['intensity']]),
            "nausea": np.array([final_col_data._vars['nausea']]),
            "reached_station": np.array([self.reached_station_end]),
            "backtracks": np.array([self.num_backtracks]),
            
            **{f'{target}': np.array([self.cur_values[target]]) for target in self.target_ranges},
        }
    
    def update_physics(self, piece, from_scratch=False):
        if piece is not None:
            super().update_physics(piece)
        
        pts = self.col_datas[-1].new_points if not from_scratch else self.col_datas[-1].points.items()
        for _, pt_dict in pts:
            x, y, z = pt_dict['pt'].tuple()
            defn = pt_dict['def']
            self.grid[x, y, z] = 1
            self.chain_lift[x, y, z] = 1 if pt_dict['seg_flags'] & CHAIN_LIFT_FLAGS else 0
            self.vangle_start[x, y, z] = VANGLE_MAPPING[defn.vangle_start]
            self.vangle_end[x, y, z] = VANGLE_MAPPING[defn.vangle_end]
            self.bank_start[x, y, z] = BANK_MAPPING[defn.bank_start]
            self.bank_end[x, y, z] = BANK_MAPPING[defn.bank_end]
            self.special_flags[x, y, z] = SPECIAL_FLAGS.get(pt_dict['seg_name'], 0)
            self.brakes[x, y, z] = pt_dict['seg_flags'] if pt_dict['seg_name'] == "ELEM_BRAKES" else 0
        
        self.update_target_arrays()
        
    def update_target_arrays(self):
        final_col_data = self.col_datas[-1]
        self.cur_values = {
            'track_elements': final_col_data.s,
            'max_speed': final_col_data._vars['max_speed_mph'],
            'avg_speed': sum(final_col_data._vars['speeds_mph']) / len(final_col_data._vars['speeds_mph']),
            'drops': final_col_data._vars['drops'] & 0x3F,
            'airtime': final_col_data._vars['total_air_time'],
            'excitement_ratio': final_col_data._vars['excitement'],
            'intensity_ratio': final_col_data._vars['intensity'],
        }
        
        self.target_ratios = {
            target: self.targets[target] / self.target_ranges[target][1] for target in self.target_ranges
        }
        
        self.cur_ratios = {
            target: min(1, self.cur_values[target] / self.target_ranges[target][1]) for target in self.target_ranges
        }
        
        self.targets_array = np.array([self.targets[target] / self.target_ranges[target][1] for target in self.target_ranges])
        self.values_array = np.array([min(1, self.cur_values[target] / self.target_ranges[target][1]) for target in self.target_ranges])
        
        self.prev_loss = self.loss
        self.loss = sum([abs(self.target_ratios[target] - self.cur_ratios[target]) for target in self.target_ranges])
                
        self.stats = [(self.target_ratios[target], self.cur_ratios[target]) for target in self.target_ranges]
    
    def reset_obs(self):
        sz = self.size #,)*3
        self.grid = np.zeros(sz, dtype=bool)
        self.chain_lift = np.zeros(sz, dtype=bool)
        self.vangle_start = np.zeros(sz, dtype=np.byte)
        self.vangle_end = np.zeros(sz, dtype=np.byte)
        self.bank_start = np.zeros(sz, dtype=np.byte)
        self.bank_end = np.zeros(sz, dtype=np.byte)
        self.special_flags = np.zeros(sz, dtype=np.byte)
        self.brakes = np.zeros(sz, dtype=np.byte)
        self.targets_array = np.zeros(len(self.target_ranges))
        self.values_array = np.zeros(len(self.target_ranges))
    
    def reset(self, seed=None, options=None, targets=None):
        self.targets = targets
        if targets is None:
            self.targets = {
                k: random.randint(v[0], v[1]) for k, v in self.target_ranges.items()
            }
        
        self.loss = 0
        self.prev_loss = 0
        
        obs = super().reset(seed, options)
        self.update_target_arrays()
                                
        return obs
    
    def is_done(self):
        return self.step_num > 250 or super().is_done()
    
    def get_done_and_reward(self):
        reward = self.prev_loss - self.loss
        done = abs(self.loss) < 0.05 or np.sum(self.valid_actions) == 0 or super().is_done()        
        return done, reward

VERBOSE = True
if __name__ == "__main__":
    #tracks, _ = load_tracks(min_track_len=50, max_track_len=300)
    #ELMT_MAPPING_INV = {v: k for k, v in ELMT_MAPPING.items()}
    #ELMT_NAMES = {SEGMENTS[k[0]] for k in ELMT_MAPPING}
    #TRACK_TEMPLATE = tracks[0]
    
    #from bridge import Bridge
    #rct_bridge = Bridge()
    #rct_bridge.bind()
    
    ELMT_MAPPING = get_elmt_mapping()
    env = TargetGridCoasterEnv(config={"size": 24, "elmt_mapping": ELMT_MAPPING})
    
    bad_speeds = 0
    for i in range(1000):
        print(i)
        obs = env.reset()
        done = False
        episode_reward = 0
        while not done:
            action = np.random.choice(range(len(ELMT_MAPPING)+1), p=env.valid_actions / np.sum(env.valid_actions))
            #print("Action:", ELMT_MAPPING_INV[action])
            obs, reward, done, info = env.step(action, verbose=VERBOSE)
        
            if env.col_datas[-1].speed < 0:
                bad_speeds += 1
                print("Bad speed")
                #print(SEGMENTS[env.col_datas[-2].pieces[-1][0]], "-->", SEGMENTS[env.col_datas[-1].pieces[-1][0]])
                #input()
            #print("Reward:", reward)
            episode_reward += reward
            # Is the episode `done`? -> Reset.
            if done:
                print("Done episode")
                #env.save_track(f'test')
                #tested_track, tot_time = rct_bridge.fill_in_fields("/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/TargetGridCoasterEnv_test.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/exportX_test.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/err_X_completed_{i}.td9")
                
                #input()
            #if done:
            #    print("DONE")
    print(bad_speeds)
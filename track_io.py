import os, statistics, math
from glob import glob
from pprint import pprint
from collections import defaultdict

import dill
import numpy as np
from tqdm import tqdm

from geo import *
from openrct2 import *
from collisions import CollisionData, get_collision_for_segment, get_collisions

class Track:
    pass

# http://freerct.github.io/RCTTechDepot-Archive/trackQualifier.html
def get_elmt_mapping():
    # determine range of elements.
    
    vangle_starts = set()
    vangle_ends = set()
    bank_starts = set()
    bank_ends = set()
    types = set()
    
    lengths = set()
    xs, ys, zs = set(), set(), set()
    
    elmts = set()
    for seg_num, seg_name in enumerate(SEGMENTS):
        if seg_name in BLACKLIST:
            continue
        if "COVERED" in seg_name:
            continue
        
        track_def = TRACK_DEFINITIONS[seg_num]
        if track_def.type not in WOODEN_ROLLER_COASTER_RTD["EnabledTrackPieces"]:
            continue
        
        types.add(track_def.type)
        bank_ends.add(track_def.bank_end)
        bank_starts.add(track_def.bank_start)
        vangle_ends.add(track_def.vangle_end)
        vangle_starts.add(track_def.vangle_start)
        
        blocks = TRACK_BLOCKS[seg_num]
        lengths.add(len(blocks)-1)
        for block in blocks:
            if block == TRACK_BLOCK_END:
                continue
            #if abs(block.x//32) >= 5 or abs(block.y//32) >= 5 or block.z//8 >= 7:
            #    #print(seg_name)
            #    continue
            xs.add(block.x//32)
            ys.add(block.y//32)
            zs.add(block.z//8)
        
        if seg_name == "ELEM_BRAKES":
            for brake_speed in range(1, 16):
                elmts.add((seg_num, brake_speed))
            continue
        
        seg_flag = 0 
        if seg_name == "ELEM_END_STATION":
            seg_flag = 1<<3

        track_flags = TRACK_FLAGS[seg_num]
        if (track_flags & TRACK_ELEM_FLAG_ALLOW_LIFT_HILL) and not (track_flags & TRACK_ELEM_FLAG_CURVE_ALLOWS_LIFT) and not (track_flags & TRACK_ELEM_FLAG_DOWN) and not (track_flags & TRACK_ELEM_FLAG_IS_STEEP_UP):
            elmts.add((seg_num, CHAIN_LIFT_FLAGS))
        
        elmts.add((seg_num, seg_flag))
    
    '''
    elmts = set()
    for track in tracks:
        for seg_num, seg_flags in track.elements:
            if "BRAKES" in SEGMENTS[seg_num]:
                elmts.add((seg_num, seg_flags))
            elif TRACK_FLAGS[seg_num] & TRACK_ELEM_FLAG_ALLOW_LIFT_HILL:
                elmts.add((seg_num, CHAIN_LIFT_FLAGS))
                elmts.add((seg_num, 0))
            else:
                elmts.add((seg_num, 0))
        #elmts.update([el for el in track.elements])
    '''
    
    print("Alphabet length:", len(elmts))
    #print("bank", len(bank_ends))
    #print(len(bank_starts))
    #print("vangle", len(vangle_ends))
    #print(len(vangle_starts))
    #print("types", len(types), types)
    #print("lengths", len(lengths), lengths)
    #print("xs", len(xs), xs)
    #print("ys", len(ys), ys)
    #print("zs", len(zs), zs)
    elmt_mapping = dict(enumerate(list(elmts)))
    elmt_mapping = {v: k+1 for k, v in elmt_mapping.items()} # k=0 -> k=1
    return elmt_mapping

def get_upward_starting_tracks(tracks):
    upward_tracks = []
    for track in tracks:
        for elmt in track.elements[:3+5]:
            track_def = TRACK_DEFINITIONS[elmt[0]]
            #ts = TS_MAP[SEGMENTS[elmt[0]]]
            #if ts['OutputDegree'] in [TRACK_DOWN_25, TRACK_DOWN_60, TRACK_DOWN_90]:
            if track_def.vangle_end in [TRACK_SLOPE_DOWN_25, TRACK_SLOPE_DOWN_60, TRACK_SLOPE_DOWN_90]:
                break
        else:
            upward_tracks.append(track)
    print("Upward tracks:", len(upward_tracks))
    return upward_tracks

def get_sequences(tracks):
    from collisions import CollisionData, get_collision_for_segment
    
    seq_size = 10
    
    seqs = []
    for track in tqdm(tracks):
        for i in range(1, len(track.elements)-seq_size):
            seq = track.elements[i:i+seq_size]
            assert len(seq) == seq_size
            # check input angle and banking
            track_def = TRACK_DEFINITIONS[seq[0][0]]
            if track_def.vangle_start != TRACK_SLOPE_NONE or track_def.bank_start != TRACK_BANK_NONE:
                continue
            seqs.append(seq)
    print(len(seqs))
    return seqs

def get_starting_sequences(tracks, max_size):
    from collisions import CollisionData, get_collision_for_segment
    start_point = Point(max_size//4, max_size//4, 0)
    
    dists = defaultdict(int)
    sequences = defaultdict(int)
    all_seqs = []
    for track in tracks:
        col_data = CollisionData.new(Point.from_Point(start_point))
        
        stations = [
            (SEGMENT_NUMS["ELEM_BEGIN_STATION"], 0),
            (SEGMENT_NUMS["ELEM_MIDDLE_STATION"], 0),
            (SEGMENT_NUMS["ELEM_END_STATION"], 8),
        ]
        for elmt in stations:
            col_data = get_collision_for_segment(elmt, col_data, stop_early=True, copy=True, verbose=False)
        
        collided = False
        elmts = []
        for elmt in track.elements[1:10]:
            seg_name = SEGMENTS[elmt[0]]
            if "STATION" in seg_name or "BRAKES" in seg_name:
                collided = True
                break
            new_col_data = get_collision_for_segment(elmt, col_data, stop_early=True, copy=True, verbose=False)
            if new_col_data.collided:
                collided = True
                break
            PADDING = 2
            if new_col_data.v.pt.x-PADDING <= 0 or new_col_data.v.pt.x+PADDING >= max_size or new_col_data.v.pt.y-PADDING <= 0 or new_col_data.v.pt.y+PADDING >= max_size or new_col_data.v.pt.z < 0:
                break
            #elmts.append((seg_name, elmt[1]))
            elmts.append(elmt) #(seg_name, elmt[1]))
            col_data = new_col_data
        if collided:
            continue
        assert len(elmts) > 0, new_col_data.v.pt
        # get distance from center.
        dx, dy = col_data.v.pt.x, col_data.v.pt.y
        dists[(dx, dy)] += 1
        sequences[tuple(elmts)] += 1
        all_seqs.append(elmts)
    
    return list(sequences), all_seqs

FIELDS = [
    'type',
    'vehicle_type',
    'cost',
    'flags',
    'ride_mode',
    'track_flags',
    'colour_scheme',
    'entrance_style',
    'total_air_time',
    'depart_flags',
    'number_of_trains',
    'number_of_cars_per_train',
    'min_waiting_time',
    'max_waiting_time',
    'operation_setting',
    'max_speed',
    'average_speed',
    'ride_length',
    'max_positive_vertical_g',
    'max_negative_vertical_g',
    'max_lateral_g',
    'inversions',
    'drops',
    'highest_drop_height',
    'excitement',
    'intensity',
    'nausea',
    'upkeep_cost',
    'flags2',
    'vehicle_object_flags',
    'space_required_x',
    'space_required_y',
    'lift_hill_speed',
    'num_circuits',
    'num_track_elements'
]
FIELDS = dict(list(enumerate(FIELDS)))

bad = []
brakes = defaultdict(int)
def load_track(path):
    #print(path)
    track = Track()
    track.name = path.split('/')[-1].split('.')[0]
    track.elements = []
    track.entrances = []
    track.scenery = []
    with open(path) as f:
        mode = 0
        for i, line in enumerate(f):
            line = line.strip()
            if i < len(FIELDS):
                setattr(track, FIELDS[i], line)
            else: # track elements
                #print(i, line)
                if 'ENT' in line:
                    mode = 1
                    continue
                elif 'SCEN' in line:
                    mode = 2
                    continue
                if mode == 1:
                    #print(line)
                    z, d, x, y = line.split(',')
                    track.entrances.append(Vector(Point(int(x), int(y), int(z)), int(d)))
                    #print(z, d, x, y)
                elif mode == 2:
                    track.scenery.append(line.split(','))
                else:
                    assert ',' in line
                    seg_num, seg_flag = line.split(',')
                    seg_num, seg_flag = int(seg_num), int(seg_flag)
                    seg_name = SEGMENTS[seg_num]
                    
                    if seg_name == "ELEM_BRAKES":
                        #seg_flag = findNextPowerOf2(seg_flag)
                        
                        for i in range(4, 6+1): # color, color, inverted:
                            if seg_flag & (1 << i):
                                seg_flag ^= (1 << i)
                        
                        brakes[seg_flag] += 1
                        track.elements.append((seg_num, seg_flag))
                        continue
                    elif 'STATION' in seg_name:
                        seg_flag = 0 if 'END' not in seg_name else 1<<3
                        track.elements.append((seg_num, seg_flag))
                        continue
                    
                    for i in range(4, 6+1): # color, color, inverted:
                        if seg_flag & (1 << i):
                            seg_flag ^= (1 << i)
                    
                    if seg_flag & (1 << 2):
                        seg_flag ^= (1 << 2)
                        
                    if seg_flag & CHAIN_LIFT_FLAGS:
                        track_flags = TRACK_FLAGS[seg_num]
                        assert track_flags & TRACK_ELEM_FLAG_ALLOW_LIFT_HILL
                        assert not (track_flags & TRACK_ELEM_FLAG_CURVE_ALLOWS_LIFT)
                        seg_flag = CHAIN_LIFT_FLAGS
                        track_def = TRACK_DEFINITIONS[seg_num]
                        if track_def.vangle_start in [TRACK_SLOPE_DOWN_25, TRACK_SLOPE_DOWN_60, TRACK_SLOPE_DOWN_90] or track_def.vangle_end in [TRACK_SLOPE_DOWN_25, TRACK_SLOPE_DOWN_60, TRACK_SLOPE_DOWN_90]:
                            seg_flag = 0
                    
                    if seg_flag not in [0, 1<<7]:
                        #print(SEGMENTS[seg_num], [i for i in range(8) if seg_flag & (1 << i)])
                        for i in range(1, 6+1):
                            if seg_flag & (1 << i):
                                seg_flag ^= (1 << i)
                    
                    track.elements.append((seg_num, seg_flag))

        if any(e[0] >= len(SEGMENTS) for e in track.elements):
            print("*** Bad track pieces:", [e[0] for e in track.elements if e[0] > len(SEGMENTS)])
    
    track.excitement = float(track.excitement[:-1] + '.' + track.excitement[-1])
    track.intensity = float(track.intensity[:-1] + '.' + track.intensity[-1])
    track.nausea = float(track.nausea[:-1] + '.' + track.nausea[-1])
    
    if float(track.cost) > 0:
        track.cost = round(350000 - float(track.cost)/10, 2)
    
    #print(track.name, track.cost)
    return track

def save_track(track, name=None, track_dir='/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks'):
    col_datas = [CollisionData.new()]
    for elmt in track.elements[:3]:
        col_datas.append(get_collision_for_segment(elmt, col_datas[-1]))

    #vectors = get_vectors(track.elements, k=3)
    # get station elements
    #stations = vectors #[:3]
    diff_x = col_datas[0].v.pt.x - col_datas[-1].v.pt.x
    diff_y = col_datas[0].v.pt.y - col_datas[-1].v.pt.y
    # get direction perpendicular...
    #print(diff_x, diff_y)
    track.entrances = []
    if diff_y != 0:
        track.entrances.append(Vector(Point(100*32, -32, 0), 1))
        track.entrances.append(Vector(Point(101*32, -32, 0), 1))
    else:
        track.entrances.append(Vector(Point(-32, 100*32, 0), 1)) #2*32
        track.entrances.append(Vector(Point(-32, 101*32, 0), 1)) #3*32
    #print(track.entrances)
    
    if not os.path.exists(track_dir):
        print("Creating folder", track_dir)
        os.makedirs(track_dir)
    path = f"{track_dir}/{track.name if name is None else name}.td9"
    with open(path, 'w') as f:
        for i, field in FIELDS.items():
            attr = getattr(track, field)
            if type(attr) is float:
                attr = str(attr).replace('.', '')
            f.write(attr + "\n")
        for i, elem in enumerate(track.elements):
            f.write(f'{elem[0]},{elem[1]}\n')
            #if i < len(track.elements)-1:
            #    f.write('\n')
        f.write('ENT\n')
        for i, ent in enumerate(track.entrances):
            f.write(f'{ent.pt.z},{ent.direction},{ent.pt.x},{ent.pt.y}')
            f.write('\n')
        f.write('SCEN\n')
        for i, scen in enumerate(track.scenery):
            f.write(','.join([str(s) for s in scen]))
            if i < len(track.scenery)-1:
                f.write('\n')
    with open(path[:-3]+'.dill', 'wb') as f:
        dill.dump(track, f)

constraint_dict = defaultdict(set)
def load_tracks(min_track_len=0, max_track_len=math.inf, check_collisions=False, track_dir=None, grid_model=False, grid_bound=None, load_all=False):
    tracks = []
    sizes = defaultdict(int)
    
    if track_dir is None:
        track_dir = "/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/exported_tracks/exported_no_scenery"
    files = sorted(glob(f"{track_dir}/*.td9"))
    print("Total TD9s in directory:", len(files))
    files = tqdm(list(enumerate(files)))
    
    #send_socket, rcv_socket, rcv_poller = bind_to_app()
    blacklisted = {x: 0 for x in BLACKLIST}
    bad_ct = 0
    
    a1, a2, a3 = 0, 0, 0
    for i, path in files:
        #if i > 100: break
        track = load_track(path)
        if 'STATION' in SEGMENTS[track.elements[-2][0]]:
            track.elements = track.elements[-2:] + track.elements[:-2]
        
        for x in track.elements:
            if SEGMENTS[x[0]] in blacklisted:
                blacklisted[SEGMENTS[x[0]]] += 1
        
        for i in range(len(track.elements)-1):
            constraint_dict[track.elements[i]].add(track.elements[i+1])
            
        if not load_all and (track.intensity > 2 * track.excitement or track.excitement < 4 or track.intensity > 9):
            bad.append(track)
            a1 += 1
            continue
        # TODO: Fix -- should compare against coordinates (pieces), not elements.
        if not load_all and (len(track.elements) < min_track_len or len(track.elements) > max_track_len):
            bad.append(track)
            a2 += 1
            continue
        
        track.speeds = []
        if check_collisions or grid_model:
            speeds, gfv, gfl, grids = [], [], [], []
            cc, col_data = get_collisions(track.elements, speeds=speeds, gfv=gfv, gfl=gfl, grids=grids, verbose=False, stop_early=False, increase_speed=True, make_grids=grid_model, grid_bound=grid_bound, skip_flat=True)
            #print(cc)
            track.speeds = speeds
            track.gfv = gfv
            track.gfl = gfl
            track.grids = grids
            track.final_col_data = col_data
            if cc > 0:
                bad_ct+=1
                a3 += 1
                if not load_all:
                    continue
                
        tracks.append(track)
        sizes[len(track.elements)] += 1
    
    #print(len(bad))
    print("Bad ct:", bad_ct)
    
    #print(a1, a2, a3)
    print("Num tracks:", len(tracks))
    
    assert all(track for track in tracks)
    return tracks, constraint_dict

def encode_tracks(tracks, window_size, elmt_mapping, grid_model=False):
    # determine max length
    max_len = 0
    for track in tracks:
        max_len = max(max_len, len(track.elements))
    
    for track in tqdm(tracks):
        if grid_model:
            track.encoded_grids = defaultdict(list)
            
            for data in track.grids: # a list, one per track segment.
                for name, arr in data.items(): # a dictionary, one per data type.
                    track.encoded_grids[name].append(arr)
        
        track.encoded_elements = []
        track.encoded_speeds = []
    
        if not grid_model:
            # padding for before window size
            for i in range(window_size):
                track.encoded_elements.append(0)
                track.encoded_speeds.append([0, 0, 0])

        # track elements: (seg_num, seg_flat) -> int
        for i, elem in enumerate(track.elements):
            assert elem in elmt_mapping, f"Piece {elem} {SEGMENTS[elem[0]]} is not in the mapping!"
            track.encoded_elements.append(elmt_mapping[elem])
            if len(track.speeds) > 0:
                track.encoded_speeds.append([track.speeds[i], track.gfv[i], track.gfl[i]])
    
        if not grid_model:
            # padding for tracks shorter than < 500
            num_missing = max_len - len(track.elements)
            track.encoded_elements = [0] * (num_missing//2) + track.encoded_elements
            track.encoded_elements.extend([0] * (num_missing - num_missing//2))
            track.encoded_speeds = [[0, 0, 0]] * (num_missing//2) + track.encoded_speeds
            track.encoded_speeds.extend([[0, 0, 0]] * (num_missing - num_missing//2))

            # padding for after window size
            for i in range(window_size):
                track.encoded_elements.append(0)
                track.encoded_speeds.append([0, 0, 0])

def get_train_test_split(encoded_tracks, window_size, speed=False, grid_model=False):
    train_xs, train_ys, val_xs, val_ys, test_xs, test_ys = [], [], [], [], [], []
    train_speed_xs, val_speed_xs, test_speed_xs = [], [], []
    train_pct = 0.7
    train_ind = (0, len(encoded_tracks) * train_pct)
    val_pct = 0.15
    val_ind = (train_ind[1], train_ind[1] + (len(encoded_tracks) * val_pct))
    #test_pct = 0.3
    test_ind = (val_ind[1], len(encoded_tracks))

    #if grid_model:
    #    train_xs_parts, val_xs_parts, test_xs_parts = [], [], []
    if grid_model:
        num_arrays = len(encoded_tracks[0].encoded_grids)
        train_xs, val_xs, test_xs = [[] for i in range(num_arrays)], [[] for i in range(num_arrays)], [[] for i in range(num_arrays)]
        for t, track in tqdm(enumerate(encoded_tracks)):
            if t < train_ind[1]:
                xs, xss, ys = train_xs, train_speed_xs, train_ys
            elif t < val_ind[1]:
                xs, xss, ys =   val_xs,   val_speed_xs,   val_ys
            else:
                xs, xss, ys =  test_xs,  test_speed_xs,  test_ys
            
            #assert len(track.encoded_elements) == len(track.encoded_grids['brakes']), f"{t}, {len(track.encoded_elements)}, {len(track.encoded_grids['brakes'])}"
            for i in range(1, len(track.encoded_elements)):
                for n, name in enumerate(track.encoded_grids): # each data type...n=0,name='grid';n=1,name='chain'
                    x = track.encoded_grids[name][i-1] #[i-window_size : i]   # 16 lists of 10 lists
                    #assert len(x) == window_size, f"{x}-{len(x)}"
                    xs[n].append(x)
                y = track.encoded_elements[i]  # 10
                ys.append(y)
    else:
        for t, track in tqdm(enumerate(encoded_tracks)):
            if t < train_ind[1]:
                xs, xss, ys = train_xs, train_speed_xs, train_ys
            elif t < val_ind[1]:
                xs, xss, ys = val_xs, val_speed_xs, val_ys
            else:
                xs, xss, ys = test_xs, test_speed_xs, test_ys
        
            for i in range(window_size, len(track.encoded_elements)):
                x = track.encoded_elements[i-window_size : i]   # 16 lists of 10 lists
                #print(len(x))
                y = track.encoded_elements[i]  # 10
                #print(len(y))
                #input()
                if hasattr(track, 'encoded_speeds'):
                    z = track.encoded_speeds[i-window_size : i]
                    xss.append(z)
                assert len(x) == window_size
                #assert len(z) == window_size
            
                xs.append(x)
                ys.append(y)
    
    #print(test_ind, test_xs)
    
    print("Converting to array form")
    if grid_model:
        for xs in [train_xs, val_xs, test_xs]:
            for i in range(num_arrays):
                '''
                lens = set()
                lens2 = set()
                
                for k in xs[i]:
                    lens.add(len(k))
                    for j in k:
                        lens2.add(j.shape)
                '''
                print(i)
                
                xs[i] = np.stack(xs[i], axis=0)
                xs[i] = xs[i].reshape((*xs[i].shape, 1)) #***3D***
        print("Train: length", len(train_xs))
        print("Lengths 0-10:", [len(x) for x in train_xs])
        print("Shapes 0-10:", [x.shape for x in train_xs])
        #input()
    else:
        train_xs = np.stack(train_xs, axis=0)    
        train_speed_xs = np.stack(train_speed_xs, axis=0) if speed else []
        val_xs = np.stack(val_xs, axis=0)
        val_speed_xs = np.stack(val_speed_xs, axis=0) if speed else []
        test_xs = np.stack(test_xs, axis=0)
        test_speed_xs = np.stack(test_speed_xs, axis=0) if speed else []
        print("Done train xs:", train_xs.shape)

    train_ys = np.vstack(train_ys)
    val_ys = np.vstack(val_ys)
    test_ys = np.vstack(test_ys)
    return train_xs, train_ys, val_xs, val_ys, test_xs, test_ys, train_speed_xs, val_speed_xs, test_speed_xs

def get_stats(tracks):
    for track in tracks:
        track.num_elements = len(track.elements)
    
    print("Num tracks:", len(tracks))
    attrs = ['excitement', 'intensity', 'nausea', 'cost', 'num_elements']
    for attr in attrs:
        vals = [getattr(track, attr) for track in tracks]
        print(f"{attr}\t{round(sum(vals)/len(vals), 2)}\t{round(statistics.stdev(vals), 2)}")

def get_track_size_stats(tracks):
    import matplotlib.pyplot as plt
    sizes = np.zeros((150, 150), dtype=int)
    xs_, ys_, zs_ = [], [], []
    for track in tqdm(tracks):
        col_data = track.final_col_data
        xs = [pt['pt'].x for pt in col_data.points.values()]
        ys = [pt['pt'].y for pt in col_data.points.values()]
        zs = [pt['pt'].z for pt in col_data.points.values()]
        size_x, size_y, size_z = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
        sizes[:size_x, :size_y] += 1
        xs_.append(max(size_x, size_y))
        ys_.append(min(size_x, size_y))
        zs_.append(size_z)
    print("X:", sum(xs_)/len(xs_))
    print("Y:", sum(ys_)/len(ys_))
    print("Z:", sum(zs_)/len(zs_))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(np.linspace(0, 150, 150), np.linspace(0, 150, 150))
    ax.plot_surface(X, Y, Z=sizes, alpha=1)
    plt.show()

def get_track_subset_by_size(tracks, max_xy, max_z, max_coords):
    subset = []
    for track in tracks:
        col_data = track.final_col_data
        if len(col_data.points) > max_coords:
            continue
        
        xs = [pt['pt'].x for pt in col_data.points.values()]
        ys = [pt['pt'].y for pt in col_data.points.values()]
        size_xy = max(max(xs), max(ys)) - min(min(xs), min(ys))
        if size_xy > max_xy:
            continue
        
        zs = [pt['pt'].y for pt in col_data.points.values()]
        size_z = max(zs) - min(zs)
        if size_z > max_z:
            continue
        
        subset.append(track)
    
    return subset

if __name__ == '__main__':
    if not os.path.exists("tracks_50_300_cols.dl"):
        tracks, constraint_dict = load_tracks(min_track_len=50, max_track_len=300, check_collisions=True)
        dill.dump(tracks, open("tracks_50_300_cols.dl", "wb"))
    else:
        tracks = dill.load(open("tracks_50_300_cols.dl", "rb"))
        
        max_z = []
        for track in tqdm(tracks):
            col_data = track.final_col_data
            xs = [pt['pt'].x for pt in col_data.points.values()]
            ys = [pt['pt'].y for pt in col_data.points.values()]
            zs = [pt['pt'].z for pt in col_data.points.values()]
            max_z.append(max(zs) - min(zs))
        max_z.sort()
        print(len([x for x in max_z if x <= 10])/len(tracks), len([x for x in max_z if x <= 20])/len(tracks), len([x for x in max_z if x <= 30])/len(tracks))
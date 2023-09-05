import os, time, dill
from glob import glob

from geo import *
from openrct2 import *
from track_io import *
from collisions import *
from bridge import *
from track_generators import *

path = OPENRCT_BUILD_DIRECTORY + "exportX.td6.td9"
if os.path.exists(path):
    os.remove(path)

MODE = "generate"

# generation params
NUM_TRACKS_TO_GENERATE = 1000
LIMIT_FLATS = False
LIMIT_INTENSITY = False

# determined by dataset averages
MAX_TRACK_LENGTH = (40, 16) #(24, 24)
MAX_TRACK_HEIGHT = 35 #20 #35
MAX_TRACK_SEGMENTS = 232 # 145 # 232

gen_classes = {
    RLTrackGen: {'checkpoint_folder': "/Users/jcampbell/ray_results/PPO/PPO_TargetGridCoasterEnv_2023-03-16_06-12-53_20x20x20/checkpoint_000150"},
}
assert len(gen_classes) == 1

if __name__ == '__main__':
    if len(glob(OPENRCT_TRACK_FOLDER + f'/exportX_*.td9')) > 0:
        input("Tracks already exist in the track folder. Continue?")
    
    elmt_mapping = get_elmt_mapping()
    num_elmts = len(elmt_mapping)
    
    gen_class = list(gen_classes)[0]
    tracks_fname = f"tracks_{gen_class.__name__}.dl"
    print(tracks_fname)
        
    args = list(gen_classes.values())[0]
    gen_class = gen_class(elmt_mapping=elmt_mapping, max_track_length=MAX_TRACK_LENGTH, max_track_height=MAX_TRACK_HEIGHT, max_track_segments=MAX_TRACK_SEGMENTS, limit_flats=LIMIT_FLATS, limit_intensity=LIMIT_INTENSITY, bridge=True, **args)
    
    print("Generating tracks")
    
    rct_bridge = Bridge()
    rct_bridge.bind()

    save_dir = f'shots/{type(gen_class).__name__}_n{MAX_TRACK_SEGMENTS}_l{MAX_TRACK_LENGTH}_h{MAX_TRACK_HEIGHT}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    i = 0
    while i < NUM_TRACKS_TO_GENERATE:
        print(type(gen_class).__name__, i)
        if os.path.exists(f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/exportX_{type(gen_class).__name__}{i}.td9") or len(list(glob(f"{save_dir}/*_{type(gen_class).__name__}{i}.td9"))) == 1:
            i += 1
            continue
        
        if os.path.exists(f"{save_dir}/untested_{i}..dill"):
            track = dill.load(open(f"{save_dir}/untested_{i}..dill", "rb")) #  load_track(f"{save_dir}/untested_{i}.td9")
            track.name = 'X'
            save_track(track, 'X_completed') # save track with completion
            tested_track, tot_time = rct_bridge.fill_in_fields("/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/X_completed.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/exportX_{type(gen_class).__name__}{i}.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/err_X_completed_{i}.td9")
        
            if tested_track is None:
                i += 1
                continue
        
            time.sleep(1)
            name = f"E{round(tested_track.excitement, 2)}__I{round(tested_track.intensity, 2)}_{type(gen_class).__name__}{i}"
            rct_bridge.capture_rct_window_to_file(f'{save_dir}/{name}.png')

            print(f"using untested_{i}...: Excitement {tested_track.excitement}, intensity {tested_track.intensity}, nausea {tested_track.nausea}\n")            
            #with open(f"{save_dir}/{name}_coldatas.dl", 'wb') as f:
            #    dill.dump(col_datas, f)
            tested_track.num_backtracks = track.num_backtracks
            #tested_track.gen_time = (end_time - start_time) // len(tracks)
            save_track(tested_track, track_dir=save_dir, name=name)

            i += 1
            continue
        
        start_time = time.time()
        track = gen_class.gen_track(i)
        end_time = time.time() - start_time

        if track is None: # or len(track.elements) < MAX_TRACK_SEGMENTS:
            continue
        
        save_track(track) # save track

        completion, col_datas = gen_class.complete_track(track.elements)
        if len(completion) == 0:
            continue
        track.elements += completion
    
        track.name = 'X'
        save_track(track, 'X_completed') # save track with completion
        
        tested_track, tot_time = rct_bridge.fill_in_fields("/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/X_completed.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/exportX_{type(gen_class).__name__}{i}.td9", f"/Applications/Games/RollerCoaster Tycoon 2.app/Contents/Resources/drive_c/Program Files/RollerCoaster Tycoon 2/Tracks/err_X_completed_{i}.td9")
    
        if tested_track is None:
            #get_collisions(track.elements)
            continue
    
        time.sleep(1)
        name = f"E{round(tested_track.excitement, 2)}__I{round(tested_track.intensity, 2)}_{type(gen_class).__name__}{i}"
        rct_bridge.capture_rct_window_to_file(f'{save_dir}/{name}.png')

        print(f"Excitement {tested_track.excitement}, intensity {tested_track.intensity}, nausea {tested_track.nausea}\n")            
        with open(f"{save_dir}/{name}_coldatas.dl", 'wb') as f:
            dill.dump(col_datas, f)
        tested_track.num_backtracks = track.num_backtracks
        tested_track.gen_time = (end_time - start_time) // len(tracks)
        save_track(tested_track, track_dir=save_dir, name=name)
            
        i += 1

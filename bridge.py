import os, time

from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
import zmq

from track_io import load_track

class Bridge:
    def __init__(self):
        self.context = zmq.Context()
        self.bound = False

    def bind(self):
        print("Binding")
        self.send_socket = self.context.socket(zmq.CLIENT)
        self.send_socket.connect("tcp://localhost:5555")
    
        self.rcv_socket = self.context.socket(zmq.SERVER)
        self.rcv_socket.bind("tcp://*:5556")
        
        self.rcv_poller = zmq.Poller()
        self.rcv_poller.register(self.rcv_socket, zmq.POLLIN)
        
        self.bound = True
    
    def fill_in_fields(self, track_path, success_path, fail_path):
        assert self.bound
        print(track_path)
    
        start_time = time.time()
        #print(f"Sending request")
        self.send_socket.send_string(track_path)
    
        tested_track = None
        #print("Waiting for reply...")
        socks = dict(self.rcv_poller.poll(10000))
        if socks:
            if socks.get(self.rcv_socket) == zmq.POLLIN:
                pass
                #print("got message") #" ",work_receiver.recv(zmq.NOBLOCK))
        else:
            print("TIMEOUT")
            if os.path.exists("/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/exportX.td9"):
                os.rename("/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/exportX.td9", fail_path)
            os.rename(track_path, fail_path)
            return None, time.time() - start_time

        message = self.rcv_socket.recv()
        #print(f"Received reply {message} ]")
        end_time = time.time()

        path = "/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/exportX.td9"
        while not os.path.exists(path):
            pass    
        if os.path.exists(path):
            tested_track = load_track(path)
            #os.remove(path)
    
        os.rename("/Users/jcampbell/Projects/Games/OpenRCT2/build/tracknet/exportX.td9", success_path)
        
        return tested_track, end_time - start_time

    def capture_rct_window_to_file(self, filename):
        window_name = 'OpenRCT2'
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
        for window in window_list:
            try:
                if window_name.lower() in window['kCGWindowOwnerName'].lower() and str(window['kCGWindowStoreType']) == '1':
                    os.system(f"screencapture -l {window['kCGWindowNumber']} \"{filename}\"")
                    break
            except:
                pass
        else:
            raise Exception(f'Window {window_name} not found.')
    

import datetime
import os
import pathlib
import subprocess
import threading
import time
import signal
import psutil

time_start = None
def main():
    while True:
        print(f"Main threading {datetime.datetime.now()}")
        time.sleep(10)

class ScrCpyTask(threading.Thread):
    def __init__(self, timeout, stop_event):
        super().__init__()
        self.record_process = None
        self.stop_event = stop_event
        self.timeout = timeout

    def run(self) -> None:

        while not self.stop_event.is_set():
            init_file_name = pathlib.Path(f"file_{datetime.datetime.now().strftime('%H_%M_%S')}.mkv")

            self.record_process = subprocess.Popen(
                ["cmd","/c",r"C:\Users\asus\Desktop\Books\ml\scrcpy-win64-v2.3.1\scrcpy-win64-v2.3.1\scrcpy.exe",
                 "--no-display", "--record", init_file_name], cwd=os.getcwd(), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            pid = self.record_process.pid

            time.sleep(200)

            parent = psutil.Process(pid)
            print(parent.pid)
            for child in parent.children(recursive=True):
                if child.name() == 'scrcpy.exe':
                    print(child)
                    # child.send_signal(signal.SIGTERM)
                    subprocess.run("Taskkill /PID %d /F" % child.pid)
            subprocess.run("Taskkill /PID %d /F" % parent.pid)

            self.record_process.send_signal(signal.SIGTERM)
            self.record_process.wait()
            final_path = init_file_name.with_stem(
                init_file_name.stem + "___" + datetime.datetime.now().strftime("%H_%M_%S"))
            os.rename(init_file_name, final_path)










if __name__ == '__main__':
    try:
        stop_recording_event = threading.Event()
        record_thread = ScrCpyTask(10, stop_recording_event)
        main_thread = threading.Thread(target=main)

        record_thread.start()
        main_thread.start()


        record_thread.join()
        main_thread.join()

    except KeyboardInterrupt:

        stop_recording_event.set()
        record_thread.join()
        main_thread.join()
        print("Recording stopped")



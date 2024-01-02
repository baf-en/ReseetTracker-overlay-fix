import os, time
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

file_paths = ['obs/EnterAvg.txt', 'obs/NPH.txt']
fix_paths = ['obs/EnterAvg_fix.txt', 'obs/NPH_fix.txt']
temp = ['None', 0.00]

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global temp
        # print(f"File {event.src_path} has been modified")
        if os.path.basename(event.src_path) == os.path.basename(file_paths[0]):
            # print("enterAvg")
            with open(event.src_path, mode='r') as f1:
                self.data = f1.read()
                if self.data != 'None':
                    # print(round(self.data, 1))
                    self.fixed_enterAvg = self.time_format(float(self.data))
                    if temp[0] != self.fixed_enterAvg:
                        temp[0] = self.fixed_enterAvg
                        print(f'Enter Avg: {self.fixed_enterAvg}')
                        with open(fix_paths[0], 'w+') as f2:
                            f2.write(self.fixed_enterAvg)

        elif os.path.basename(event.src_path) == os.path.basename(file_paths[1]):
            # print("NPH")
            with open(event.src_path, mode='r') as f1:
                self.data = float(f1.read())
                # print(self.data)
                self.fixed_nph = round(self.data, 2)
                if temp[1] != self.fixed_nph:
                    temp[1] = self.fixed_nph
                    print(f'NPH: {self.fixed_nph}')
                    with open(fix_paths[1], 'w+') as f2:
                        f2.write(str(self.fixed_nph))
                
    def time_format(self, number):
        minutes = int(number // 60)
        seconds = round((number - (minutes * 60)), 1)
        return f"{minutes:02}:{seconds:04}"

if __name__ == "__main__":
    print("Resetting...")
    try:
        for afile in fix_paths:
            with open(afile, mode='w+') as txtFile:
                if afile == fix_paths[0]:
                    txtFile.write(temp[0])
                elif afile == fix_paths[1]:
                    txtFile.write(str(temp[1]))

        with open('obs/EnterCount.txt', mode='w+') as f:
            f.write(str("0"))

        for afile in file_paths:
            with open(afile, mode='w+') as f:
                f.write(str("0"))

        event_handler = MyHandler()
        observer = PollingObserver()

        for afile in file_paths:
            observer.schedule(event_handler, path=afile, recursive=False)

        observer.start()

        print("Starting")

        try:
            while True:
                time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(100)
            observer.stop()
        finally:
            observer.stop()
            print("Stopping")
        
    except Exception as e_:
        print(e_)
        time.sleep(100)

import argparse
import atexit
import sys
import time
from collections import OrderedDict
from multiprocessing import Event, Process, Queue
from typing import Any, List

import cv2
import keyboard

parser = argparse.ArgumentParser()
ip = parser.add_argument("-i", "--ip", type=str)
args = parser.parse_args()
alive_set = Event()


def test_fps(args: Any, event: Event, fps_q: Queue, name: str):
    frame_id = 0

    cap = cv2.VideoCapture(
        f"rtsp://admin:zwsz1234@{args.ip}:554/Streaming/Channels/101"
    )
    string = ""
    current_time = time.time()
    while True:
        try:
            ret, _ = cap.read()
            if not ret:
                break
            else:
                frame_id += 1

                if frame_id < 100:
                    remainder = frame_id % 5
                    first_100_time = time.time()

                    if remainder == 0 and current_time < first_100_time:
                        string = (
                            f"wait: {(first_100_time - current_time) * 1000:.4f} ms"
                        )
                if frame_id == 100:
                    time_start = time.time()
                    event.set()
                    string = ""

                if frame_id > 100:
                    time_end = time.time()
                    string = f"{(frame_id - 100) / (time_end - time_start):.8f}"

            fps_q.put([name, string])

        except KeyboardInterrupt:
            exit(0)


def test_time(time_start: float, event: Event, time_q: Queue, name: str):
    while True:
        if event.is_set():
            time_now = time.time()
            cost = f"{time_now - time_start:.3f}s."
            time_q.put([name, cost])


def print_progress(progress: "OrderedDict"):
    # sys.stdout.write("\033[2J\033[H")  # clear screen
    out_list = []
    for name, data in progress.items():
        if data:
            out_list.append(f"{name}: {data}")

    string = ""
    if len(out_list) == 1:
        string = "\r" + out_list[0].replace("fps:", "").strip()

    elif len(out_list) > 1:
        string = "\r" + " | ".join(out_list)
    else:
        string = "\r" + "waiting..."

    sys.stdout.write(string)
    sys.stdout.flush()


def kill_pid(processes: List[Process]):
    try:
        for p in processes:
            p.kill()

    except Exception as e:
        sys.stderr.write(e)


def main():
    print(f"Enter `q` to exit...\n{'-' * 40}")
    status = Queue(maxsize=2)
    progress = OrderedDict()
    processes = []

    try:
        time_start = time.time()
        tasks = [
            Process(target=test_fps, args=(args, alive_set, status, "fps"), name="fps"),
            Process(
                target=test_time,
                args=(time_start, alive_set, status, "time"),
                name="time",
            ),
        ]

        for t in tasks:
            t.start()
            processes.append(t)
            progress[t.name] = None

        while any(i.is_alive() for i in tasks):
            while not status.empty():
                try:
                    name, data = status.get()
                    progress[name] = data
                    print_progress(progress)

                    keyboard.add_hotkey("q", kill_pid, args=(processes,))

                except KeyboardInterrupt:
                    break

    except KeyboardInterrupt:
        atexit.register(kill_pid, args=(processes,))
        exit(0)


if __name__ == "__main__":
    main()
    print("\nAll processes have exited.")

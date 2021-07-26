import cv2, threading, wave, queue, time, pyaudio
from PIL import ImageGrab
import numpy as np
from moviepy.editor import *
from typing import List


class Recorder:
    firstImage = ImageGrab.grab()

    def __init__(self, chunk: int=1024, channels: int=2, rate: int=44100):
        self.__running: bool = True
        self.queue: queue.Queue = queue.Queue()

        self.width: int = self.firstImage.size[0]
        self.height: int = self.firstImage.size[1]
        self.frame: int = 13
        self.aviFileName: str = "test.avi"

        self.CHUNK: int = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS: int = channels
        self.RATE: int = rate
        self._frames: List = []
        self.audioFileName: str = "audio.wav"
        self.audio = pyaudio.PyAudio()
        self.audio_size = self.audio.get_sample_size(self.FORMAT)

        self.mergeFileName: str = "1-1.avi"

    def Produce(self):
        start_time = time.time()
        sum : int = 0

        while self.__running:
            if time.time() - start_time >= 1:
                start_time = time.time()
                sum = 0

            if sum < self.frame:
                img_rgb = ImageGrab.grab()
                img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)
                cv2.imshow('capturing', np.zeros((1, 255), np.uint8))
                cv2.moveWindow('capturing', self.height - 100, self.width - 100)
                self.queue.put(img_bgr)
                sum += 1

        cv2.destroyAllWindows()

    def Consume(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(self.aviFileName, fourcc, self.frame, (self.width, self.height))

        while self.__running:
            img_bgr = self.queue.get()
            video.write(img_bgr)

        video.release()

    def Audio(self):
        # TODO 音频录制
        # 获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备
        def findInternalRecordingDevice(p):
            # 要找查的设备名称中的关键字
            target = '立体声混音'
            for i in range(p.get_device_count()):
                devInfo = p.get_device_info_by_index(i)
                if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
                    print('已找到系统内录设备,序号是 ', i)
                    return i
            return -1

        dev_idx = findInternalRecordingDevice(self.audio)
        if dev_idx < 0:
            return
        # 在打开输入流时指定输入设备
        stream = self.audio.open(input_device_index=dev_idx, format=self.FORMAT, channels=self.CHANNELS,
                                 rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        # 循环读取输入流
        while self.__running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        # 停止读取输入流
        stream.stop_stream()
        # 关闭输入流
        stream.close()
        self.save(self.audioFileName)
        self.audio.terminate()

    def stop(self):
        self.__running = False

    def save(self, fileName: str):
        with wave.open(fileName, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio_size)
            wf.setframerate(self.RATE)
            # 写入数据
            wf.writeframes(b''.join(self._frames))

    def merge(self):
        audioclip = AudioFileClip(self.audioFileName)
        videoclip = VideoFileClip(self.aviFileName)
        videoclip2 = videoclip.set_audio(audioclip)
        video = CompositeVideoClip([videoclip2])
        video.write_videofile(self.mergeFileName, codec='mpeg4')


if __name__ == '__main__':
    recorder = Recorder()

    tasks: list = []
    for var in (recorder.Produce, recorder.Consume, recorder.Audio):
        t = threading.Thread(target=var)
        tasks.append(t)

    for i in tasks:
        i.start()

    for m in tasks:
        m.join()


    input("请输入任意键开始视频录制:")
    recorder.stop()
    recorder.merge()

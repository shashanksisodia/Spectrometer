from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import wave
import pyaudio
import threading

class Application_Real_Time():
    def __init__(self):

        self.DURATION = 100

        self.SAMPLING_RATE = 44100
        self.SAMPLE_WIDTH = 2
        self.CHANNELS = 2
        self.CHUNK = 1024

        self.p = pyaudio.PyAudio()
        self.stream_rec = self.p.open(rate = self.SAMPLING_RATE,
                                      channels = self.CHANNELS,
                                      format = self.p.get_format_from_width(self.SAMPLE_WIDTH),
                                      frames_per_buffer = self.CHUNK,
                                      input = True,
                                      start = False)
        self.stream_play = self.p.open(rate = self.SAMPLING_RATE,
                                       channels = self.CHANNELS,
                                       format = self.p.get_format_from_width(self.SAMPLE_WIDTH),
                                       output = True,
                                       start = False)

        self.data = np.zeros(1024)

        self.app = QtGui.QApplication([])
        self.mw = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.mw.setLayout(self.layout)

        self.spectrum = pg.PlotWidget(title='SPECTRAL CONTENT', labels = {'left':('ENERGY'), 'bottom':('FREQUENCY','Hz')})
        self.layout.addWidget(self.spectrum)

        self.signal = pg.PlotWidget(title='WAVE')
        self.layout.addWidget(self.signal)

        threading.Thread(target=self.analyze).start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.plot_data)
        self.timer.start(50)

    def analyze(self):
        self.stream_rec.start_stream()
        self.stream_play.start_stream()

        for i in range(int(self.SAMPLING_RATE/self.CHUNK * self.DURATION)):
            raw_data = self.stream_rec.read(self.CHUNK)
            self.stream_play.write(raw_data)
            data = np.fromstring(raw_data, dtype=np.int16)
            channel_data = [[], []]
            for index, value in enumerate(data):
                channel_data[index%2].append(value)

            self.data = np.array(channel_data[0])


    def plot_data(self):
        self.spectrum.clear()
        self.signal.clear()
        T = self.CHUNK / self.SAMPLING_RATE
        k = np.arange(len(self.data))

        freq = (k / T)[:len(k) / 2]
        fft_y = np.fft.fft(self.data - np.mean(self.data))[:len(k) / 2]

        self.signal.plotItem.plot(self.data)
        self.spectrum.plotItem.plot(freq, np.absolute(fft_y))

    def run(self):
        self.mw.show()
        self.app.exec_()


class Application_From_File():

    def __init__(self):

        self.wf = wave.open('Utility_Belt/9.0 kHz (Sine Wave)_new.wav','rb')

        self.SAMPLING_RATE = self.wf.getframerate()
        self.SAMPLE_WIDTH = self.wf.getsampwidth()
        self.CHANNELS = self.wf.getnchannels()
        self.CHUNK = 1024

        self.p = pyaudio.PyAudio()

        self.stream_play = self.p.open(rate = self.SAMPLING_RATE,
                                       channels = self.CHANNELS,
                                       format = self.p.get_format_from_width(self.SAMPLE_WIDTH),
                                       output = True,
                                       start = False)

        self.data = np.zeros(self.CHUNK)

        self.app = QtGui.QApplication([])
        self.mw = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.mw.setLayout(self.layout)

        self.spectrum = pg.PlotWidget(title='SPECTRAL CONTENT', labels = {'left':('ENERGY'), 'bottom':('FREQUENCY','Hz')})
        self.layout.addWidget(self.spectrum)

        threading.Thread(target=self.analyze).start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.plot_data)
        self.timer.start(50)

    def analyze(self):
        self.stream_play.start_stream()

        raw_data = self.wf.readframes(self.CHUNK)
        while(len(raw_data)>0):
            self.stream_play.write(raw_data)
            data = np.fromstring(raw_data, dtype=eval(self.get_format(self.SAMPLE_WIDTH)))
            channel_data = [[] for i in range(self.CHANNELS)]
            for index, value in enumerate(data):
                channel_data[index%self.CHANNELS].append(value)

            self.data = np.array(channel_data[0])
            raw_data = self.wf.readframes(self.CHUNK)


    def plot_data(self):
        self.spectrum.clear()
        T = self.CHUNK / self.SAMPLING_RATE
        k = np.arange(len(self.data))

        freq = (k / T)[:len(k) / 2]
        fft_y = np.fft.fft(self.data - np.mean(self.data))[:len(k) / 2]

        self.spectrum.plotItem.plot(freq, np.absolute(fft_y))

    def get_format(self, x):
        if (x == 1):
            return 'np.uint8'
        else:
            return 'np.int16'

    def run(self):
        self.mw.show()
        self.app.exec_()



if __name__ == '__main__':
    app = Application_Real_Time()
    app.run()
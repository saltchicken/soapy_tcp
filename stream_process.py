import numpy as np
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import zmq
import time

NUM_RECV_FRAMES = 512 
# BUFFER_STRIDE = 100 

TCP_IP = '0.0.0.0' # Unused
TCP_PORT = 1234

def run_sdr(device, rate, center_freq, gain):

    args = dict(driver=device) 
    sdr = SoapySDR.Device(args) 

    sdr.setSampleRate(SOAPY_SDR_RX, 0, rate)
    sdr.setFrequency(SOAPY_SDR_RX, 0, center_freq)  
    sdr.setGain(SOAPY_SDR_RX, 0, gain)

    rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    sdr.activateStream(rx_stream)
    # buffer_samps = streamer.get_max_num_samps()
    # print(buffer_samps)
    recv_buffer = np.zeros(NUM_RECV_FRAMES, dtype=np.complex64)
    # samples = np.zeros(NUM_RECV_FRAMES * BUFFER_STRIDE, dtype=np.complex64)

    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://{}:{}".format(TCP_IP, TCP_PORT))

    SENT = 0
    try:
        while True:
            try:
                resp = socket.recv(flags=zmq.NOBLOCK)
                print(resp)
                break
            except zmq.Again as e:
                pass
            sr = sdr.readStream(rx_stream, [recv_buffer], len(recv_buffer))
            # samples[i * NUM_RECV_FRAMES : (i + 1) * NUM_RECV_FRAMES] = recv_buffer
            samples = recv_buffer
            socket.send(samples)
            SENT += 1
    except KeyboardInterrupt:
        print('Breaking out of loop')

    print('Done streaming')
    print('SENT ', SENT)
    sdr.deactivateStream(rx_stream)
    sdr.closeStream(rx_stream)
    print("Cleaned device")

if __name__ == "__main__":
    run_sdr('rtlsdr', 2e6, 105.7e6, 10)

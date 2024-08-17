import numpy as np
import serial
import time
import math
import os
import json
import requests
from threading import Thread
from time import sleep
import statistics
from BCSystems.overhead import TimeCode, Security,Email,Costing,DateCode,Greetings,StringThings
#from scipy.stats import linregress

#https://www.codeconvert.ai/vb.net-to-python-converter
# converts VB.NET to Python :)

def generate_x_axis(start_freq, stop_freq, points,resolution=1,inverted=False):
    temp_array = np.zeros(points)
    new_temp_array=[]
    step_size = (stop_freq - start_freq) / points
    if inverted:
        temp_array = np.round(stop_freq - (step_size * np.arange(points)), resolution)
    else:
        temp_array = np.round(start_freq + (step_size * np.arange(points)), resolution)
    
    for temp in temp_array:
        new_temp_array.append(temp)
    return new_temp_array


def get_com_ports():
    import serial.tools.list_ports
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    return com_ports

def extract_int_from_string(input_str):
    try:
        numbers = ''.join(c for c in input_str if c.isdigit())
        return int(numbers)
    except ValueError:
        return -1

def convert_string_to_bytes(input_str):
    return input_str.encode('utf-16')

def convert_bytes_to_string(input_bytes):
    return input_bytes.decode('utf-16')

def convert_hex_to_int(input_bytes):
    return int.from_bytes(input_bytes, byteorder='big')

def receive_serial_data(sp):
    try:
        return_str = ""
        incoming = ""
        while True:
            incoming = sp.read_until(expected=b'\n')
            if not incoming:
                break
            else:
                return_str += incoming.decode('utf-16') + '\n'
        if DEBUG:
            return_str = "Testing String"
    except serial.SerialTimeoutException:
        return_str = "Error: Serial Port read timed out."
    finally:
        if sp is not None:
            sp.close()
    return return_str

def send_serial_data(data, comport, baud_rate, data_bits, parity, stop_bits, debug=False, debug_string=""):
    try:
        sp = serial.Serial(comport)
        sp.baudrate = baud_rate
        sp.bytesize = data_bits
        if parity == "Even":
            sp.parity = serial.PARITY_EVEN
        elif parity == "Mark":
            sp.parity = serial.PARITY_MARK
        elif parity == "None":
            sp.parity = serial.PARITY_NONE
        elif parity == "Odd":
            sp.parity = serial.PARITY_ODD
        elif parity == "Space":
            sp.parity = serial.PARITY_SPACE
        if stop_bits == "None":
            sp.stopbits = serial.STOPBITS_NONE
        elif stop_bits == "One":
            sp.stopbits = serial.STOPBITS_ONE
        elif stop_bits == "OnePointFive":
            sp.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        elif stop_bits == "Two":
            sp.stopbits = serial.STOPBITS_TWO
        sp.timeout = 10
        sp.write(data.encode('utf-16'))
        time.sleep(0.1)
        if not debug:
            return_str = sp.read_all().decode('utf-16')
        else:
            return_str = debug_string
    except Exception as e:
        return_str = str(e)
    finally:
        if sp is not None:
            sp.close()
    return return_str


def get_computer_name():
    try:
        return os.getenv('USERNAME')
    except:
        return "Automated Test Solutions"

def check_network_folder(network_data_base_path):
    return os.path.exists(network_data_base_path)



def file_exists(path):
    return os.path.isfile(path)

def load_coeff_cal_to_file(file_name, buffer):
    with open(file_name, 'w') as f:
        f.write(buffer)

def read_coeff_cal_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def delay(delay_time):
    sleep(delay_time / 1000)  # Convert milliseconds to seconds

def api_requests():
    try:
        response = requests.get("http://inn-autocon:8888/report_queue/")
        print(response.status_code)
        print(response.text)
    except Exception as e:
        pass

def post_api():
    url = "http://inn-autocon:8888/report_queue/"
    json_string = json_serializer()
    json_data = json.dumps(json_string).encode('utf-8')
    send_request(url, json_data, "application/json", "POST")

def send_request(uri, json_data_bytes, content_type, method):
    try:
        response = requests.request(method, uri, data=json_data_bytes, headers={'Content-Type': content_type})
        return response.text
    except Exception as e:
        pass

def json_serializer():
    # Implement your JSON serialization logic here
    pass

def encode(string):
    return string.encode('utf-8')

def store_trace(my_ary, s_freq, st_freq):
    my_string = str(round(s_freq, 0)) + "," + str(round(st_freq, 0))
    for x in range(len(my_ary)):
        my_string += "," + str(round(my_ary[x], 2))
    return my_string

def string_trace(my_ary):
    my_string = ""
    for x in range(len(my_ary) - 1):
        my_string += str(round(my_ary[x], 2)) + ","
    my_string += str(round(my_ary[-1], 2))
    return my_string
    
def slope(x_array, y_array):
    #slope = np.polyfit(x_array, y_array, 1)[0]
    #print(f"Slope: {slope:.4f}")
    #slope, intercept, r_value, p_value, std_err = linregress(x_array, y_array)
    slope='N/A'    
    print('slope=',slope)
    return slope

def intercept(x_array, y_array):
    #slope, intercept, r_value, p_value, std_err = linregress(x_array, y_array)
    intercept='N/A'
    print('intercept=',intercept)
    return intercept
    
def truncate_decimal(value: float, precision: int) -> float:
    stepper = 10 ** precision
    tmp = math.trunc(stepper * value)
    return tmp / stepper

def mean(y_array):
    mean = statistics.mean(y_array) 
    return mean
   
def int_max(data_pts):
    for i in range(len(data_pts)):
        if i==0:
            int_max = data_pts[i]
        if data_pts[i] == 0:
            continue
        if data_pts[i] > int_max:
            int_max = data_pts[i]
    return int_max

def max(data_pts):
    
    for i in range(len(data_pts)):
        if i==0:
            int_max = data_pts[i]
        if data_pts[i] == 0:
            continue
        if data_pts[i] > int_max:
            int_max = data_pts[i]
    return int_max

def max_no_zero(data_pts):
    for i in range(len(data_pts)):
        if i==0:
            int_max = data_pts[i]
        if data_pts[i] == 0:
            continue
        if data_pts[i] > int_max:
            int_max = data_pts[i]
    return int_max
    
def min_no_zero(data_pts):
    int_min = None
    for i in range(len(data_pts)):
        if i==0:
            int_mi = data_pts[i]
        if data_pts[i] == 0:
            continue
        if int_min is None or data_pts[i] < int_min:
            int_min = data_pts[i]
    return int_min

def max_x(data_pts):
    int_max = None
    max_x = 0
    for i in range(len(data_pts)):
        if int_max is None or data_pts[i] > int_max:
            int_max = data_pts[i]
            max_x = i
    return max_x

def min_value(data_pts):
    int_min = None
    for i in range(len(data_pts)):
        if int_min is None or data_pts[i] < int_min:
            int_min = data_pts[i]
    return int_min

def min_x(data_pts):
    int_min = None
    min_x = 0
    for i in range(len(data_pts)):
        if int_min is None or data_pts[i] < int_min:
            int_min = data_pts[i]
            min_x = i
    return min_x

def log10(value):
    try:
        return math.log(value) / math.log(10)
    except:
        return None

def magnitude_from_real_imag(real_part, imag_part):
    return (imag_part ** 2 + real_part ** 2) ** 0.5

def vswr_to_rl(vswr):
    return 20 * log10((vswr - 1) / (vswr + 1))
    
def no_repeats(data, recent_data):
    for item in data:
        if recent_data in item:
            return False
    return True

def stringify_trace(trace):
    return " ".join(map(str, trace))

def expand_trace(trace):
    split_trace = trace.split(" ")
    thistrace = [float(x) for x in split_trace]
    return thistrace
    
def trim_y(y_array, offset=0):
    temp_array=[]
    if len(y_arry)==201:
        for data in y_array:
            temp_array.append(float(data) + offset)
    else: 
        for x in range(201):
            temp_array.append(float(y_array[x]) + offset)
    return temp_array
   
def trim_x(x_array, offset=0):
    temp_array=[]
    if len(x_arry)==201:
        for data in x_array:
            temp_array.append(float(data) + offset)
    else: 
        for x in range(201):
            temp_array.append(float(x_array[x]) + offset)
    return temp_array   
     


def FindGoldTraceDeltas(test, xArr, YArr, title,part_number):
        TempArray=[]
        get_golden_trace(title,part_number)
        for x in range(len(YArr)-1):
            TempArray.append(abs(YArr(x) - GoldenYArray(x)))
        if test == "Delta1":
            GoldentraceDelta1 = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta1H":
            GoldentraceDelta1H = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta1L":
            GoldentraceDelta1L = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta2":
            GoldentraceDelta2 = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta3":
            GoldentraceDelta3 = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta3L":
            GoldentraceDelta3L = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta3H":
            GoldentraceDelta3H = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta4":
            GoldentraceDelta4 = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta4L":
            GoldentraceDelta4L = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta4H":
            GoldentraceDelta4H = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta5":
            GoldentraceDelta5 = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta5H":
            GoldentraceDelta5H = truncate_decimal(MaxNoZero(TempArray), 2)
        elif test == "Delta5L":
            GoldentraceDelta5L = truncate_decimal(MaxNoZero(TempArray), 2)  
            
def get_golden_trace(title,part_number):            
    return TestData.objects.filter(jobnumber = 'Golden Part',part_number = part_number).last()
    
def int_from_str(string):
    return int(re.search(r'\d+', string).group())
    
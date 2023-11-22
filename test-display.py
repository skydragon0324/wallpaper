from PIL import Image, ImageDraw, ImageFont
import ctypes, struct, time, sys, os
import psutil, pynvml, cpuinfo
from helper import *
import threading

class WallpaperSys:
    def __init__(self, font_path, stop_flag, style):
        try:
            pynvml.nvmlInit()
            self.num_gpus = pynvml.nvmlDeviceGetCount() 
            self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        except:
            self.num_gpus = 0

        self.stop_flag = stop_flag
        self.prev_cpu = -90
        self.prev_ram = -90
        self.net_io = psutil.net_io_counters()
        # self.background = Image.open(image_path)
        if style == 1:
            self.background = Image.new(mode="RGB", size=(1920, 1080), color = "#0055ff")
        elif style == 2:
            tmp_image = Image.open('data/image/computer.jpg').resize((1920, 1080)).convert('RGBA')
            transparent_layer = Image.new('RGBA', (1920, 1080), (0, 0, 0, 200))
            self.background = Image.alpha_composite(tmp_image, transparent_layer)

        self.font_15 = ImageFont.truetype(font_path, size=15)
        self.font_20 = ImageFont.truetype(font_path, size=20)
        self.font_25 = ImageFont.truetype(font_path, size=25)
        self.font_40 = ImageFont.truetype(font_path, size=40)
        self.cf_font_60 = ImageFont.truetype('data/font/cf.ttf', size=60)
        self.draw = ImageDraw.Draw(self.background)
        self.image_width, self.image_height = self.background.size
        self.total_gpu = 0
        self.disk_usage_start = psutil.disk_io_counters()
        self.start_time = time.time()
        self.partitions = psutil.disk_partitions()
    def __del__(self):
        try:
            pynvml.nvmlShutdown()
        except:
            pass

    def draw_info(self, background):
        cpu_usage = psutil.cpu_percent()
        cpu_frequency = psutil.cpu_freq().current
        cpu_frequency_percent = round(cpu_frequency/psutil.cpu_freq().max * 100)
        ram_usage = psutil.virtual_memory().percent
        ram_total = str(round(psutil.virtual_memory().total/1024/1024/1024, 1)) + "GB"
        ram_used = str(round(psutil.virtual_memory().used/1024/1024/1024, 1)) + "GB"
        net_io_updated = psutil.net_io_counters()
        net_i = (net_io_updated.bytes_recv - self.net_io.bytes_recv)
        net_o = (net_io_updated.bytes_sent - self.net_io.bytes_sent)
        self.net_io = net_io_updated

        gpu_usage, gpu_temperature, gpu_frequency, gpu_frequency_percent = 0, 0, 0, 0
        if self.num_gpus != 0:
            gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(self.handle).gpu
            gpu_temperature = pynvml.nvmlDeviceGetTemperature(self.handle, pynvml.NVML_TEMPERATURE_GPU)
            gpu_frequency = pynvml.nvmlDeviceGetClockInfo(self.handle, pynvml.NVML_CLOCK_GRAPHICS)
            gpu_frequency_percent = round(gpu_frequency/pynvml.nvmlDeviceGetMaxClockInfo(self.handle, pynvml.NVML_CLOCK_GRAPHICS) * 100)
        # Create a new ImageDraw object
        self.draw = ImageDraw.Draw(background)
        
        #cpu
        cpu_end_angle = (cpu_usage / 100) * 360 - 90
        draw_ellipse(background, [300, 300, 480, 480], 2, "#60b8ff", 2)
        draw_arc(background, [300, 300, 480, 480], -90, cpu_end_angle, 4, '#0033ff', 3, 15)
        self.draw.text((320, 230), "CPU", fill='red', font=self.cf_font_60)
        drawTextCenter(self.draw, (390, 370), str(cpu_usage) + '%', "white", self.font_40)

        self.draw.line((530, 300, 860, 300), width=3, fill="#60b8ff")
        self.draw.line((530, 300, 530 + cpu_frequency_percent * 3.3, 300), width=3, fill="#2222ff")
        self.draw.text((530, 310), "Clock rate", fill="white", font=self.font_15)
        drawTextRight(self.draw, [860, 310], str(cpu_frequency) + "MHz", fill="white", font=self.font_15 )

        # cpu_info = cpuinfo.get_cpu_info()
        # print(cpu_info)

        # self.draw.line((530, 350, 860, 350), width=3, fill="#60b8ff")
        # self.draw.line((530, 350, 530 + cpu_frequency_percent * 3.3, 350), width=3, fill="#2222ff")
        # self.draw.text((530, 360), "Clock rate", fill="white", font=self.font_15)
        # drawTextRight(self.draw, [860, 360], str(cpu_frequency) + "MHz", fill="white", font=self.font_15 )

        # self.draw.line((530, 400, 860, 400), width=3, fill="#60b8ff")
        # self.draw.line((530, 400, 530 + 0 * 3.3, 400), width=3, fill="#2222ff")
        # self.draw.text((530, 410), "Fan speed", fill="white", font=self.font_15)
        # drawTextRight(self.draw, [860, 410], "0RPM", fill="white", font=self.font_15 )

        #ram
        ram_end_angle = (ram_usage / 100) * 360 - 90
        draw_ellipse(background, [1100, 300, 1280, 480], 2, "#60b8ff", 2)
        draw_arc(background, [1100, 300, 1280, 480], -90, ram_end_angle, 4, '#ebd777', 3, 15)
        self.draw.text((1110, 230), "RAM", fill='red', font=self.cf_font_60)
        # self.draw.text((1155, 420), "LOAD", fill='white', font=self.font_25)
        drawTextCenter(self.draw, (1190, 360), str(ram_usage) + '%', "white", self.font_40)
        self.draw.text((1140, 510), ram_used + "/" + ram_total, fill="white", font=self.font_15)

        #Network
        self.draw.text((1470, 260), "NETWORK", fill='red', font=self.cf_font_60)
        self.draw.text((1470, 310), "IN : " + str(round(net_i/1024)) + " Kb/s", fill='white', font=self.font_15)
        self.draw.line((1470, 350, 1670, 350), width=1, fill="#60b8ff")
        self.draw.text((1470, 370), "OUT : " + str(round(net_o/1024)) + " Kb/s", fill='white', font=self.font_15)

        #GPU
        gpu_end_angle = (gpu_usage / 100) * 360 - 90
        draw_ellipse(background, [300, 640, 480, 820], 2, "#60b8ff", 2)
        draw_arc(background, [300, 640, 480, 820], -90, gpu_end_angle, 4, '#4defff', 3, 15)
        self.draw.text((370, 600), "GPU", fill='red', font=self.cf_font_60)
        # self.draw.text((355, 760), "LOAD", fill='white', font=self.font_25)
        drawTextCenter(self.draw, (390, 710), str(gpu_usage) + '%', "white", self.font_40)

        self.draw.line((530, 640, 860, 640), width=3, fill="#60b8ff")
        self.draw.line((530, 640, 530 + gpu_temperature * 3.3, 640), width=3, fill="#2222ff")
        self.draw.text((530, 650), "Temperature", fill="white", font=self.font_15)
        drawTextRight(self.draw, [860, 650], str(gpu_temperature) + "°C", fill="white", font=self.font_15 )

        self.draw.line((530, 690, 860, 690), width=3, fill="#60b8ff")
        self.draw.line((530, 690, 530 + gpu_frequency_percent * 3.3, 690), width=3, fill="#2222ff")
        self.draw.text((530, 700), "Clock rate", fill="white", font=self.font_15)
        drawTextRight(self.draw, [860, 700], str(gpu_frequency) + "MHz", fill="white", font=self.font_15 )

        #Storage
        self.draw.text((1060, 600), "STORAGE", fill='red', font=self.cf_font_60)
        index = 0
        for partition in self.partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            self.draw.line((1060, 650 + index * 50, 1460, 650 + index * 50), width=3, fill="#60b8ff")
            self.draw.line((1060, 650 + index * 50, 1060 + usage.percent * 4, 650 + index * 50), width=3, fill="#ea0033")
            partition_total = str(round(usage.total/1024/1024/1024)) + "GB"
            partition_used = str(round(usage.used/1024/1024/1024)) + "GB"
            self.draw.text((1060, 660 + index * 50), partition.mountpoint[0] + ' :: ' + partition_used + " / " + partition_total, fill="white", font=self.font_15)
            drawTextRight(self.draw, [1460, 660 + index * 50], str(round(usage.percent))+ '%', "white", self.font_15)
            index = index + 1

        self.draw.line((250, 540, 860, 540), width=1, fill="#60b8ff")
        self.draw.line((1060, 540, 1670, 540), width=1, fill="#60b8ff")
        self.draw.line((250, 100, 1670, 100), width=1, fill="#60b8ff")
        

    def is_64bit_windows(self):
        """Check if 64 bit Windows OS"""
        return struct.calcsize('P') * 8 == 64

    def set_wallpaper(self, background):
        temp_file = os.path.dirname(os.path.abspath(sys.argv[0])) + r'\tmp\temp_wallpaper.png'
        background.save(temp_file, "PNG")

        if os.path.exists(temp_file):
            if self.is_64bit_windows():
                ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_file, 3)
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, temp_file, 3)

    def run(self):
        while not self.stop_flag.is_set():
            start = time.time()
            tmp_background = self.background.copy()
            self.draw_info(tmp_background)
            self.set_wallpaper(tmp_background)
            net_time = time.time() - start
            if(net_time > 1):
                time.sleep(0.1)
            else:
                time.sleep(1 - net_time)

def main():
    stop_flag = threading.Event()
    SysWallpaper = WallpaperSys( "data/font/font.ttf", stop_flag, 2)
    SysWallpaper.run()

if __name__ == "__main__":
    main()
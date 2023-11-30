from PIL import Image, ImageDraw, ImageFont
import ctypes, struct, time, os
import psutil, pynvml, cpuinfo
from helper import *
import threading


class   WallpaperSys:
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
        if style == 1:
            # self.background = Image.new(mode="RGB", size=(1920, 1080), color = "#0055ff")
            tmp_image = Image.new(mode="RGB", size=(1920, 1080), color = "#0055ff")
        elif style == 2:
            
            tmp_image = Image.open(getDataFilePath('data/image/computer.jpg')).resize((1920, 1080)).convert('RGBA')
            # transparent_layer = Image.new('RGBA', (1920, 1080), (0, 0, 0, 200))
            # self.background = Image.alpha_composite(tmp_image, transparent_layer)
        self.background = tmp_image


        # self.font_20 = ImageFont.truetype('data/font/sd.ttf', size=20)
        # self.font_40 = ImageFont.truetype('data/font/sd.ttf', size=40)
        self.font_20 = ImageFont.truetype(font_path, size=20)
        self.font_40 = ImageFont.truetype(font_path, size=45)
        self.cf_font_60 = ImageFont.truetype(getDataFilePath('data/font/cf.ttf'), size=60)
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
        cpu_info = cpuinfo.get_cpu_info()
        hz_actual = cpu_info['hz_actual'][0]
        count = cpu_info['count']
        cpu_total = round( hz_actual* count/1024/1024/1024,1)

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
            gpu_usage = 0
            try:
                gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(self.handle).gpu
                gpu_temperature = pynvml.nvmlDeviceGetTemperature(self.handle, pynvml.NVML_TEMPERATURE_GPU)
                gpu_frequency = pynvml.nvmlDeviceGetClockInfo(self.handle, pynvml.NVML_CLOCK_GRAPHICS)
                gpu_frequency_percent = round(gpu_frequency/pynvml.nvmlDeviceGetMaxClockInfo(self.handle, pynvml.NVML_CLOCK_GRAPHICS) * 100)
            except Exception as e:
                pass

        # Create a new ImageDraw object
        self.draw = ImageDraw.Draw(background)
        #cpu
        
        cpu_base_x = 200
        cpu_base_y = 150
        cpu_end_angle = (cpu_usage / 100) * 360 - 90
        draw_ellipse(background, [cpu_base_x, cpu_base_y + 100, cpu_base_x+ 180, cpu_base_y + 280], 2, "#60b8ff", 2)
        draw_arc(background, [cpu_base_x, cpu_base_y + 100, cpu_base_x + 180, cpu_base_y + 280], -90, cpu_end_angle, 4, calcColor(cpu_usage/100), 3, 15)
        drawTextCenter(self.draw, (cpu_base_x + 275, cpu_base_y), "CPU", '#00ff00', font=self.cf_font_60)
        drawTextCenter(self.draw, (cpu_base_x + 90, cpu_base_y + 170), str(cpu_usage) + '%', calcColor(cpu_usage/100), self.font_40)

        self.draw.line((cpu_base_x + 220, cpu_base_y + 150, cpu_base_x + 550, cpu_base_y + 150), width=3, fill="#60b8ff")
        self.draw.line((cpu_base_x + 220, cpu_base_y + 150, cpu_base_x + 220 + cpu_frequency_percent * 3.3, cpu_base_y + 150), width=3, fill=calcColor(cpu_frequency_percent/100))
        self.draw.text((cpu_base_x + 220, cpu_base_y + 160), "Clock rate", fill="#00ff00", font=self.font_20)
        drawTextRight(self.draw, [cpu_base_x + 550, cpu_base_y + 160], str(cpu_frequency) + "MHz", fill=calcColor(cpu_frequency_percent/100), font=self.font_20 )

        self.draw.line((cpu_base_x + 220, cpu_base_y + 200, cpu_base_x + 550, cpu_base_y + 200), width=3, fill="#60b8ff")
        self.draw.line((cpu_base_x + 220, cpu_base_y + 200, cpu_base_x + 220 + cpu_usage * 3.3, cpu_base_y + 200), width=3, fill=calcColor(cpu_usage/100))
        self.draw.text((cpu_base_x + 220, cpu_base_y + 210), "CPU Usage", fill="#00ff00", font=self.font_20)
        drawTextRight(self.draw, [cpu_base_x + 550, cpu_base_y + 210], str(round(float(cpu_total) * float(cpu_usage) /100,1)) + " / " + str(cpu_total) + "GHz", fill=calcColor(cpu_usage/100), font=self.font_20 )
        

        # self.draw.line((530, 350, 860, 350), width=3, fill="#60b8ff")
        # self.draw.line((530, 350, 530 + cpu_frequency_percent * 3.3, 350), width=3, fill="#2222ff")
        # self.draw.text((530, 360), "Clock rate", fill="#00ff00", font=self.font_20)
        # drawTextRight(self.draw, [860, 360], str(cpu_frequency) + "MHz", fill="#00ff00", font=self.font_20 )

        # self.draw.line((530, 400, 860, 400), width=3, fill="#60b8ff")
        # self.draw.line((530, 400, 530 + 0 * 3.3, 400), width=3, fill="#2222ff")
        # self.draw.text((530, 410), "Fan speed", fill="#00ff00", font=self.font_20)
        # drawTextRight(self.draw, [860, 410], "0RPM", fill="#00ff00", font=self.font_20 )

        #ram
        ram_base_x = 870
        ram_base_y = 150
        ram_end_angle = (ram_usage / 100) * 360 - 90
        draw_ellipse(background, [ram_base_x, ram_base_y + 100, ram_base_x + 180, ram_base_y + 280], 2, "#60b8ff", 2)
        draw_arc(background, [ram_base_x, ram_base_y + 100, ram_base_x + 180, ram_base_y + 280], -90, ram_end_angle, 4, '#ebd777', 3, 15)
        drawTextCenter(self.draw, (ram_base_x + 90, ram_base_y), "RAM", '#00ff00', font=self.cf_font_60)
        # self.draw.text((1155, 420), "LOAD", fill='#00ff00', font=self.font_35)
        drawTextCenter(self.draw, (ram_base_x + 90, ram_base_y + 170), str(ram_usage) + '%', calcColor(ram_usage/100), self.font_40)
        drawTextCenter(self.draw, (ram_base_x + 90, ram_base_y + 290), ram_used + "/" + ram_total, calcColor(ram_usage/100), font=self.font_20)

        #Network
        net_base_x = 1020
        net_base_y = 570
        self.draw.text((net_base_x, net_base_y), "NETWORK", fill='#00ff00', font=self.cf_font_60)
        self.draw.text((net_base_x, net_base_y + 80), "IN : " + str(round(net_i/1024)) + " Kb/s", fill='#00ff00', font=self.font_20)
        self.draw.line((net_base_x, net_base_y + 120, net_base_x + 200, net_base_y + 120), width=2, fill="#60b8ff")
        self.draw.text((net_base_x, net_base_y + 140), "OUT : " + str(round(net_o/1024)) + " Kb/s", fill='#00ff00', font=self.font_20)

        #GPU
        gpu_base_x = 1170
        gpu_base_y = 150
        gpu_end_angle = (gpu_usage / 100) * 360 - 90
        draw_ellipse(background, [gpu_base_x + 370, gpu_base_y + 100, gpu_base_x + 550, gpu_base_y + 280], 2, "#60b8ff", 2)
        draw_arc(background, [gpu_base_x + 370, gpu_base_y + 100,  gpu_base_x + 550, gpu_base_y + 280], -90, gpu_end_angle, 4,calcColor(gpu_usage/100), 3, 15)
        drawTextCenter(self.draw, (gpu_base_x + 275, gpu_base_y), "GPU", '#00ff00', font=self.cf_font_60)
        # self.draw.text((355, 760), "LOAD", fill='#00ff00', font=self.font_35)
        drawTextCenter(self.draw, (gpu_base_x + 460, gpu_base_y + 170), str(gpu_usage) + '%', calcColor(gpu_usage/100), self.font_40)

        self.draw.line((gpu_base_x, gpu_base_y + 150, gpu_base_x + 330, gpu_base_y + 150), width=3, fill="#60b8ff")
        self.draw.line((gpu_base_x, gpu_base_y + 150, gpu_base_x + gpu_temperature * 3.3, gpu_base_y + 150), width=3, fill=calcColor(gpu_temperature/100))
        self.draw.text((gpu_base_x, gpu_base_y + 160), "Temperature", fill="#00ff00", font=self.font_20)
        drawTextRight(self.draw, [gpu_base_x + 300, gpu_base_y + 160], str(gpu_temperature) + "°C", fill=calcColor(gpu_temperature/100), font=self.font_20 )

        self.draw.line((gpu_base_x, gpu_base_y + 200, gpu_base_x + 330, gpu_base_y + 200), width=3, fill="#60b8ff")
        self.draw.line((gpu_base_x, gpu_base_y + 200, gpu_base_x + gpu_frequency_percent * 3.3, gpu_base_y + 200), width=3, fill=calcColor(gpu_frequency_percent/100))
        self.draw.text((gpu_base_x, gpu_base_y + 210), "Clock rate", fill="#00ff00", font=self.font_20)
        drawTextRight(self.draw, [gpu_base_x + 300, gpu_base_y + 210], str(gpu_frequency) + "MHz", fill=calcColor(gpu_frequency_percent/100), font=self.font_20 )

        #Storage
        storage_base_x = 900
        storage_base_y = 570
        drawTextRight(self.draw, (storage_base_x, storage_base_y), "STORAGE", '#00ff00', font=self.cf_font_60)
        index = 0
        for partition in self.partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            self.draw.line((storage_base_x - 400, storage_base_y + 80 + index * 50, storage_base_x, storage_base_y + 80 + index * 50), width=3, fill="#60b8ff")
            self.draw.line((storage_base_x - 400, storage_base_y + 80 + index * 50, storage_base_x - 400 + usage.percent * 4, storage_base_y+ 80 + index * 50), width=3, fill=calcColor(usage.percent/100))
            partition_total = str(round(usage.total/1024/1024/1024)) + "GB"
            partition_used = str(round(usage.used/1024/1024/1024)) + "GB"
            self.draw.text((storage_base_x - 400, storage_base_y + 90 + index * 50), partition.mountpoint[0] + ' :: ' + partition_used + " / " + partition_total, fill="#00ff00", font=self.font_20)
            drawTextRight(self.draw, [storage_base_x, storage_base_y + 90 + index * 50], str(round(usage.percent))+ '%', calcColor(usage.percent/100), self.font_20)
            index = index + 1
        self.draw.line((820, 275, 820, 425), width=1, fill="#60b8ff")
        self.draw.line((1100, 275, 1100, 425), width=1, fill="#60b8ff")
        self.draw.line((960, 650, 960, 800), width=1, fill="#60b8ff")
        self.draw.line((660, 540, 1260, 540), width=1, fill="#60b8ff")
        # self.draw.line((250, 540, 860, 540), width=1, fill="#60b8ff")
        # self.draw.line((1060, 540, 1670, 540), width=1, fill="#60b8ff")
        # self.draw.line((250, 100, 1670, 100), width=1, fill="#60b8ff")

    def is_64bit_windows(self):
        """Check if 64 bit Windows OS"""
        return struct.calcsize('P') * 8 == 64

    def set_wallpaper(self, background):
        temp_file = getDataFilePath('tmp/temp_wallpaper')
        background.save(temp_file, "PNG")

        if os.path.exists(temp_file):
            if self.is_64bit_windows():
                ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_file, 3)
            else:
                ctypes.windll.user32.SystemParametersInfoA(20, 0, temp_file, 3)

    # save current background so If I close this program, backgroud is set by the preview image
    def get_current_background_path(self):
        SPI_GETDESKWALLPAPER = 0x73
        buffer_size = 260  # Maximum path length for a file in Windows
        path = ctypes.create_unicode_buffer(buffer_size)
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, buffer_size, path, 0)
        wallpaper_path = path.value
        return wallpaper_path
    
    def set_background(background):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, background, 3)
    def run(self):
        while not self.stop_flag.is_set():
            start = time.time()
            tmp_background = self.background.copy()
            self.draw_info(tmp_background)
            self.set_wallpaper(tmp_background)
            net_time = time.time() - start
            # time.sleep(0.1)
            # print(f"net_time: {net_time}")
            # if(net_time > 1):
            #     time.sleep(0.1)
            # else:
            #     time.sleep(0.1)

def main():
    stop_flag = threading.Event()
    SysWallpaper = WallpaperSys( getDataFilePath("data/font/font.ttf"), stop_flag, 0)
    SysWallpaper.run()

if __name__ == "__main__":
    main()
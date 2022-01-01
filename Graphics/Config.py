from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'multisamples', '0')
Config.set('kivy', 'window_icon', 'Assets/Media/downloader.png')



import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

app_version = "2.8.00"
total_downloads = 0
total_sizes = 100
total_speeds = 100
product_id = "ASDTR 12RGT 1WE45 DER90"
flavour = "win64"
last_update = "1/2/34"
release_date = "1/21/12"

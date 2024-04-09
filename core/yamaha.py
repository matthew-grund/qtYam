import time
import requests
import threading

class YamahaAmp():

    def __init__(self, ipaddress):
        self.ip_address = ipaddress
        self.base_url = f"http://{self.ip_address}/YamahaExtendedControl/v1/"
        self.art_url = f"http://{self.ip_address}"
        self.got_info = False
        self.got_features = False
        self.got_radio_faves = False
        self.got_net_status = False
        self.name = 'Unknown'


    def get_info(self):
        if not self.got_info:
            url = self.base_url + "system/getDeviceInfo"
            ret = requests.get(url)
            info = ret.json()
            self.device_info = info
            return info
        else:
            return self.device_info
        
    def get_ip_address(self):
        return self.ip_address    

    def get_features(self):
        if not self.got_features:
            url = self.base_url + "system/getFeatures"  
            ret = requests.get(url)
            features = ret.json()
            self.features = features
            return features
        else:
            return self.features


    def get_inputs(self):
        f = self.get_features()        
        inputs = f['system']['input_list']
        return inputs


    def get_net_radio_favorites(self):
        if not self.got_radio_faves:
            url = self.base_url + "netusb/getListInfo?input=net_radio"
            

    def get_network_status(self):
        if not self.got_net_status:
            url = self.base_url + "system/getNetworkStatus"
            ret = requests.get(url)
            net_status = ret.json()
            self.net_status = net_status
        else:
            net_status = self.net_status

        return net_status
    

    def get_status(self,zone='main'):
        url = self.base_url + f"{zone}/getStatus"
        ret=requests.get(url)
        status = ret.json() 
        return status
    
    def get_now_playing(self):
        url = self.base_url + "netusb/getPlayInfo"
        ret=requests.get(url)
        now_playing = ret.json() 
        return now_playing


    def set_mute(self,mute=True,zone='main'):
        url = self.base_url + f"{zone}/setMute"
        if mute:
            url += "?enable=true"
        else:
            url += "?enable=false"
        ret=requests.get(url)


    def set_power(self,on=True,zone='main'):
        url = self.base_url + f"{zone}/setPower"
        if on:
            url += "?power=on"
        else:
            url += "?power=standby"
        ret=requests.get(url)


    def set_play(self,play=True):
        url = self.base_url + "netusb/setPlayback"
        if play:
            url += "?playback=play"
        else:
            url += "?playback=pause"
        ret=requests.get(url)


    def set_skip(self,forward=True):
        url = self.base_url + "netusb/setPlayback"
        if forward:
            url += "?playback=next"
        else:
            url += "?playback=previous"
        ret=requests.get(url)


    def increment_volume(self, volume_change,zone='main'):
        stat = self.get_status(zone)
        vol0 = stat['volume']
        vol1 = vol0 + volume_change
        url = self.base_url + f"{zone}/setVolume?volume={vol1}"
        ret = requests.get(url)


    def set_volume(self, volume,zone='main'):
        url = self.base_url + f"{zone}/setVolume?volume={volume}"
        ret = requests.get(url)


    def get_volume_string(self):
        status=self.get_status()
        rawvol = status['volume']   
        str=f"Volume is raw[{rawvol}] actual: {status['actual_volume']['value']} {status['actual_volume']['unit']}."
        return str


    def get_volume(self):
        status=self.get_status()
        rawvol = status['volume']   
        return rawvol


    def get_volume_string_actual(self):
        status=self.get_status()
        str=f"{status['actual_volume']['value']} {status['actual_volume']['unit']}"        
        return str
    

if __name__ == '__main__':
    y = YamahaAmp("10.0.0.187") 
    ns=y.get_network_status()
    print(f"Unit has name: '{ns['network_name']}'.")
    print(f"Unit connection is: {ns['connection']}.")
    status = y.get_status()
    print(f"Unit is {status['power'].capitalize()}.")
    print(f"Unit volume is {status['actual_volume']['value']} {status['actual_volume']['unit']}.")
    print(f"Unit is muted: {status['mute']}.")
    info = y.get_info()
    print(f"Yamaha model name is {info['model_name']}.")  
    features = y.get_features()
    print(f"Unit has {features['system']['zone_num']} zones.")
    hdmi_count = 0
    av_count = 0
    analog_count = 0 
    netusb_count = 0
    has_airplay = False
    has_bluetooth = False
    has_net_radio = False
    inputs = y.get_inputs()
    for input in inputs:
        if 'hdmi' in input['id']:
            hdmi_count += 1
        elif 'av' in input['id']:
            av_count += 1
        elif  'audio' in input['id']:
            analog_count += 1
        elif 'airplay' == input['id']:
            has_airplay = True
        elif 'bluetooth' == input['id']:
            has_bluetooth = True           
        elif 'net_radio' == input['id']:
            has_net_radio = True   
        elif 'netusb' == input['play_info_type']:
            netusb_count += 1
        # else:
        #    print(input)    
    print(f"Unit has {hdmi_count} digital video inputs.")
    print(f"Unit has {av_count} analog video inputs.")    
    print(f"Unit has {analog_count} analog audio inputs.")
    print(f"Unit has {netusb_count} streaming inputs.")
    print(f"Unit has Network Radio radio: {has_net_radio}.")
    print(f"Unit has AirPlay:  {has_airplay}.")
    print(f"Unit has Bluetooth: {has_bluetooth}.")

    
    # test play/pause
    playing = y.get_now_playing()
    print(f"Now playing '{playing['track']}' by {playing['artist']}.")
    time.sleep(2.0)
    y.set_play(False) # pause
    print("Pause.")
    time.sleep(2.0)
    y.set_play(True) # play
    print("Play.")
    time.sleep(1.0)

    # test mute control
    y.set_mute(True)
    print("Mute On.")
    time.sleep(1.0)
    y.set_mute(False)
    print("Mute Off.")
    time.sleep(1.0)
    y.set_mute(True)
    print("Mute On.")    
    time.sleep(0.5)
    y.set_mute(False)
    print("Mute Off.")
    time.sleep(1.5)

    # test power control
    y.set_power(False)
    print("Power Off.")
    time.sleep(4.0)
    y.set_power(True)
    print("Power On.")
    time.sleep(4.0)
    
    # test skips
    playing = y.get_now_playing()
    print(f"Now playing '{playing['track']}' by {playing['artist']}.")

    print("Skipping forward.")
    y.set_skip()
    time .sleep(1.0)
    playing = y.get_now_playing()
    print(f"Now playing '{playing['track']}' by {playing['artist']}.")
    
    time.sleep(7.0)

    print("Skipping backward.")
    y.set_skip(False)
    time .sleep(1.0)
    playing = y.get_now_playing()
    print(f"Now playing '{playing['track']}' by {playing['artist']}.")

    time.sleep(0.7)

    print("Skipping backward.")
    y.set_skip(False)
    time .sleep(1.0)
    playing = y.get_now_playing()
    print(f"Now playing '{playing['track']}' by {playing['artist']}.")

    origvol = y.get_volume()
    print(y.get_volume_string())

    y.increment_volume(-12)
    print(y.get_volume_string_actual())
    time.sleep(6.0)

    y.increment_volume(-12)
    print(y.get_volume_string_actual())
    time.sleep(6.0)

    y.increment_volume(-12)
    print(y.get_volume_string_actual())
    time.sleep(6.0)

    y.set_volume(origvol)
    status=y.get_status()
    rawvol = status['volume']
    print(y.get_volume_string())
    

import time
import threading
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# получить все активные аудио-устройства
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# уровень громкости для сравнения
thresholdVolumeDb = -20.0  # значение, на которое нужно уменьшить громкость

# восстановление громкости
def restore_volume(original_volume):
    time.sleep(10)
    volume.SetMasterVolumeLevel(original_volume, None)

original_volume = volume.GetMasterVolumeLevel()

while True:
    current_volume = volume.GetMasterVolumeLevel()
    if current_volume > thresholdVolumeDb:
        volume.SetMasterVolumeLevel(thresholdVolumeDb, None)
        threading.Thread(target=restore_volume, args=(original_volume,)).start()
    time.sleep(0.1)  # задержкa
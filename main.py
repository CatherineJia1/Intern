import machine
import time
from mpr121 import MPR121

# Initialize I2C with custom pins for AtomS3 and reduced speed
i2c = machine.I2C(0, scl=machine.Pin(39), sda=machine.Pin(38), freq=50000)  # Speed set to 50kHz

# Initialize the MPR121 sensor with the correct I2C address (0x5A)
mpr = MPR121(i2c, address=0x5A)

# Set higher touch and release thresholds for less sensitivity
mpr.set_thresholds(touch=20, release=15)

# Timing parameters
time_window = 0.5  # Time window in seconds to consider simultaneous presses
last_touched_time = [0] * 12  # Last touched time for each pad

def main():
    while True:
        try:
            touched = mpr.touched()
            current_time = time.time()

            # Collect coordinates of currently touched pads
            touched_pads = []
            for i in range(12):
                if touched & (1 << i):
                    last_touched_time[i] = current_time
                    touched_pads.append(i)
            
            # Check for simultaneous touches within the time window
            valid_touches = []
            for i in touched_pads:
                for j in touched_pads:
                    if i != j and abs(last_touched_time[i] - last_touched_time[j]) <= time_window:
                        valid_touches.append(i)
                        valid_touches.append(j)
            
            valid_touches = list(set(valid_touches))  # Remove duplicates
            if valid_touches:
                valid_touches.sort()  # Sort for consistent output
                print(', '.join(map(str, valid_touches)))
            elif touched_pads and len(touched_pads) == 1:
                # If there's only one pad touched, print it
                print(touched_pads[0])

        except Exception as e:
            print(f'Error: {e}')
        
        time.sleep(0.1)  # Faster loop for more responsive touch detection

if __name__ == '__main__':
    main()
。 

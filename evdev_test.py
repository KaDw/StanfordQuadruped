from evdev import InputDevice, categorize, ecodes, list_devices

# gamepad = InputDevice(list_devices()[0])
# print(gamepad)

gamepad = InputDevice('/dev/input/event0')
print(gamepad)


ls = [0,0]
rs = [0,0]
dpad_x = 0
dpad_y = 0

try:
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                ls[0] = ((event.value - 32767.0) / 32768.0)
                print('ls0:{}'.format(ls[0]))
            elif event.code == ecodes.ABS_Y:
                ls[1] = ((event.value - 32767.0) / 32768.0)
                print('ls1:{}'.format(ls[1]))
            elif event.code == ecodes.ABS_Z:
                rs[0] = ((event.value - 32767.0) / 32768.0)
                print('rs0:{}'.format(rs[0]))
            elif event.code == ecodes.ABS_RZ:
                rs[1] = ((event.value - 32767.0) / 32768.0)
                print('rs1:{}'.format(rs[1]))
            elif event.code == 16:
                dpad_x = event.value
                print('dpad_x:{}'.format(dpad_x))
            elif event.code == 17:
                dpad_y = event.value
                print('dpad_x:{}'.format(dpad_y))
        elif event.type == ecodes.EV_KEY:
            if event.code == 308: # Code for Y
                print('Y')
            if event.code == 305: # Code for B
                print('B')
            if event.code == 304: # Code for A
                print('A')
            if event.code == 307: # Code for X
                print('X')
            elif event.code == 310: # Code for L1
                print('L1')
            elif event.code == 311: # Code for R1
                print('R1')
except:
    print("error:", sys.exc_info()[0])


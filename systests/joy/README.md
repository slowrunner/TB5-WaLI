# Logitech F710 Game Controller for TB5-WaLI

- Verify visible, Determine switch mode
```
ubuntu@TB5WaLI:~/TB5-WaLI/systests/joy$ lsusb
...
Bus 001 Device 004: ID 046d:c219 Logitech, Inc. F710 Gamepad [DirectInput Mode]  
or
Bus 001 Device 005: ID 046d:c21f Logitech, Inc. F710 Wireless Gamepad [XInput Mode]

...

```

- Install joystick test tools
```
sudo apt install joystick
```

- Test in XinputMode
```
buntu@TB5WaLI:~/TB5-WaLI/systests/joy$ jstest --normal /dev/input/js0
Driver version is 2.1.0.
Joystick (Logitech Gamepad F710) has 8 axes (X, Y, Z, Rx, Ry, Rz, Hat0X, Hat0Y)
and 11 buttons (BtnA, BtnB, BtnX, BtnY, BtnTL, BtnTR, BtnSelect, BtnStart, BtnMode, BtnThumbL, BtnThumbR).
Testing ... (interrupt to exit)
Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0  6:     0  7:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:off  9:off

PRESS LOGITECH BUTTON  (Button 8:on):
Axes:  0:     0  1:   518  2:-32767  3:     0  4:    -2  5:-32767  6:     0  7:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:on   9:off


```

### XinputMode:

Back  (6 - TB4-l2):  WallFollow Left
Start (7 - TB4-r2):  WallFollow Right

Logitech (8):  no action

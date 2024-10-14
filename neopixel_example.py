# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# 라즈베리 파이에서 NeoPixels을 테스트하는 간단한 예제
import time
import board
import neopixel

# NeoPixel 스트립의 Data In에 연결된 빈 핀을 선택합니다. 예를 들어, board.D18
# NeoPixels은 D10, D12, D18 또는 D21에 연결되어야 작동합니다.
pixel_pin = board.D18

# NeoPixels의 개수
num_pixels = 8

# 픽셀 색상의 순서 - RGB 또는 GRB. 일부 NeoPixels에는 빨간색과 녹색이 반대로 되어 있습니다!
# RGBW NeoPixels의 경우 ORDER를 RGBW 또는 GRBW로 변경합니다.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

rainbow_cycle(0.0001)  # 1ms 지연으로 무지개 순환
def wheel(pos):
    # 0에서 255 사이의 값을 입력하여 색상 값을 얻습니다.
    # 색상은 r - g - b - 다시 r로 전환됩니다.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


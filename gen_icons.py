#!/usr/bin/env python3
"""Generate simple PWA icons for Obsidian Clipper"""
import struct, zlib, base64

def make_png(size, bg=(13,13,15), fg=(124,106,255)):
    """Create a minimal PNG with a diamond/star mark"""
    pixels = []
    cx = cy = size // 2
    r_outer = size * 0.32
    r_inner = size * 0.13

    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x - cx, y - cy

            # Rounded rectangle background
            pad = size * 0.1
            in_rect = (pad <= x <= size - pad) and (pad <= y <= size - pad)
            # Corner rounding approximation
            for corner in [(pad,pad),(size-pad,pad),(pad,size-pad),(size-pad,size-pad)]:
                cdx, cdy = x - corner[0], y - corner[1]
                dist = (cdx**2 + cdy**2) ** 0.5
                if abs(x - corner[0]) < size*0.1 and abs(y - corner[1]) < size*0.1:
                    if dist > size * 0.1:
                        in_rect = False

            # Star / diamond shape
            angle_steps = 4
            import math
            in_star = False
            for i in range(angle_steps * 2):
                a1 = math.pi * i / angle_steps
                a2 = math.pi * (i+1) / angle_steps
                r1 = r_outer if i % 2 == 0 else r_inner
                r2 = r_outer if (i+1) % 2 == 0 else r_inner
                # point in triangle
                x1, y1 = r1 * math.cos(a1), r1 * math.sin(a1)
                x2, y2 = r2 * math.cos(a2), r2 * math.sin(a2)
                # cross product test
                d1 = (x2-x1)*(dy-y1) - (y2-y1)*(dx-x1)
                d2 = (0-x2)*(dy-y2) - (0-y2)*(dx-x2)
                d3 = (x1-0)*(dy-0) - (y1-0)*(dx-0)
                has_neg = (d1<0) or (d2<0) or (d3<0)
                has_pos = (d1>0) or (d2>0) or (d3>0)
                if not (has_neg and has_pos):
                    in_star = True
                    break

            if in_rect:
                if in_star:
                    row.extend([255, 255, 255, 255])
                else:
                    row.extend([fg[0], fg[1], fg[2], 255])
            else:
                row.extend([bg[0], bg[1], bg[2], 255])
        pixels.append(bytes(row))

    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    # RGBA -> use color type 6
    ihdr_data = struct.pack('>II', size, size) + bytes([8, 6, 0, 0, 0])

    raw = b''
    for row in pixels:
        raw += b'\x00' + row

    idat = zlib.compress(raw, 9)

    png = header
    png += chunk(b'IHDR', ihdr_data)
    png += chunk(b'IDAT', idat)
    png += chunk(b'IEND', b'')
    return png

if __name__ == '__main__':
    for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
        data = make_png(size)
        with open(name, 'wb') as f:
            f.write(data)
        print(f'Created {name} ({len(data)} bytes)')

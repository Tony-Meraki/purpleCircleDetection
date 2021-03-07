
import math


def get_circle(r, blur_factor=0.85):
    """
    Bresenham Algorithm
    :param r: radius int
    :return:
    """
    x = 0
    y = r
    p = 3-2*r
    circle_points = []
    dirs = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

    while x <= y:
        for yi in range(x, y+1):
            now_r = math.sqrt(x*x*1.0 + yi*yi)
            factor = 1.0 if now_r / r <= blur_factor else 1.0 - (now_r/r - blur_factor) / (1 - blur_factor)
            factor = min(1.0, factor)
            factor = max(0.0, factor)
            if factor > 1.0:
                print(x, yi, now_r)
            s = set()
            for dir in dirs:
                x_, y_ = x*dir[0], yi*dir[1]
                if (x_, y_) not in s:
                    circle_points.append([x_, y_, factor])
                    s.add((x_, y_))
            for dir in dirs:
                x_, y_ = yi*dir[0], x*dir[1]
                if (x_, y_) not in s:
                    circle_points.append([x_, y_, factor])
                    s.add((x_, y_))
        if p >= 0:
            p += 4*(x-y) + 10
            y -= 1
        else :
            p += 4*x + 6
        x += 1
    return circle_points


def make_color_palette(gradient_conf):
    ret = []
    now_color = (0, 0, 255)
    last_idx = 0
    for gradient in gradient_conf:
        pos_ratio, col = gradient
        pos = int(255 * pos_ratio)
        for idx in range(last_idx+1, pos+1):
            ratio_at_interval = 1.0 * (idx - last_idx) / (pos - last_idx)
            r = int(now_color[0] + (col[0] - now_color[0]) * ratio_at_interval)
            g = int(now_color[1] + (col[1] - now_color[1]) * ratio_at_interval)
            b = int(now_color[2] + (col[2] - now_color[2]) * ratio_at_interval)
            ret.append([r, g, b])
        now_color = col
        last_idx = pos
    return ret

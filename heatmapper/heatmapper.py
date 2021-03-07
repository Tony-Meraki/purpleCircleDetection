# -*- coding: utf-8 -*-

from . import utils
from PIL import Image
from PIL import ImageDraw


class HeatMapper(object):
    def __init__(self,
               radius=10,
               blur_factor=0.8,
               width=0,
               height=0,
                 gradient=None
               ):
        if gradient is None:
            gradient = [(0.3, (0, 0, 255)), (0.5, (0, 255, 0)), (0.8, (255, 255, 0)), (1.0, (255, 0, 0))]
        self.radius = radius
        self.blur_factor = blur_factor
        self.width = width
        self.height = height
        self.data = {}
        self.data_img = {}
        self.point_count = 0
        self.val_count = 0
        self.max_val = 0
        self.min_val = 0
        self.gradient = gradient

    def add_point(self, x, y, val=1):
        assert type(x) is int
        assert type(y) is int
        assert type(val) is int

        self.val_count += val
        if (x, y) not in self.data:
            self.data[(x, y)] = val
            self.point_count += 1
            self.max_val = max(self.max_val, val)
        else:
            self.data[(x, y)] += val
            self.max_val = max(self.max_val, self.data[(x, y)])

    def add_batch_points(self, data):
        assert type(data) in (tuple, list)
        for data_i in data:
            length = len(data_i)
            if length == 2:
                x, y, val = data_i[0], data_i[1], 1
            elif length == 3:
                x, y, val = data_i[0], data_i[1], data_i[2]
            else:
                raise Exception("invalid points length ! ")

            self.add_point(x, y, val)
            self.width = max(self.width, x)
            self.height = max(self.height, y)

    def get_data(self):
        return self.data

    def get_figure_size(self):
        return self.width, self.height

    def heatmap(self, save_path=None):
        circle_points = utils.get_circle(self.radius, self.blur_factor)
        for point in self.data.keys():
            x = point[0]
            y = point[1]
            val = self.data[point]
            global_alpha = 1.0 * (val - self.min_val) / (self.max_val - self.min_val)
            for ci in circle_points:
                dx, dy, alpha = ci
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    continue
                final_alpha = global_alpha * alpha
                last_alpha = 0.0
                if (nx, ny) in self.data_img:
                    last_alpha = self.data_img[(nx, ny)]
                # reference : https://en.wikipedia.org/wiki/Alpha_compositing
                self.data_img[(nx, ny)] = final_alpha + (1.0 - final_alpha) * last_alpha

        im = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        palette_list = utils.make_color_palette(self.gradient)
        for x, y in self.data_img.keys():
            alpha = self.data_img[(x, y)]
            alpha = min(254, int(alpha * 255))
            r, g, b = palette_list[alpha]
            im.putpixel((x, y), (r, g, b, alpha))

        if save_path is not None:
            im.save(save_path)
        return im

    def heatmap_with_palette(self, save_path=None, border_size=(100, 60), pos_origin=(30, 30), palette_size=(5, 100)):
        # get origin image
        im_origin = self.heatmap()

        palette_width, palette_height = palette_size
        im = Image.new("RGBA", (self.width+border_size[0], self.height+border_size[1]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.rectangle([(pos_origin[0]-1, pos_origin[1]-1), pos_origin[0]+self.width+1, pos_origin[1]+self.height+1],
                       outline='black')
        im.paste(im_origin, (pos_origin[0], pos_origin[1]))

        # draw coordinate axis
        for idx in range(0, self.width, 50):
            draw.line(( (idx+pos_origin[0], pos_origin[1] + self.height),
                        (idx+pos_origin[0], pos_origin[1] + self.height+5)),
                      fill='black')
            draw.text((idx+pos_origin[0]-5, pos_origin[1] + self.height+5), str(idx), fill='black')

        for idx in range(0, self.height, 50):
            draw.line(( (pos_origin[0], idx+pos_origin[1]),
                        (pos_origin[0]-5, idx+pos_origin[1])),
                      fill='black')
            w, h = draw.textsize(str(idx))
            draw.text((pos_origin[0]-w-5, idx+pos_origin[1]-5), str(idx), fill='black')

        # draw palette
        palette_im = self.__make_palette_img()
        palette_im = palette_im.resize((palette_width, palette_height), Image.ANTIALIAS)
        im.paste(palette_im, (pos_origin[0]+self.width+10, pos_origin[1]))
        # add 'min' and 'max' value
        draw.text((pos_origin[0] + self.width + palette_width + 15, pos_origin[1]), str(self.max_val), fill='black')
        draw.text((pos_origin[0] + self.width + palette_width + 15, pos_origin[1]+palette_height-5), str(0), fill='black')
        if save_path is not None:
            im.save(save_path)
        return im

    def __make_palette_img(self):
        palette_list = utils.make_color_palette(self.gradient)
        im = Image.new("RGBA", (10, 255), (255, 255, 255, 255))
        draw = ImageDraw.Draw(im)
        idx = 0
        for ci in palette_list:
            r, g, b = ci
            draw.line((0, 255-idx, 10, 255-idx), (r, g, b, 255))
            idx += 1
        return im

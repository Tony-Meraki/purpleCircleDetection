
from heatmapper.heatmapper import HeatMapper

if __name__ == '__main__':
    data = []
    with open('./example.data', 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            data.append([int(xi) for xi in line.strip().split(',')])
    mapper = HeatMapper(width=300, height=100, blur_factor=0.2, radius=10)
    mapper.add_batch_points(data)

    mapper.heatmap('./heatmap.png')
    mapper.heatmap_with_palette('./heatmap_with_palette.png')


import heatmapper


if __name__ == '__main__':
    heatmapper = heatmapper.HeatMapper(width=300, height=100, radius=10, blur_factor=0.01)
    heatmapper.add_batch_points([[1,2,2], [2,2,3], [21,2,55] ,[50, 50, 200], [45, 45, 8]])
    res = heatmapper.heatmap_with_palette(save_path='./b.png')
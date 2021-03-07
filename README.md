# HeatMapper

`HeatMapper` is Python library for creating heatmap. The logical realization refers to [heatmap.js](https://github.com/pa7/heatmap.js).

## Install 

### source code

```shell
git clone https://github.com/luckcul/heatmapper
cd heatmapper
python setup.py install
```

## Demo

We can get this demo from `example` folder.

```python
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

```
 the results of `heatmap` function :

![heatmap](https://user-images.githubusercontent.com/10364724/110246263-e9912d80-7fa1-11eb-8aa6-dae80d6fe148.png)

the results of `heatmap_with_palette` function:

![heatmap_with_palette](https://user-images.githubusercontent.com/10364724/110246281-ff9eee00-7fa1-11eb-980f-5ddfadadd5b4.png)

## Parameters
`HeatMapper.__init__` 

radius: The expansion radius of each point, the larger the value, the smoother the result

blur_factor: Blur factor, the smaller the value, the smoother the result

width: Width of the result

height: Height of the result

gradient: Parameters of palette color gradient. Default : ` [(0.3, (0, 0, 255)), (0.5, (0, 255, 0)), (0.8, (255, 255, 0)), (1.0, (255, 0, 0))]`
    



`HeatMapper.heatmap_with_palette`
save_path: Storage path

border_size： width and height of border.  Default:`(100, 60)`

pos_origin: postion of original heatmap (from left-top).  Default:`(30, 30)`

palette_size: width and height of palette. Default`(5, 100)`



## TODO
[] Add original picture as background
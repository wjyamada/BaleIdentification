Use the CreateFiles.ipynb to extract an dataset to train/validate/test

Train (need to download the pretrained weights)
	python3 train.py --cfg yolov3-spp.cfg --data data/bales.data --batch-size 1 --epochs 60


Detect

	python3 detect.py --names 'data/bales.names' --weights 'weights/bales.pt'


refer to https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data

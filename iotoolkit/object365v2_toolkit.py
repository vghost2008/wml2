from iotoolkit.coco_toolkit import *
import os.path as osp
from .o365_to_coco import *
from .coco_data_fwd import ID_TO_TEXT


def trans_file_name(filename,image_dir):
    names = filename.split("/")[-2:]
    return osp.join(*names)

def trans_label2coco(id):
    if id in o365_id_to_coco_id:
        return o365_id_to_coco_id[id]
    else:
        return None

class Object365V2(COCOData):
    def __init__(self,is_relative_coordinate=False,trans2coco=False,remove_crowd=True):
        super().__init__(is_relative_coordinate=is_relative_coordinate,remove_crowd=remove_crowd)
        if trans2coco:
            self.trans_label = trans_label2coco
        self.trans_file_name = trans_file_name
        if trans2coco:
            self.id2name = {}
            for k,info in ID_TO_TEXT.items():
                self.id2name[k] = info['name']

class TorchObject365V2(Object365V2):
    def __init__(self, img_dir, anno_path,trans2coco=False):
        super().__init__(is_relative_coordinate=False,trans2coco=trans2coco)
        super().read_data(anno_path, img_dir)

    def __getitem__(self, item):
        x = super().__getitem__(item)
        full_path, shape, category_ids, category_names, boxes, binary_mask, area, is_crowd, num_annotations_skipped = x
        try:
            img = wmli.imread(full_path)
        except Exception as e:
            print(f"Read {full_path} faild, error:{e}")
            img = np.zeros([shape[0],shape[1],3],dtype=np.uint8)
        img = Image.fromarray(img)
        res = []
        nr = len(category_ids)
        boxes = odb.npchangexyorder(boxes)
        boxes[..., 2:] = boxes[..., 2:] - boxes[..., :2]
        #new bboxes is [N,4], [x0,y0,w,h]
        for i in range(nr):
            item = {"bbox": boxes[i], "category_id": category_ids[i], "iscrowd": is_crowd[i],"area":area[i]}
            res.append(item)

        return img, res
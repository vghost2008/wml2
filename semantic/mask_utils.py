#coding=utf-8
import numpy as np
import logging
import img_utils as wmli
import cv2

def np_iou(mask0,mask1):
    if mask0.dtype is not np.bool:
        mask0 = mask0.astype(np.bool)
    if mask1.dtype is not np.bool:
        mask1 = mask1.astype(np.bool)

    if len(mask0.shape) != len(mask1.shape):
        logging.warning("Mask not compatible with each other")
        return 0.

    different = np.logical_xor(mask0,mask1)
    different = different.astype(np.float32)
    different = np.sum(different)

    union = np.logical_or(mask0,mask1)
    union = union.astype(np.float32)
    union = np.sum(union)
    #logging.info("union={}, different={}, mask={}, gt={}".format(union,different,np.sum(mask0.astype(np.float32)),np.sum(mask1.astype(np.float32))))

    if union == 0:
        return 100.0

    return 100.0-different*100.0/union

'''
mask:[H,W,NUM_CLASSES]
mask:[H,W]
'''
def np_mask2masklabels(mask,begin_label=1):
    res = np.zeros(mask.shape[:2],np.int32)
    h = mask.shape[0]
    w = mask.shape[1]
    num_classes = mask.shape[2]

    for i in range(h):
        for j in range(w):
            for k in range(num_classes):
                if mask[i,j,k]>0:
                    res[i,j] = k+begin_label
                    break

    return res

def resize_img_and_mask(img,mask,size,img_pad_value=127,mask_pad_value=255,pad_type=1):
    '''

    Args:
        img:
        mask:
        size: (w,h)
        img_pad_value:
        mask_pad_value:
        pad_type:

    Returns:

    '''
    img = np.array(img)
    mask = np.array(mask)
    img = wmli.resize_img(img, size, keep_aspect_ratio=True)
    mask = wmli.resize_img(mask, img.shape[:2][::-1], keep_aspect_ratio=False, interpolation=cv2.INTER_NEAREST)
    img, px0, px1, py0, py1 = wmli.pad_img(img, size, pad_value=img_pad_value, pad_type=pad_type, return_pad_value=True)
    mask = wmli.pad_imgv2(mask, px0, px1, py0, py1, pad_value=mask_pad_value)
    return img,mask


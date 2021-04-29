import argparse
import numpy as np
from pathlib import Path
import cv2
from model import get_model
from keras import backend as K
from noise_model import get_noise_model
import tensorflow as tf


def get_args():
    parser = argparse.ArgumentParser(description="Test trained model",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image_dir", type=str, required=True,
                        help="test image dir")
    parser.add_argument("--model", type=str, default="srresnet",
                        help="model architecture ('srresnet' or 'unet')")
    parser.add_argument("--weight_file", type=str, required=True,
                        help="trained weight file")
    parser.add_argument("--test_noise_model", type=str, default="gaussian,25,25",
                        help="noise model for test images")
    parser.add_argument("--output_dir", type=str, default=None,
                        help="if set, save resulting images otherwise show result using imshow")
    args = parser.parse_args()
    return args


def get_image(image):
    image = np.clip(image, 0.0, 255.0)
    return image.astype(dtype=np.uint8)

def tf_log10(x):
    numerator = tf.log(x)
    denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
    return numerator / denominator

def main():
    args = get_args()
    image_dir = args.image_dir
    weight_file = args.weight_file
    val_noise_model = get_noise_model(args.test_noise_model)
    model = get_model(args.model)
    model.load_weights(weight_file)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(Path(image_dir).glob("*.*"))
    PSNR=[]
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        h, w, _ = image.shape
        image = image[:(h // 16) * 16, :(w // 16) * 16]  # for stride (maximum 16)
        h, w, _ = image.shape

        out_image = np.zeros((h, w * 3, 3), dtype=np.uint8)
        noise_image = val_noise_model(image)
        pred = model.predict(np.expand_dims(noise_image, 0))
        denoised_image = get_image(pred[0])
        out_image[:, :w] = image
        out_image[:, w:w * 2] = noise_image
        out_image[:, w * 2:] = denoised_image
        max_pixel = 255.0   #changes from here
        denoised_image = np.clip(denoised_image, 0.0, 255.0)
        PSNR_test=10.0 * tf_log10((max_pixel ** 2) / (K.mean(K.square(denoised_image - noise_image))))
        print("PSNR value:",PSNR_test)
        with tf.Session() as sess_p:  
          PSNR.append(PSNR_test.eval())
          print(PSNR_test.eval())
        

        if args.output_dir:
            cv2.imwrite(str(output_dir.joinpath(image_path.name))[:-4] + ".png", out_image)
        else:
            cv2.imshow("result", out_image)
            key = cv2.waitKey(-1)
            # "q": quit
            if key == 113:
                return 0
    return PSNR
res=main()
print("Result:",res)

if __name__ == '__main__':
    main()

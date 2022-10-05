
#test_prediction =getPrediction('example.jpg')

from keras.preprocessing.image import load_img, img_to_array
from keras.models import Model, load_model
from skimage.io import imread, imshow
from skimage.transform import resize
import numpy as np
def get_pred(filepath):
  img = load_img(filepath)
  input = img_to_array(img)[:,:,1]
  X_test = np.zeros((1, 64, 64, 1), dtype=np.uint8)
  inputs = resize(input, (64, 64, 1), mode='constant', preserve_range=True)
  X_test[0] = inputs
  print(input.shape)
  model = load_model('segmentation')
  result = model.predict(X_test, verbose=1)
  result_t = (result > 0.5).astype(np.uint8)
  tmp = np.squeeze(result).astype(np.float32)
  res = np.dstack((tmp,tmp,tmp))
  return res
#   imshow(np.dstack((tmp,tmp,tmp)))
#   plt.show()

# res = get_pred("00a3af90ab.png")

# imshow(res)
# plt.savefig("result.png")

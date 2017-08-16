# Build a HDF5 dataset (only required once) from the google flower dataset using the tflearn api
from tflearn.data_utils import build_hdf5_image_dataset
build_hdf5_image_dataset('flower_photos', image_shape=(64, 64), mode='folder', output_path='dataset_test.h5', categorical_labels=True, normalize=True)


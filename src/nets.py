from keras.layers import Dropout, Input, Dense, Conv2D, Flatten, Reshape, Conv2DTranspose, BatchNormalization, Concatenate, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.engine.topology import InputSpec, Layer
from tensorflow.keras.initializers import VarianceScaling
import tensorflow as tf
K.set_image_data_format('channels_last')


# def autoencoder(input_shape=(128, 128, 1), act='relu'):
    
#     dims=[128*128, 8192, 512]
#     n_stacks = len(dims) - 1

#     init = VarianceScaling(scale=1. / 3., mode='fan_in', distribution='uniform')
    
#     input_img = Input(shape=input_shape, name='input')

#     h = Reshape((128*128,))(input_img)
#     # Encoder
#     for i in range(n_stacks-1):
#         h = Dense(dims[i + 1], activation=act, kernel_initializer=init, name='encoder_%d' % i)(h)

#     # hidden layer
#     h = Dense(dims[-1], kernel_initializer=init, name='encoder_%d' % (n_stacks - 1))(h)

#     y = h
#     # internal layers in decoder
#     for i in range(n_stacks-1, 0, -1):
#         y = Dense(dims[i], activation=act, kernel_initializer=init, name='decoder_%d' % i)(y)

#     # output
#     y = Dense(dims[0], kernel_initializer=init, name='decoder_0')(y)
#     y = Reshape((128, 128, 1))(y)

#     return Model(inputs=input_img, outputs=y, name='AE'), Model(inputs=input_img, outputs=h, name='encoder')


# def encoder(input_shape=(128, 128, 1), act='relu'):

#     dims=[128*128, 8192, 512]
#     n_stacks = len(dims) - 1

#     init = VarianceScaling(scale=1. / 3., mode='fan_in', distribution='uniform')
    
#     input_img = Input(shape=input_shape, name='input')

#     h = Reshape((128*128,))(input_img)
#     # Encoder
#     for i in range(n_stacks-1):
#         h = Dense(dims[i + 1], activation=act, kernel_initializer=init, name='encoder_%d' % i)(h)

#     # hidden layer
#     h = Dense(dims[-1], kernel_initializer=init, name='encoder_%d' % (n_stacks - 1))(h)

#     return Model(inputs=input_img, outputs=h, name='encoder')



def autoencoder(input_shape=(128, 128, 1), filters=[32, 64, 300]):

    input_img = Input(shape=input_shape)
    init = VarianceScaling(scale=1. / 3., mode='fan_in', distribution='uniform')

    # Encoder
    x = Conv2D(filters[0], 4, strides=2, padding='same', activation='relu', name='conv1', input_shape=input_shape, kernel_initializer=init)(input_img)
    x = Conv2D(filters[1], 4, strides=2, padding='same', activation='relu', name='conv2', kernel_initializer=init)(x)

    x = Flatten(name='flatten_1')(x)
    
    encoded = Dense(units=filters[-1], name='encoded', kernel_initializer=init)(x)

    # Decoder
    x = Dense(units=32*32*filters[1], activation='relu', kernel_initializer=init)(encoded)
    x = Reshape((32, 32, filters[1]))(x)
    x = Conv2DTranspose(filters[0], 4, strides=2, padding='same', activation='relu', name='deconv2', kernel_initializer=init)(x)
    decoded = Conv2DTranspose(1, 4, strides=2, padding='same', name='deconv1', kernel_initializer=init)(x)

    return Model(inputs=input_img, outputs=decoded, name='CAE')


def encoder(input_shape=(128, 128, 1), filters=[32, 64, 300]):

    input_img = Input(shape=input_shape)
    init = VarianceScaling(scale=1. / 3., mode='fan_in', distribution='uniform')

    # Encoder
    x = Conv2D(filters[0], 4, strides=2, padding='same', activation='relu', name='conv1', input_shape=input_shape, kernel_initializer=init)(input_img)
    x = Conv2D(filters[1], 4, strides=2, padding='same', activation='relu', name='conv2', kernel_initializer=init)(x)

    x = Flatten(name='flatten_1')(x)
    
    encoded = Dense(units=filters[-1], activation='relu', name='encoded', kernel_initializer=init)(x)

    return Model(inputs=input_img, outputs=encoded, name='CE')


if __name__ == "__main__":
    import pdb; pdb.set_trace()

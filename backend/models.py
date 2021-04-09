import json
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import datasets, layers, models, losses, Model

def create_baseline(num_classes, dropout_prob, regularizer_type, regularizer_value):
    """
    arguments:
    no. of classes
    dropout probability
    regularizer type
    regularizer value
    returns the baseline keras model instance
    """
    model = keras.models.Sequential([    
    keras.layers.Conv2D(filters=16, kernel_size=(3,3), activation='relu', input_shape=(48,48,3)),
    keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu'),
    keras.layers.MaxPool2D(pool_size=(2, 2)),
    keras.layers.BatchNormalization(axis=-1),
    
    keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu'),
    keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu'),
    keras.layers.MaxPool2D(pool_size=(2, 2)),
    keras.layers.BatchNormalization(axis=-1),
    
    keras.layers.Flatten(),
    ])

    if regularizer_type == 'L1':
        model.add(keras.layers.Dense(512, kernel_regularizer=keras.regularizers.L1(regularizer_value), activation='relu'))
    elif regularizer_type == 'L2':
        model.add(keras.layers.Dense(512, kernel_regularizer=keras.regularizers.L2(regularizer_value), activation='relu'))
    else:
        model.add(keras.layers.Dense(512, activation='relu'))
    
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(rate=dropout_prob))
    model.add(keras.layers.Dense(num_classes, activation='softmax'))
    return model

def create_mobilenet(num_classes, dropout_prob):
    """
    arguments:
    no. of classes
    dropout probability
    returns the mobilenet keras model instance
    """
    inp = keras.layers.Input(shape=(48, 48, 3))

    model = keras.applications.MobileNet(
    input_shape=None, alpha=1.0, depth_multiplier=1, dropout= dropout_prob,
    include_top=True, weights=None, input_tensor=inp, pooling='max',
    classes=num_classes, classifier_activation='softmax')

    return model


def create_resnet(num_classes, dropout_prob):
    """
    arguments:
    no. of classes
    dropout probability
    returns the resnet keras model instance
    """
    inp = keras.layers.Input(shape=(48, 48, 3))

    model = keras.applications.ResNet50(
    include_top=True, weights=None, input_tensor=inp,
    input_shape=None, pooling='max', classes=num_classes)
    
    return model

def create_googlenet(num_classes, dropout_prob):
    """
    arguments:
    no. of classes
    dropout probability
    returns the googlenet keras model instance
    """
    def inception(x,
              filters_1x1,
              filters_3x3_reduce,
              filters_3x3,
              filters_5x5_reduce,
              filters_5x5,
              filters_pool):

      path1 = layers.Conv2D(filters_1x1, (1, 1), padding='same', activation='relu')(x)

      path2 = layers.Conv2D(filters_3x3_reduce, (1, 1), padding='same', activation='relu')(x)
      path2 = layers.Conv2D(filters_3x3, (1, 1), padding='same', activation='relu')(path2)

      path3 = layers.Conv2D(filters_5x5_reduce, (1, 1), padding='same', activation='relu')(x)
      path3 = layers.Conv2D(filters_5x5, (1, 1), padding='same', activation='relu')(path3)

      path4 = layers.MaxPool2D((3, 3), strides=(1, 1), padding='same')(x)
      path4 = layers.Conv2D(filters_pool, (1, 1), padding='same', activation='relu')(path4)

      return tf.concat([path1, path2, path3, path4], axis=3)

    inp = layers.Input(shape=(48, 48, 3))
    input_tensor = layers.experimental.preprocessing.Resizing(224, 224, interpolation="bilinear", input_shape=(48,48,3))(inp)

    x = layers.Conv2D(64, 7, strides=2, padding='same', activation='relu')(input_tensor)
    x = layers.MaxPooling2D(3, strides=2)(x)

    x = layers.Conv2D(64, 1, strides=1, padding='same', activation='relu')(x)
    x = layers.Conv2D(192, 3, strides=1, padding='same', activation='relu')(x)

    x = layers.MaxPooling2D(3, strides=2)(x)

    x = inception(x,
                  filters_1x1=64,
                  filters_3x3_reduce=96,
                  filters_3x3=128,
                  filters_5x5_reduce=16,
                  filters_5x5=32,
                  filters_pool=32)

    x = inception(x,
                  filters_1x1=128,
                  filters_3x3_reduce=128,
                  filters_3x3=192,
                  filters_5x5_reduce=32,
                  filters_5x5=96,
                  filters_pool=64)

    x = layers.MaxPooling2D(3, strides=2)(x)

    x = inception(x,
                  filters_1x1=192,
                  filters_3x3_reduce=96,
                  filters_3x3=208,
                  filters_5x5_reduce=16,
                  filters_5x5=48,
                  filters_pool=64)

    aux1 = layers.AveragePooling2D((5, 5), strides=3)(x)
    aux1 = layers.Conv2D(128, 1, padding='same', activation='relu')(aux1)
    aux1 = layers.Flatten()(aux1)
    aux1 = layers.Dense(1024, activation='relu')(aux1)
    aux1 = layers.Dropout(0.7)(aux1)
    aux1 = layers.Dense(num_classes, activation='softmax')(aux1)

    x = inception(x,
                  filters_1x1=160,
                  filters_3x3_reduce=112,
                  filters_3x3=224,
                  filters_5x5_reduce=24,
                  filters_5x5=64,
                  filters_pool=64)

    x = inception(x,
                  filters_1x1=128,
                  filters_3x3_reduce=128,
                  filters_3x3=256,
                  filters_5x5_reduce=24,
                  filters_5x5=64,
                  filters_pool=64)

    x = inception(x,
                  filters_1x1=112,
                  filters_3x3_reduce=144,
                  filters_3x3=288,
                  filters_5x5_reduce=32,
                  filters_5x5=64,
                  filters_pool=64)

    aux2 = layers.AveragePooling2D((5, 5), strides=3)(x)
    aux2 = layers.Conv2D(128, 1, padding='same', activation='relu')(aux2)
    aux2 = layers.Flatten()(aux2)
    aux2 = layers.Dense(1024, activation='relu')(aux2)
    aux2 = layers.Dropout(0.7)(aux2)
    aux2 = layers.Dense(num_classes, activation='softmax')(aux2)

    x = inception(x,
                  filters_1x1=256,
                  filters_3x3_reduce=160,
                  filters_3x3=320,
                  filters_5x5_reduce=32,
                  filters_5x5=128,
                  filters_pool=128)

    x = layers.MaxPooling2D(3, strides=2)(x)

    x = inception(x,
                  filters_1x1=256,
                  filters_3x3_reduce=160,
                  filters_3x3=320,
                  filters_5x5_reduce=32,
                  filters_5x5=128,
                  filters_pool=128)

    x = inception(x,
                  filters_1x1=384,
                  filters_3x3_reduce=192,
                  filters_3x3=384,
                  filters_5x5_reduce=48,
                  filters_5x5=128,
                  filters_pool=128)

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dropout(dropout_prob)(x)
    out = layers.Dense(num_classes, activation='softmax')(x)

    model = Model(inputs = inp, outputs = [out, aux1, aux2])
    return model

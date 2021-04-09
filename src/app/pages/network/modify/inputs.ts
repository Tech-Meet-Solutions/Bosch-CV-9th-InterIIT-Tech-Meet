export const LeftHyperparamInputs = [
    {
        name : 'Learning Rate',
        property : 'lr',
        type : 'range',
        min : 1e-6,
        max : 1,
        placeholder : '1e-6 to 1',
    },
    {
        name : 'Decay Rate',
        property : 'decay_rate',
        type : 'range',
        min : 1e-8,
        max : 1e-4,
        placeholder : '1e-8 - 1e-4',
    },
    {
        name : 'Regularizer value',
        property : 'regularizer_value',
        type : 'range',
        min : 0,
        max : 10,
        placeholder : '0-10',
    },
    {
        name : 'Epochs',
        property : 'epochs',
        type : 'range',
        min : 0,
        max : 50,
        placeholder : '0-50',
    },
]
export const LossInputs = [
    {
        name : 'Loss',
        property : 'loss',
        type : 'dropdown',
        options : [
            {
                name : 'Categorical Cross Entropy',
                value : 'categorical_crossentropy',
            },
            {
                name : 'Kullback Leibler',
                value : 'kullback_leibler_divergence',
            },
        ]
    },
    {
        name : 'Optimizer',
        property : 'optimizer',
        type : 'dropdown',
        options : [
            {
                name : 'Adam',
                value : 'Adam',
            },
            {
                name : 'Adagrad',
                value : 'Adagrad',
            },
            {
                name : 'RMSprop',
                value : 'RMSprop',
            },
            {
                name : 'SGD',
                value : 'SGD',
            }
        ]
    },
    {
        name : 'Regularizer',
        property : 'regularizer_type',
        type : 'dropdown',
        options : [
            {
                name : 'L1',
                value : 'l1',
            },
            {
                name : 'L2',
                value : 'L2',
            },
        ]
    }
]

export const RightHyperparamInputs = [
    {
        name : 'Rotation',
        property : 'rotation_range',
        type : 'range',
        min : 0,
        max : 20,
        placeholder : 'Ex 10',
    },
    {
        name : 'Zoom',
        property : 'zoom_range',
        type : 'range',
        min : 0,
        max : 10,
        placeholder : 'Ex 0.1',
    },
    {
        name : 'Width shift',
        property : 'width_shift_range',
        type : 'range',
        min : 0,
        max : 10,
        placeholder : 'Ex 0.2',
    },
    {
        name : 'Height shift',
        property : 'height_shift_range',
        type : 'range',
        min : 0,
        max : 10,
        placeholder : 'Ex 0.1',
    },
    {
        name : 'Shear range',
        property : 'shear_range',
        type : 'range',
        min : 0,
        max : 10,
        placeholder : 'Ex 0.1',
    },
]
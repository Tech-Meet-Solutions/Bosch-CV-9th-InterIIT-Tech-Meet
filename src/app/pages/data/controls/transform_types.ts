export const transformTypes = [
    {
        name : 'Geometric',
        transforms : [
            {
                name : 'Translate',
                inputs : [
                    {
                        name : 'Horizontal',
                        property : 'translateX',
                        type : 'number',
                        min : -20,
                        max : 20,
                        step : 1,
                    },
                    {
                        name : 'Vertical',
                        property : 'translateY',
                        type : 'number',
                        min : -20,
                        max : 20,
                        step : 1,
                    },
                ]
            },
            {
                name : 'Rotate',
                property : 'rotate',
                type : 'number',
                min : -25,
                max : 25,
                step : 1,
            },
            {
                name : 'Flip',
                inputs : [
                    {
                        name : 'Vertical',
                        property : 'flipV',
                        type : 'bool',
                    },
                    {
                        name : 'Horizontal',
                        property : 'flipH',
                        type : 'bool',
                    }
                ]
            },
            {
                name : 'Shear',
                inputs : [
                    {
                        name : 'Vertical',
                        property : 'shearY',
                        type : 'number',
                        min : 0,
                        max : 1,
                        step : 0.1,
                    },
                    {
                        name : 'Horizontal',
                        property : 'shearX',
                        type : 'number',
                        min : 0,
                        max : 1,
                        step : 0.1,
                    }
                ]
            },
            {
                name : 'Padding',
                inputs : [
                    {
                        name : 'Horizontal',
                        property : 'padY',
                        type : 'number',
                        min : 0,
                        max : 20,
                        step : 1,
                    },
                    {
                        name : 'Vertical',
                        property : 'padX',
                        type : 'number',
                        min : 0,
                        max : 20,
                        step : 1,
                    }
                ]
            },
        ]
    },
    {
        name : 'Colorspace',
        transforms : [
            {
                name : 'Brightness',
                property : 'brightness',
                type : 'number',
                min : -20,
                max : 20,
                step : 1,
            },
            {
                name : 'Contrast',
                property : 'contrast',
                type : 'number',
                min : 0.5,
                max : 2,
                step : 0.1,

            },
            {
                name : 'Sharpen',
                property : 'sharpen',
                type : 'number',
                min : 0,
                max : 4,
                step : 0.1,
            },
            {
                name : 'Blur',
                property : 'blur',
                type : 'number',
                min : 1,
                max : 11,
                step :2,
            },
            {
                name : 'Gamma',
                property : 'gamma',
                type : 'number',
                min : 0.5,
                max : 2,
                step : 0.1,
            },
        ]
    },
    {
        name : 'Pixel',
        transforms : [
            {
                name : 'Clip',
                inputs :[
                    {
                        name : 'Min value',
                        property : 'clip_min',
                        type : 'number',
                        min : 0,
                        max :255,
                        step :1,
                    },
                    {
                        name : 'Max value',
                        property : 'clip_max',
                        type : 'number',
                        min : 0,
                        max :255,
                        step : 1,
                    }
                ]
            },
            {
                name : 'Gaussian Noise',
                property : 'noise',
                type : 'number',
                min : 0,
                max : 50,
                step :1 ,
            },
        ]
    },
    {
        name : 'Advanced',
        transforms : [
            {
                name : 'CLAHE',
                property : 'clahe',
                type : 'number',
                min : 1,
                max : 11,
                step : 1,
            },
            {
                name : 'Histogram Equalization',
                property : 'hist_eq',
                type : 'bool'
            },
            {
                name : 'Lens Distortion',
                property : 'lens_dis',
                type : 'bool'
            },
            
        ]
    }
]
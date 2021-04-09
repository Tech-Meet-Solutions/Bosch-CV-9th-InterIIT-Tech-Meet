
export interface Result  {
    "embd_imgs": [string],
    "loss": number,
    "optimizer": number,
    "regularization_type": string,
    "lr": string,
    "decay_rate": string,
    "regularization_value": string,
    "epochs": string,
    "best_worst": {
        class1: [string],
        class1_name: string,
        class2: [string],
        class2_name: string,
        class3: [string],
        class3_name: string,
        class4: [string],
        class4_name: string,
        class5: [string],
        class5_name: string,
        class6: [string],
        class6_name: string,
        class7: [string],
        class7_name: string,
        class8: [string],
        class8_name: string,
        class9: [string],
        class9_name: string,
        class0: [string],
        class0_name: string,
    },
    "conf_dim": number,
    "conf_matrix": [
        [number],
        [number],
        [number],
        [number],
        [number],
        [number],
        [number],
        [number],
        [number],
        [number]
    ]
}

export interface ResultName {
    net_name: string,
    result_name: string
}
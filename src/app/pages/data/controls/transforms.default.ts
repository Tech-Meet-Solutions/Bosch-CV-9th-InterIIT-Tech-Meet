import { Transforms } from "src/app/interfaces/transforms.interface";

export const defaults : Transforms = {
    translateX : 0,
    translateY : 0,
    rotate : 0,
    flipH : false,
    flipV : false,
    shearX : 0,
    shearY : 0,
    clip_min : 0,
    clip_max : 255,
    sharpen : 0,
    brightness : 0,
    contrast : 1,
    blur : 1,
    padX : 0,
    padY : 0,
    clahe : 1,
    lens_dis : false,
    hist_eq : false,
}
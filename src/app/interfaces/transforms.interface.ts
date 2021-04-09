import { NumberSymbol } from "@angular/common";

export interface Transforms{
    clip_max? : number;
    clip_min? : number;
    sharpen? : number;
    translateX? : number;
    translateY? : number;
    rotate? : number;
    brightness? : number;
    contrast? : number;
    flipV? : boolean;
    flipH? : boolean;
    shearX? : number;
    shearY? : number;
    blur? : number;
    noise? : number;
    padX? : number;
    padY? : number;
    gamma? : number;
    hist_eq? : boolean;
    clahe? : number;
    lens_dis? : boolean; 
    cropX? : number;
    cropY? : number;
    cropW? : number;
    cropH? : number;
}
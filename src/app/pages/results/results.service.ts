import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject, Subject } from "rxjs";
import { ResultName } from "./result.interface";

@Injectable()
export class ResultService {
    conf_url : string = "http://127.0.0.1:8000/api/conf_mat/";
    wr_url : string = "http://127.0.0.1:8000/api/getwrongresults/";
    lime_url : string = "http://127.0.0.1:8000/api/startgradcamlime/";
    result = new BehaviorSubject<ResultName>({net_name : undefined, result_name : undefined });

    resultChanged$ = this.result.asObservable();

    changeResult(result: ResultName) {
        this.result.next(result);
    }

    constructor(private http : HttpClient){
        
    }

    getConfMatrix(network,result){
        return this.http.get(this.conf_url,{
            params:{
                network : network,
                result : result 
            }
        })
    }

    getWrongResults(network,result,predClass,trueClass){
        return this.http.get(this.wr_url,{
            params : {
                net_name : network,
                result_name : result,
                corr_class : trueClass,
                pred_class : predClass,
            }
        })
    }

    startGradcamLime(network,result,corrClass,paths){
        return this.http.get(this.lime_url,{
            params :{
                model_name : network,
                corr_label :corrClass,
                result_name : result,
                paths : paths,
            }
        })
    }
}
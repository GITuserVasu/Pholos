import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RoleService {

  constructor(private http:HttpClient) { }


  createRole(data:any){
    return this.http.post(environment.apiUrl+"/createRole", data).pipe(catchError(this.handleError))
  }

  getRole(id:number){
    return this.http.get(environment.apiUrl+"/getRole/"+id).pipe(catchError(this.handleError));
  }
  getIdwiseData(id:number){
    return this.http.get(environment.apiUrl+"/getIdwise/"+id).pipe(catchError(this.handleError));
  }

  update(id:number, data:any){
    return this.http.put(environment.apiUrl+"/update/"+id, data).pipe(catchError(this.handleError));
  }

  
  handleError(error: HttpErrorResponse) {
    let msg = '';
    if (error.error instanceof ErrorEvent) {
      // client-side error
      msg = error.error.message;
      console.log(msg);
    } else {
      // server-side error
      msg = `Error Code: ${error.status}\nMessage: ${error.message}`;
      console.log(msg);
    }
    return throwError(msg);
  }
}

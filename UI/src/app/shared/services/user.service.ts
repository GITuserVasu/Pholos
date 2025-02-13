import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http:HttpClient) { }


  createUser(data:any){
    return this.http.post(environment.apiUrl+"/createUser", data).pipe(catchError(this.handleError))
  }

  getUser(orgid:number){
    return this.http.get(environment.apiUrl+"/getUsers/"+orgid).pipe(catchError(this.handleError));
  }

  getIdwiseUsers(id:number){
    return this.http.get(environment.apiUrl+"/getIdwiseUsers/"+id).pipe(catchError(this.handleError));
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

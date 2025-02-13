import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../../../src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private http: HttpClient) { }

  validateUser(data: any) {
    let username = data.username;
    let password = data.password;
    const body = {
      "username": username.trim(),
      "password": password
    }//http://192.168.1.23:8085/validationUser/
    return this.http.post(environment.apiUrl+"/validationUser/", body).pipe(catchError(this.handleError));
  //  return this.http.post("https://ezaitool.com:8888"+"/validationUser/", body).pipe(catchError(this.handleError));
  }

  handleError(error:  HttpErrorResponse) {
    let msg = '';
    if (error.error instanceof ErrorEvent) {
      // client-side error
      msg = error.error.message;

    } else {
      // server-side error
      msg = `Error Code: ${error.status}\nMessage: ${error.message}`;

    }
    return throwError(msg);
  }

}



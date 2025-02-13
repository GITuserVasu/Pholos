import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LogininfoService {
  accessToken: string = "";

  constructor(private http:HttpClient) { }
  registration(data:any){
    return this.http.post(environment.apiUrl+"Registration", data).pipe(catchError(this.handleError));
  }
  getregistration(){
    return this.http.get(environment.apiUrl+"Registration").pipe(catchError(this.handleError));
  }
  login(data:any){
    return this.http.post(environment.apiUrl+"login", data).pipe(catchError(this.handleError));
  }
  emplogin(data:any){
    return this.http.post(environment.apiUrl+"emplogin", data).pipe(catchError(this.handleError));
  }
  pdfinfocount(data:any){
    return this.http.post(environment.apiUrl+"pdfInfo_details", data).pipe(catchError(this.handleError));
  }
  empregistration(data:any){
    return this.http.post(environment.apiUrl+"empRegistration", data).pipe(catchError(this.handleError));
  }
  empgetregistration(){
    return this.http.get(environment.apiUrl+"empRegistration").pipe(catchError(this.handleError));
  }
  orgDetials(orgid:any){
    return this.http.get(environment.apiUrl+"orgDetilas/"+orgid).pipe(catchError(this.handleError));
  }
  emailActivate(data:any){
    return this.http.post(environment.apiUrl+"emailActivate", data).pipe(catchError(this.handleError));
  }
  empStatusUpdate(id:any,data:any){
    return this.http.put(environment.apiUrl+"empStatusUpdate/"+id, data).pipe(catchError(this.handleError));
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

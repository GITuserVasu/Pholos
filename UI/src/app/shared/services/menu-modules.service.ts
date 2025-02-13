import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class MenuModulesService {

  constructor(private http:HttpClient) { }
  
  public getModules():any{
    return this.http.get(environment.apiUrl+"/getmodules/").pipe(catchError(this.handleError));
  }
  

  createMenu(data:any){
    return this.http.post(environment.apiUrl+"/createMenu/",data).pipe(catchError(this.handleError));
  }


  //Sub Menu Serivce

  createSubMenu(data:any){
    return this.http.post(environment.apiUrl+"/createSubMenu/",data).pipe(catchError(this.handleError));
  }
  getSubmenu(){
    return this.http.get(environment.apiUrl+"/getSubMenu/").pipe(catchError(this.handleError));
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

import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class OrganizationService {

  constructor(private http:HttpClient) { }


  sendData(data:any){
    return this.http.post(environment.apiUrl+"/createorganization/", data).pipe(catchError(this.handleError));
  }
  getData(){
    return this.http.get(environment.apiUrl+"/orgList/").pipe(catchError(this.handleError));
  }
  getIdByData(id:any){
    return this.http.get(environment.apiUrl+"/createorganization/"+id).pipe(catchError(this.handleError));
  }
  updateData(id:any, data:any){
    return this.http.put(environment.apiUrl+"/updateorganization/"+id, data).pipe(catchError(this.handleError));
  }
  getOrgidwiseData(id:any){
    return this.http.get(environment.apiUrl+"/getOrglist/"+id).pipe(catchError(this.handleError));
  }

  sendEmail(data:any){
    return this.http.post(environment.apiUrl+"/email",data).pipe(catchError(this.handleError));
  }

  resetPassword(email:any, data:any){
    return this.http.put(environment.apiUrl+"PasswordChange/"+email,data).pipe(catchError(this.handleError));
  }

  fotgotPassword(data:any){
  //  return this.http.post(environment.apiUrl+"/forgotemail",data).pipe(catchError(this.handleError));
    return this.http.post(environment.apiUrl+"email",data).pipe(catchError(this.handleError));
  }

  asyncioTextract(data:any){
    return this.http.post(environment.apiUrl+"/asyncioTextract/", data).pipe(catchError(this.handleError));
  }
  get_textract_results(data:any){
    return this.http.post(environment.apiUrl+"/get_textract_results/", data).pipe(catchError(this.handleError));
  }
  
  packageUpdate(email:any, data:any){
    return this.http.put(environment.apiUrl+"packageUpdate/"+email,data).pipe(catchError(this.handleError));
  }
  empStatusUpdate(id:any, data:any){
    return this.http.put(environment.apiUrl+"empStatusUpdate/"+id,data).pipe(catchError(this.handleError));
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

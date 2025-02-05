import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../../../src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DepartmentService {

  constructor(private http:HttpClient) { }


  createDepartment(data:any){
    return this.http.post(environment.apiUrl+"/departmentCreate",data).pipe(catchError(this.handleError));
  }
  getDepartment(org_id:any){
    return this.http.get(environment.apiUrl+"/departmentList/"+org_id).pipe(catchError(this.handleError))
  }

  getDepartmentIdWise(id:number){
    
    return this.http.get(environment.apiUrl+"/departmentIdwise/"+id).pipe(catchError(this.handleError))
  }

  updateDepartment(id:number, data:any){
    return this.http.put(environment.apiUrl+"/updateIdwise/"+id, data).pipe(catchError(this.handleError))
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

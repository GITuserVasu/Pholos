import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private Router:Router) { 

  }

  canActivate(): boolean {
    if(window.localStorage.getItem('username')){
      return true;
    }else{
      return false;
    }
  }

  logOut(){
    // window.localStorage.removeItem('username');
    // window.localStorage.removeItem('role');
    // window.localStorage.removeItem('theme');
    // window.localStorage.removeItem('usermenu');
    // window.localStorage.removeItem('userInfo');
    // window.localStorage.removeItem('organization_id');
    // window.localStorage.removeItem('business_unit_value');
    localStorage.clear();
    this.Router.navigate(['/login']);
    return true;
  }

  isLoggedIn(){
    if(window.localStorage.getItem('username')){
      return true;
    }
    return false;
  }


  
}

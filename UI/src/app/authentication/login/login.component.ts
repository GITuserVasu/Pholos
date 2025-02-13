import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common' ;
//import { FormGroup, ReactiveFormsModule } from '@angular/forms' ;
import { ReactiveFormsModule } from '@angular/forms' ;
import { FormGroup, FormControl } from '@angular/forms' ;
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from '../../../../src/app/shared/services/login/login.service';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';

@Component({
    selector: 'app-login',
    imports: [ CommonModule, ReactiveFormsModule ] ,
//    imports: [ReactiveFormsModule ] ,
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css'],
//    standalone: true
})
export class LoginComponent implements OnInit {
  //loginForm: FormGroup;
  loginData: UntypedFormGroup;
  password:any;

  show = false; 

  constructor(private fb: UntypedFormBuilder, private _loginServices: LoginService, private router: Router, private LoginInfo: LogininfoService, private toaster: NotificationService, private loginService: LogininfoService, private activateRouter:ActivatedRoute) {
    //this.loginData = this.fb.group({
    this.loginData = new UntypedFormGroup({
      email: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    //  email: ['', Validators.required],
    //  password: ['', Validators.required],
      // phone:['', Validators.required],
    })
  }

  ngOnInit(): void {
    this.password = 'password';
    this.activateRouter.params.subscribe((res:any) => {
      if(res){
        console.log("res",res.id)
        var data = {
          "status":res.status == 'Approve'?"Active":"Inactive"
        }
          this.loginService.empStatusUpdate(res.id,data).subscribe((res:any) => {
            if(res.errorCode == 200){
              this.toaster.showSuccess("Success", "Successfully Activated Thank you");
              this.router.navigate(['/']);
            }
            
          })
      }
      
    })
    
  }
  onSubmit() {
    //alert(this.loginData.controls['username'].value);
    //alert(this.loginData.controls['password'].value);
    console.log("login form", this.loginData.value);
    // return;
    // let data = {
    //   username: 'admin',
    //   password: 'admin'
    // }
    this.loginService.login(this.loginData.value).subscribe((res: any) => {
     
      if(res.errorCode == 200){
        console.log("result", res);
        localStorage.setItem('role', "admin");
        localStorage.setItem('org_id', res.response[0].orgid);
        localStorage.setItem('empOrgid', '');
        localStorage.setItem('info', JSON.stringify(res.response[0]));
        localStorage.setItem('username', res.response[0].email);
        this.toaster.showSuccess("Success", "Successfull Login");
        this.router.navigate(['/']);
      }else{
        this.toaster.showError("Error", "Enter Valid Details!");
      }



    })
    

    // console.log("data", data);
    // if(this.loginData.value.username == 'admin' && this.loginData.value.password == 'admin@123'){

    //   localStorage.setItem('username', this.loginData.value.username);
    //   localStorage.setItem('role', "admin");
    //   localStorage.setItem('org_id', "0");
    //   this.router.navigate(['/']);
    // }else{

    //   this.toaster.showError("Error", "Enter Valid Detials!");
    // }

    // if () {
    //   let userInfo = res.data[0];
    //   console.log("userInfo", userInfo);
    //   localStorage.setItem('username', userInfo.username);
    //   if (userInfo.org_id === '0') {
    //     localStorage.setItem('role', "admin");
    //     localStorage.setItem('org_id', "0");
    //   }
    //   else {
    //     this.LoginInfo.accessToken = 'user';
    //     localStorage.setItem('role', JSON.stringify("user"));
    //     //localStorage.setItem('userData',JSON.stringify(res.data));
    //     localStorage.setItem('org_id', userInfo.org_id);
    //   }
    //   this.router.navigate(['/']);
    // }else{
    //   this.toaster.showError("Error", "Enter Valid Detials!");
    // }

    // this._loginServices.validateUser(data).subscribe((res: any) => {
    //     console.log("res Testing",res.data[0]);
    //   if (res.statusCode == 200) {
    //     let userInfo = res.data[0];
    //     console.log("userInfo", userInfo);
    //     localStorage.setItem('username', userInfo.username);
    //     if (userInfo.org_id === '0') {
    //       localStorage.setItem('role', "admin");
    //       localStorage.setItem('org_id', "0");
    //     }
    //     else {
    //       this.LoginInfo.accessToken = 'user';
    //       localStorage.setItem('role', JSON.stringify("user"));
    //       //localStorage.setItem('userData',JSON.stringify(res.data));
    //       localStorage.setItem('org_id', userInfo.org_id);
    //     }
    //     this.router.navigate(['/']);
    //   }else{
    //     this.toaster.showError("Error", "Enter Valid Detials!");
    //   }
    // });
  }
  onClick() {
    if (this.password === 'password') {
      this.password = 'text';
      this.show = true;
    } else {
      this.password = 'password';
      this.show = false;
    }
  }
  redirectUrl(value:any){
    // alert("Success" + value)
    if(value == 'Company'){
      this.router.navigate(['login/registrationPage'])
      // window.location.reload()
    }else{
      this.router.navigate(['/empRegistration'])
    }
  }
  loginRedirectUrl(value:any){
    // alert("Success" + value)
    if(value == 'Company'){
      this.router.navigate(['login'])
      // window.location.reload()
    }else{
      this.router.navigate(['login/employee'])
    }
  }
}

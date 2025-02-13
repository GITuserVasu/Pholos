import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginService } from '../../../../src/app/shared/services/login/login.service';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-employee-login',
    templateUrl: './employee-login.component.html',
    styleUrls: ['./employee-login.component.css'],
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule] 
})
export class EmployeeLoginComponent implements OnInit {
 //loginForm: FormGroup;
 loginData: UntypedFormGroup;
 password:any;

 show = false; 

 constructor(private fb: UntypedFormBuilder, private _loginServices: LoginService, private router: Router, private LoginInfo: LogininfoService, private toaster: NotificationService, private loginService: LogininfoService) {
   this.loginData = this.fb.group({
     email: ['', Validators.required],
     password: ['', Validators.required],
     // phone:['', Validators.required],
   })
 }

 ngOnInit(): void {
   this.password = 'password';
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
   this.loginService.emplogin(this.loginData.value).subscribe((res: any) => {
    
     if(res.errorCode == 200){
       console.log("result", res);
       localStorage.setItem('role', "admin");
       localStorage.setItem('org_id', res.response[0].orgid);
       localStorage.setItem('info', JSON.stringify(res.response[0]));
       localStorage.setItem('username', res.response[0].email);
       localStorage.setItem('empOrgid', res.response[0].empOrgid);
       this.toaster.showSuccess("Success", "Successfull Login");
       this.router.navigate(['/']);
     }else{
      if(res.response =="Account Not Activated"){
        this.toaster.showError("Thank you !", "Your Account is not Activated Please contact your organization ");
      }else{
        this.toaster.showError("Error", "Enter Valid Detials!");
      }
      
     }



   })
   
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
   alert("Success" + value)
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

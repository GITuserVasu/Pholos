import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner';
import { finalize } from 'rxjs/operators';
import { LoginService } from '../../../../src/app/shared/services/login/login.service';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { OrganizationService } from '../../../../src/app/shared/services/organization.service';
import {CommonModule} from '@angular/common' ;
import {ReactiveFormsModule} from '@angular/forms' ;

@Component({
    selector: 'app-forgot-password',
    imports: [CommonModule, ReactiveFormsModule, NgxSpinnerModule ],
    templateUrl: './forgot-password.component.html',
    styleUrls: ['./forgot-password.component.css'],
    standalone: true
})
export class ForgotPasswordComponent implements OnInit {
  forgotPassword:UntypedFormGroup;
  submitted:boolean = false;
  Msg:any;
  emailIdNo:any = [];
  constructor(private fb:UntypedFormBuilder, private orgService:OrganizationService, private toastr:NotificationService, private router:Router,private spinner: NgxSpinnerService, private logininfo:LogininfoService) { 
    this.forgotPassword = this.fb.group({
    //  username:['', Validators.required],
      email:['', Validators.required],
    })
  }


  get form(){
    return this.forgotPassword.controls;
  }
  ngOnInit(): void {
  }

  onSubmit(){
    //alert(this.forgotPassword.controls['email'].value)
    // this.spinner.show();

    this.logininfo.getregistration().subscribe((res:any) => {

      res.response.map((item:any) => {
        if(this.forgotPassword.controls['email'].value == item.email){
          this.emailIdNo.push(item.id)
        }
      })
      console.log("this.emailIdNo",this.emailIdNo[0])
 

  if(this.emailIdNo[0] != null || this.emailIdNo[0] != undefined){
    this.orgService.fotgotPassword(this.forgotPassword.value).pipe(finalize(() => {
      //this.orgService.fotgotPassword(this.forgotPassword.value).pipe(finalize(() => {
        this.spinner.hide();
        this.toastr.showSuccess("Successfully", "Forgot Password link sent on registered Email");
        this.forgotPassword.reset();
        this.router.navigate(['/']);
      })).subscribe((result:any)=>{
        if(result.statusCode == 200){
          this.Msg = "Forgot Password link sent on registered Email";
          this.toastr.showSuccess("Successfully", "Forgot Password link sent on registered Email");
          this.forgotPassword.reset();
          //this.router.navigate(['/']);
        }
       
      })
      console.log(this.forgotPassword.value);
  }else{
    this.toastr.showError("Error", "Please check username");
  }
})
    
  }

}

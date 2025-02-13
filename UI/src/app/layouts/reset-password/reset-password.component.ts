import { Component, OnInit } from '@angular/core';
import { AbstractControl, UntypedFormBuilder, UntypedFormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner';
import { finalize } from 'rxjs/operators';
import { ConfirmedValidator } from '../../../../src/app/shared/customevalidation/confirmed.validator';
import { PasswordStrengthValidator } from '../../../../src/app/shared/customevalidation/password-strength.validators';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { OrganizationService } from '../../../../src/app/shared/services/organization.service';
import { ReactiveFormsModule } from '@angular/forms' ;
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-reset-password',
    imports: [CommonModule , ReactiveFormsModule],
    templateUrl: './reset-password.component.html',
    styleUrls: ['./reset-password.component.css'],
    standalone: true
})
export class ResetPasswordComponent implements OnInit {
  resetPassword:UntypedFormGroup ;
  submitted:boolean = false;
  EmailId:any;
  emailIdNo:any = [];
  get form(){
    return this.resetPassword.controls;
  }

  constructor(private fb:UntypedFormBuilder, private activatedRoute:ActivatedRoute, private OrgService:OrganizationService, private toastr:NotificationService, private router:Router,private spinner: NgxSpinnerService, private logininfo:LogininfoService) { 
    this.resetPassword= this.fb.group({
      password: [null, [Validators.required,PasswordStrengthValidator]],
      confirm_password: [null, Validators.required]
    }, { 
      validator: ConfirmedValidator('password', 'confirm_password')
    })

  }

  ngOnInit(): void {
   
    this.activatedRoute.params.subscribe((res)=>{
      this.EmailId = res.email;
      console.log("EmailId",this.EmailId);
          this.logininfo.getregistration().subscribe((res:any) => {
              // if()
              res.response.map((item:any) => {
                if(this.EmailId == item.email){
                  this.emailIdNo.push(item.id)
                }
              })
              console.log("this.emailIdNo",this.emailIdNo[0])
          })
    })
  }

  

  setPassword(){
    this.submitted = true;
    this.spinner.show();
    this.OrgService.resetPassword(this.emailIdNo[0], this.resetPassword.value).pipe(finalize(() => {
      this.spinner.hide();

    })).subscribe((result:any)=>{
      if(result.errorCode == 200){
        this.toastr.showSuccess("Successfully", "Password as Changed ");
          localStorage.clear()
          this.router.navigate(['/']);
      }
    },
    (error) =>{
      this.toastr.showError('Failed', 'Email Id Not Match Please Contact Administrator');
    })
    
    
  }

}

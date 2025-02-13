import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { CommonModule } from '@angular/common' ;
import { ReactiveFormsModule } from '@angular/forms' ;
import { RecaptchaModule } from 'ng-recaptcha' ;

@Component({
    selector: 'app-registrationform',
    imports: [ CommonModule, ReactiveFormsModule, RecaptchaModule ],
    templateUrl: './registrationform.component.html',
    styleUrls: ['./registrationform.component.css'],
    standalone: true
})
export class RegistrationformComponent implements OnInit {
  loginData!:UntypedFormGroup
  password:any;

  show = false;

  constructor(private fb:UntypedFormBuilder, private loginservice:LogininfoService,private toaster:NotificationService,private router:Router) {
    this.loginData = this.fb.group({
      name:['', Validators.required],
      email:['', Validators.required],
      bName:['', Validators.required],
      password:['', Validators.required],
      domain:['', Validators.required],
      orgid:[Math.floor(Math.random() * (999999 - 100000)) + 100000],
      packegStatus:['free']
     // phone:['', Validators.required],
    })
   }

  ngOnInit(): void {
    this.password = 'password';
  }
  onSubmit(){
      console.log("this.loginData.value",this.loginData.value);
      this.loginservice.getregistration().subscribe((item:any) =>{
        console.log("Item Details", item);
        var datafilter = item.response.filter((item:any) => item.email == this.loginData.controls['email'].value )
        console.log("datafilter",datafilter);
        //return;
        if(datafilter.length != 0){
          this.toaster.showWarning("Warning", "Already registered this email id");
        }else{
          this.loginservice.registration(this.loginData.value).subscribe((res:any) =>{
            if(res.errorCode == 200){

              console.log("result ", res)
              var data =  {
                "pages": "0",
                "document": "0",
                "orgid":res.response.orgid
            }
            this.loginservice.pdfinfocount(data).subscribe((res:any) =>{
              if(res.errorCode == 200){
                this.toaster.showSuccess("Success", "Successfully Registration Completed!");
                this.router.navigate(['/']);
              }
              
            })
              
            }else{
              this.toaster.showError("Error", "Please try later!");
            }
          })
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

  resolved(captchaResponse: any) {
    console.log(`Resolved captcha with response: ${captchaResponse}`);
  }
}

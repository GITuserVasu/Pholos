import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LogininfoService } from '../../../../src/app/shared/services/logininfo.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common' ;
import {RecaptchaModule} from 'ng-recaptcha' ;

@Component({
    selector: 'app-emp-registration',
    imports: [ ReactiveFormsModule, CommonModule , RecaptchaModule],
    templateUrl: './emp-registration.component.html',
    styleUrls: ['./emp-registration.component.css'],
    standalone: true
})
export class EmpRegistrationComponent implements OnInit {

  loginData!: UntypedFormGroup
  password: any;

  show = false;

  constructor(private fb: UntypedFormBuilder, private loginservice: LogininfoService, private toaster: NotificationService, private router: Router) {
    this.loginData = this.fb.group({
      name: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required],
      orgid: ['', Validators.required],
      status: ['Inactive', Validators.required],
      empOrgid: [Math.floor(Math.random() * (999999 - 100000)) + 100000],
      // packegStatus:['free']
      // phone:['', Validators.required],
    })
  }

  ngOnInit(): void {
    this.password = 'password';
  }
  onSubmit() {
    // alert("Hi"+this.loginData.controls['orgid'].value)
    this.loginservice.orgDetials(this.loginData.controls['orgid'].value).subscribe((orgdetails: any) => {
      if (orgdetails.response[0]) {
        console.log("this.loginData.value", this.loginData.value);
        console.log("this.orgdetailsorgdetails.value", orgdetails);
        this.loginservice.empgetregistration().subscribe((item: any) => {
          console.log("Item Detials", item);
          var datafilter = item.response.filter((item: any) => item.email == this.loginData.controls['email'].value)
          console.log("datafilter", datafilter);
          //return;
          if (datafilter.length != 0) {
            this.toaster.showWarning("Warning", "Already registered this email id");
          } else {
            this.loginservice.empregistration(this.loginData.value).subscribe((res: any) => {
              if (res.errorCode == 200) {
                var emailInfo = {
                  "email":orgdetails.response[0].email,
                  'id':res.response.id,
                  "orgId":this.loginData.controls['orgid'].value,
                  "empEmail":this.loginData.controls['email'].value,
                  "empName":this.loginData.controls['name'].value

                }
                this.loginservice.emailActivate(emailInfo).subscribe((res:any) => {
                  console.log("testing", res)
                })
                console.log("result ", res)
                var data = {
                  "pages": "0",
                  "document": "0",
                  "orgid": res.response.orgid
                }
                this.loginservice.pdfinfocount(data).subscribe((res: any) => {
                  if (res.errorCode == 200) {
                    this.toaster.showSuccess("Success", "Successfully Registered!");
                    this.router.navigate(['/']);
                  }

                })

              } else {
               
                  this.toaster.showError("Error", "Please try later!");
                
               
              }
            })
          }
        })
      } else {
        this.toaster.showError("Error", "Organization Code does not match Please check");
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


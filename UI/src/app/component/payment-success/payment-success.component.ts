import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs/operators';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { OrganizationService } from '../../../../src/app/shared/services/organization.service';

@Component({
    selector: 'app-payment-success',
    templateUrl: './payment-success.component.html',
    styleUrls: ['./payment-success.component.css'],
    standalone: false
})
export class PaymentSuccessComponent implements OnInit {
  info:any
  constructor(private OrgService:OrganizationService, private activateRouter:ActivatedRoute, private toastr:NotificationService, private router:Router) { }

  ngOnInit(): void {
    this.info = localStorage.getItem("info")
    
    this.info = JSON.parse(this.info)
    console.log("this.info test", this.info.id);


    this.activateRouter.params.subscribe((res:any) => {
      console.log("resresresresres",res.package)
      var data = {
        packegStatus:res.package
      }
      this.OrgService.packageUpdate(this.info.id, data).pipe(finalize(() => {


    })).subscribe((result:any)=>{
      if(result.errorCode == 200){
        this.toastr.showSuccess("Successfully", "Thank you for choose the package");
        localStorage.clear();
        this.router.navigate(['/login'])
      }
    },
    (error) =>{
      this.toastr.showError('Failed', 'Email Id Not Match Please Contact Administrator');
    })
    })

    

    

  }

}

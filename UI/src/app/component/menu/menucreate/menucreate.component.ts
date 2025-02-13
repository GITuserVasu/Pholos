import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MenuModulesService } from '../../../../../src/app/shared/services/menu-modules.service';
import { NotificationService } from '../../../../../src/app/shared/services/notification.service';
import {ReactiveFormsModule} from '@angular/forms' ;
import { CommonModule } from '@angular/common' ;

@Component({
    selector: 'app-menucreate',
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './menucreate.component.html',
    styleUrls: ['./menucreate.component.css'],
    standalone:  true
})
export class MenucreateComponent implements OnInit {
  submitted:boolean = false;
  subMenudata:UntypedFormGroup
  constructor(private menuservice:MenuModulesService, private fb:UntypedFormBuilder, private toastr:NotificationService, private router:Router) {
    this.subMenudata = this.fb.group({
      name:['', [Validators.required]],
      url:['', [Validators.required]]
    })
   }

get form(){
 return this.subMenudata.controls;
}

  ngOnInit(): void {
  }

  submitData(){
    console.log(this.subMenudata.value);
    this.menuservice.createMenu(this.subMenudata.value).subscribe((result:any)=>{
      if(result.statusCode=== 200){
        console.log("result",result);
        this.toastr.showSuccess("Successfully", "Successfully Create");
        this.router.navigate(['/menu']);
      }else{
        this.toastr.showError('Failed', "Please Try Again Later");
      }
    })
  }
}

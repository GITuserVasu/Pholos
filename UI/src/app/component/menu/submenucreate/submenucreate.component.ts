import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MenuModulesService } from '../../../../../src/app/shared/services/menu-modules.service';
import { NotificationService } from '../../../../../src/app/shared/services/notification.service';
import {ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common' ; 

@Component({
    selector: 'app-submenucreate',
    imports: [ReactiveFormsModule, CommonModule],
    templateUrl: './submenucreate.component.html',
    styleUrls: ['./submenucreate.component.css'],
    standalone: true
})
export class SubmenucreateComponent implements OnInit {
  submitted:boolean = false;
  subMenudata:UntypedFormGroup;
  menudata:any;
  constructor(private menuservice:MenuModulesService, private fb:UntypedFormBuilder,private toastr:NotificationService, private router:Router) {
    this.subMenudata = this.fb.group({
      menu_id:['', Validators.required],
      menu_name:[''],
      sub_menu:['', Validators.required],
      url:['', Validators.required]
    })
   }

get form(){
 return this.subMenudata.controls;
}
ngOnInit(): void {
  this.getMenu();
}


submitData(){
  var split = this.subMenudata.value['menu_id'].split("|");
  this.subMenudata.value['menu_id']=split[0];
  this.subMenudata.value['menu_name']=split[1];
  console.log(this.subMenudata.value);
  this.menuservice.createSubMenu(this.subMenudata.value).subscribe((result:any)=>{
    if(result.statusCode=== 200){
      console.log("result",result);
      this.toastr.showSuccess("Successfully", "Successfully Create");
      this.router.navigate(['/menu/submenulist']);
    }else{
      this.toastr.showError('Failed', "Please Try Again Later");
    }
  })

}
getMenu(){
  this.menuservice.getModules().subscribe((data:any)=>{

   this.menudata = data.data;
   console.log("this.menudata",this.menudata);

   
  })
}

}

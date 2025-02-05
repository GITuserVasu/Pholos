import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { finalize } from 'rxjs/operators';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { RoleService } from '../../../../src/app/shared/services/role.service';

@Component({
    selector: 'app-role',
    templateUrl: './role.component.html',
    styleUrls: ['./role.component.css'],
    standalone: false
})
export class RoleComponent implements OnInit {
  role:UntypedFormGroup;
  idEditable:boolean = false;
  submitted:any;
  org_id:any;
  roleList:any;
  UpdateId:any;
  isEdited:boolean = false;
  constructor(private fb:UntypedFormBuilder, private _roleService:RoleService, private toastr:NotificationService,private spinner: NgxSpinnerService, private activateRouter:ActivatedRoute, private router:Router) {
    this.org_id = window.localStorage.getItem('org_id');
    this.role = this.fb.group({
      name:['', Validators.required],
      org_id:[parseInt(this.org_id)],
    })
   }

   get form(){
     return this.role.controls;
   }
  ngOnInit(): void {
    this.getList();
   
    this.activateRouter.params.subscribe((res)=>{
        if(res.id){
          this.isEdited = true;
          this.spinner.show()
          this.UpdateId = res.id;
          this._roleService.getIdwiseData(res.id).pipe(finalize(()=>{
            this.spinner.hide()
          })).subscribe((result:any)=>{
              const data = result.data[0];
              this.role.controls['name'].setValue(data.name);
          })
        }
     
    })

  }

  submitData(){
    this.spinner.show();
    console.log(this.role.value);
    this._roleService.createRole(this.role.value).pipe(finalize(()=>{
      this.spinner.hide();
    })).subscribe((data:any)=>{
      if(data.statusCode == 200){
        this.toastr.showSuccess("Successfully", "Created Successfully ");
        this.role.reset();
        this.getList();
      }
    })
  }

  getList(){
    this._roleService.getRole(this.org_id).subscribe((data:any)=>{
      this.roleList = data.data;
      console.log(this.roleList);
    })
  }

  updateData(){
    
    console.log(this.role.value);

    this._roleService.update(this.UpdateId, this.role.value).subscribe((data:any)=>{
      if(data.statusCode == 200){
        this.toastr.showSuccess("Successfully", "Updated Successfully ");
        this.router.navigate(['/role']);
        this.getList();
      }
    })
  }

}

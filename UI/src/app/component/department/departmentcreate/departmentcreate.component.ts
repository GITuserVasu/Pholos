import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { BrowserAnimationsModule} from '@angular/platform-browser/animations' ;
import { NgxSpinnerService } from 'ngx-spinner';
import { NgxSpinnerModule } from 'ngx-spinner' ;
import { finalize } from 'rxjs/operators';
import { DepartmentService } from '../../../../../src/app/shared/services/department.service';
import { NotificationService } from '../../../../../src/app/shared/services/notification.service';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router' ;

@Component({
    selector: 'app-departmentcreate',
  //  imports: [ CommonModule, ReactiveFormsModule , RouterModule],
    templateUrl: './departmentcreate.component.html',
    styleUrls: ['./departmentcreate.component.css'],
    standalone: false 
})
export class DepartmentcreateComponent implements OnInit {
  department:UntypedFormGroup;
  submitted:boolean = false;
  org_id:any;
  departmentList:any;
  departmentEditId:any;
  idEditable:boolean = false;
  constructor(private fb:UntypedFormBuilder, private _department:DepartmentService,private spinner: NgxSpinnerService, private toastr:NotificationService, private router:Router, private activatedRoute:ActivatedRoute) { 
    this.org_id = window.localStorage.getItem('org_id');
    this.department= this.fb.group({
      name:['', Validators.required],
      org_id:[parseInt(this.org_id)]
    })
  }
get form(){
  return this.department.controls;
}
  ngOnInit(): void {
    //this.org_id = window.localStorage.getItem('org_id');
this.getDepartmentList();

    this.activatedRoute.params.subscribe((res)=>{
      if(res.id){
        const id = res.id;
        this.idEditable = true;
      this._department.getDepartmentIdWise(id).subscribe((result:any)=>{
          if(result.statusCode == 200){
            const data = result.data[0];
            this.departmentEditId= id;
            this.department.controls['name'].setValue(data.name);
          }
      })
      }
      

    });


  }


  submitData(){
    this.spinner.show();
    this._department.createDepartment(this.department.value).pipe(finalize(()=>{
      this.spinner.hide();
    })).subscribe((result:any)=>{
      if(result.statusCode == 200){
        this.toastr.showSuccess("Successfully", "Created Successfully ");
       this.department.reset();
       this.getDepartmentList();
      }
    })

      console.log(this.department.value);
  }

  getDepartmentList(){
    this._department.getDepartment(this.org_id).subscribe((result:any)=>{
      this.departmentList = result.data;
      console.log(this.departmentList );
    })
  }

  updateData(){
    console.log(this.department.value);
    this.spinner.show()
    this._department.updateDepartment(this.departmentEditId, this.department.value).pipe(finalize(()=>[
      this.spinner.hide()
    ])).subscribe((result:any)=>{
        if(result.statusCode == 200){
          this.toastr.showSuccess("Successfully", "Update Successfully ");
       this.router.navigate(['/department']);
          this.getDepartmentList();
        }
    })

  }
}

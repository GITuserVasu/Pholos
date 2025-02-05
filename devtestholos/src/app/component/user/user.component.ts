import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { finalize } from 'rxjs/operators';
import { DepartmentService } from '../../../../src/app/shared/services/department.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { RoleService } from '../../../../src/app/shared/services/role.service';
import { UserService } from '../../../../src/app/shared/services/user.service';
import { CommonModule } from '@angular/common' ;
import { ReactiveFormsModule } from '@angular/forms' ;

@Component({
    selector: 'app-user',
    imports: [ CommonModule, ReactiveFormsModule] ,
    templateUrl: './user.component.html',
    styleUrls: ['./user.component.css'],
    standalone: true
})
export class UserComponent implements OnInit {
  emplayeeRegister:UntypedFormGroup;
  submitted:boolean= false;
  isEdit:boolean= false;
  org_id:any;
  departmentList:any;
  roleList:any;
  generatePassword:any;
  userEdit:any;
  depSelected:any ;
  roleSelected:any;
  
  constructor(private fb:UntypedFormBuilder, private _department:DepartmentService, private _role:RoleService, private _user:UserService,private spinner: NgxSpinnerService, private toastr:NotificationService, private router:Router, private activateRoute:ActivatedRoute) { 
    this.generatePassword= this.getPasswordGen();
    this.org_id = window.localStorage.getItem('org_id');
    this.emplayeeRegister = this.fb.group({
      firstname:['', [Validators.required]],
      lastname:['', Validators.required],
      email:['', [Validators.required, Validators.email]],
      department:['',Validators.required],
      department_id:[''],
      role:['',Validators.required],
      role_id:[''],
      username:['',Validators.required],
      password:[this.generatePassword],
      address:['',Validators.required],
      org_id:[this.org_id]
    })
  }

  get form(){
    return this.emplayeeRegister.controls;
  }
  ngOnInit(): void {
    this.getPasswordGen();


    this.getDepartment();
    this.getRole();


    // Showing edit data in the form
this.activateRoute.params.subscribe((res)=>{

  if(res.id){
    this.isEdit=true;
    this.userEdit = res.id;
    
    this._user.getIdwiseUsers(this.userEdit).pipe(finalize(()=>{
  
    })).subscribe((result:any)=>{
       const body = result.data[0];
       console.log("body",body.department_id +"|"+ body.department);
       this.emplayeeRegister.controls['firstname'].setValue(body.firstname);
       this.emplayeeRegister.controls['lastname'].setValue(body.lastname);
       this.emplayeeRegister.controls['email'].setValue(body.email);
       this.emplayeeRegister.controls['department'].setValue(body.department_id +"|"+ body.department);
       this.emplayeeRegister.controls['role'].setValue(body.role_id +"|"+ body.role);
       this.emplayeeRegister.controls['username'].setValue(body.username);
       this.emplayeeRegister.controls['password'].setValue(body.password);
       this.emplayeeRegister.controls['address'].setValue(body.address);
       this.depSelected = body.department_id +"|"+ body.department;
       this.roleSelected = body.role_id +"|"+ body.role;
    })
  }
  

})

  }
  getPasswordGen(){
    var generatePassword = (
      length = 8,
      wishlist = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@-#$'
    ) =>
      Array.from(crypto.getRandomValues(new Uint32Array(length)))
        .map((x) => wishlist[x % wishlist.length])
        .join('')
    return generatePassword()
  }
 

  getDepartment(){
      this._department.getDepartment(this.org_id).subscribe((data:any)=>{
        this.departmentList = data.data;
      })
  }
  getRole(){
      this._role.getRole(this.org_id).subscribe((data:any)=>{
        this.roleList = data.data;
      })
  }
  onSubmit(){
   
    const depsplit = this.emplayeeRegister.value['department'];
   
   const splitDep = depsplit.split("|");
   this.emplayeeRegister.value['department']= splitDep[1];
   this.emplayeeRegister.value['department_id']= splitDep[0];
   const rolesplit = this.emplayeeRegister.value['role'];
   const splitrole = rolesplit.split("|");
   this.emplayeeRegister.value['role']= splitrole[1];
   this.emplayeeRegister.value['role_id']= splitrole[0];
   console.log(this.emplayeeRegister.value);
    this.spinner.show()
    this._user.createUser(this.emplayeeRegister.value).pipe(finalize(()=>{
      this.spinner.hide()
    })).subscribe((result:any)=>{
      if(result.statusCode == 200){
        this.toastr.showSuccess("Successfully", "Created Successfully ");
        this.router.navigate(['/user']);
      }
    })
  }

  updateData(){

  }

}

import { Component, OnInit } from '@angular/core';
import { FormArray, UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MenuModulesService } from '../../../../src/app/shared/services/menu-modules.service';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { OrganizationService } from '../../../../src/app/shared/services/organization.service';
import { BrowserAnimationsModule } from '@angular/platform-browser-animations' ;
import { NgxSpinnerModule } from 'ngx-spinner' ;
import { NgxSpinnerService } from 'ngx-spinner';
import { finalize } from 'rxjs/operators';
import { CommonModule } from '@angular/common' ;
import {ReactiveFormsModule } from '@angular/forms' ;

@Component({
    selector: 'app-organization',
    imports: [ CommonModule, ReactiveFormsModule, NgxSpinnerModule ],
    templateUrl: './organization.component.html',
    styleUrls: ['./organization.component.css'],
    standalone: true
})
export class OrganizationComponent implements OnInit {
  moduleList:any;
  subModulesList:any;
  organizationData:UntypedFormGroup;
  submitted:boolean=false;
  pushModuleList:any =[];
  pushSubModuleList:any = [];
  modulesId:any;
  orgid:any;
  editId:any;
  idEditBtn: boolean = false;
  moduleId:any;
  generatePasswordOrg:any;
  get form(){
    return this.organizationData.controls;
  }
  
  constructor(private modules:MenuModulesService, private fb:UntypedFormBuilder, private Orgservice:OrganizationService,private toastr:NotificationService,private router:Router, private activatedRoute:ActivatedRoute,private spinner: NgxSpinnerService) { 
    
    this.orgid = this.orgNumber();
    this.generatePasswordOrg= this.generatePassword();
    this.organizationData =  this.fb.group({
      org_name:['', Validators.required],
      org_id:[this.orgid, Validators.required],
      email:['', [Validators.required, Validators.email]],
      phone:['', Validators.required],
      username:['', Validators.required],
      password:[this.generatePasswordOrg, Validators.required],
      city:['', Validators.required],
      state:['', Validators.required],
      zip:['', Validators.required],
      sub_module:[],
      module:[]
    })
  }




  ngOnInit(): void {

    this.generatePassword();

    //this.spinner.show();
console.log("generatePasswordOrg",this.generatePasswordOrg)

    this.modules.getModules().subscribe((result: any) => {
      this.moduleList = result.data;
    })

    this.modules.getSubmenu().subscribe((result: any) => {
      this.subModulesList = result.data;

      this.subModulesList = this.subModulesList.map((item:any) => item);

      console.log("subModulesList",this.subModulesList);
    })


    this.activatedRoute.params.subscribe((res)=>{
        this.editId = res.id;
        if(res.id){
             this.idEditBtn = true;
           this.Orgservice.getIdByData(res.id).subscribe((data:any)=>{
            let body = data.data;
            console.log("body",body[0]);
            this.organizationData.controls['org_name'].setValue(body[0].org_name);
            this.organizationData.controls['org_id'].setValue(body[0].org_id);
            this.organizationData.controls['email'].setValue(body[0].email);
            this.organizationData.controls['phone'].setValue(body[0].phone);
            this.organizationData.controls['username'].setValue(body[0].username);
            this.organizationData.controls['password'].setValue(body[0].password);
            this.organizationData.controls['city'].setValue(body[0].city);
            this.organizationData.controls['state'].setValue(body[0].state);
            this.organizationData.controls['zip'].setValue(body[0].zip);

           
            this.moduleId=body[0].module.split(',').map(Number);
            this.pushModuleList =  this.moduleId
            console.log("pushModuleList",this.pushModuleList);
          this.moduleList.forEach((item:any) => {
            for (var i = 0; i < this.moduleId.length; i++) {
              if (item.id == this.moduleId[i]) {
                item.checked = true; 
                break;
              }else{
               item.checked = false; 
              }
            }
           
          });
         
        })
        }
        
        
    })


  }

  generatePassword(){
    var generatePassword = (
      length = 8,
      wishlist = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~!@-#$'
    ) =>
      Array.from(crypto.getRandomValues(new Uint32Array(length)))
        .map((x) => wishlist[x % wishlist.length])
        .join('')
    return generatePassword()
  
  }
  submitData(){
    this.spinner.show();
    console.log("module",this.organizationData.value['module']);
    this.organizationData.value['password']=this.generatePasswordOrg;
    this.organizationData.value['sub_module']= this.pushSubModuleList.toString();
    this.organizationData.value['module']= this.pushModuleList.toString();
    console.log("organizationData",this.organizationData.value);
    this.Orgservice.sendData(this.organizationData.value).pipe(finalize(()=>{
    
    })).subscribe((result:any)=> {
          if(result.statusCode=== 200){
            let emaildata= {
              email: this.organizationData.value['email'],
              password: this.organizationData.value['password'],
              name: this.organizationData.value['org_name']
            }
            console.log("emaildata",emaildata);
              this.Orgservice.sendEmail(emaildata).pipe(finalize(()=>{
                this.spinner.hide();
              })).subscribe((resilt)=>{
                console.log("result",result);
                this.toastr.showSuccess("Successfully", "Successfully Create");
                this.router.navigate(['/organization/list']);
              })
           
          }else{
            this.toastr.showError('Failed', "Please Try Again Later");
          }
    })

  }
  updateData(){
      console.log("pushModuleList", this.pushModuleList);
      this.organizationData.value['module'] = this.pushModuleList.toString();
      console.log(" this.organizationData.value",  this.organizationData.value);
       this.Orgservice.updateData(this.editId,this.organizationData.value).subscribe((result:any)=> {
          if(result.statusCode=== 200){
            console.log("result",result);
            this.toastr.showSuccess("Successfully", "Successfully Create");
            this.router.navigate(['/organization/list']);
          }else{
            this.toastr.showError('Failed', "Please Try Again Later");
          }
    })
  }

  moduleAceess(id:number, index:number, event:any){

    console.log("event",event);
    
      this.modulesId = id;
      if(event.target.checked == true){
        this.pushModuleList.push(id);
      }else{
        this.pushModuleList.splice(index);
      }
      
  }

  submenus(module:any):any{
    return this.subModulesList.filter((item: any) => { return item.menu_id == module; });
  }

  submoduleAceess(id:number, index:number, event:any){
      // this.modulesId = id;
      console.log("event", event);
      if(event.target.checked == true){
        this.pushSubModuleList.push(id);
      }else{
        this.pushSubModuleList.splice(index);
      }
     
  }
  orgNumber(): any {
    let now = Date.now().toString() 
    now += now + Math.floor(Math.random() * 10)
    return [now.slice(0, 6)]
  }

}

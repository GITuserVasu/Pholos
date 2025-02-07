import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AgGridAngular } from 'ag-grid-angular' ;
import type { ColDef } from 'ag-grid-community';
//import { CellClickedEvent } from 'ag-grid-community/dist/lib/events';
import { CellClickedEvent } from 'ag-grid-community';
import { BrowserAnimationsModule } from '@angular/platform-browser-animations' ;
import { FormsModule } from '@angular/forms' ;
import { ToastrService } from 'ngx-toastr';
import { LogininfoService } from '../../shared/services/logininfo.service';
import { MenuModulesService } from '../../shared/services/menu-modules.service';
import { environment } from '../../../environments/environment';
import { DashboardModule } from './dashboard.module' ;
import {CommonModule } from '@angular/common' ;
import { ModuleRegistry } from 'ag-grid-community'; 
import { ClientSideRowModelModule } from 'ag-grid-community'; 
import { themeBalham } from 'ag-grid-community';



ModuleRegistry.registerModules([ClientSideRowModelModule]);
declare var $ : any;
//declare var Module:any = []

@Component({
    selector: 'app-dashboard',
    imports: [ AgGridAngular, CommonModule ],
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css'],
    standalone: true
})
export class DashboardComponent implements OnInit {

  userRole:string = '';
  moduleList:any;
  rowData:any = [];
  data:any = [];
  verified:any = [];
  inprogress:any = [];
  orgid:any;
  rowSelection: any = 'multiple'
  //mymodules: type of Module[] = [ClientSideRowModelModule] ;
  mymodules:any = [];
  myTheme = themeBalham.withParams({ accentColor: 'red' });

  

  constructor(private LoginInfo:LogininfoService,private modules:MenuModulesService, private http:HttpClient, private notification:ToastrService, private router:Router) { }

  ngOnInit(): void {
    this.userRole = this.LoginInfo.accessToken;
    console.log(this.userRole);
    this.getAllrecords();
    this.orgid = localStorage.getItem('org_id')
    console.log("Org id", this.orgid)
    this.mymodules.push('ClientSideRowModelModule');
  }
  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
  };
  columnDefs = [
    { field: 'id', width: 120, maxWidth: 150, resizable: true,checkboxSelection: true},
    // { headerName: 'Tool', field: 'ocrType', width: 150, maxWidth: 150, resizable: true,},
    { field: 'status', width: 200, maxWidth: 300, resizable: true,
    valueGetter:(param:any) =>{
      console.log(param)
      if(param.data['status'] == 'Inprogress'){
        return "In Progress"
      }else{
        return param.data['status']
      }
      
  
    } },
    { headerName: 'Project', field: 'projectName',width: 400, maxWidth: 600, resizable: true, },
    //{ headerName: 'Folder', field: 'folderName',width: 200, maxWidth: 300,  resizable: true, },
   
    //{ headerName: 'File', field: 'fileName', width: 150, maxWidth: 500,  resizable: true,},
   
    { headerName: 'Created', field: 'CreatedDate',  width: 300, maxWidth: 500,  resizable: true,
    valueGetter:(param:any) =>{
      return new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true});
      console.log("params",new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true}))
    }
  },
    {
      headerName:'Action', width: 200, cellRenderer:(param:any) =>{
      console.log("cell", param)
      if(param.data['status'] == 'Inprogress'){
        return '<a class="btn btn-info btn-sm btn-rounded waves-effect waves-light" disabled >View Details</a>'
      }else{
        return `<a href="#/ocrdetail/${param.data['id']}/${param.data['ocrType']}" class="btn btn-primary btn-sm btn-rounded waves-effect waves-light" >View Details</a>`
      }
      
    }
  },
  /* { 
    headerName:'Comprehend', width:150, cellRenderer:(param:any) =>{
    console.log("cell", param)

    if(param.data['status'] == 'Inprogress'){
      return '<a class="btn btn-info btn-sm btn-rounded waves-effect waves-light" disabled >View Details</a>'
    }else{
      return `<a href="#/comprehend/${param.data['id']}/${param.data['ocrType']}" class="btn btn-primary btn-sm btn-rounded waves-effect waves-light" >View Details</a>`
    }  }
} */
  ];
  columnDefs_admin = [
    { field: 'id',width:100},
    { field: 'status' ,
    valueGetter:(param:any) =>{
      console.log(param)
      if(param.data['status'] == 'Inprogress'){
        
        return '<h6 style="color:red">In Progress</h6>'
      }else{
        return param.data['status']
      }
      
  
    }},
    { field: 'fileName'},
   
    { field: 'CreatedDate', minWidth:250, 
     valueGetter:(param:any) =>{
      return new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true});
      console.log("params",new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true}))
    }
  },
    { 
      headerName:'Action', width:150, cellRenderer:(param:any) =>{
      console.log("cell", param)

      return `<a href="#/ocrdetail/${param.data['id']}" class="btn btn-primary btn-sm btn-rounded waves-effect waves-light" >View Details</a>`
    },
    
    
  },
 /*  { 
    headerName:'Comprehend', width:150, cellRenderer:(param:any) =>{
    console.log("cell", param)

    return `<a href="#/ocrdetail/${param.data['id']}" class="btn btn-primary btn-sm btn-rounded waves-effect waves-light" >View Details</a>`
  },
  
  
}, */
  { headerName:'Delete', width:100, 
  cellRenderer:(param:any) =>{
    console.log("cell", param)

    return '<a class="btn btn-danger btn-sm btn-rounded waves-effect waves-light" (click)="delete()">delete</a>'
  },
  onCellClicked:(event:CellClickedEvent) =>{
    this.http.delete(environment.apiUrl+'Case_Detiles/'+event.data['id']).subscribe((res:any) => {
      if(res.statusCode = 200){
        this.notification.success("Successfully Deleted", "success")
        this.router.navigate(['/dashboard'])
        //window.location.reload()
      }
    })
  }
  
}
  ];


  getAllrecords(){
    this.http.get(environment.apiUrl+'Case_Detiles/').subscribe((res:any) => {
      console.log('getAllrecords', res.response);
     // this.data =res.response;
      res.response.map((item:any) =>{


        if(localStorage.getItem('org_id') == 'admin'){
          this.data.push(item);
          if(item.status == 'Verified'){
            this.verified.push(item)
          }else{
            this.inprogress.push(item)
          }
        }else{
          if((item.orgid == localStorage.getItem("org_id") && localStorage.getItem("empOrgid") == '')){
            if(item.status == 'Verified'){
              this.verified.push(item)
            }else{
              this.inprogress.push(item)
            }
            this.data.push(item)
         
          }else if(item.empOrgid == localStorage.getItem("empOrgid")){
            if(item.status == 'Verified'){
              this.verified.push(item)
            }else{
              this.inprogress.push(item)
            }
            this.data.push(item)
          }
        }

       
       
      })
      this.rowData = this.data;
      console.log("this.rowData",this.rowData)
      // if(res.errorCode == 200){
      // }
    })
  }
  getstatusdetials(){
    this.http.get(environment.apiUrl+'Case_Detiles/').subscribe((res:any) => {
      console.log('getStatusDetails', res.response);
     this.data =res.response;
      
      // if(res.errorCode == 200){
      // }
    })
  }
  delete(){
    //alert("HI")
  }
 

}

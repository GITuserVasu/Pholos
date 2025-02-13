import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ColDef } from 'ag-grid-community';
import { environment } from '../../../../src/environments/environment';

@Component({
    selector: 'app-status-wisedetials',
    templateUrl: './status-wisedetials.component.html',
    styleUrls: ['./status-wisedetials.component.css'],
    standalone: false
})
export class StatusWisedetialsComponent implements OnInit {
  data:any = [];
  verified:any = [];
  inprogress:any = [];
  statusdesply:any;
  rowData:any = [];
  constructor(private http:HttpClient, private activateRouter:ActivatedRoute) { }

  ngOnInit(): void {
    this.activateRouter.params.subscribe((item:any) =>{
      console.log("item",item.status);
      this.statusdesply = item.status
      this.rowData = [];
      this.getAllrecords(item.status);
      this.getAllrecords1()
    })
    
  }
  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
  };
  columnDefs = [
    { field: 'id', width: 100, maxWidth: 150, resizable: true,checkboxSelection: true},
    { field: 'ocrType', width: 100, maxWidth: 150, resizable: true,},
    { field: 'status',width: 100, maxWidth: 150, resizable: true,
    valueGetter:(param:any) =>{
      console.log(param)
      if(param.data['status'] == 'Inprogress'){
        
        return `Error`
      }else{
        return param.data['status']
      }
      
  
    } },
    { field: 'projectName',width: 150, maxWidth: 300, resizable: true, },
    { field: 'folderName',width: 150, maxWidth: 300,  resizable: true, },
    { field: 'fileName'},
   
    { field: 'CreatedDate', minWidth:250, 
    valueGetter:(param:any) =>{
      return new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true});
      console.log("params",new Date(param.data['CreatedDate']).toLocaleString('en-US',{hour12:true}))
    }
  },
    { headerName:'Action', cellRenderer:(param:any) =>{
      console.log("cell", param)
      if(param.data['status'] == 'Inprogress'){
        return `<button class="btn btn-info btn-sm btn-rounded waves-effect waves-light" disabled >View Details</a>`
      }else{
        return `<a href='#/ocrdetail/${param.data['id']}/${param.data['ocrType']}' class="btn btn-primary btn-sm btn-rounded waves-effect waves-light" >View Details</a>`
      }
      
    }
  }
  ];
  getAllrecords1(){
    this.inprogress = []
    this.verified = []
    this.http.get(environment.apiUrl+'Case_Detiles/').subscribe((res:any) => {
      console.log('statuswisedetails getAllrecords1', res.response);
     // this.data =res.response;
      res.response.map((item:any) =>{
        if(item.orgid == localStorage.getItem("org_id")){
          if(item.status == 'Verified'){
            this.verified.push(item)
          }else{
            this.inprogress.push(item)
          }
          this.data.push(item)
        }
       
      })
      this.rowData = this.data
      // if(res.errorCode == 200){
      // }
    })
  }


  getAllrecords(status:any){

    this.data = []
    this.http.get(environment.apiUrl+'status_on_Case_Detiles/'+status).subscribe((res:any) => {
      console.log('statuswisedetails getAllrecords', res.response);
      //this.data =res.response;
      res.response.map((item:any) =>{
        

        if(localStorage.getItem('org_id') == 'admin'){
          this.data.push(item);
        }else{
          
          if(item.orgid == localStorage.getItem("org_id")){
            console.log("item",item)
            this.data.push(item)
          }
        }
      })
      console.log("this.data from statuswisedetails",this.data)
      this.rowData = this.data
      // if(res.errorCode == 200){
      // }
    })
  }
}

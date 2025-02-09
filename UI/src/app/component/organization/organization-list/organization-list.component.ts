import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OrganizationService } from '../../../../../src/app/shared/services/organization.service';
import {CommonModule} from '@angular/common';
import {OrganizationModule} from '../organization.module';
import {OrganizationRoutingModule} from '../organization-routing.module';


@Component({
    selector: 'app-organization-list',
    imports: [ CommonModule, OrganizationModule, OrganizationRoutingModule ],
    templateUrl: './organization-list.component.html',
    styleUrls: ['./organization-list.component.css'],
    standalone: true
})
export class OrganizationListComponent implements OnInit {
 
  OrgList:any;

  
  constructor(private orgService:OrganizationService, private router: Router) { }

  ngOnInit(): void {
    this.getOrgList();
  }

  getOrgList(){
    this.orgService.getData().subscribe((data:any)=>{
      this.OrgList = data.data;
    })
  }
  rowEditData(id:any){
    // this._dataServices.editStructureData(id).subscribe((result:any)=>{ });
     this.router.navigate(['organization/create',id]);
  }

}

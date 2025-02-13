import { Component, OnInit } from '@angular/core';
import { MenuModulesService } from '../../../../../src/app/shared/services/menu-modules.service';
import {CommonModule} from '@angular/common';
import {MenuRoutingModule} from '../menu-routing.module' ;

@Component({
    selector: 'app-submenulist',
    imports: [ CommonModule, MenuRoutingModule],
    templateUrl: './submenulist.component.html',
    styleUrls: ['./submenulist.component.css'],
    standalone: true
})
export class SubmenulistComponent implements OnInit {
  submenudata:any;
  constructor(private menuservice:MenuModulesService) { }

  ngOnInit(): void {
    this.getSubmenu();
  }

  getSubmenu(){
    this.menuservice.getSubmenu().subscribe((result:any)=>{
      this.submenudata = result.data;
    })
  }

}

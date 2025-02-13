import { Component, OnInit } from '@angular/core';
import { MenuModulesService } from '../../../../../src/app/shared/services/menu-modules.service';
import {MenuRoutingModule } from '../menu-routing.module' ;
import {CommonModule} from '@angular/common' ;

@Component({
    selector: 'app-menulist',
    imports: [MenuRoutingModule, CommonModule ],
    templateUrl: './menulist.component.html',
    styleUrls: ['./menulist.component.css'],
    standalone: true
})
export class MenulistComponent implements OnInit {
  menudata:any;
  constructor(private menuservice:MenuModulesService) { }

  ngOnInit(): void {
    this.getMenu();
  }

  getMenu(){
    this.menuservice.getModules().subscribe((data:any)=>{

     this.menudata = data.data;
     console.log("this.menudata",this.menudata)
    })
  }
}

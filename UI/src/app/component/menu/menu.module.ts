import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MenuRoutingModule } from './menu-routing.module';
import { MenucreateComponent } from './menucreate/menucreate.component';
import { MenulistComponent } from './menulist/menulist.component';
import { SubmenulistComponent } from './submenulist/submenulist.component';
import { SubmenucreateComponent } from './submenucreate/submenucreate.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
/**    MenucreateComponent,
    MenulistComponent,
    SubmenulistComponent,
    SubmenucreateComponent **/  
  ],
  imports: [
    CommonModule,
    MenuRoutingModule,
    ReactiveFormsModule
  ]
})
export class MenuModule { }

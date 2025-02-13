import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MenucreateComponent } from './menucreate/menucreate.component';
import { MenulistComponent } from './menulist/menulist.component';
import { SubmenucreateComponent } from './submenucreate/submenucreate.component';
import { SubmenulistComponent } from './submenulist/submenulist.component';

const routes: Routes = [
  {
    path:'',
    component:MenulistComponent
  },
  {
    path:'create',
    component:MenucreateComponent
  },
  {
    path:'submenulist',
    component:SubmenulistComponent
  },
  {
    path:'submenu',
    component:SubmenucreateComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MenuRoutingModule { }

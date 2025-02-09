import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DepartmentcreateComponent } from './departmentcreate/departmentcreate.component';

const routes: Routes = [
  {
    path:'',
    component:DepartmentcreateComponent
  },
  {
    path:':id',
    component:DepartmentcreateComponent
  }
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DepartmentRoutingModule { }

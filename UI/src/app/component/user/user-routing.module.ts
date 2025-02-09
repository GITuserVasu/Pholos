import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserComponent } from './user.component';
import { UserlistComponent } from './userlist/userlist.component';

const routes: Routes = [
  {
    path:'',
    component:UserlistComponent
  },
  {
    path:'create',
    component:UserComponent
  },
  {
    path:'create/:id',
    component:UserComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule { }

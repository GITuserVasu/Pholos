import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationListComponent } from './organization-list/organization-list.component';
import { OrganizationComponent } from './organization.component';

const routes: Routes = [
  {
    path: 'create',
    component: OrganizationComponent,
    data: {
        title: 'Dashboard ',
    }
},
{
  path: 'list',
  component: OrganizationListComponent,
  data: {
      title: 'Organization List ',
      
  }
},
{
  path:'create/:id',
component:OrganizationComponent
},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationRoutingModule { }

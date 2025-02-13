import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard.component';

const routes: Routes = [
  
  {
    path: '',
    component: DashboardComponent,
    data: {
        title: 'Dashboard ',
        headerDisplay: "none"
    }
},
{
  path: 'test',
  component: DashboardComponent,
  data: {
      title: 'Dashboard ',
      headerDisplay: "none"
  }
},
{
  path:'dashboard',
  redirectTo:'',
  pathMatch:'full'
}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule { }

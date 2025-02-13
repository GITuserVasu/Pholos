import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { AgGridModule } from 'ag-grid-angular';
import { AgGridAngular } from 'ag-grid-angular' ;


@NgModule({
  declarations: [
    //DashboardComponent
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    AgGridModule,
    AgGridAngular
  ]
//  schemas: [ CUSTOM_ELEMENTS_SCHEMA ]
})
export class DashboardModule { 

  
}

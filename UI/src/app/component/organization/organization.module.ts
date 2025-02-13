import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { OrganizationRoutingModule } from './organization-routing.module';
import { OrganizationComponent } from './organization.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { OrganizationListComponent } from './organization-list/organization-list.component';
import { NgxSpinnerModule } from 'ngx-spinner';

@NgModule({
  declarations: [
/*    OrganizationComponent,
    OrganizationListComponent */
  ],
  imports: [
    CommonModule,
    OrganizationRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    NgxSpinnerModule
  ]
})
export class OrganizationModule { }

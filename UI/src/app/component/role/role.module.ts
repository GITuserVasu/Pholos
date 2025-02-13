import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RoleRoutingModule } from './role-routing.module';
import { RoleComponent } from './role.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxSpinnerModule } from 'ngx-spinner';


@NgModule({
  declarations: [
    RoleComponent
  ],
  imports: [
    CommonModule,
    RoleRoutingModule,
    ReactiveFormsModule,
    NgxSpinnerModule
  ]
})
export class RoleModule { }

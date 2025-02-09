import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent } from './user.component';
import { UserlistComponent } from './userlist/userlist.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxSpinnerModule } from 'ngx-spinner';


@NgModule({
  declarations: [
  //  UserComponent,
    UserlistComponent 
  ],
  imports: [
    CommonModule,
    UserRoutingModule,
    ReactiveFormsModule,
    NgxSpinnerModule
  ]
})
export class UserModule { }

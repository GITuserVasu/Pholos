import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxSpinnerModule } from 'ngx-spinner';


@NgModule({
  declarations: [
  ],
  imports:[NgxSpinnerModule],
  exports: [
    CommonModule,
    NgxSpinnerModule,
  ]
})
export class SharedModule { }

import { NgModule,CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { CommonLauoutComponent } from './layouts/common-lauout/common-lauout.component';
import { FullLayoutComponent } from './layouts/full-layout/full-layout.component';
import { HeaderComponent } from './shared/template/header/header.component';
import { SideNavComponent } from './shared/template/side-nav/side-nav.component';
import { FooterComponent } from './shared/template/footer/footer.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { CommonModule, HashLocationStrategy, LocationStrategy } from '@angular/common';
import { ResetPasswordComponent } from './layouts/reset-password/reset-password.component';
import { ForgotPasswordComponent } from './layouts/forgot-password/forgot-password.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import { PagenotfoundComponent } from './layouts/pagenotfound/pagenotfound.component';
import { RegistrationformComponent } from './layouts/registrationform/registrationform.component';
import { AgGridModule } from 'ag-grid-angular';
import { AgGridAngular } from 'ag-grid-angular';
import { SharedModule } from './shared/shared.module';
import { EmpRegistrationComponent } from './layouts/emp-registration/emp-registration.component';
import {RecaptchaModule} from 'ng-recaptcha' ;
import { RouterModule } from '@angular/router' ;


@NgModule({ declarations: [
   /*     AppComponent,
        CommonLauoutComponent,
        FullLayoutComponent,
        HeaderComponent,
        SideNavComponent,
        FooterComponent,
        ResetPasswordComponent,
        ForgotPasswordComponent,
        PagenotfoundComponent,
        RegistrationformComponent,
        EmpRegistrationComponent,  
        HeaderComponent,
        SideNavComponent,
        FooterComponent,*/ 
    ],
    /*exports: [ 
        HeaderComponent,
        SideNavComponent,
        FooterComponent,
      ],*/
    bootstrap: [AppComponent],
    schemas: [
        CUSTOM_ELEMENTS_SCHEMA
    ], imports: [BrowserModule,
        RouterModule,
        AppRoutingModule,
	RecaptchaModule,
        FormsModule,
        ReactiveFormsModule,
        ToastrModule.forRoot(),
        BrowserAnimationsModule,
        NgxSpinnerModule,
        AgGridModule,
        AgGridAngular,
        SharedModule
    ], 
	providers: [{ provide: LocationStrategy, useClass: HashLocationStrategy }, provideHttpClient(withInterceptorsFromDi())] })
export class AppModule { }

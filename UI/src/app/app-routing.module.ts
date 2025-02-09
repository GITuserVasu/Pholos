import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { CommonLauoutComponent } from './layouts/common-lauout/common-lauout.component';
import { FullLayoutComponent } from './layouts/full-layout/full-layout.component';
import { CommonModule } from "@angular/common";

import { CommonLayout_ROUTES } from "./shared/routes/common-layout.routes";
import { FullLayout_ROUTES } from './shared/routes/full-layout.routes';
import { AuthGuard } from './shared/services/auth.guard';
import { ResetPasswordComponent } from './layouts/reset-password/reset-password.component';
import { PagenotfoundComponent } from './layouts/pagenotfound/pagenotfound.component';
import { TestCaseComponent } from './component/test-case/test-case.component';
import { EmpRegistrationComponent } from './layouts/emp-registration/emp-registration.component';
import { LoginComponent } from './authentication/login/login.component';

const routes: Routes =  [

  {
    path: 'login',
    component: FullLayoutComponent,
   children: FullLayout_ROUTES,
   
  },
  {
    path: '',
    component: CommonLauoutComponent,
    children: CommonLayout_ROUTES,
    
  },
  {
    path:'resetPassword/:email',
    component:ResetPasswordComponent
  }
  , {
    path:'userCases',
    component:TestCaseComponent
  },
  {
    path:'empRegistration',
    component:EmpRegistrationComponent
  },
  {
    path:'statuschange/:email/:id/:status',
    component:LoginComponent
  },
  {
    path:'**',
    component:PagenotfoundComponent
  }
  
 
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    preloadingStrategy: PreloadAllModules,
    anchorScrolling: 'enabled',
    scrollPositionRestoration: 'enabled'
  }),CommonModule],
  exports: [RouterModule]
})
export class AppRoutingModule {

  
 }

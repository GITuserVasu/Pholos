import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ForgotPasswordComponent } from '../layouts/forgot-password/forgot-password.component';
import { RegistrationformComponent } from '../layouts/registrationform/registrationform.component';
import { ResetPasswordComponent } from '../layouts/reset-password/reset-password.component';
import { EmployeeLoginComponent } from './employee-login/employee-login.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  {
    path: '',
    component: LoginComponent,
    data: {
        title: 'Login ',
    }
},
{
  path: 'reset-password/:email',
  component: ResetPasswordComponent,
  
},
{
  path: 'forgot-password',
  component: ForgotPasswordComponent,
  
},
{
  path: 'registrationPage',
  component: RegistrationformComponent,
  
},
{
  path: 'employee',
  component: EmployeeLoginComponent,
  
}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthenticationRoutingModule { }

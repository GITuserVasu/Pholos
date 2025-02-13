import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from '../shared/services/auth.guard';
import { CommonModule } from "@angular/common";
import { OcrscreenComponent } from './ocrscreen/ocrscreen.component';
import { OcrdetailviewComponent } from './ocrdetailview/ocrdetailview.component';
import { StatusWisedetialsComponent } from './status-wisedetials/status-wisedetials.component';
import { PriceListComponent } from './price-list/price-list.component';
import { PaymentSuccessComponent } from './payment-success/payment-success.component';
import { PaymentFailureComponent } from './payment-failure/payment-failure.component';
import { ComprehendComponent } from './comprehend/comprehend.component';
import { AIpredictionmodelsComponent } from './aipredictionmodels/aipredictionmodels.component';

const routes: Routes = [
    {
      path: '',
      loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule),
     
    },
    {
      path: 'organization',
      loadChildren: () => import('./organization/organization.module').then(m => m.OrganizationModule),
     
    },
    {
      path: 'menu',
      loadChildren: () => import('./menu/menu.module').then(m => m.MenuModule),
     
    },
    {
      path: 'department',
      loadChildren: () => import('./department/department.module').then(m => m.DepartmentModule),
     
    },
    {
      path:'role',
      loadChildren: ()=>import('./role/role.module').then(m => m.RoleModule),
    },
    {
      path:'user',
      loadChildren:()=>import('./user/user.module').then(m =>m.UserModule)
    },
    {
      path:'ocr',
      component:OcrscreenComponent
    },
    {
      path:'ocrdetail/:id/:ocrType',
      component:OcrdetailviewComponent
    },
    {
      path:'comprehend/:id/:ocrType',
      component:ComprehendComponent
    },
    {
      path:'statusWiseDetials/:status',
      component:StatusWisedetialsComponent
    },
    {
      path:'packages',
      component:PriceListComponent
    },
    {
      path:'packages/success/:package',
      component:PaymentSuccessComponent
    },
    {
      path:'packages/failure',
      component:PaymentFailureComponent
    },
    {
      path:'aipredictionmodels',
      component:AIpredictionmodelsComponent
    } 
    
   
   
  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ComponentRoutingModule { }

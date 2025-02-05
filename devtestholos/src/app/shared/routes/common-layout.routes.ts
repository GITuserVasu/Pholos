import { Routes } from "@angular/router";
import { AuthGuard } from "../services/auth.guard";

export const CommonLayout_ROUTES: Routes = [

    {
      path: '',
      loadChildren: () => import('../../component/component.module').then(m => m.ComponentModule),
      canActivate: [AuthGuard],
    }
   
   
    
  ];
  
import { Routes } from "@angular/router";
import { AuthGuard } from "../services/auth.guard";

export const FullLayout_ROUTES: Routes = [
    {
      path: '',
      loadChildren: () => import('../../authentication/authentication.module').then(m => m.AuthenticationModule),
     
    }
  ];
  
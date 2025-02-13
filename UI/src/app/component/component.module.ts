import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ComponentRoutingModule } from './component-routing.module';
import { OcrscreenComponent } from './ocrscreen/ocrscreen.component';
//import { PdfViewerModule } from 'ng2-pdf-viewer';
import { NgxSpinnerModule } from 'ngx-spinner';
import { OcrdetailviewComponent } from './ocrdetailview/ocrdetailview.component';
import { StatusWisedetialsComponent } from './status-wisedetials/status-wisedetials.component';
import { AgGridModule } from 'ag-grid-angular';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PriceListComponent } from './price-list/price-list.component';
import { PaymentSuccessComponent } from './payment-success/payment-success.component';
import { PaymentFailureComponent } from './payment-failure/payment-failure.component';
import { SharedModule } from "../shared/shared.module";
import { TestCaseComponent } from './test-case/test-case.component';
//import { ComprehendComponent } from './comprehend/comprehend.component';
import { AIpredictionmodelsComponent } from './aipredictionmodels/aipredictionmodels.component';

@NgModule({
    declarations: [
        OcrscreenComponent, 
        OcrdetailviewComponent, 
        StatusWisedetialsComponent, 
	AIpredictionmodelsComponent,
        PriceListComponent, 
   //     PaymentSuccessComponent, 
        PaymentFailureComponent, 
        TestCaseComponent 
 //       ComprehendComponent
    ],
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
    imports: [
        CommonModule,
        ComponentRoutingModule,
        ReactiveFormsModule,
        FormsModule,
     //   PdfViewerModule,
        NgxSpinnerModule,
        AgGridModule,
        SharedModule
    ]
})
export class ComponentModule { }

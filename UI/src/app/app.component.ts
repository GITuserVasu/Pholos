import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
//import { AgGridAngular } from 'ag-grid-angular';
import { AIpredictionmodelsComponent } from 'component/aipredictionmodels.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'devtestholos';
}

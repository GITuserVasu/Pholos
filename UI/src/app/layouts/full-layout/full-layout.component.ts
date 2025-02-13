import { Component, OnInit } from '@angular/core';
import {RouterModule} from '@angular/router' ;

@Component({
    selector: 'app-full-layout',
    imports: [RouterModule],
    templateUrl: './full-layout.component.html',
    styleUrls: ['./full-layout.component.css'],
    standalone: true
})
export class FullLayoutComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}

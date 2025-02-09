import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router' ;
import {HeaderComponent } from '../../shared/template/header/header.component' ;
import {FooterComponent } from '../../shared/template/footer/footer.component' ;
import {SideNavComponent } from '../../shared/template/side-nav/side-nav.component' ;

@Component({
    selector: 'app-common-lauout',
    imports: [RouterModule , HeaderComponent, FooterComponent, SideNavComponent],
    templateUrl: './common-lauout.component.html',
    styleUrls: ['./common-lauout.component.css'],
    standalone: true
})
export class CommonLauoutComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}

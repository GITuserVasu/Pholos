import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../../../src/app/shared/services/user.service';

@Component({
    selector: 'app-userlist',
    templateUrl: './userlist.component.html',
    styleUrls: ['./userlist.component.css'],
    standalone: false
})
export class UserlistComponent implements OnInit {
  org_id:any;
  userList:any;
  constructor(private _user:UserService) { 
    this.org_id = window.localStorage.getItem('org_id');
  }

  ngOnInit(): void {
    this.getUserList();
  }

  getUserList(){
    this._user.getUser(this.org_id).subscribe((result:any)=>{
      this.userList = result.data;
    })
  }
}

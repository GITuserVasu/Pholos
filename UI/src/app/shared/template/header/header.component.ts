import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/login/auth.service';
import { LoginService } from '../../services/login/login.service';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.css'],
    standalone: true
})
export class HeaderComponent implements OnInit {
  info: any;
  expireDate: any;
  currentDate: any;
  packagestatus:boolean = true;
  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.info = localStorage.getItem("info")

    this.info = JSON.parse(this.info)
    console.log("info", this.info)
    console.log("this.info", this.info.CreatedDate.split("T")[0]);
    var date = new Date(this.info.CreatedDate.split("T")[0]);
    // alert(this.info.CreatedDate.split("T")[0])
// alert(this.info.packegStatus)
    if(this.info.packegStatus == 'Individual'){
      // alert("Hi")
      date.setDate(date.getDate() + 30);
      var date1 = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();
      // alert(month)
      //alert(month+'/'+date +'/'+year);
      this.expireDate = year + '-' + month + '-' + date1
    }else if(this.info.packegStatus == 'free'){
      date.setDate(date.getDate() + 7);
      var date1 = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();
      // alert(month)
      //alert(month+'/'+date +'/'+year);
      this.expireDate = year + '-' + month + '-' + date1
    }else if(this.info.packegStatus == "Small Business"){
 // alert("Hi")
 date.setDate(date.getDate() + 30);
 var date1 = date.getDate();
 var month = date.getMonth() + 1;
 var year = date.getFullYear();
 // alert(month)
 //alert(month+'/'+date +'/'+year);
 this.expireDate = year + '-' + month + '-' + date1
    }
    
   

    // alert(this.expireDate)
    //CURENT DATE 

    var date_1 = new Date();
    
    // date.setDate(date.getDate());
    var date2 = date_1.getDate();
    var month2 = date_1.getMonth() + 1;
    var year2 = date_1.getFullYear();
    // alert(month2)
    //alert(month+'/'+date +'/'+year);
    this.currentDate = year2 + '-' + month2 + '-' + date2

    var x = new Date(this.expireDate)

    console.log("currentDatecurrentDatecurrentDatecurrentDate", this.currentDate)
    console.log("expireDateexpireDateexpireDateexpireDateexpireDate", this.expireDate)

    if(+date_1 >= +x){
      this.packagestatus = false
    }else{
      this.packagestatus = true
    }

  }

  logout() {
    this.auth.logOut();
  }

}

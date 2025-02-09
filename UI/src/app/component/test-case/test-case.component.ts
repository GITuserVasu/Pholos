import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { environment } from '../../../../src/environments/environment';

@Component({
    selector: 'app-test-case',
    templateUrl: './test-case.component.html',
    styleUrls: ['./test-case.component.css'],
    standalone: false
})
export class TestCaseComponent implements OnInit {
  insurancemenuShow:any = false;
  legalmenuShow:any = false;
  realestatemenuShow:any = false;
  healthmenuShow:any = false;
  insuranceShow:any = false;
  legalShow:any = false;
  realestateShow:any = false;
  healthShow:any = false
  UCdata: any;
  UCnewdata: any;
  UCpageData: any;
  useCaseparam: any;
  industry: any;
  title: any;
  userPersona: any;
  process: any;
  description: any;
  processDiagram: any;
  input: any;
  sampleInput: any;
  output: any;
  sampleOutput: any;
  videoLink: any;
  otherLink: any;
  otherCollateral: any;

  constructor(private activateroute:ActivatedRoute,private http:HttpClient,private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }
  
  insurancemenu(){
    this.insurancemenuShow = true;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = false;
  }
  healthmenu(){
    this.insurancemenuShow = false;
    this.healthmenuShow = true;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = false;
  }
  legalmenu(){
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = true;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = false;
  }
  realestatemenu(){
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = true;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = false;
  }
  PolicyValuation(){
    // Call the python function to read the appropriate file from the server
    // Server file location can be /var/www/html/ocrApp/assets/USECASES/filename
    // Get the data in the file
    // Changed on 8/29/2023 from reading a file to reading the DB
    // const industry = "Insurance"
    // const useCaseName = "Policy Valuation"
    this.useCaseparam = "Insurance"+"-"+"Policy Valuation"
    this.getUseCaseData(this.useCaseparam)
    /* this.http.get(environment.apiUrl+'get_usecasedata/'+this.useCaseparam).subscribe((res:any) => {
      this.UCdata =res.response;
      this.industry = this.UCdata.industry ;
      this.title = this.UCdata.title ;
      this.userPersona = this.UCdata.userPersona;
      this.process = this.UCdata.process;
      this.description = this.UCdata.description;
      this.processDiagram = this.UCdata.processDiagram;
      this.input = this.UCdata.input ;
      this.sampleInput = this.UCdata.sampleInput ;
      this.output = this.UCdata.title ;
      this.sampleOutput = this.UCdata.title ;
      this.videoLink = this.UCdata.title ;
      this.otherLink = this.UCdata.title ;
      this.otherCollateral = this.UCdata.title ;
      //this.UCdata =res.response[0].data;
      console.log("this.data before", this.UCdata)
      //this.UCdata = this.UCdata.split("\\n")
      //this.UCnewdata = this.UCdata.split("|")

      this.UCpageData = this.UCdata
    }) */
    // Pass it to the html and display the same
    // Will have to work on the formatting on the html side
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = true;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = false;
  }
  health(){
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = true;
    this.realestateShow = false;
    this.legalShow = false;
  }
  legal(){
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = false;
    this.legalShow = true;
  }
  realestate(){
    this.insurancemenuShow = false;
    this.healthmenuShow = false;
    this.realestatemenuShow = false;
    this.legalmenuShow = false;
    this.insuranceShow = false;
    this.healthShow = false;
    this.realestateShow = true;
    this.legalShow = false;
  }

  getUseCaseData(UCparam:any){
  this.http.get(environment.apiUrl+'get_usecasedata/'+UCparam).subscribe((res:any) => {
    this.UCdata =res.response;
    this.industry = this.UCdata.industry ;
    this.title = this.UCdata.title ;
    this.userPersona = this.UCdata.userPersona;
    this.process = this.UCdata.process;
    this.description = this.UCdata.description;
    this.processDiagram = this.UCdata.processDiagram;
    this.input = this.UCdata.input ;
    this.sampleInput = this.UCdata.sampleInput ;
    this.output = this.UCdata.title ;
    this.sampleOutput = this.UCdata.sampleOutput ;
    this.videoLink = this.UCdata.videoLink ;
    this.otherLink = this.UCdata.otherLink ;
    this.otherCollateral = this.UCdata.otherCollateral ;
    //this.UCdata =res.response[0].data;
    console.log("this.data before", this.UCdata)
    //this.UCdata = this.UCdata.split("\\n")
    //this.UCnewdata = this.UCdata.split("|")

    this.UCpageData = this.UCdata
  })
}

}

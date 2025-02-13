import { HttpClient } from '@angular/common/http';
//type HttpClient = typeof HttpClient ;
import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
//import { FormBuilder, FormGroup, Validators } from '@angular/forms';
//import { FormGroup as AngularFormGroup} from '@angular/forms';
//import { FormBuilder as AngularFormBuilder } from '@angular/forms';
//type FormGroup = typeof AngularFormGroup;
//type FormBuilder = typeof AngularFormBuilder ;
import { Router } from '@angular/router';
//type Router = typeof Router ;
import { NgxSpinnerService } from 'ngx-spinner';
import { NotificationService } from '../../../../src/app/shared/services/notification.service';
import { environment } from '../../../../src/environments/environment';

import fetch from 'node-fetch';

// for OpenLayers
import Style from 'ol/style/Style' ;
//import Draw, { createBox, createRegularPolygon } from 'ol/interaction/Draw';
import Draw from 'ol/interaction/Draw';

import {createBox} from 'ol/interaction/Draw';
import {createRegularPolygon}  from 'ol/interaction/Draw';
import Map from 'ol/Map';
import Polygon from 'ol/geom/Polygon';
import View from 'ol/View';
import { OSM, Vector as VectorSource } from 'ol/source';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import Vector from "ol/layer/Vector";
//import  "ol/geom/Geometry";
import {transform} from 'ol/proj';
import Feature from 'ol/Feature';
import Geometry from 'ol/geom/Geometry';
import * as proj from 'ol/proj';
import Source from 'ol/source/Source';
import Layer from 'ol/layer/Layer';
import Point from 'ol/geom/Point';
import * as Coordinate from 'ol/coordinate';
import {fromLonLat} from 'ol/proj';


@Component({
    selector: 'app-ocrscreen',
    templateUrl: './ocrscreen.component.html',
    styleUrls: ['./ocrscreen.component.css'],
    standalone: false
})
export class OcrscreenComponent implements OnInit {
  fileUpload!: UntypedFormGroup;
  setProjectform!: UntypedFormGroup;
  UploadX!: UntypedFormGroup;
  UploadCUL!: UntypedFormGroup;
  searchForm!: UntypedFormGroup;
  file: any;
  fileList: string[] = [];
  invoiceDataFieleName: string[] = [];
  invoiceDataFiele: string[] = [];
  data: any;
  pageData: any;
  pageDataArray: any;
  numPages: any;
  pdfSrc: any;
  flag: boolean = false;
  isPdfUploaded: boolean = false;
  Create_new: boolean = false;
  Create_existing: boolean = false;
  Create_default: boolean = false;
  Create_folder_new: boolean = false;
  Create_folder_existing: boolean = false;
  Create_folder_default: boolean = false;
  Create_search_new: boolean = false;
  Create_search_existing: boolean = false;
  Create_search_default: boolean = false;
  projectList: any;
  radiobuttonchangevalue4: any;
  radiobuttonchangevalue3: any;
  radiobuttonchangevalue2: any;
  radiobuttonchangevalue1: any;
  radiobuttonchangevalue: any;
  ocrtarget_value: any = 'Amazon Textract';
  targetfolder_value: any;
  orgid: any ;
  username: any;
  folderList: any ;
  searchList: any ;
  searchtextwords: any ;
  info: any;
  expireDate: any;
  currentDate: any;
  documentNo: any;
  pageCount: any;
  mymap: any;
  mydraw:any;
  product_choice: any;
  coordinates: any;
  string_coords: any;
  useExistingFarm: boolean =  false;
  createNewFarm: boolean =  false;
  Xfile_as_string:any = "";
  Xfile :any;
  Xfilename: any="";
  XfileList: any;
  CULfile_as_string:any = "";
  CULfile: any;
  CULfilename: any="";
  CULfileList: any;
  plantingmethodvalue:string =  "";
  farmlist: any;
  farmdetails: any;
  X_existing_new:any = "Default";
  CUL_existing_new:any = "Default";
  farm_existing_new:any;
  Xfile_flag: any = 1;
  CULfile_flag: any = 1;
  farmname : any ;
  farmsavedflag: any = 0;

  erroranywhere:any = 0;

  userlon:any;
  userlat:any;
  lonlatarray:number[] = [];
  periodvalue: string = "";
  climatemodelvalue: string = "";
  climatescenariovalue: string = "";
  countryvalue: string = "";
  //ccatmco2:any;
  //period:any;
  myarea:any;

  city:string = "";
  state:string = "";
  country:string = "";

  //pdfSrc = "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf";
  //constructor(private spinner: NgxSpinnerService, private fb: FormBuilder, private http: HttpClient, private notification: NotificationService, private router: Router) {addInteraction(); }
  constructor(private spinner: NgxSpinnerService, private fb: UntypedFormBuilder, private http: HttpClient, private notification: NotificationService, private router: Router) { }
  //constructor(private spinner: NgxSpinnerService, private fb: typeof UntypedFormBuilder, private http: typeof HttpClient, private notification: NotificationService, private router: typeof Router) { };

  clear_map = 0
  raster = new TileLayer({
    source: new OSM(),
  });
  source = new VectorSource({ wrapX: false });
  vector = new VectorLayer({
    source: this.source,
  });

  // typeSelect = document.getElementById('type') as HTMLSelectElement;
  
  ngOnInit(): void {
    this.getSetProject()

    this.setProjectform = this.fb.group({
      existingProject: [''],
      projectName: [''],
      newFolder: [''],
      oldFolder: [''],
      file: ['', Validators.required],
    })
    this.UploadX = this.fb.group({

    })

    this.UploadCUL = this.fb.group({

    })

    this.fileUpload = this.fb.group({
      file: ['', Validators.required]
    })
    
    this.searchForm = this.fb.group({
      newSearch: [''],
      oldSearch: [''],
      file: ['', Validators.required],
    })

    this.spinner.show();

    setTimeout(() => {
      /** spinner ends after 5 seconds */
      this.spinner.hide();
    }, 1000);


    this.info = localStorage.getItem("info")

    this.info = JSON.parse(this.info)
    console.log("this.info", this.info);



    //CURENT DATE 

    var date_1 = new Date();
    var day1 = date_1.getDate();
    var day2 ="";
    if (day1 < 10) {day2 = "0"+ day1 ;} else {day2 = String(day1);}
    var month1 = date_1.getMonth() + 1;
    var month2 ="";
    if (month1 < 10) {month2 = "0"+ month1 ;} else {month2 = String(month1);}
    var year2 = date_1.getFullYear(); 
   
    this.currentDate = year2 + '-' + month2 + '-' + day2

    // Start Open Layers
    this.countryvalue = "NotSelected" ;
    this.createNewMap();
    // End Open Layers

  } // End ngOn Init

   createNewMap(){  
    /* var lonlatfromname :any ;
    lonlatfromname = fetch('https://nominatim.openstreetmap.org/search?addressdetails=1&q=davis+california&format=jsonv2&limit=1', {
                     method: 'GET',
                     headers: {
                     Accept: 'application/json',
      },
    });
    if (!lonlatfromname.ok) {
      throw new Error(`Error! status: ${lonlatfromname.status}`);
    }
    var lonlatresult = lonlatfromname.json() ;
    console.log('result is: ', JSON.stringify(lonlatresult, null, 4)); */

    console.log(this.info.city, this.info.state, this.info.country);
    
    var lon:any;
    var lat:any;

    if(this.countryvalue == "NotSelected") {
    if(this.info.city != null){this.city = this.info.city;} else{this.city = "";}
    if(this.info.state != null){this.state = this.info.state;} else{this.state = "";}
    if(this.info.country != null){this.country = this.info.country;} else{this.country = "";}
    } else {
      const countrystate = this.countryvalue.split("|")
      console.log("before split", countrystate);
      this.city ="";
      this.state = countrystate[1];
      this.country = countrystate[0] ;
    }
    console.log("state", this.state);
    console.log("country", this.country);

    var myURL = "https://nominatim.openstreetmap.org/search?addressdetails=1&q="+this.city+"+"+this.state+"+"+this.country+"&format=jsonv2&limit=1"
    //var myURL = "https://nominatim.openstreetmap.org/search?addressdetails=1&q=davis+california&format=jsonv2&limit=1";
    this.http.get(myURL).subscribe((data: any) => {
      if (data.length != 0){
      console.log("Data from nominatim", data);
      this.userlon = data[0]["lon"];
      this.userlat = data[0]["lat"];
      console.log("lon", this.userlon);
      console.log("lat", this.userlat);
    
    var templon:any;
    var templat:any;
    if (this.userlon == 0) {
      console.log("templon is zero");
      templon = 8677393.50021071;
    } else {
      templon = this.userlon;
      console.log(templon);
    }
    if (this.userlat == 0) {
      console.log("templat is zero");
      templat = 1072418.425384313 ;
    } else {
      templat = this.userlat;
      console.log(templat);
    }
    this.lonlatarray = [templon,templat];
    console.log(this.lonlatarray[0]);
    console.log(this.lonlatarray[1]);
    this.lonlatarray = fromLonLat(this.lonlatarray,'EPSG:3857');
    console.log(this.lonlatarray[0]);
    console.log(this.lonlatarray[1]);
    lon = this.lonlatarray[0];
    lat = this.lonlatarray[1]; 
  } else {
    lon = 8677393.50021071;
    lat = 1072418.425384313;
  }

    this.mymap = new Map({
      layers: [this.raster, this.vector],
      target: 'map',
      view: new View({
        //center: [8573440.974117048, 1229715.2544146648],
        //center: [8677393.50021071, 1072418.425384313],
        center: [lon, lat],
        zoom: 8,
      }),
    });
      
    this.createInteraction();

  })
    
   }  // end createNewMap

   createInteraction(){
    
    this.mydraw = new Draw({
      "source": this.source,
      "type": "Polygon",
    //  "geometryFunction": geomFunction,
    });
     if (this.clear_map == 0){
    this.mymap.addInteraction(this.mydraw);
    } else {
    this.mymap.removeInteraction(this.mydraw)
  } 
  this.mydraw.on('drawend', (event:any) => {
    const feature = event.feature;
    const feature_clone = feature.clone();
    const geometry = feature.getGeometry();
    const geometry_clone = feature_clone.getGeometry();
    geometry_clone.transform('EPSG:3857', 'EPSG:4326')
    this.coordinates = geometry_clone.getCoordinates();
    const nucoordinates = geometry.getCoordinates();
    //const nucoordinates = transform(coordinates[0][0],'EPSG:3857', 'EPSG:4326');
    console.log(this.coordinates); // Output the coordinates to console
    console.log(this.coordinates[0]);
    console.log(nucoordinates);
   this.string_coords = JSON.stringify(this.coordinates);
   console.log("after json stringify", this.string_coords);
    
   var mypolygon = new Polygon(nucoordinates);
   this.myarea = mypolygon.getArea();
   console.log("Area", this.myarea);

  }); 

   } // end createInteraction


clearMap(event:any){
  

if(this.vector != null){
this.vector.getSource()?.clear();
}

} // end clearMap

undolastpoint(event:any) {

  this.mydraw.removeLastPoint();

}

selectonchange(value:string) {
 
  this.plantingmethodvalue  = value;
 

}

countryselectonchange(value:string) {
 
  this.countryvalue  = value;
  //console.log(this.countryvalue);
  if (this.mymap){
  this.mymap.setTarget(null);
  }
  this.createNewMap();
 

}

periodselectonchange(value:string) {
 
   this.periodvalue  = value;
 
 
 }

 climatemodelselectonchange(value:string) {
  
   this.climatemodelvalue  = value;
  
 
 }

 climatescenarioselectonchange(value:string) {
  
   this.climatescenariovalue  = value;
  
 
 }

showFarm(value:string) {
//showFarm({id,name}) : void{  
  
   //alert("Farm Selected changed");
   console.log("Calling get farm details");
   let coords: any = [];
   const farmid = value;
   //const farmid = id;
   console.log(farmid)
    this.http.get(environment.apiUrl + 'getfarmdetails' + '?farmid=' + farmid ).subscribe((data: any) => {
      console.log("Data in getfarmdetails", data.response);

    const b = data.response;
    //const b = JSON.parse(data.response);
    this.farmname = b['farmname'];
    console.log("b",b);
    console.log("farmname",this.farmname);

    console.log("farmarea", b['farmarea']);

    console.log("b",b['polygon_coords']);
    var final_coords: any = '';
    
    var coordsa = b['polygon_coords'];
    console.log("coordsa", coordsa);
    var coordsb = JSON.parse(coordsa);
    console.log("coordsb", coordsb);
    var numpoints = coordsb[0].length;
    console.log("numpoints",numpoints);
    for (let i = 0; i < numpoints; i++) {
      var coordscc = coordsb[0][i]
      console.log("coordscc",coordscc);
      coords[i] = transform(coordscc,  'EPSG:4326', 'EPSG:3857');
      console.log("coordsi", coords[i]);
      if (i == numpoints -1){
      final_coords = final_coords+"["+coords[i]+"]";
      } else {
        final_coords = final_coords+"["+coords[i]+"],";
      }
      console.log("final",final_coords);
    }
    final_coords = "[["+final_coords+"]]"; 
    console.log("final coords",final_coords);

    var mylon = coords[0][0] ;
    var mylat = coords[0][1] ;

    if (this.mymap){
      this.mymap.setTarget(null);
      }
    this.mymap = new Map({
        layers: [this.raster, this.vector],
        target: 'map',
        view: new View({
          //center: [8573440.974117048, 1229715.2544146648],
          //center: [8677393.50021071, 1072418.425384313],
          center: [mylon, mylat],
          zoom: 8,
        }),
      });
    

    var marker = new Feature({
      //geometry: new Point(transform([77.02657421147529,11.051931828419981], 'EPSG:4326', 'EPSG:3857')),
      geometry: new Polygon(JSON.parse(final_coords)),      
    });
  
  var markers = new VectorSource({
      features: [marker]
  });
  
  var markerVectorLayer = new VectorLayer({
      source: markers,
  });
  this.mymap.addLayer(markerVectorLayer);

    })    
 
 }

 
  saveFarm(event:any) {
   
   this.farmsavedflag = 0;
   const roiname = document.getElementById('roiname') as HTMLInputElement | null;
    let roinamevalue = roiname?.value;
    if (roinamevalue == null) {roinamevalue = "None"};
    this.farmname = roinamevalue ;
   const farmInfo = {
    "companyID":this.info.orgid,
    "UserID": this.info.id,
    "Coordinates": this.string_coords,
    "farmname":roinamevalue,
    "farmarea":this.myarea
    //"farmdesc":farmdesc
    }
   console.log(farmInfo["UserID"]);
   
   this.http.post(environment.apiUrl + 'createFarm', farmInfo).subscribe((farmdata: any) => {
     console.log('resstatusCodestatusCode in create farm save farm', farmdata.statusCode);
     if (farmdata.statusCode == 200) {
       console.log("Farm record created");
       //console.log(farmdata.farmname);
       alert ("Farm Saved; You can reuse this farm in future experiments");
       this.farmsavedflag = 1 ;
     }
     })
   
  
  }
  
  uploadFile(event: any) {

      const numFiles = (event.target.files).length;
      console.log("num of files", numFiles);
      
       for (let i = 0; i < numFiles; i++) {
        const reader: any = new FileReader();
        const fileInfo = event.target.files[i];
      this.invoiceDataFiele[i] = event.target.files[i];
      this.invoiceDataFieleName[i] = event.target.files[i].name;

        if (this.Create_new == true && this.Xfile_flag == 1){
        reader.onload=()=> {this.Xfile_as_string = reader.result as string;};
        this.Xfile = event.target.files[i];
        this.Xfilename = event.target.files[i].name;
        
        this.Xfile_flag = 0 ;
        //this.Create_new = false;
        }
        if (this.Create_folder_new == true && this.CULfile_flag == 1){
          reader.onload=()=> {this.CULfile_as_string = reader.result as string;};
          this.CULfile = event.target.files[i];
          this.CULfilename = event.target.files[i].name;
          this.CULfile_flag = 0 ;
          //this.Create_folder_new = false;
          }
        reader.readAsText(event.target.files[i]); 
        //console.log("reader result", this.Xfile_as_string);
     }
    
  }
  onSubmit() {
    this.erroranywhere = 0 ;
    const numyears = document.getElementById('numyears') as HTMLInputElement | null;
    var numyearsvalue = numyears?.value;
    if(this.product_choice == "CLIMCHNG") {numyearsvalue = "1";}

    const subblocksize = document.getElementById('subblocksize') as HTMLInputElement | null ;
    const subblocksizevalue = subblocksize?.value ; 
    const mydate = document.getElementById("tgtplantingdate") as HTMLInputElement;
    const mydatevalue = mydate.value ;

    const farmSelect = document.getElementById('selectedfarm') as HTMLSelectElement;
    const XfileSelect = document.getElementById('selectedXfile') as HTMLSelectElement;
    const CULfileSelect = document.getElementById('selectedCULfile') as HTMLSelectElement;

    const plantingmethodSelect = document.getElementById('plantingmethod') as HTMLSelectElement;
    this.plantingmethodvalue = plantingmethodSelect?.value ; 
    const periodSelect = document.getElementById('period') as HTMLSelectElement;
    var periodvalue = periodSelect?.value ; 
    if(periodvalue == "" || periodvalue === undefined) {
      periodvalue = "none"; // default value
    }
    const modelSelect = document.getElementById('climatemodel') as HTMLSelectElement;
    var modelvalue = modelSelect?.value ; 
    if(periodvalue == "baseline"){modelvalue = "none";}
    if(modelvalue == "" || modelvalue === undefined) {
      modelvalue = "none"; // default value
    }

    
    const scenarioSelect = document.getElementById('climatescenario') as HTMLSelectElement;
    var scenariovalue = scenarioSelect?.value ; 
    if(periodvalue == "baseline"){scenariovalue = "none";}
    if(scenariovalue == "" || scenariovalue === undefined) {
      scenariovalue = "none"; // default value
    }

    



    var tempprojectName =  this.setProjectform.controls['projectName'].value 
    if (tempprojectName == '') {
      alert("Project Name cannot be blank");
      location.reload();
    }

   
    
    //const farmid = farmSelect.value;
    //var Xfileexisting = "";
    //var CULfileexisting = "";

    var Xfileid = "";
    var CULfileid = "";

  
    //if (XfileSelect != null){
    var Xfileexisting = XfileSelect?.value;
    var Xfileid = XfileSelect?.value;
    //}

   
    if (this.Create_existing == true){ 
      this.X_existing_new = "existing";
    }
   
    if (this.Create_new == true){  this.X_existing_new = "new" ;}

    console.log("X existing new", this.X_existing_new);

    //if (CULfileSelect != null) {
    var CULfileexisting = CULfileSelect?.value;
    var CULfileid = CULfileSelect?.value;
    //}

    if (this.Create_folder_existing == true){ 
      this.CUL_existing_new = "existing";
    }
    if (this.Create_folder_new == true){ this.CUL_existing_new = "new"}

    console.log("CUL existing new", this.CUL_existing_new);
    
    var farmid = "0";
    if (this.useExistingFarm == true){ 
      this.farm_existing_new = "existing";
      farmid = farmSelect.value;
      
    }
    if (this.createNewFarm == true){ 
      this.farm_existing_new = "new";
      if(this.farmsavedflag == 0){
        this.saveFarm("event");
      }

    }

    var x = mydatevalue?.split("-");  
      var tpyear = x[0] ;
      var tpmonth = x[1] ;
      tpmonth = tpmonth.replace(/^0+/, '');
      var tpday = x[2] ;
      tpday = tpday.replace(/^0+/, '');
    
    /* const analogyear = document.getElementById('analogyear') as HTMLInputElement | null;
    var analogyearvalue = analogyear?.value ; */

    // if(this.product_choice == "CLIMCHNG") {
      var analogyearvalue = "2017"; // default value
    // }

    /* if(analogyearvalue == ""){
      alert("Please enter Analog Year Value and then reSubmit");
      this.erroranywhere = 1 ;
    } */

    const ccatmco2 = document.getElementById('co2level') as HTMLInputElement | null;
    var ccatmco2value = ccatmco2?.value ;

    if(ccatmco2value == "" || ccatmco2value === undefined) {
      ccatmco2value = "100"; // default value
    }

    if(ccatmco2value == ""){
      alert("Please enter Atmospheric CO2 level and then reSubmit");
      this.erroranywhere = 1 ;
    }

    const plantdensity = document.getElementById('plantdensity') as HTMLInputElement | null;
    const plantdensityvalue = plantdensity?.value;

    if(plantdensityvalue == ""){
      alert("Please enter Plant Density Value and then reSubmit");
      this.erroranywhere = 1 ;
    }


    const roiname = document.getElementById('roiname') as HTMLInputElement | null;
    let roinamevalue = roiname?.value;
    if (roinamevalue == null) {roinamevalue = "None"};
    if (this.farm_existing_new == "new"){
      this.farmname = roinamevalue ;
    }
    
    if(this.X_existing_new == "new"){
      
    this.Xfile_as_string = this.Xfile_as_string.replaceAll("\r\n","\\n");
    this.Xfile_as_string = this.Xfile_as_string.replaceAll("\n","\\n");
    this.Xfile_as_string = this.Xfile_as_string.replaceAll("\u001a","\\u001a");
    }
    if(this.X_existing_new == "existing"){
      this.Xfilename = Xfileexisting
    
    }
     
    if(this.CUL_existing_new == "new"){
      
    this.CULfile_as_string = this.CULfile_as_string.replaceAll("\r\n","\\n");
    this.CULfile_as_string = this.CULfile_as_string.replaceAll("\n","\\n");
    }
    if(this.CUL_existing_new == "existing"){
      this.CULfilename = CULfileexisting
    }
    
    const simulationname = this.setProjectform.controls['projectName'].value;
    
    const exptJson = {
    "companyID":this.info.orgid,
    "UserName": this.info.name,
    "UserEmailID": this.info.email,
    "SimulationName" : simulationname,
    "SelectedHolosProduct": this.product_choice,
    "Coordinates": this.string_coords,
    "Xfile_as_string":this.Xfile_as_string,
    "Xfilename":this.Xfilename,
    "CULfile_as_string":this.CULfile_as_string,
    "CULfilename":this.CULfilename,
    "nyers":numyearsvalue,
    "subblocksize": subblocksizevalue,
    "analogyear": analogyearvalue,
    "plantdensity": plantdensityvalue,
    "plantingmethod":this.plantingmethodvalue,
    "roiname":roinamevalue,
    "tpyear":tpyear,
    "tpmonth":tpmonth,
    "tpday":tpday,
    "farm_existing_new":this.farm_existing_new,
    "farmid":farmid,
    "X_existing_new":this.X_existing_new,
    //"Xfileid":Xfileid,
    "CUL_existing_new": this.CUL_existing_new,
    //"CULfileid":CULfileid
    "ccperiod":periodvalue,
    "ccmodel":modelvalue,
    "ccscenario":scenariovalue,
    "ccatmco2":ccatmco2value,
    "city":this.city,
    "state":this.state,
    "country":this.country
    }
    console.log("CCATMCO2",exptJson["ccatmco2"]);
    this.http.post(environment.apiUrl + 'make_json', exptJson).subscribe((jsondata: any) => {
      console.log('resstatusCodestatusCode in Submit make json', jsondata.statusCode);
      if (jsondata.statusCode == 200) {
        this.erroranywhere = 0;
        console.log("JSON Success");
        console.log(jsondata.name);
      } else {
        alert('Error in submission. Did you forget to enter the Planting Date?');
        this.erroranywhere = 1;
        location.reload();
      }
    //  })
      
   

    // if (this.radiobuttonchangevalue == 'New') {
      var data = {
        "setProjectName": this.setProjectform.controls['projectName'].value,
        "bname": this.info.bname,
        "email": this.info.email,
        "orgid": localStorage.getItem('org_id'),
        "username": this.info.name
      }
      this.http.post(environment.apiUrl + "setProject", data).subscribe((res: any) => {
        console.log("New Project Created Successfully")
      })
    // }

    const numFiles = (this.invoiceDataFiele).length
    console.log("num of files invoiceDataFiele", numFiles)

    const formData = new FormData();        
    //const CreatedDate = this.currentDate;
    const CreatedDate = new Date() ;
    
    console.log("X file name before adding to DB", this.Xfilename);
   
    console.log("CUL file name before adding to DB", this.CULfilename);
    //createing the casedetailas
    // for (let i = 0; i < numFiles; i++) {
    var casedetials = {
      status: "Inprogress",
      fileName: "not used",
      //fileName: this.invoiceDataFieleName[i],
      XfileName: this.Xfilename,
      CULfileName: this.CULfilename,
      orgid: localStorage.getItem("org_id"),
      projectType: "New",
      projectName: this.setProjectform.controls['projectName'].value ,
      folderType: "Not Used",
      folderName: "Not Used",
      // ocrType: this.ocrtarget_value,
      ocrType: "Various",
      targetfiles: "Not Used",
      empOrgid: localStorage.getItem("empOrgid") != '' ? localStorage.getItem("empOrgid") : null,
      searchtextwords: "Not Used",
      username:this.info.name,
      CreatedDate: CreatedDate,
      selectedholosproduct: this.product_choice,
      nyers: numyearsvalue,
      subblocksize: subblocksizevalue,
      analogyear: analogyearvalue,
      plantdensity: plantdensityvalue,
      plantingmethod:this.plantingmethodvalue,
      farmid:farmid,
      farmname: this.farmname,
      plantingdate: mydatevalue
    }

    console.log("casedetials...", casedetials);

    this.http.post(environment.apiUrl + "Case_Detiles/", casedetials).subscribe((res: any) => {
      console.log("myresres");
      console.log('res');
      this.data = res.data
      this.orgid = localStorage.getItem('org_id');
      this.username = this.info.name;
      this.username = this.username.replaceAll(" ","");
      console.log(this.orgid);
      console.log(this.username);
      if (res.errorCode == 200) {  
        if ((this.X_existing_new == "new") || (this.CUL_existing_new == "new")){
          formData.append('X_existing_new', this.X_existing_new);
          formData.append('CUL_existing_new', this.CUL_existing_new);
        formData.append('userid', this.info.id);
        //formData.append('file', this.invoiceDataFiele[i]);
        formData.append('Xfilename', this.Xfilename);
        formData.append('Xfile', this.Xfile);
        formData.append('CULfile', this.CULfile);
        formData.append('CULfilename', this.CULfilename);
        formData.append('caseId', res.response.id);
        formData.append('orgid', this.orgid);
        this.ocrtarget_value = 'Amazon Textract'
        formData.append('ocrType', this.ocrtarget_value);
        formData.append('projectname', `${this.radiobuttonchangevalue == 'New' ? this.setProjectform.controls['projectName'].value : this.setProjectform.controls['existingProject'].value}`);
        formData.append('path', `${this.orgid.toString()}/${this.username.toString()}`);
        this.http.post(environment.apiUrl + 'pdf_to_img/', formData).subscribe((ocrdata: any) => {
            console.log('resstatusCodestatusCode in Submit pdf to img', ocrdata.statusCode);
            if (ocrdata.statusCode == 200) {
              console.log("Call to pdf_to_img successful");
            }
          })
        } // if X or CUL file is new

        this.erroranywhere = 0;

      }  else {  // if res code <> 200

        this.erroranywhere = 1;

      }
    })
  })  // end JSON submit to AWS
  if( this.erroranywhere == 0){
  this.notification.showSuccess("Successfully Submitted, Check back in a while for results ", "Submit Another or go to Dashboard to check on Status");
        //this.router.navigate(['/'])
  }
  //  } // end for
  } // end OnSubmit


  


  radiobuttonchange(event: any) {
   
    this.radiobuttonchangevalue = event.target.value

    if (event.target.value == "New") {
      this.Create_existing = false;
      this.Create_new = true;
      this.Create_default = false;
    } else if (event.target.value == "Existing") {
      this.getXfilelist(event);
      this.Create_existing = true;
      this.Create_new = false;
      this.Create_default = false;
    } else {
      this.Create_existing = false;
      this.Create_new = false;
      this.Create_default = true;
    }
 
  }
  radiobuttonchange1(event: any) {
  
    this.radiobuttonchangevalue1 = event.target.value

    if (event.target.value == "New") {
      this.Create_folder_existing = false;
      this.Create_folder_new = true;
      this.Create_folder_default = false;
    } else if (event.target.value == "Existing") {
      this.getCULfilelist(event);
      this.Create_folder_existing = true;
      this.Create_folder_new = false;
      this.Create_folder_default = false;
    } else {
      this.Create_folder_existing = false;
      this.Create_folder_new = false;
      this.Create_folder_default = true;
    }
  }

  radiobuttonchange2(event: any) {
    
    this.radiobuttonchangevalue2 = event.target.value

    if (event.target.value == "New") {
      this.Create_search_existing = false;
      this.Create_search_new = true;
      this.Create_search_default = false;
    } else if (event.target.value == "Existing") {
      this.Create_search_existing = true;
      this.Create_search_new = false;
      this.Create_search_default = false;
      this.getSetSearch(event)
    } else {
      this.Create_search_existing = false;
      this.Create_search_new = false;
      this.Create_search_default = true;
    }
  }

  radiobuttonchange3(event: any) {
    
    this.radiobuttonchangevalue3 = event.target.value
    this.product_choice = "PRSEASON";
    if (event.target.value == "Pre-Season") {
      this.product_choice = "PRSEASON";
    } else if (event.target.value == "In-Season") {
      this.product_choice = "INSEASON";
    } else if (event.target.value == "Climate-Change") {
      this.product_choice = "CLIMCHNG";
    }
  }

  radiobuttonchange4(event: any) {
    
    this.radiobuttonchangevalue4 = event.target.value
    if (event.target.value == "Existing") {
      this.useExistingFarm = true;
      this.createNewFarm = false;
      this.getfarmlist(event);
    } else if (event.target.value == "New") {
      this.useExistingFarm = false;
      this.createNewFarm = true;
    } 
  }

  getSetProject() {
    this.http.get(environment.apiUrl + 'setProject_orgid/' + localStorage.getItem('org_id')).subscribe((data: any) => {
      console.log("Data", data.response);
      this.projectList = data.response
    })
  }

  getXfilelist(event: any) {
    console.log("Calling get file list");
    
    this.http.get(environment.apiUrl + 'getfilelist' + '?orgid=' + this.info.orgid +'&userid=' +this.info.id+'&filetype=Xfile').subscribe((data: any) => {
      console.log("Data in getXfileList", data.response);
      this.XfileList = data.response;
      console.log("Xfilelist");
      console.log(this.XfileList);
    })
  }

  getCULfilelist(event: any) {
    console.log("Calling get file list");
    this.http.get(environment.apiUrl + 'getfilelist' + '?orgid=' + this.info.orgid +'&userid=' +this.info.id+'&filetype=CULfile').subscribe((data: any) => {
      console.log("Data in getCULfileList", data.response);
      this.CULfileList = data.response
    })
  }

  getfarmlist(event: any) {
    console.log("Calling get farm list");
    this.http.get(environment.apiUrl + 'getfarmlist' + '?orgid=' + this.info.orgid +'&userid=' +this.info.id).subscribe((data: any) => {
      console.log("Data in getfarmlist", data.response);
      this.farmlist = data.response
    })
  }

  getSetFloder(event: any) {
    console.log("radiobuttonchangevalue1 =")
    
    this.http.get(environment.apiUrl + 'setFolder/' + event.target.value).subscribe((data: any) => {
      console.log("Data in getsetFloder", data.response);
      this.folderList = data.response
    })
  }

  getSetSearch(event: any) {
    
    this.http.get(environment.apiUrl + 'setSearch/' + localStorage.getItem('org_id')).subscribe((data: any) => {
      console.log("Data i  get set search ts", data.response);
      this.searchList = data.response
    })
  }

  uploadfiles() {

  }
  ocrtarget(event: any) {
    this.ocrtarget_value = event.target.value
    
  }
  targetfolder(event: any) {
    this.targetfolder_value = event.target.value
    
  }
  setProject() {
    
    console.log(this.setProjectform.value);
    console.log(this.ocrtarget_value);
    console.log(this.targetfolder_value);
    console.log(this.radiobuttonchangevalue);
    console.log(this.radiobuttonchangevalue1);
  }

  asyncioTextract() {

  }

  



}

import { HttpClient as HttpClient} from '@angular/common/http';
import { CommonModule } from '@angular/common' ;
import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
//import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Router } from '@angular/router';

import { NgxSpinnerService } from 'ngx-spinner';
import { NotificationService } from 'src/app/shared/services/notification.service';
import { environment } from 'src/environments/environment';

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
import {useGeographic} from 'ol/proj.js';

@Component({
  selector: 'app-aipredictionmodels',
//  imports: [ CommonModule ],
  templateUrl: './aipredictionmodels.component.html',
  styleUrls: ['./aipredictionmodels.component.css'],
  standalone:false
})

export class AIpredictionmodelsComponent implements OnInit {
  datasetvalue: string = "none";
  mymap: any;
  mydraw:any;
  coordinates: any;
  string_coords: any = "";
  userlon:any;
  userlat:any;
  lonlatarray:number[] = [];
  myarea:any;
  locationvalue:any = "none";
  clear_map :any = 0 ;
  
  //geometry = feature.getGeometry();

  raster = new TileLayer({
    source: new OSM(),
  });
  source = new VectorSource({ wrapX: false });
  vector:any ;
  /* vector = new VectorLayer({
    source: this.source,
  }); */
  locradiobuttonchangevalue: any;
  useblockname: boolean = true;
  usemap: boolean = false;
  useNN: boolean = true;
  useRandomForest: boolean = false;
  cultivarvalue: string = "none";
  preddata: any;
  orgid: string = "" ;
  username: any;
  info: any;
  modelradiobutton: any;

  


  //constructor(private spinner: NgxSpinnerService, private http: HttpClient, private notification: NotificationService, private router: Router) { };


  ngOnInit(): void {
    this.info = localStorage.getItem("info")
    this.info = JSON.parse(this.info)
    console.log("this.info", this.info);
    this.createNewMap();
  }

  createNewMap(){  
    
    var lon:any;
    var lat:any;
    
    var templon:any;
    var templat:any;
    
    var minlon, maxlon, minlat, maxlat

    var place: any;
    
    //useGeographic();
    
    var latlonstr = this.locationvalue

    if (latlonstr == null)
      latlonstr = "none"
   //console.log("lonlatstr: ", latlonstr)
   //alert(latlonstr)
   var comp_str = "none"
   //if (latlonstr.localeCompare(comp_str) != 0){
   if(latlonstr === comp_str){
   // Default
      lat = 10.95
      lon = 77.1
      place = [lat, lon]
   } else {
      var latlonarr = latlonstr.split(" ");
      lat = latlonarr[1]
      lon = latlonarr[3]
      place = [lon, lat]
   }

   this.lonlatarray = fromLonLat([lon,lat],'EPSG:3857');
    console.log(this.lonlatarray[0]);
    console.log(this.lonlatarray[1]);
    lon = this.lonlatarray[0];
    lat = this.lonlatarray[1]; 

    minlon = 76.5
    maxlon = 77.5
    minlat = 10.80
    maxlat = 11.10
    const a = fromLonLat([minlon,minlat],'EPSG:3857')
    const b = fromLonLat([maxlon,maxlat],'EPSG:3857')
    var mapextent = [a[0],a[1],b[0],b[1]];
    //alert (mapextent);
    //console.log(mapextent)

    if(this.useblockname == true){
       place = [lon,lat]
       const point = new Point(place);
       var feature1 = new Feature(new Point(place))
       /* var Feature1 = new Feature({
          name: "Points",
          geometry: feature1 
  }); */
       this.source.addFeature(feature1);
       this.vector = new VectorLayer({
        source: this.source,
        style: {
          'circle-radius': 5,
          'circle-fill-color': 'red',
        },
      });
      
    } else {
      this.vector = new VectorLayer({
        source: this.source,
      });

    }



    this.mymap = new Map({
      layers: [this.raster, this.vector],
      target: 'map',
      view: new View({
        //center: [8573440.974117048, 1229715.2544146648],
        //center: [8677393.50021071, 1072418.425384313],
        center: [lon, lat],
        zoom: 9,
        extent: mapextent,
      }),
    });
    if(this.usemap == true)  {
    this.createInteraction();
    }
    
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

   }  // end createInteraction


/*   createNewMap(){
    var lon:any;
    var lat:any;
    var place: any;
    var minlon, maxlon, minlat, maxlat
    
    useGeographic();
    //alert(this.locationvalue)
    var latlonstr = this.locationvalue

    if (latlonstr == null)
       latlonstr = "none"
    //console.log("lonlatstr: ", latlonstr)
    //alert(latlonstr)
    var comp_str = "none"
    //if (latlonstr.localeCompare(comp_str) != 0){
    if(latlonstr === comp_str){
    // Default
       lat = 10.95
       lon = 77.1
       place = [lat, lon]
    } else {
       var latlonarr = latlonstr.split(" ");
       lat = latlonarr[1]
       lon = latlonarr[3]
       place = [lon, lat]
    }
    
    const point = new Point(place);
    //const point = new Point(transform([parseFloat(lon), parseFloat(lat)], 'EPSG:4326', 'EPSG:3857'))

    var vertices = [[lon-0.1,lat+0.1], [lon+0.1, lat+0.1], [lon+0.1, lat -0.1], [lon-0.1, lat -0.1]]
    console.log("vertices", vertices)

    const mypolygon = new Polygon(vertices);

    /* console.log("lat", lat)
    console.log("lon", lon)
    console.log("point", point) */

    /* minlon = 76.78
    maxlon = 77.42
    minlat = 10.82
    maxlat = 11.09 */

    /* minlon = 70.0
    maxlon = 80.0
    minlat = 10.00
    maxlat = 11.00
    var mapextent = [minlon, minlat, maxlon, maxlat];

    
    
    var basic = new TileLayer({
      source: new OSM(),
    });

    var dotlayer = new VectorLayer({ */
      /* source: new VectorSource({
        features: [new Feature(point), new Feature(new Polygon([vertices]))],
    
      }), */
      /* source: this.source,
      style: {
        'circle-radius': 5,
        'circle-fill-color': 'red',
      },
    })

    const feature1 = new Feature({
      geometry: new Point(place),
      name: 'My Point',
    }); */
    /* var feature1 = new Feature(new Point(place))
    var Feature1 = new Feature({
      name: "Points",
      geometry: feature1
  }); */

  /* const feature2 = new Feature({
    geometry: new Polygon([vertices]),
    name: 'My Polygon',
  }); */
  

    //this.geometry = Feature.getGeometry();
    //var feature2 = new Feature(this.geometry : new Polygon([vertices]));
    //var Feature2 = new Feature({
    //   name: "Square",
    //   geometry: feature2
    //});
    //this.source.addFeature(feature1);
    //this.source.addFeature(feature2);

    /* var rectlayer = new VectorLayer({
      source: new VectorSource({
        features: [new Feature(new Polygon([vertices]))],
        
      }),
    })

    this.mymap = new Map({
      //layers: [this.raster, this.vector],

      target: 'map',
      //layers: [basic, dotlayer],
    
      layers: [
        new TileLayer({
          source: new OSM(),
        }), */
        /* new VectorLayer({
          source: new VectorSource({
            features: [new Feature(point)],
          }),
          style: {
            'circle-radius': 5,
            'circle-fill-color': 'red',
          },
        }), */
        /* new VectorLayer({
          source: new VectorSource({
            features: [new Feature(new Polygon(vertices))],
          }),
        }), */
        /* new VectorLayer({
          source: new VectorSource({
            features: [new Feature(mypolygon)],
          }),
        }),
      ],

      view: new View({
        //center: [8573440.974117048, 1229715.2544146648],
        //center: [8677393.50021071, 1072418.425384313],
        center: [lon, lat],
        zoom: 9,
        extent: mapextent,
      }),
      
    }); */
    //this.mymap.addLayer(dotlayer)
    //this.mymap.addLayer(rectlayer)
    
  // Adding a red point to the map at the lat , lon specified


  // } 

  onSubmit() {
    alert("Prediction will be available sooooooon, maybe :-)");
    //Validation
    /* if (this.datasetvalue == "none"){alert(" You must select one valid data set");location.reload();}
    if(this.useblockname == true && this.locationvalue == "none") {alert("You must select a block"); location.reload();}
    if(this.usemap == true && this.string_coords == "") {alert("You must draw a farm"); location.reload();} */
    // this.usemap
    // this.locationvalue
    // this.string_coords
    /* var pltgdate = document.getElementById("pdate") as HTMLInputElement;
    var pdate = pltgdate.value ;
    if(pdate == "") {alert("Please enter Planting Date"); location.reload();}
    if (this.useNN == false  && this.useRandomForest == false){alert("Please select a model"); location.reload();} */
    // this.useNN
    // this.useRandomForest
    /* if(this.cultivarvalue == "none") {alert("Please select a Cultivar"); location.reload();} */
    // End Validation
    
    /* this.username = this.info.name;
    this.username = this.username.replaceAll(" ","");
 */
    // Call the predict python code
/*     const predjson ={
      "dataset" : this.datasetvalue ,
      "useblockname": this.useblockname,
      "usemap": this.usemap,
      "blockname": this.locationvalue,
      "stringcoords": this.string_coords,
      "plantingdate": pdate,
      "useNN": this.useNN,
      "useRandomForest": this.useRandomForest,
      "cultivar": this.cultivarvalue,
      "orgid" : localStorage.getItem('org_id'),
      "username" : this.username
    } 

    alert(this.username); */

    /* this.http.post(environment.apiUrl + 'prednow', predjson).subscribe((res: any) => {
      console.log("myresres");
      console.log('res'); */
      //this.preddata = res.data
      /* if (res.statusCode == 200) {
        console.log(" Prednow Success");
        console.log(res.name);
      } else {
        alert('Error in submission');
      } */
      /* if (res.statusCode == 200) {  
        console.log("Prediction Routine Call was successful")
      }
    }) */


  }

  datasetselectonchange(value:string) {
    this.datasetvalue  = value;
  }

  cultivarselectonchange(value:string) {
    this.cultivarvalue  = value;
  }

  locationselectonchange(value:string) {
    this.locationvalue  = value;
    //alert(this.locationvalue);
    if (this.mymap){
      this.mymap.setTarget(null);
      }
      if(this.vector != null){
        this.vector.getSource()?.clear();
        }
      this.createNewMap();
       
  }
  locradiobuttonchange(event: any) {
   
    this.locradiobuttonchangevalue = event.target.value
    //alert(this.locradiobuttonchangevalue)

    if (event.target.value == "useblockname") {
      this.useblockname = true;
      this.usemap = false;
    } else if (event.target.value == "usemap") {
      this.usemap = true;
      this.useblockname = false;
    } 
    //alert(this.usemap)
    if (this.mymap){
      this.mymap.setTarget(null);
      }
      this.createNewMap();   
  }

  modelradiobuttonchange(event: any) {
    
    this.modelradiobutton = event.target.value
    if (event.target.value == "NeuralNetwork") {
      this.useNN = true;
      this.useRandomForest = false;
    } else if (event.target.value == "RandomForest") {
      this.useNN = false;
      this.useRandomForest = true;
    } 
  }


  clearMap(event:any){
    if(this.vector != null){
    this.vector.getSource()?.clear();
    }
    
    } // end clearMap

  undolastpoint(event:any) {

      this.mydraw.removeLastPoint();
    
    }  

}


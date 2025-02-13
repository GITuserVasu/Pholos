import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { environment } from '../../../../src/environments/environment';

@Component({
    selector: 'app-comprehend',
    templateUrl: './comprehend.component.html',
    styleUrls: ['./comprehend.component.css'],
    standalone: false
})
export class ComprehendComponent implements OnInit {
  ocrType:any;
  keyId:any;
  tableData:any;
  entities:any
  pii_entities:any
  sentiment_df:any
  Sentiment:any
  dominant_language_df:any
  Detect_Key_Phrases:any
  keyId_entities:any
  keyId_pii_entities:any
  keyId_sentiment_df:any
  keyId_Sentiment:any
  keyId_dominant_language_df:any
  keyId_Detect_Key_Phrases:any
  pageData:any
  data:any
  csvFileName:any = ["Entities.csv","pii_entities.csv","sentiment_df.csv","Sentiment.csv","dominant_language_df.csv","Detect_Key_Phrases.csv"]
  constructor(private activateroute:ActivatedRoute,private http:HttpClient,private sanitizer: DomSanitizer) { }
  ngOnInit(): void {

    this.activateroute.params.subscribe((res:any) =>{
      console.log(res.id)
      console.log("res.ocrType",res.ocrType)
      this.ocrType = res.ocrType
      if(res.ocrType == 'Amazon Textract'){

        this.http.get(environment.apiUrl+'Case_Detiles/'+res.id).subscribe((res:any) => {
          console.log('caseocrdatacaseocrdatacaseocrdata', res.response);
          // this.csvFileName.map((item:any) => {
          //   console.log("item", item)
            this.downloadFilecsv(res.response)
          // })
          
        })
        }
    })
  }

  downloadFilecsv(response:any) {
    // alert(fileName)
    var data = response[0]
    var fileFolder = data.fileName.split(".")[0]
    fileFolder = fileFolder.replaceAll(" ","-")
    

    this.csvFileName.map((fileName:any) => {
      var param1 = `${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/${fileFolder}${fileName}`
      this.http.get(environment.apiUrl+`downloadcsv/?path=${param1}`).subscribe((data: any) => {
        
        console.log("param1", param1)
        // console.log("keyId", this.keyId)
     
       if(fileName == 'Entities.csv'){
        this.keyId_entities = Object.keys(JSON.parse(data)[0])
        this.entities = JSON.parse(data)
        console.log("param1param1",this.keyId_entities)
        console.log("param1param1",this.entities)
       }
        if(fileName == 'pii_entities.csv'){
          // alert(fileName+"testing")
        this.keyId_pii_entities = Object.keys(JSON.parse(data)[0])
        this.pii_entities = JSON.parse(data)
        console.log("keyId_pii_entities",this.keyId_pii_entities)
        console.log("keyId_pii_entities",this.pii_entities)
       }
        if(fileName == 'sentiment_df.csv'){
       
        this.keyId_sentiment_df = Object.keys(JSON.parse(data)[0])
        this.sentiment_df = JSON.parse(data)[0];
        this.sentiment_df = Object.values(this.sentiment_df)[0]
        
       }
      //  if(fileName = 'Sentiment.csv'){
      //   this.keyId_Sentiment = Object.keys(JSON.parse(data)[0])
      //   this.Sentiment = JSON.parse(data)
      //  }
       if(fileName == 'Detect_Key_Phrases.csv'){
        this.keyId_Detect_Key_Phrases = Object.keys(JSON.parse(data)[0])
        this.Detect_Key_Phrases = JSON.parse(data)
       }
       if(fileName == 'dominant_language_df.csv'){
        this.keyId_dominant_language_df = Object.keys(JSON.parse(data)[0])
        this.dominant_language_df = JSON.parse(data)[0]['LanguageCode']
        console.log("keyId_dominant_language_df",this.keyId_dominant_language_df)
        console.log("dominant_language_df",this.dominant_language_df)
       }
      },
      (error: any) => {
        console.error('Error downloading file:', error);
      })
    })
   
  
  }
 
  getKeys(data: any): string[] {
    return Object.keys(data);
  }
  getValue(data: any, key: string): string {
    return data[key];
  }

}

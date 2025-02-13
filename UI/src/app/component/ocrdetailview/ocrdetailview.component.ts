import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { environment } from '../../../../src/environments/environment';


@Component({
    selector: 'app-ocrdetailview',
    templateUrl: './ocrdetailview.component.html',
    styleUrls: ['./ocrdetailview.component.css'],
    standalone: false
})
export class OcrdetailviewComponent implements OnInit {
  fileUrl:any
  file:any;
  tableData:any;
  invoiceDataFieleName:any;
  invoiceDataFiele:any;
  keyId:any;
  data:any;
  public pdfSrc:any;
  pageData:any;
  pageDataArray:any;
  page_summary:any;
  page_search_results: any;
  page_nltk_summ:any;
  page_googleT5_summ:any;
  numPages:any;
  table_summary:any;
  fileviewrshow:any;
  sanitizedUrl:any;
  ocrType:any;
  flag: boolean = false;
  isPdfUploaded: boolean = false;
  tablesData:any = [];
  tablesData1:any = [];
  tablesData2:any = [];
  tablesData3:any = [];
  tablesData4:any = [];
  tablesData5:any = [];
  tablesData6:any = [];
  tablesData7:any = [];
  tablesData9:any = [];
  caseocrdata:any;
  excelButtonlink:any;
  textButtonlink:any;
  searchText='MYXYSPTLK';
  highlightedText: any;
  filenameforzipfile: any;
  keyvaluesData: any;

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

  exptstatus: any
  projectname: any
  orgid: any
  username: any
  caseid: any

  csvFileName:any = ["Entities.csv","sentiment_df.csv","dominant_language_df.csv"]
  
  Xfilename: any;
  CULfilename: any;
  CreatedDate: any;
  selectedholosproduct: any;
  nyers: any;
  subblocksize: any;
  analogyear: any;
  plantdensity: any;
  plantingmethod: any;
  farmid: any;
  farmname: any;
  plantingdate: any;
  reco: any;
  bases3loc: any = "https://s3-us-east-2.amazonaws.com/docker-holos-spatial-dssat-trigger-bucket/" ;
  localdir: any = "/assets/temp/" ;
  CO2plot: any;
  N2plot: any;
  waterplot: any;
  cultivarplot: any;
  heatmap: any = [];
  zipfiles3loc: any ;
  statcpt: any;
  statprob: any;
  statprob_density: any;
  pdatesplot: any;
  heatmapco2: any = [];
  heatmapn2: any = [];
  heatmapwater: any = [];
  heatmapyield: any = [];
  co2_trend: any;
  n2_trend: any;
  water_trend: any;
  yield_trend: any;
  yield_overlay: any;
  usa_mapimage: any;
  india_mapimage: any;
  j : any = 0;
  k : any = 0;
  m : any = 0;
  p : any = 0;

  constructor(private activateroute:ActivatedRoute,private http:HttpClient,private sanitizer: DomSanitizer) { }

  ngOnInit(): void {

       this.activateroute.params.subscribe((res:any) =>{
        console.log(res.id)
        /* console.log("res.ocrType",res.ocrType)
        this.ocrType = res.ocrType */

        // this.http.get(environment.apiUrl+'pdf_view').subscribe((res:any) => {
        //   this.pdfSrc
        // })
        
        // if((res.ocrType == 'Amazon Textract') || (res.ocrType ==  'Google AI') || res.ocrType == 'Various'){
           //alert("AWS or Google")
          this.http.get(environment.apiUrl+'Case_Detiles/'+res.id).subscribe((res:any) => {
            console.log('caseocrdatacaseocrdatacaseocrdata', res.response);
            this.filenameforzipfile = res.response;
            console.log('this filename for zip',this.filenameforzipfile);
            this.exptstatus = res.response[0].status;
            console.log('expt status', this.exptstatus);
            this.orgid = res.response[0].orgid ;
            this.projectname = res.response[0].projectName ;
            this.username = res.response[0].username ;
            this.username = this.username.replaceAll(" ","");
            this.caseid = res.response[0].id;
            this.Xfilename = res.response[0].XfileName;
            this.CULfilename = res.response[0].CULfileName;
            this.CreatedDate = res.response[0].CreatedDate;
            this.selectedholosproduct = res.response[0].selectedholosproduct;
            this.nyers = res.response[0].nyers;
            this.subblocksize = res.response[0].subblocksize;
            this.analogyear = res.response[0].analogyear;
            this.plantdensity = res.response[0].plantdensity;
            this.plantingmethod = res.response[0].plantingmethod;
            this.farmid = res.response[0].farmid;
            this.farmname = res.response[0].farmname;
            this.plantingdate = res.response[0].plantingdate;
              
            
            if(this.exptstatus == "Verified"){
              this.usa_mapimage = "https://www.gaiadhi.net/assets/images/usa-heatmap.jpg";
              this.india_mapimage = "https://www.gaiadhi.net/assets/images/india-heatmap.jpg_large";
              this.http.get(environment.apiUrl + 'getexptresults' + '?caseid=' + this.caseid ).subscribe((result: any) => {
                console.log('from results table',result.response);
                const b = result.response;
                console.log("b length",b.length);

                for (var i=0; i<b.length;i++){
                   var c = b[i];
                   console.log("c",c['files3loc']);
                   var d = c['files3loc'];
                   var n = d.lastIndexOf('/');
                   var e = d.substring(n + 1);
                   var filedir = this.localdir + this.projectname + "/results/" 

                   if (d.includes("zip")){
                    this.zipfiles3loc = e ;
                    console.log("zip",this.zipfiles3loc);
                   }
                   if (d.includes("co2_box") || d.includes("co2_barh")){
                    //this.CO2plot = filedir + e ;
                    this.CO2plot = this.bases3loc + d ;
                    console.log("Co2",this.CO2plot);
                   }
                   if (d.includes("n2_box") || d.includes("n2_barh")){
                    //this.N2plot = filedir + e ;
                    this.N2plot = this.bases3loc + d ;
                    console.log("N2",this.N2plot);
                   }
                   if (d.includes("water_box") || d.includes("water_barh")){
                    //this.waterplot = filedir + e ;
                    this.waterplot = this.bases3loc + d ;
                    console.log("water",this.waterplot);
                   }
                   if (d.includes("yield_box") || d.includes("yield_barh")){
                    //d = "362592/karthik/TanjoreRiceRecommendations-Project/results/cultivar_yield_box_plot.png"
                    //this.cultivarplot = filedir + e ;
                    this.cultivarplot = this.bases3loc + d ;
                    console.log("Cultivar yield",this.cultivarplot);
                   }
                   if (d.includes("pdates_yield")){
                    this.pdatesplot = this.bases3loc + d ;
                    console.log("Cultivar yield",this.pdatesplot);
                   }
                   if (d.includes("recommendations")){
                    //this.reco = c['reco'];
                    this.reco = c['reco'].split(/\r?\n/);
                    console.log("reco",this.reco);
                   }
                   if (d.includes("heatmap")){
                    //this.heatmap[j] = filedir + e  ;
                      if (d.includes("co2")) {
                        this.heatmapco2[this.j] = this.bases3loc + d ;
                        this.j = this.j +1;
                    }
                    if (d.includes("n2")) {
                        this.heatmapn2[this.k] = this.bases3loc + d ;
                        this.k = this.k +1;
                    }
                      if (d.includes("water")) {
                        this.heatmapwater[this.m] = this.bases3loc + d ;
                        this.m = this.m +1;
                    }
                      if (d.includes("yield")) {
                        this.heatmapyield[this.p] = this.bases3loc + d ;
                        this.p = this.p +1;
                    }
                   }
                   if (d.includes("cpt")){
                    this.statcpt = this.bases3loc + d ;
                   }
                   if (d.includes("prob")){
                    this.statprob = this.bases3loc + d ;
                   }
                   if (d.includes("prob_density")){
                    this.statprob_density = this.bases3loc + d ;
                   }
                   if (d.includes("co2_trend")){
                    this.co2_trend = this.bases3loc + d ;
                   }
                   if (d.includes("n2_trend")){
                    this.n2_trend = this.bases3loc + d ;
                   }
                   if (d.includes("water_trend")){
                    this.water_trend = this.bases3loc + d ;
                   }
                   if (d.includes("yield_trend")){
                    this.yield_trend = this.bases3loc + d ;
                   }
                   if (d.includes("html")){
                    if(d.includes("yield_overlay")){
                      this.yield_overlay = this.bases3loc + d ;
                   }
                  }
                }
              })
            }
            //this.downloadFile(res.response)
            //this.downloadFilecsv(res.response)
            //this.downloadFilecsv_1(res.response)
          })
          /*this.http.get(environment.apiUrl+'get_textract_results_by_caseid/'+res.id).subscribe((res:any) => {
            this.fileviewrshow = res.response[0].file.split(".")[1];
            this.pdfSrc = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.pdfUrl}${res.response[0].file}`);
            //this.pdfSrc = `${environment.pdfUrl}${res.response[0].file}`;
            //this.pdfSrc = `${environment.pdfUrl}/../tmp/${res.response[0].file}`;

            const csvfilename = res.response[0].file.split(".")[0].replaceAll(" ","-") + ".csv"
            console.log("csvfilename", csvfilename)
            //this.excelButtonlink = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.pdfUrl}`+ csvfilename);
            this.excelButtonlink = `${environment.pdfUrl}`+ csvfilename ;
            console.log("excel button link",this.excelButtonlink)

            console.log("res data",res.response[0].file)
            console.log("res pdf",this.pdfSrc)
            this.data =res.response[0].text;
            console.log("this.data before", this.data)
            this.data =res.response[0].text.replaceAll(","," ");
            this.data = this.data.replaceAll("'"," ");
            this.data = this.data.replaceAll("[","");
            this.data = this.data.replaceAll("]","");
            this.data = this.data.replaceAll("\"","");
            this.data = this.data.split("\\n")
            console.log("this.data after", this.data)
            this.pageData = this.data

            this.page_search_results =res.response[0].search_results.replaceAll(","," ");
            this.page_search_results = this.page_search_results.replaceAll("'"," ");
            this.page_search_results = this.page_search_results.replaceAll("[","");
            this.page_search_results = this.page_search_results.replaceAll("]","");
            this.page_search_results = this.page_search_results.replaceAll("\"","");
            this.page_search_results = this.page_search_results.split("\\n")

            //console.log("key Value data before")
            this.keyvaluesData = res.response[0].key_values
            //this.keyvaluesData = this.keyvaluesData.replaceAll("defaultdict(<class 'list'>,","")
            this.keyvaluesData = this.keyvaluesData.replaceAll("]","")
            this.keyvaluesData = this.keyvaluesData.replaceAll("[","")
            //this.keyvaluesData = this.keyvaluesData.replaceAll("{","")
            //this.keyvaluesData = this.keyvaluesData.replaceAll("}","")
            this.keyvaluesData = this.keyvaluesData.replaceAll("'"," ")
            this.keyvaluesData = this.keyvaluesData.replaceAll("\"","")
            this.keyvaluesData = this.keyvaluesData.replaceAll(","," ")
            this.keyvaluesData = this.keyvaluesData.split("\\n")
            //console.log("key Value data after")
            console.log("key Value data", this.keyvaluesData)
          })
          this.http.get(environment.apiUrl+'setSummary/'+res.id).subscribe((res:any) => {
            console.log('res fileNameres fileNameres fileNameres fileNameres fileName', res.response[0].summary.split("\r\n"));
            this.page_summary = res.response[0].summary.split("\\n")
            
            this.page_nltk_summ = res.response[0].nltksumm
            this.page_nltk_summ = this.page_nltk_summ.replaceAll("'", "")
            this.page_nltk_summ = this.page_nltk_summ.replaceAll("[", "")
            this.page_nltk_summ = this.page_nltk_summ.replaceAll("]", "")
            this.page_nltk_summ = this.page_nltk_summ.replaceAll(",", "")
            this.page_nltk_summ = this.page_nltk_summ.replaceAll("'", "")
            this.page_nltk_summ = this.page_nltk_summ.split("\\n")


            this.page_googleT5_summ = res.response[0].googleT5summ
            this.page_googleT5_summ = this.page_googleT5_summ.replaceAll("'", "")
            this.page_googleT5_summ = this.page_googleT5_summ.split("\\n")
            console.log(this.page_googleT5_summ)
           
          })
        }else{
          this.http.get(environment.apiUrl+'Whole_Data/'+res.id).subscribe((item:any) => {
            console.log('res fileName testig anik', item);
            this.data =item.response;
            this.pageData = this.data
            this.fileviewrshow = item.response[0].fileName.split(".")[1];
            console.log("fileviewrshow",this.fileviewrshow)
          
           
          
          this.http.get(environment.apiUrl+'Case_Detiles/'+res.id).subscribe((res:any) => {
            console.log('caseocrdatacaseocrdatacaseocrdata', res.response);
            console.log('caseocrdatacaseocrdatacaseocrdata', `${environment.apiUrl}mediafiles/${res.response[0].orgid}/${res.response[0].projectName}/${res.response[0].folderName}/output0.csv`);
            this.excelButtonlink = `${environment.apiUrl}mediafiles/${res.response[0].orgid}/${res.response[0].projectName}/${res.response[0].folderName}/output`
            this.sanitizedUrl = this.sanitizer.bypassSecurityTrustUrl(this.excelButtonlink);
            //alert(this.excelButtonlink)
            this.textButtonlink = `${environment.apiUrl}mediafiles/${res.response[0].orgid}/${res.response[0].projectName}/${res.response[0].folderName}/output.txt`

            this.caseocrdata =res.response;
            //this.pdfSrc = `${environment.pdfUrl}mediafiles/${res.response[0].orgid}/${res.response[0].projectName}/${res.response[0].folderName}/${item.response[0].fileName}`;
            this.pdfSrc = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.pdfUrl}${item.response[0].fileName}`);
   
            console.log("this.pdfSrc",this.pdfSrc)
          })
        })
          this.http.get(environment.apiUrl+'setSummary/'+res.id).subscribe((res:any) => {
            console.log('res fileNameres fileNameres fileNameres fileNameres fileName', res.response[0].summary.split("\r\n"));
            this.page_summary = res.response[0].summary.split("\\n")
           
          })
          this.http.get(environment.apiUrl+'tablesData/'+res.id).subscribe((res:any) => {
            console.log('res fileName', res.response);
            this.table_summary = res.response.summary
            res.response.map((item:any) =>{
              //console.log("item",eval(item.summary.replace(/["]+/g, ''))[0])
  
              if(eval(item.summary.replace(/["]+/g, '')).length == 2){
                // var data = {
                //   "Key":eval(item.summary.replace(/["]+/g, '')),
                // }
                this.tablesData.push(eval(item.summary.replace(/["]+/g, '')))
              }else if(eval(item.summary.replace(/["]+/g, '')).length == 6){
                // var data = {
                //   "Key":eval(item.summary.replace(/["]+/g, '')),
                // }
                this.tablesData1.push(eval(item.summary.replace(/["]+/g, '')))
              }else if(eval(item.summary.replace(/["]+/g, '')).length == 8){
                // var data = {
                //   "Key":eval(item.summary.replace(/["]+/g, '')),
                // }
                this.tablesData2.push(eval(item.summary.replace(/["]+/g, '')))
              }else if(eval(item.summary.replace(/["]+/g, '')).length == 7){
                // var data = {
                //   "Key":eval(item.summary.replace(/["]+/g, '')),
                // }
                this.tablesData3.push(eval(item.summary.replace(/["]+/g, '')))
              }
  
             
              //this.tablesData.push(data.summary.replace(/["]+/g, ''))
  
            })
            console.log("tablesData",this.tablesData)
            //
          })
          this.data = this.data.split("\\n")
          this.pageData = this.data
        }
        // const data = 'some text';
        // const blob = new Blob([data], { type: 'application/octet-stream' });
    
        // this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(window.URL.createObjectURL(blob));*/
      // }
       
      }) 

  }
  getocrdetials(id:any){

  }
  downloadtxt(textdata:any){

    const data = textdata;
    const blob = new Blob([data], { type: 'application/octet-stream' });

    this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(window.URL.createObjectURL(blob));
  }
  sanitize(url:string){
    
    return this.sanitizer.bypassSecurityTrustUrl(url);
}
downloadexcelfile(pageNo:any){
  console.log("excelButtonLink",this.excelButtonlink);
  window.open(this.excelButtonlink, "_blank");
}

downloadFile(response:any) {
  var data = response[0]
  var fileFolder = data.fileName.split(".")[0]
  fileFolder = fileFolder.replaceAll(" ","-")
  console.log("fileFolder", fileFolder)
  console.log("response",`${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/${fileFolder}_text.txt`)
 

   if(this.ocrType == 'Google AI'){
    var param1 = `${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/google_${fileFolder}.txt`
   }else{
    var param1 = `${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/${fileFolder}_text.txt`
   }
  
  this.http.get(environment.apiUrl+`download/?path=${param1}`,
  {responseType: 'text'}).subscribe((data: any) => {
      console.log("TEXT FILE DATA",data)
      const file = new Blob([data]);
      this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(file));
      console.log("fileUrl",this.fileUrl)
      if(this.ocrType == 'Google AI'){
        this.pageData = data
        this.pageData = this.pageData.replaceAll("[","");
        this.pageData = this.pageData.replaceAll("]","");
        this.pageData = this.pageData.replaceAll(","," ");
        this.pageData = this.data.replaceAll("'"," ");
        this.pageData = this.data.replaceAll("\""," ");
        this.pageData = this.data.split("\\n")
        // this.pageData = data
      }else{
        this.pageData = data
      }
     
      
      console.log("this.pageDatathis.pageData",this.pageData)
    })
    // (error: any) => {
    //   console.error('Error downloading file:', error);
    // })
}
downloadFilecsv_1(response:any) {
  var data = response[0]
  var fileFolder = data.fileName.split(".")[0]
  fileFolder = fileFolder.replaceAll(" ","-")
  console.log("response",`${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/${fileFolder}.csv`)
   var param1 = `${data.orgid}/${data.projectName}/${data.folderName}/${fileFolder}/${fileFolder}.csv`
  
  this.http.get(environment.apiUrl+`downloadcsv/?path=${param1}`).subscribe((data: any) => {
    this.keyId = Object.keys(JSON.parse(data)[0])
      console.log("keyId", this.keyId)
      // const file = new Blob([data]);
      // this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(file));
      // console.log("fileUrl",JSON.parse(data).filter((v:any,i:any,a:any)=>a.findIndex((v2:any)=>(v2[this.keyId]===v[this.keyId]))===i))
      // this.tableData = JSON.parse(data).filter((v:any,i:any,a:any)=>a.findIndex((v2:any)=>(v2[this.keyId]===v[this.keyId]))===i)
      this.tableData = JSON.parse(data)
      console.log("JSON.parse(data)",JSON.parse(data))
      console.log("keyId", this.keyId[0])
      console.log("keyId", this.keyId[1])
    },
    (error: any) => {
      console.error('Error downloading file:', error);
    })
}
getKeys(data: any): string[] {
  return Object.keys(data);
}

getValue(data: any, key: string): string {
  return data[key];
}

searchTest(value: any) {
  if (this.searchText == ''){
    //this.searchText = "Enter Search Text";
    const result = 'false';
    return result ;
  }
  const re = new RegExp(this.searchText, 'igm');
  const result = re.test(value);
  return result;
}
downloadzipfile(){
  // alert(this.filenameforzipfile[0].fileName)
  const myfilename = "results.zip"
  this.orgid
  this.username
  this.projectname
  const dir = "results";
  this.zipfiles3loc
  this.http.get(environment.apiUrl+'create_zip' +'?orgid=' + this.orgid +'&username='+this.username+'&projectname='+this.projectname +'&dir='+dir +'&zipfiles3loc='+this.zipfiles3loc ,{
    responseType: 'arraybuffer'
  }).subscribe((item:any) => {
    // console.log(item)
    // this.downloadFile1(item);
    const blob = new Blob([item], {
      type: 'application/zip'
    });
    const url = window.URL.createObjectURL(blob);
    window.open(url);
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
// downloadFile1(data: any) {
//   const blob = new Blob([data], { type: 'application/octet-stream' });
//   fs.saveAs(blob, 'test.zip');
// }

}

import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'highlighter'
})
export class HighlighterPipe implements PipeTransform {

  transform(value: any, args: any,type:string): unknown {
    if(!args) return value;
    if(type==='full'){
      const re = new RegExp("\\b("+args+"\\b)", 'igm');
      const result = re.test(value);
      value= value.replace(re, '<span class="highlighted-text" style = "background-color: yellow";>$1</span>');
    //  value= value.replace(re, '>>>>$1<<<<');
    }
    else{
      const re = new RegExp(args, 'igm');
      const result = re.test(value);
      value= value.replace(re, '<span class="highlighted-text" style = "background-color: yellow";>$&</span>');
    //  value= value.replace(re, '>>>>$&<<<<');
    }
  
      return value;
  }

}

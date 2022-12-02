
export function parseTranscript(data) {
  var el = document.createElement('html');
  el.innerHTML = data;
  var majors = new Array(10);
  var a = el.getElementsByTagName('th');
  var b = el.getElementsByTagName('td'); 
  var i = 6;
  while(true){
    if (a[i].innerText == "Major and Department:") {
      console.log(b[i+20]);
      i++;
    }
    else{
      break;
    }
  }

};
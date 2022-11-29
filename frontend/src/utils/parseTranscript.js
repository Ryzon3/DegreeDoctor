
export function parseTranscript(data) {
  var transcript = data.replace('&amp','&');
  console.log(transcript);
  var arrayOfData = transcript.split("STUDENT INFORMATION");
  var info = arrayOfData[1];
  var splitInfo = info.split("<!--  ** START OF twbkwbis.P_CloseDoc **  -->");
  var majors = splitInfo[0];
  var yourMajors = majors.split("<th colspan=\"3\" class=\"ddlabel\" scope=\"row\">Major and Department:</th>") 
  for (let i = 0; i < yourMajors.length; i++){
    console.log(yourMajors[i]);
    console.log("\n\n\n");
  }
};

export function parseTranscript(transcript) {
  var arrayOfData = transcript.split("STUDENT INFORMATION");
  var info = arrayOfData[1];
  var splitInfo = info.split("<!--  ** START OF twbkwbis.P_CloseDoc **  -->");
  console.log(splitInfo[0]);
};
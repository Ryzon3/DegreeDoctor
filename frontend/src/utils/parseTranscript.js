
export function parseTranscript(transcript) {
  var arrayOfData = transcript.split("STUDENT INFORMATION");
  var info = arrayOfData[1];
  console.log(info);
};
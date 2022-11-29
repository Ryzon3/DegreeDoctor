
export function parseTranscript(transcript) {
  var arrayOfData = transcript.split("STUDENT INFORMATION");
  arrayOfData =  arrayOfData[1];
  arrayOfData = arrayOfData.split("Unofficial Transcript");
  arrayOfData.pop();
  console.log(arrayOfData);
};
// var JSSoup = require('jssoup').default;

export function parseTranscript(transcript) {
  const soup = new JSSoup(transcript);
  const paragraphs = soup.findAll('p');
};
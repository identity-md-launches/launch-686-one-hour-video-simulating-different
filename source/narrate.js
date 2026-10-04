const fs = require('fs');
const path = require('path');
const meSpeak = require('./vendor/mespeak/package');
meSpeak.loadConfig(require('./vendor/mespeak/package/src/mespeak_config.json'));
meSpeak.loadVoice(require('./vendor/mespeak/package/voices/en/en-us.json'));
const [input, output, scene] = process.argv.slice(2);
const cards = JSON.parse(fs.readFileSync(input, 'utf8'));
for (let i=Number(scene); i<=Number(scene); i++) {
 const text = cards[i].title + '. ' + cards[i].body;
 const wav = meSpeak.speak(text, { rawdata: 'buffer', speed: 172, amplitude: 85 });
 fs.writeFileSync(path.join(output, `speech-${String(i).padStart(3,'0')}.wav`), Buffer.from(wav));
}

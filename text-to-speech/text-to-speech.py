from pathlib import Path
from openai import OpenAI
client = OpenAI()


#get input as cli parameter


#input = "Hello, my name is Aimie. I am a virtual assistant. I am here to help you with your medical inquiries. I can do things like collect information about your inquiry and tell you exact and latest approved medical information available about Rhabarbatan. I can also tell check on your previous cases and update you about their progress. I am still learning, so I may not be able to do everything you ask me to do. I am sorry if I make any mistakes. I am still learning."
input = "Labas, mano vardas - Aimius. Aš esu virtualus asistentas. Aš  čia, kad padėčiau jums su jūsų medicininiais klausimais. Aš galiu daryti dalykus kaip rinkti ir pildyti informaciją apie jūsų klausimą ar pasakoti jums tiksliausią ir naujausią patvirtintą medicininę informaciją apie Rhabarbataną. Aš taip pat galiu patikrinti jūsų ankstesnes užklausas ir informuoti jus apie jų būklę. Aš vis dar mokausi, todėl galiu nepadaryti visko ko prašote. Atsiprašau, jei padarysiu kokių nors klaidų."

speech_file_path = Path(__file__).parent / "outputs/aimius-fable.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="fable", #alloy, echo, fable, onyx, nova, shimmer
  input=input
)

response.stream_to_file(speech_file_path)
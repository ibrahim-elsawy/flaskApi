from transformers import PegasusForConditionalGeneration, PegasusTokenizer, PegasusConfig
import torch
import gc
# from createStudent import create_student_with_configuration
from .createStudent import *

model_name = "google/pegasus-xsum"

#TODO 
#[x] load the trained student checkpoint .pt



configuration = PegasusConfig(vocab_size=96103,encoder_layers=16,decoder_layers=16, max_position_embeddings=1000)
model_name = 'google/pegasus-xsum'
# teacher = torch.load('teacher_16_4.pt', map_location=torch.device('cpu'))
teacher = PegasusForConditionalGeneration(configuration).from_pretrained(model_name, config=configuration)
student = create_student_with_configuration(teacher,
                                     e=12,
                                     d=3,
                                     copy_first_teacher_layers = False,
                                     save_path='./student')
checkpoint = torch.load('trained_student_12ecn_3dec.pt', map_location=torch.device('cpu'))
student.load_state_dict(checkpoint['model_state_dict'])
del teacher
gc.collect()
# torch.cuda.empty_cache()
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = torch.nn.ModuleDict({"student": student})



def get_response(input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1000, return_tensors="pt")
  translated = student.generate(**batch,max_length=60,use_cache=True )
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text
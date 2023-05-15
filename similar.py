import pandas as pd
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')

def similarity(text_pemda, bagan_akun, mod = model):
    # encode sentences to get their embeddings
    embedding1 = mod.encode(text_pemda, convert_to_tensor=True)
    embedding2 = bagan_akun
    # compute similarity scores of two embeddings
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2).cpu().tolist()[0]
    max_score = max(cosine_scores)

    #Output passages & scores
    return cosine_scores.index(max_score)

apbd = pd.read_excel('Program APBD.xlsx')
program = pd.read_excel('List Program.xlsx')

def getProgram(topik):
    program_enc = model.encode(program['Program'].tolist(), convert_to_tensor=True)
    a = similarity(topik, program_enc)
    out = program.iloc[a]['Program']
    return out

# print(getProgram('sekolah'))
import re
import numpy as np

def predict_sentiment(sentence, tokenizer, model):

    seq_len = 128

    text=re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence)
    input_id = tokenizer.encode(text,
                                truncation=True,
                                padding='max_length',
                                max_length=seq_len)

    # attention_mask : 토큰화한 문장 내 패딩인 경우 0
    padding_count = input_id.count(0)
    attention_mask = [1] * (seq_len - padding_count) + [0] * padding_count

    # segment : 세그먼트 임베딩을 위한 것으로 문장이 1개이므로 전부 0
    segment = [0] * seq_len


    # numpy array로 저장
    input_ids = np.array(input_id).reshape(1, -1)
    attention_masks = np.array(attention_mask).reshape(1, -1)
    segments = np.array(segment).reshape(1, -1)

    new_inputs = (input_ids, attention_masks, segments)

    # prediction
    prediction = model.predict(new_inputs)
    predicted_probability = np.round(np.max(prediction) * 100, 2)
    temp = np.round(prediction * 100, 2)
    prob = np.concatenate(temp).tolist()
    print(prob)
    predicted_class = ['기쁨', '당황', '분노', '불안', '상처', '슬픔'][np.argmax(prediction, axis=1)[0]]
    result = "{}% 확률로 {} 감정입니다.".format(predicted_probability, predicted_class)


    return result, prob




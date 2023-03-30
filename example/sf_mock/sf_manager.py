from gpt_cache.view import openai
from gpt_cache.core import cache, Config
from gpt_cache.cache.factory import get_si_data_manager
from gpt_cache.similarity_evaluation.simple import pair_evaluation
import numpy as np


d = 8


def mock_embeddings(data, **kwargs):
    return np.random.random((d, )).astype('float32')


def run():
    data_manager = get_si_data_manager("sqlite", "faiss", dimension=d, max_size=8, clean_size=2, top_k=3)
    cache.init(embedding_func=mock_embeddings,
               data_manager=data_manager,
               evaluation_func=pair_evaluation,
               similarity_threshold=10000,
               similarity_positive=False,
               config=Config(),
               )

    mock_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "foo"}
    ]
    # you should CLOSE it if you SECONDLY run it
    for i in range(10):
        question = f"foo{i}"
        answer = f"receiver the foo {i}"
        cache.data_manager.save(question, answer, cache.embedding_func(question))

    answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mock_messages,
    )
    print(answer)


if __name__ == '__main__':
    run()